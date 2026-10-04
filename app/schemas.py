from pydantic import BaseModel, Field
from typing import Literal


class RiskRequest(BaseModel):
    time_of_day: str = Field(..., example="night")
    day_type: str = Field(..., example="weekend")
    incident_count: int = Field(..., ge=0, example=6)
    environment_activity: str = Field(..., example="poor_lighting")


class RiskResponse(BaseModel):
    risk_score: int
    level: str
    recommendation: str
    factors: dict


class SafeWalkCreateRequest(BaseModel):
    user_id: str = Field(..., example="user_123")
    destination: str = Field(..., example="Downtown Station")
    time_of_day: str = Field(..., example="night")
    day_type: str = Field(..., example="weekday")
    incident_count: int = Field(..., ge=0, example=3)
    environment_activity: str = Field(..., example="low_activity")


class CountdownRequest(BaseModel):
    session_id: str = Field(..., example="651d7db7c3c20a640126749f")
    user_id: str = Field(..., example="user_123")
    countdown_seconds: int = Field(default=10, ge=1, le=120)


class CheckInRequest(BaseModel):
    session_id: str = Field(..., example="651d7db7c3c20a640126749f")
    user_id: str = Field(..., example="user_123")
    status: Literal["safe", "delayed", "emergency"] = Field(..., example="safe")
    message: str = Field(default="", example="I am safe and on my route.")


class FinishSafeWalkRequest(BaseModel):
    session_id: str = Field(..., example="651d7db7c3c20a640126749f")
    user_id: str = Field(..., example="user_123")
    status: Literal["safe", "unsafe", "emergency"] = Field(..., example="safe")
    notes: str = Field(default="", example="Reached destination without issues.")
