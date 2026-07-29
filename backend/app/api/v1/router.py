"""
Aggregates all v1 domain routers into a single APIRouter mounted by main.py.
"""
from fastapi import APIRouter

from app.api.v1.admin.router import router as admin_router
from app.api.v1.analytics.router import router as analytics_router
from app.api.v1.authentication.router import router as auth_router
from app.api.v1.career_score.router import router as career_score_router
from app.api.v1.documents.router import router as documents_router
from app.api.v1.emi.router import router as emi_router
from app.api.v1.employees.router import router as employees_router
from app.api.v1.employers.router import router as employers_router
from app.api.v1.financial_wellness.router import router as financial_wellness_router
from app.api.v1.lenders.router import router as lenders_router
from app.api.v1.loans.router import router as loans_router
from app.api.v1.notifications.router import router as notifications_router
from app.api.v1.payroll.router import router as payroll_router
from app.api.v1.reports.router import router as reports_router

api_v1_router = APIRouter()

api_v1_router.include_router(auth_router)
api_v1_router.include_router(employers_router)
api_v1_router.include_router(employees_router)
api_v1_router.include_router(loans_router)
api_v1_router.include_router(emi_router)
api_v1_router.include_router(payroll_router)
api_v1_router.include_router(career_score_router)
api_v1_router.include_router(financial_wellness_router)
api_v1_router.include_router(documents_router)
api_v1_router.include_router(notifications_router)
api_v1_router.include_router(admin_router)
api_v1_router.include_router(lenders_router)
api_v1_router.include_router(analytics_router)
api_v1_router.include_router(reports_router)
