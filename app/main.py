"""
SalaryFund AI - FastAPI application entrypoint.
Wires together middlewares, exception handlers, routers, and startup/shutdown events.
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.api.health import router as health_router
from app.api.v1.router import api_v1_router
from app.core.config import settings
from app.core.logging_config import configure_logging, get_logger
from app.middlewares.exception_handlers import register_exception_handlers
from app.middlewares.rate_limiter import limiter
from app.middlewares.request_logging import RequestLoggingMiddleware
from app.middlewares.security_headers import SecurityHeadersMiddleware

configure_logging()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("application_startup", environment=settings.ENVIRONMENT)
    yield
    logger.info("application_shutdown")


app = FastAPI(
    title=settings.PROJECT_NAME,
    description=(
        "SalaryFund AI - Enterprise Earned Wage Access & AI-Powered Lending Platform. "
        "Provides salary advances, personal loans, AI-driven eligibility scoring, "
        "fraud detection, Career Credit Score(tm), and financial wellness tracking."
    ),
    version="1.0.0",
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# --- Rate limiting ---
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# --- CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Security & logging middlewares ---
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(RequestLoggingMiddleware)

# --- Exception handlers ---
register_exception_handlers(app)

# --- Routers ---
app.include_router(health_router)
app.include_router(api_v1_router, prefix=settings.API_V1_PREFIX)
