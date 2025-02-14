from pydantic import BaseModel, Field

class HealthCheckResponse(BaseModel):
    version: str = Field(..., example='1.0.0')
    status: str = Field(..., example='UP')
