from collections.abc import Callable

from fastapi import APIRouter, Depends, HTTPException

from app.schemas.estimation import EstimationRequest, EstimationResponse
from app.services.estimation import generate_estimation
from app.services.llm import LanguageModel, LanguageModelError


def create_router(get_language_model: Callable[[], LanguageModel]) -> APIRouter:
    router = APIRouter(tags=["estimations"])
    require_language_model = Depends(get_language_model)

    @router.post("/estimate", response_model=EstimationResponse)
    def create_estimation(
        request: EstimationRequest,
        language_model: LanguageModel = require_language_model,
    ) -> EstimationResponse:
        try:
            estimation = generate_estimation(request.transcription, language_model)
        except LanguageModelError:
            raise HTTPException(status_code=500, detail="Estimation failed") from None
        return EstimationResponse.model_validate(estimation.model_dump())

    return router
