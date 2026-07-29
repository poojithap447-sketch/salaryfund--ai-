"""
Loan Eligibility Engine - runtime inference.

Loads the three persisted candidate models (RandomForest, XGBoost, LogisticRegression),
runs all three, reports a full comparison, selects the best-performing model's prediction
as the operative decision, computes SHAP explainability for that decision, and derives
an eligible loan amount and a routing decision (auto-approve / manual review / auto-reject).
"""
import json
import time
from pathlib import Path

import joblib
import numpy as np
import shap

from app.ai.eligibility.features import EligibilityFeatures, FEATURE_NAMES
from app.core.config import settings
from app.core.exceptions import AIModelException
from app.core.logging_config import get_logger

logger = get_logger(__name__)

AUTO_APPROVE_THRESHOLD = 0.80
AUTO_REJECT_THRESHOLD = 0.35


class EligibilityEngine:
    """Loads model artifacts lazily and caches them for the process lifetime."""

    _instance: "EligibilityEngine | None" = None

    def __init__(self):
        self.model_dir = Path(settings.MODEL_ARTIFACT_DIR) / "eligibility" / settings.ELIGIBILITY_MODEL_VERSION
        self._models: dict = {}
        self._scaler = None
        self._comparison_meta: dict = {}
        self._shap_background = None
        self._shap_background_scaled = None
        self._loaded = False

    @classmethod
    def instance(cls) -> "EligibilityEngine":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def _ensure_loaded(self):
        if self._loaded:
            return
        try:
            self._models["random_forest"] = joblib.load(self.model_dir / "random_forest.joblib")
            self._models["xgboost"] = joblib.load(self.model_dir / "xgboost.joblib")
            self._models["logistic_regression"] = joblib.load(self.model_dir / "logistic_regression.joblib")
            self._scaler = joblib.load(self.model_dir / "scaler.joblib")
            with open(self.model_dir / "comparison.json") as f:
                self._comparison_meta = json.load(f)
            self._shap_background = joblib.load(self.model_dir / "shap_background.joblib")
            self._shap_background_scaled = joblib.load(self.model_dir / "shap_background_scaled.joblib")
            self._loaded = True
        except FileNotFoundError as exc:
            raise AIModelException(
                "Eligibility models are not trained yet. Run `python -m app.ai.training.train_eligibility` "
                "or wait for the scheduled Celery training job to complete."
            ) from exc

    def predict(self, features: EligibilityFeatures) -> dict:
        self._ensure_loaded()
        start = time.perf_counter()

        x_raw = features.to_array()
        x_scaled = self._scaler.transform(x_raw)

        probs = {}
        probs["random_forest"] = float(self._models["random_forest"].predict_proba(x_raw)[0, 1])
        probs["xgboost"] = float(self._models["xgboost"].predict_proba(x_raw)[0, 1])
        probs["logistic_regression"] = float(self._models["logistic_regression"].predict_proba(x_scaled)[0, 1])

        best_model_name = self._comparison_meta.get("best_model", "xgboost")
        approval_probability = probs[best_model_name]
        risk_score = round(1 - approval_probability, 4)

        # Confidence = agreement between models (1 - normalized spread across the three probabilities)
        spread = max(probs.values()) - min(probs.values())
        confidence = round(max(0.0, 1 - spread), 4)

        eligible_amount = self._compute_eligible_amount(features, approval_probability)
        shap_explanation = self._explain(best_model_name, x_raw, x_scaled)

        decision_hint = self._route_decision(approval_probability, risk_score)

        latency_ms = round((time.perf_counter() - start) * 1000, 2)
        logger.info(
            "eligibility_inference",
            best_model=best_model_name,
            approval_probability=approval_probability,
            risk_score=risk_score,
            latency_ms=latency_ms,
        )

        return {
            "approval_probability": round(approval_probability, 4),
            "risk_score": risk_score,
            "eligible_amount": eligible_amount,
            "confidence": confidence,
            "best_model": best_model_name,
            "model_comparison": {
                "candidate_probabilities": {k: round(v, 4) for k, v in probs.items()},
                "training_metrics": self._comparison_meta.get("metrics", {}),
            },
            "shap_explanation": shap_explanation,
            "decision_hint": decision_hint,
            "inference_latency_ms": latency_ms,
        }

    @staticmethod
    def _route_decision(approval_probability: float, risk_score: float) -> str:
        if approval_probability >= AUTO_APPROVE_THRESHOLD:
            return "AUTO_APPROVE"
        if approval_probability <= AUTO_REJECT_THRESHOLD:
            return "AUTO_REJECT"
        return "MANUAL_REVIEW"

    @staticmethod
    def _compute_eligible_amount(features: EligibilityFeatures, approval_probability: float) -> float:
        """
        Eligible amount = a fraction of requested amount scaled by approval probability and
        capped by an affordability rule (salary * multiplier based on risk).
        """
        affordability_cap = features.monthly_net_salary * (2.5 if approval_probability > 0.6 else 1.2)
        scaled = features.requested_amount * min(1.0, approval_probability + 0.15)
        return round(min(scaled, affordability_cap, features.requested_amount), 2)

    def _explain(self, best_model_name: str, x_raw: np.ndarray, x_scaled: np.ndarray) -> dict:
        try:
            model = self._models[best_model_name]
            if best_model_name in ("random_forest", "xgboost"):
                explainer = shap.TreeExplainer(model)
                shap_values = explainer.shap_values(x_raw)
                # For binary classifiers TreeExplainer may return a list [class0, class1] or a single array
                values = shap_values[1][0] if isinstance(shap_values, list) else shap_values[0]
            else:
                explainer = shap.LinearExplainer(model, self._shap_background_scaled)
                shap_values = explainer.shap_values(x_scaled)
                values = shap_values[0]

            contributions = {
                name: round(float(val), 5) for name, val in zip(FEATURE_NAMES, np.ravel(values))
            }
            # Sort by absolute contribution, most influential first
            sorted_contribs = dict(sorted(contributions.items(), key=lambda kv: abs(kv[1]), reverse=True))
            top_positive = [k for k, v in sorted_contribs.items() if v > 0][:3]
            top_negative = [k for k, v in sorted_contribs.items() if v < 0][:3]
            return {
                "feature_contributions": sorted_contribs,
                "top_positive_factors": top_positive,
                "top_negative_factors": top_negative,
            }
        except Exception as exc:  # SHAP failures should never break the eligibility decision
            logger.warning("shap_explanation_failed", error=str(exc))
            return {"feature_contributions": {}, "top_positive_factors": [], "top_negative_factors": [], "note": "SHAP unavailable"}
