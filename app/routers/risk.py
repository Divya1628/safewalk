from fastapi import APIRouter

from app.schemas import RiskRequest, RiskResponse
from app.services.risk_service import calculate_risk

router = APIRouter()


@router.post("/calculate", response_model=RiskResponse)
def calculate_risk_endpoint(payload: RiskRequest):
    result = calculate_risk(
        payload.time_of_day,
        payload.day_type,
        payload.incident_count,
        payload.environment_activity,
    )
    return result
