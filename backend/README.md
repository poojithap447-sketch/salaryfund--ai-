# SalaryFund AI — Backend

Enterprise fintech backend for an AI-powered earned-wage-access and lending platform. Pure Python/FastAPI, clean architecture, async SQLAlchemy 2.0, and three real trained ML subsystems (loan eligibility, fraud detection, career credit scoring) plus a rules-based financial wellness engine.

This backend has been **built and verified end-to-end** in a live environment: Postgres schema migrated via Alembic, seed data loaded, models trained, and a full user journey (register → login → onboard employer → onboard employee → submit loan → AI review → disburse → EMI schedule) exercised successfully against real HTTP requests. All 33 automated tests pass.

## Architecture

Clean architecture with strict separation of concerns:

```
app/
  api/v1/<domain>/router.py   # HTTP layer only — thin, delegates to services
  services/                   # business logic, orchestrates repositories + AI engines
  repositories/                # SQLAlchemy queries, one per aggregate
  models/                      # SQLAlchemy 2.0 ORM models (29 tables)
  schemas/                     # Pydantic v2 request/response contracts
  ai/
    eligibility/                # inference engine (loads trained models, runs SHAP)
    fraud_detection/             # rule engine + IsolationForest anomaly scoring
    career_credit/                # Career Credit Score(tm) calculator
    financial_wellness/            # DTI/savings/EMI-burden calculator
    training/                       # model training pipelines
  core/                         # config, logging, exception hierarchy
  security/                     # JWT, password hashing, OTP, field encryption
  dependencies/                 # FastAPI DI: current-user, RBAC
  middlewares/                  # rate limiting, security headers, request logging, exception handlers
  background_tasks/             # Celery app + tasks (reminders, retraining, reports)
  database/                     # async engine/session, seed scripts
  utils/                        # EMI math, OCR, encryption, email/SMS clients
```

## What is fully implemented (real logic, not stubs)

- **Auth**: register, login, OTP (login/email/phone/password-reset/MFA purposes), JWT access+refresh with rotation, RBAC via roles/permissions, account lockout after repeated failures, audit-logged.
- **Employers/Employees/Departments**: full onboarding, PII (PAN/Aadhaar/bank account) encrypted at rest with Fernet.
- **Loans**: application submission → AI eligibility + fraud review → auto-approve/reject/manual-review/flag-fraud → manual decisioning → disbursement → EMI schedule generation via correct reducing-balance amortization → repayment processing with automatic loan closure.
- **Loan Eligibility Engine**: trains and compares RandomForestClassifier, XGBoostClassifier, and LogisticRegression; selects the best by ROC-AUC; returns approval probability, risk score, eligible amount, confidence, and full SHAP feature-contribution explainability; routes to AUTO_APPROVE / MANUAL_REVIEW / AUTO_REJECT.
- **Fraud Detection**: duplicate-PAN, salary-volatility, multi-application, and document-forgery rule checks combined with an IsolationForest anomaly score into a composite risk score and severity-tagged alerts.
- **Career Credit Score™**: six weighted sub-scores (employment stability, salary growth, attendance, promotions, performance, repayment behavior) → 300–900 score with band, computed from real EMI/payroll history, stored with full history.
- **Financial Wellness**: debt-to-income, savings ratio, EMI burden, loan utilization, emergency reserve months → 0–100 wellness score with plain-language recommendations.
- **OCR/Documents**: OpenCV preprocessing (denoise, adaptive threshold) + pytesseract extraction of PAN/Aadhaar, plus a document forgery heuristic (ELA-style re-compression diff, edge density, sharpness) feeding the fraud engine.
- **Payroll**: bulk cycle ingestion with automatic EMI-deduction netting.
- **Notifications**: email/SMS dispatch via Celery with dev-mode logging fallback (no provider credentials required to run locally).
- **Admin**: fraud alert queue and resolution workflow.
- **Analytics**: portfolio summary, application funnel, per-employer utilization.
- **Reports**: async CSV report generation via Celery.
- **Security**: bcrypt password hashing, JWT (python-jose), Redis-backed rate limiting (SlowAPI), Helmet-equivalent security headers, global exception handling, structured JSON logging with correlation IDs, field-level PII encryption.
- **52 REST endpoints**, full OpenAPI/Swagger at `/docs`.

## What is scaffolded for extension (clearly marked in code, not disguised as complete)

- **HRMS payroll sync connector** (`app/background_tasks/payroll_tasks.py`): entry point present; provider-specific OAuth/API integration (Keka, Zoho Payroll, etc.) needs to be added per your chosen HRMS.
- **SMS/Email providers**: abstracted behind `app/utils/sms_client.py` / `email_client.py` with a generic REST example — swap in Twilio/MSG91/SES specifics.
- **KYC third-party verification** (PAN/Aadhaar verification against government APIs, liveness/face-match): the `KYC` model and status machine exist; the actual verification-provider integration is not wired up (most providers require paid API contracts).
- **Fraud/eligibility model retraining data source**: currently bootstraps from a realistic synthetic dataset (`app/ai/training/synthetic_eligibility_data.py`) so the platform is trainable and demoable from day one. Once real loan-outcome history accumulates, point `train_and_compare()` at a real data extract instead.

## Quick start (Docker — recommended)

```bash
cd backend
cp .env.example .env
# edit .env: set SECRET_KEY and FIELD_ENCRYPTION_KEY (commands provided inline in the file)
docker compose up --build
```

This brings up Postgres, Redis, the API (auto-runs migrations, seed data, and initial model training on startup), a Celery worker, Celery beat, and Flower (Celery monitoring UI) at `localhost:5555`.

API docs: `http://localhost:8000/docs`
Health check: `http://localhost:8000/health`

## Quick start (local, no Docker)

```bash
cd backend
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# Postgres + Redis must be running locally; then:
cp .env.example .env   # edit DATABASE_URL(_SYNC)/REDIS_URL for localhost, set SECRET_KEY + FIELD_ENCRYPTION_KEY

alembic upgrade head
python -m app.database.seeds.seed_data
python -m app.ai.training.train_eligibility

uvicorn app.main:app --reload
```

Run the Celery worker + beat scheduler in separate terminals:
```bash
celery -A app.background_tasks.celery_app worker --loglevel=info
celery -A app.background_tasks.celery_app beat --loglevel=info
```

## Tests

```bash
pytest tests/ -v
```

33 tests covering auth flows, EMI amortization math, and all three AI engines (career score, financial wellness, fraud detection) as pure-function unit tests plus API integration tests.

## Example end-to-end flow (verified working)

```bash
# 1. Register + login
curl -X POST localhost:8000/api/v1/auth/register -H "Content-Type: application/json" \
  -d '{"email":"admin@x.com","phone_number":"+919876543210","password":"Passw0rd!23","user_type":"PLATFORM_ADMIN"}'
curl -X POST localhost:8000/api/v1/auth/login -H "Content-Type: application/json" \
  -d '{"email":"admin@x.com","password":"Passw0rd!23"}'

# 2. Onboard employer, then employee (see /docs for full payloads)

# 3. Employee submits a loan application
curl -X POST localhost:8000/api/v1/loans/applications -H "Authorization: Bearer <employee_token>" \
  -H "Content-Type: application/json" \
  -d '{"loan_type_id":"<uuid>","requested_amount":20000,"requested_tenure_months":3,"purpose":"Medical emergency"}'

# 4. Admin triggers AI review (eligibility + fraud engines run here)
curl -X POST localhost:8000/api/v1/loans/applications/<id>/ai-review -H "Authorization: Bearer <admin_token>"

# 5. Disburse (if approved) — generates the full EMI schedule automatically
curl -X POST "localhost:8000/api/v1/loans/applications/<id>/disburse?lender_id=<uuid>&approved_amount=20000&risk_band=B" \
  -H "Authorization: Bearer <admin_token>"
```

## Database

29 normalized tables across identity/RBAC, organization (employers/departments/employees), loans (types/policies/applications/loans/EMIs/transactions/lenders/interest-rates), documents/KYC, and AI/wellness (predictions/fraud-alerts/career-scores/wellness-records/notifications/reports). Full schema is in `alembic/versions/` — generated by `alembic revision --autogenerate` directly from the SQLAlchemy models, so migrations and models are guaranteed in sync.

## Postman / API exploration

The complete, always-accurate API contract is served at `/docs` (Swagger UI) and `/redoc`, and the raw OpenAPI spec at `/api/v1/openapi.json` — import that URL directly into Postman or Insomnia for an always-current collection rather than a hand-maintained file that drifts from the code.

## Security notes for production deployment

- Rotate `SECRET_KEY` and `FIELD_ENCRYPTION_KEY` — never reuse the values in `.env.example`.
- Put this behind a TLS-terminating reverse proxy (nginx/ALB) — the app is HTTPS-ready but doesn't terminate TLS itself.
- Review `CORS_ORIGINS` before going live.
- The rate limits in `.env.example` are conservative defaults — tune to your traffic profile.
- `MAX_UPLOAD_SIZE_MB` and `ALLOWED_DOCUMENT_TYPES` guard the document upload endpoint against abuse.
