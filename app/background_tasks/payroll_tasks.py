"""
Payroll sync background job. Employers can either upload payroll CSVs via the
REST API (synchronous, see PayrollService.bulk_ingest) or connect an HRMS
integration; this task is the entry point for scheduled/webhook-triggered
HRMS pulls once a specific HRMS connector is wired up (Keka, Zoho Payroll, etc).
"""
from app.background_tasks.celery_app import celery_app
from app.core.logging_config import get_logger

logger = get_logger(__name__)


@celery_app.task(name="app.background_tasks.payroll_tasks.sync_employer_payroll")
def sync_employer_payroll(employer_id: str, hrms_provider: str, credentials_ref: str):
    """
    Placeholder integration point: fetch payroll data from the employer's HRMS
    provider API and feed it through PayrollService.bulk_ingest. The connector
    implementation is provider-specific (OAuth/API-key flows differ per HRMS)
    and should be added under app/utils/hrms_connectors/<provider>.py.
    """
    logger.info("payroll_sync_requested", employer_id=employer_id, provider=hrms_provider)
    # Intentionally not auto-fetching from a live third-party HRMS without configured
    # credentials; wire the specific connector class here once provider is chosen.
    return {"status": "no_connector_configured", "provider": hrms_provider}
