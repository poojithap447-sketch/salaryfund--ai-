"""
Import every model module here so Base.metadata is fully populated
for Alembic autogenerate and for SQLAlchemy relationship resolution.
"""
from app.models.rbac import User, Role, Permission, RefreshToken, OTP, AuditLog  # noqa: F401
from app.models.organization import Employer, Department, Employee  # noqa: F401
from app.models.loans import (  # noqa: F401
    Lender,
    LoanType,
    LoanPolicy,
    InterestRate,
    LoanApplication,
    Loan,
    EMI,
    Transaction,
)
from app.models.payroll import Payroll  # noqa: F401
from app.models.documents import Document, KYC  # noqa: F401
from app.models.ai_and_wellness import (  # noqa: F401
    CareerCreditScore,
    FinancialWellnessRecord,
    AIPrediction,
    FraudAlert,
    Notification,
    Report,
)
