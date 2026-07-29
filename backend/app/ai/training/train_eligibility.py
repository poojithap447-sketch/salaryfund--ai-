"""
Trains and compares three candidate models for the Loan Eligibility Engine:
RandomForestClassifier, XGBoostClassifier, LogisticRegression.

Run standalone: `python -m app.ai.training.train_eligibility`
Also invoked by the Celery periodic task `retrain_eligibility_models`.

Persists:
  - the best-performing model (by ROC-AUC) as the active inference model
  - all three fitted models + scaler + comparison metrics for transparency
  - a fitted SHAP TreeExplainer/LinearExplainer for the best model
"""
import json
import os
from pathlib import Path

import joblib
import numpy as np
import shap
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier

from app.ai.eligibility.features import FEATURE_NAMES
from app.ai.training.synthetic_eligibility_data import generate_dataset
from app.core.config import settings
from app.core.logging_config import get_logger

logger = get_logger(__name__)


def _model_dir() -> Path:
    path = Path(settings.MODEL_ARTIFACT_DIR) / "eligibility" / settings.ELIGIBILITY_MODEL_VERSION
    path.mkdir(parents=True, exist_ok=True)
    return path


def train_and_compare(df=None) -> dict:
    if df is None:
        df = generate_dataset()

    X = df[FEATURE_NAMES].values
    y = df["approved"].values

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    models = {
        "random_forest": RandomForestClassifier(
            n_estimators=300, max_depth=8, min_samples_leaf=5, class_weight="balanced", random_state=42, n_jobs=-1
        ),
        "xgboost": XGBClassifier(
            n_estimators=300,
            max_depth=5,
            learning_rate=0.05,
            subsample=0.8,
            colsample_bytree=0.8,
            eval_metric="logloss",
            random_state=42,
            n_jobs=-1,
        ),
        "logistic_regression": LogisticRegression(max_iter=1000, class_weight="balanced"),
    }

    comparison = {}
    fitted_models = {}

    for name, model in models.items():
        # Tree models trained on raw features (scale-invariant); logistic regression on scaled features.
        if name == "logistic_regression":
            model.fit(X_train_scaled, y_train)
            preds = model.predict(X_test_scaled)
            probs = model.predict_proba(X_test_scaled)[:, 1]
        else:
            model.fit(X_train, y_train)
            preds = model.predict(X_test)
            probs = model.predict_proba(X_test)[:, 1]

        comparison[name] = {
            "accuracy": round(float(accuracy_score(y_test, preds)), 4),
            "precision": round(float(precision_score(y_test, preds, zero_division=0)), 4),
            "recall": round(float(recall_score(y_test, preds, zero_division=0)), 4),
            "f1_score": round(float(f1_score(y_test, preds, zero_division=0)), 4),
            "roc_auc": round(float(roc_auc_score(y_test, probs)), 4),
        }
        fitted_models[name] = model

    best_model_name = max(comparison, key=lambda k: comparison[k]["roc_auc"])
    logger.info("eligibility_training_complete", best_model=best_model_name, metrics=comparison)

    model_dir = _model_dir()
    joblib.dump(fitted_models["random_forest"], model_dir / "random_forest.joblib")
    joblib.dump(fitted_models["xgboost"], model_dir / "xgboost.joblib")
    joblib.dump(fitted_models["logistic_regression"], model_dir / "logistic_regression.joblib")
    joblib.dump(scaler, model_dir / "scaler.joblib")

    with open(model_dir / "comparison.json", "w") as f:
        json.dump({"best_model": best_model_name, "metrics": comparison, "feature_names": FEATURE_NAMES}, f, indent=2)

    # Persist background samples for SHAP explainers: raw-scale for tree models (TreeExplainer
    # ignores this but keeping the interface consistent), and a *scaled* sample for the
    # LinearExplainer, since LogisticRegression was fit on standardized features - passing an
    # unscaled background there would silently distort the SHAP contribution magnitudes.
    sample_idx = np.random.choice(X_train.shape[0], size=min(100, X_train.shape[0]), replace=False)
    background = X_train[sample_idx]
    background_scaled = X_train_scaled[sample_idx]
    joblib.dump(background, model_dir / "shap_background.joblib")
    joblib.dump(background_scaled, model_dir / "shap_background_scaled.joblib")

    return {"best_model": best_model_name, "metrics": comparison}


if __name__ == "__main__":
    result = train_and_compare()
    print(json.dumps(result, indent=2))
