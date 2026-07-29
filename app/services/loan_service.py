"""
Loan application lifecycle service: submission, AI eligibility scoring,
fraud screening, manual decisioning, disbursement, EMI schedule generation,
and repayment processing.
"""
import uuid
from datetime import datetime, timedelta, timezone
from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.eligibility.engine import EligibilityEngine
from app.ai.eligibility.features import EligibilityFeatures
from app.ai.fraud_detection.engine import FraudSignals, evaluate_fraud_signals
from app.core.exceptions import InsufficientEligibilityException, NotFoundException, ValidationException
from app.models.ai_and_wellness import AIPrediction, FraudAlert, FraudAlertSeverity, PredictionType
from app.models.loans import (
    EMIStatus,
    Loan,
    LoanApplication,
    LoanApplicationStatus,
    LoanStatus,
    TransactionStatus,
    TransactionType,
)
from app.repositories.loan_repository import (
    EMIRepository,
    LenderRepository,
    LoanApplicationRepository,
    LoanRepository,
    LoanTypeRepository,
    TransactionRepository,
)
from app.repositories.organization_repository import EmployeeRepository
from app.schemas.loans import LoanApplicationCreate, LoanApplicationDecision
from app.utils.finance import generate_amortization_schedule


class LoanApplicationService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.application_repo = LoanApplicationRepository(db)
        self.loan_type_repo = LoanTypeRepository(db)
        self.employee_repo = EmployeeRepository(db)
        self.loan_repo = LoanRepository(db)
        self.lender_repo = LenderRepository(db)
        self.emi_repo = EMIRepository(db)
        self.txn_repo = TransactionRepository(db)

    async def submit_application(self, employee_id: uuid.UUID, payload: LoanApplicationCreate) -> LoanApplication:
        employee = await self.employee_repo.get_by_id(employee_id)
        if not employee:
            raise NotFoundException("Employee not found")

        loan_type = await self.loan_type_repo.get_by_id(payload.loan_type_id)
        if not loan_type:
            raise NotFoundException("Loan type not found")

        if not (loan_type.min_amount <= payload.requested_amount <= loan_type.max_amount):
            raise ValidationException(
                f"Requested amount must be between {loan_type.min_amount} and {loan_type.max_amount} for this loan type"
            )
        if not (loan_type.min_tenure_months <= payload.requested_tenure_months <= loan_type.max_tenure_months):
            raise ValidationException(
                f"Tenure must be between {loan_type.min_tenure_months} and {loan_type.max_tenure_months} months"
            )

        policy = await self.loan_type_repo.get_active_policy(loan_type.id)
        active_count = await self.application_repo.count_active_loans(employee_id)
        if policy and active_count >= policy.max_active_loans:
            raise ValidationException(f"You already have {active_count} active applications - maximum allowed is {policy.max_active_loans}")

        application = await self.application_repo.create(
            employee_id=employee_id,
            loan_type_id=payload.loan_type_id,
            requested_amount=payload.requested_amount,
            requested_tenure_months=payload.requested_tenure_months,
            purpose=payload.purpose,
            status=LoanApplicationStatus.SUBMITTED,
            submitted_at=datetime.now(timezone.utc),
        )
        await self.db.commit()
        await self.db.refresh(application)
        return application

    async def run_ai_review(
        self,
        application: LoanApplication,
        career_score: int,
        dti_ratio: float,
        emi_burden_ratio: float,
        attendance_score: float,
        avg_repayment_delay_days: float,
        salary_growth_pct_yoy: float,
        num_previous_defaults: int,
        age_years: float,
        tenure_at_employer_months: float,
        existing_active_loans: int,
        duplicate_pan_count: int,
        salary_volatility_pct: float,
        document_forgery_score: float,
    ) -> dict:
        """Runs both the eligibility engine and fraud engine, persists an AIPrediction record,
        and transitions the application status accordingly."""
        employee = await self.employee_repo.get_by_id(application.employee_id)

        features = EligibilityFeatures(
            monthly_net_salary=float(employee.monthly_net_salary),
            requested_amount=float(application.requested_amount),
            requested_tenure_months=float(application.requested_tenure_months),
            salary_to_request_ratio=float(employee.monthly_net_salary) / max(float(application.requested_amount), 1.0),
            tenure_at_employer_months=tenure_at_employer_months,
            career_credit_score=float(career_score),
            existing_active_loans=float(existing_active_loans),
            debt_to_income_ratio=dti_ratio,
            emi_burden_ratio=emi_burden_ratio,
            attendance_score=attendance_score,
            avg_repayment_delay_days=avg_repayment_delay_days,
            salary_growth_pct_yoy=salary_growth_pct_yoy,
            num_previous_defaults=float(num_previous_defaults),
            age_years=age_years,
        )

        eligibility_result = EligibilityEngine.instance().predict(features)

        fraud_result = evaluate_fraud_signals(
            FraudSignals(
                duplicate_pan_count=duplicate_pan_count,
                salary_volatility_pct=salary_volatility_pct,
                active_applications_last_30_days=existing_active_loans,
                document_forgery_score=document_forgery_score,
                monthly_net_salary=float(employee.monthly_net_salary),
                requested_amount=float(application.requested_amount),
            )
        )

        prediction = AIPrediction(
            loan_application_id=application.id,
            employee_id=application.employee_id,
            prediction_type=PredictionType.ELIGIBILITY,
            model_name=eligibility_result["best_model"],
            model_version="v1",
            approval_probability=eligibility_result["approval_probability"],
            risk_score=eligibility_result["risk_score"],
            eligible_amount=eligibility_result["eligible_amount"],
            confidence=eligibility_result["confidence"],
            shap_values=eligibility_result["shap_explanation"],
            model_comparison=eligibility_result["model_comparison"],
            raw_features=features.to_dict(),
            inference_latency_ms=eligibility_result["inference_latency_ms"],
        )
        self.db.add(prediction)

        if fraud_result["is_high_risk"]:
            application.status = LoanApplicationStatus.FLAGGED_FRAUD
            for alert in fraud_result["alerts"]:
                self.db.add(
                    FraudAlert(
                        employee_id=application.employee_id,
                        loan_application_id=application.id,
                        alert_type=alert["alert_type"],
                        severity=FraudAlertSeverity(alert["severity"]),
                        risk_score=fraud_result["risk_score"],
                        details=alert,
                    )
                )
        elif eligibility_result["decision_hint"] == "AUTO_REJECT":
            application.status = LoanApplicationStatus.REJECTED
            application.rejection_reason = "AI eligibility engine assessed high credit risk"
            application.decisioned_at = datetime.now(timezone.utc)
        elif eligibility_result["decision_hint"] == "AUTO_APPROVE":
            application.status = LoanApplicationStatus.APPROVED
            application.decisioned_at = datetime.now(timezone.utc)
        else:
            application.status = LoanApplicationStatus.UNDER_MANUAL_REVIEW

        await self.db.commit()

        return {"eligibility": eligibility_result, "fraud": fraud_result, "application_status": application.status}

    async def manual_decision(self, application_id: uuid.UUID, reviewer_id: uuid.UUID, decision: LoanApplicationDecision) -> LoanApplication:
        application = await self.application_repo.get_by_id(application_id)
        if not application:
            raise NotFoundException("Loan application not found")
        if application.status not in (LoanApplicationStatus.UNDER_MANUAL_REVIEW, LoanApplicationStatus.FLAGGED_FRAUD):
            raise ValidationException("Only applications under manual review can be manually decisioned")

        application.reviewed_by_user_id = reviewer_id
        application.decisioned_at = datetime.now(timezone.utc)

        if decision.approve:
            application.status = LoanApplicationStatus.APPROVED
        else:
            application.status = LoanApplicationStatus.REJECTED
            application.rejection_reason = decision.rejection_reason or "Rejected by underwriting team"

        await self.db.commit()
        await self.db.refresh(application)
        return application

    async def disburse_loan(self, application_id: uuid.UUID, lender_id: uuid.UUID, approved_amount: Decimal, risk_band: str = "B") -> Loan:
        application = await self.application_repo.get_by_id(application_id)
        if not application:
            raise NotFoundException("Loan application not found")
        if application.status != LoanApplicationStatus.APPROVED:
            raise ValidationException("Loan application must be APPROVED before disbursement")

        rate = await self.lender_repo.get_best_rate(lender_id, application.loan_type_id, risk_band)
        if not rate:
            raise NotFoundException("No active interest rate configured for this lender/loan-type/risk-band")

        # Defensive conversion: callers (e.g. query-param floats from the API layer)
        # may pass a plain float; all downstream money math requires Decimal.
        approved_amount = Decimal(str(approved_amount))
        processing_fee = (approved_amount * rate.processing_fee_pct / Decimal(100)).quantize(Decimal("0.01"))
        disbursed_amount = approved_amount - processing_fee

        loan = await self.loan_repo.create(
            application_id=application.id,
            employee_id=application.employee_id,
            lender_id=lender_id,
            principal_amount=approved_amount,
            interest_rate_pct=rate.annual_rate_pct,
            tenure_months=application.requested_tenure_months,
            processing_fee=processing_fee,
            disbursed_amount=disbursed_amount,
            disbursed_at=datetime.now(timezone.utc),
            outstanding_principal=approved_amount,
            status=LoanStatus.ACTIVE,
        )

        schedule = generate_amortization_schedule(
            principal=approved_amount,
            annual_rate_pct=rate.annual_rate_pct,
            tenure_months=application.requested_tenure_months,
            first_due_date=(datetime.now(timezone.utc) + timedelta(days=30)).date(),
        )
        for installment in schedule:
            await self.emi_repo.create(loan_id=loan.id, status=EMIStatus.UPCOMING, **installment)

        await self.txn_repo.create(
            employee_id=application.employee_id,
            loan_id=loan.id,
            transaction_type=TransactionType.DISBURSEMENT,
            amount=disbursed_amount,
            status=TransactionStatus.SUCCESS,
            reference_id=f"DISB-{uuid.uuid4().hex[:12].upper()}",
        )

        await self.db.commit()
        await self.db.refresh(loan)
        return loan

    async def pay_emi(self, emi_id: uuid.UUID, amount: Decimal, payment_gateway_ref: str | None = None):
        emi = await self.emi_repo.get_by_id(emi_id)
        if not emi:
            raise NotFoundException("EMI installment not found")
        if emi.status == EMIStatus.PAID:
            raise ValidationException("This EMI installment is already fully paid")

        emi.amount_paid = (emi.amount_paid or Decimal(0)) + amount
        if emi.amount_paid >= emi.emi_amount:
            emi.status = EMIStatus.PAID
            emi.paid_at = datetime.now(timezone.utc)
        else:
            emi.status = EMIStatus.PARTIALLY_PAID

        loan = await self.loan_repo.get_by_id(emi.loan_id)
        loan.outstanding_principal = max(Decimal(0), loan.outstanding_principal - emi.principal_component)
        if loan.outstanding_principal <= 0:
            loan.status = LoanStatus.CLOSED
            loan.closed_at = datetime.now(timezone.utc)

        await self.txn_repo.create(
            employee_id=loan.employee_id,
            loan_id=loan.id,
            emi_id=emi.id,
            transaction_type=TransactionType.EMI_PAYMENT,
            amount=amount,
            status=TransactionStatus.SUCCESS,
            reference_id=f"EMI-{uuid.uuid4().hex[:12].upper()}",
            payment_gateway_ref=payment_gateway_ref,
        )

        await self.db.commit()
        await self.db.refresh(emi)
        return emi
