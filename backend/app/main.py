"""FastAPI application: CORS, Sentry, routers, lifespan."""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.api.v1.router import api_router
from app.middleware.logging_middleware import RequestLoggingMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan: init DB pool, cleanup on shutdown."""
    yield
    # Cleanup if needed (e.g. close DB pool)


def create_application() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title=settings.PROJECT_NAME,
        openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",
        docs_url="/docs" if settings.ENVIRONMENT == "dev" else None,
        redoc_url="/redoc" if settings.ENVIRONMENT == "dev" else None,
        lifespan=lifespan,
    )

    app.add_middleware(RequestLoggingMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    if settings.SENTRY_DSN and settings.ENVIRONMENT == "prod":
        import sentry_sdk
        from sentry_sdk.integrations.fastapi import FastApiIntegration
        from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration

        sentry_sdk.init(
            dsn=settings.SENTRY_DSN,
            environment=settings.SENTRY_ENVIRONMENT,
            integrations=[FastApiIntegration(), SqlalchemyIntegration()],
            traces_sample_rate=0.1,
        )

    app.include_router(api_router, prefix=settings.API_V1_PREFIX)

    @app.get("/health")
    def health():
        return {"status": "ok"}

    return app


app = create_application()
