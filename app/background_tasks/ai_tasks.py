"""
AI background jobs: periodic career-score / financial-wellness recalculation
and scheduled model retraining for the eligibility and fraud engines.
"""
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.background_tasks.celery_app import celery_app
from app.core.config import settings
from app.core.logging_config import get_logger
from app.models.organization import Employee
from sqlalchemy import create_engine

logger = get_logger(__name__)
_sync_engine = create_engine(settings.DATABASE_URL_SYNC, pool_pre_ping=True)


@celery_app.task(name="app.background_tasks.ai_tasks.recalculate_all_career_scores")
def recalculate_all_career_scores():
    """
    Iterates all active employees and triggers a fresh Career Credit Score computation.
    Delegates to the async CareerScoreService via a short-lived event loop since the
    service layer is async-first (SQLAlchemy AsyncSession).
    """
    import asyncio

    from app.database.session import AsyncSessionLocal
    from app.services.career_score_service import CareerScoreService

    async def _run():
        async with AsyncSessionLocal() as session:
            with Session(_sync_engine) as sync_session:
                employee_ids = [row[0] for row in sync_session.execute(select(Employee.id)).all()]
            service = CareerScoreService(session)
            processed = 0
            for employee_id in employee_ids:
                try:
                    await service.compute_and_store(employee_id)
                    processed += 1
                except Exception as exc:
                    logger.error("career_score_recalc_failed", employee_id=str(employee_id), error=str(exc))
            return processed

    processed = asyncio.run(_run())
    logger.info("career_scores_recalculated", count=processed)
    return {"processed": processed}


@celery_app.task(name="app.background_tasks.ai_tasks.recalculate_all_financial_wellness")
def recalculate_all_financial_wellness():
    import asyncio

    from app.database.session import AsyncSessionLocal
    from app.services.financial_wellness_service import FinancialWellnessService

    async def _run():
        async with AsyncSessionLocal() as session:
            with Session(_sync_engine) as sync_session:
                employee_ids = [row[0] for row in sync_session.execute(select(Employee.id)).all()]
            service = FinancialWellnessService(session)
            processed = 0
            for employee_id in employee_ids:
                try:
                    await service.compute_and_store(employee_id)
                    processed += 1
                except Exception as exc:
                    logger.error("wellness_recalc_failed", employee_id=str(employee_id), error=str(exc))
            return processed

    processed = asyncio.run(_run())
    logger.info("financial_wellness_recalculated", count=processed)
    return {"processed": processed}


@celery_app.task(name="app.background_tasks.ai_tasks.retrain_eligibility_model")
def retrain_eligibility_model():
    from app.ai.training.train_eligibility import train_and_compare

    result = train_and_compare()
    logger.info("eligibility_model_retrained", best_model=result["best_model"])
    return result


@celery_app.task(name="app.background_tasks.ai_tasks.retrain_fraud_model")
def retrain_fraud_model():
    """
    Re-bootstraps the IsolationForest fraud model. In production this should be
    extended to pull real anonymized application/transaction features instead
    of the synthetic baseline distribution.
    """
    from app.ai.fraud_detection.engine import _bootstrap_isolation_forest

    _bootstrap_isolation_forest()
    logger.info("fraud_model_retrained")
    return {"status": "retrained"}
