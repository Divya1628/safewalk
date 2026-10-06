from pydantic import BaseModel, EmailStr, Field
from typing import Literal, Optional
from datetime import datetime


class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)
    full_name: str = Field(..., min_length=2)
    phone: str = Field(..., regex=r"^\+?[0-9]{10,15}$")


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    user_id: str
    email: str
    full_name: str
    phone: str
    created_at: datetime


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class TrustedContact(BaseModel):
    name: str
    phone: str
    email: Optional[str] = None
    relationship: str = "friend"


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
    destination: str = Field(..., example="Downtown Station")
    time_of_day: str = Field(..., example="night")
    day_type: str = Field(..., example="weekday")
    incident_count: int = Field(..., ge=0, example=3)
    environment_activity: str = Field(..., example="low_activity")


class CountdownRequest(BaseModel):
    session_id: str = Field(..., example="651d7db7c3c20a640126749f")
    countdown_seconds: int = Field(default=10, ge=1, le=120)


class CheckInRequest(BaseModel):
    session_id: str = Field(..., example="651d7db7c3c20a640126749f")
    status: Literal["safe", "delayed", "emergency"] = Field(..., example="safe")
    message: str = Field(default="", example="I am safe and on my route.")


class FinishSafeWalkRequest(BaseModel):
    session_id: str = Field(..., example="651d7db7c3c20a640126749f")
    status: Literal["safe", "unsafe", "emergency"] = Field(..., example="safe")
    notes: str = Field(default="", example="Reached destination without issues.")
