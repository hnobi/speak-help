from pydantic import BaseModel


class HealthResponse(BaseModel):
    ok: bool = True
    app: str = "speaking-coach-api"
    version: str = "0.1.0"


class ErrorResponse(BaseModel):
    detail: str
