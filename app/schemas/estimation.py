from pydantic import BaseModel, Field


class EstimationRequest(BaseModel):
    transcription: str = Field(min_length=1)


class TokenUsageResponse(BaseModel):
    input_tokens: int
    output_tokens: int
    total_tokens: int


class EstimationResponse(BaseModel):
    estimation: str
    model: str
    provider: str
    usage: TokenUsageResponse
