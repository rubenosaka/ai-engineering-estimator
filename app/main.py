from fastapi import FastAPI
from pydantic import BaseModel

from app.config import get_settings
from app.routers.estimations import create_router
from app.services.llm import LanguageModel
from app.services.providers.factory import build_language_model


class HealthResponse(BaseModel):
    status: str
    version: str
    environment: str


def get_language_model() -> LanguageModel:
    return build_language_model(get_settings())


def create_app() -> FastAPI:
    application = FastAPI(
        title="Servicio de estimación de software (CAG)",
        description=(
            "Genera una estimación de software a partir de la transcripción de una reunión. "
            "El contexto de referencia viaja en el prompt."
        ),
        version="0.1.0",
    )
    application.include_router(create_router(get_language_model), prefix="/api/v1")

    @application.get("/health", response_model=HealthResponse)
    def health() -> HealthResponse:
        settings = get_settings()
        return HealthResponse(status="healthy", version="0.1.0", environment=settings.APP_ENV)

    return application


app = create_app()
