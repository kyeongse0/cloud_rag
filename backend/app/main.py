"""FastAPI application entry point."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    # Startup
    print(f"Starting {settings.app_name}...")
    yield
    # Shutdown
    print(f"Shutting down {settings.app_name}...")


app = FastAPI(
    title=settings.app_name,
    description="Test and compare local LLM models",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Welcome to LLM Test Platform API"}


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "app": settings.app_name,
        "version": "0.1.0",
    }


# API routers will be added here
# from app.api.v1 import auth, models, prompts, tests
# app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
# app.include_router(models.router, prefix="/api/v1/models", tags=["models"])
# app.include_router(prompts.router, prefix="/api/v1/prompts", tags=["prompts"])
# app.include_router(tests.router, prefix="/api/v1/tests", tags=["tests"])
