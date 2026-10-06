from fastapi import APIRouter
from app.schemas import RiskRequest
from app.services.ai_risk_engine import RealTimeRiskEngine

router = APIRouter()


@router.post("/calculate")
def calculate_risk_endpoint(payload: RiskRequest):
    """
    Calculate risk using real-time AI engine.
    """
    engine = RealTimeRiskEngine()
    result = engine.compute_dynamic_risk(
        time_of_day=payload.time_of_day,
        day_type=payload.day_type,
        environment_activity=payload.environment_activity,
        incident_count=payload.incident_count,
    )
    return result


@router.post("/calculate-advanced")
def calculate_risk_advanced(payload: dict):
    """
    Advanced AI risk assessment with sensor data.
    """
    engine = RealTimeRiskEngine()
    result = engine.compute_dynamic_risk(
        time_of_day=payload.get("time_of_day", "daytime"),
        day_type=payload.get("day_type", "weekday"),
        environment_activity=payload.get("environment_activity", "high_activity"),
        incident_count=payload.get("incident_count", 0),
        weather=payload.get("weather", "clear"),
        heart_rate=payload.get("heart_rate", 0),
        movement_pattern=payload.get("movement_pattern", "normal"),
        response_time=payload.get("response_time", 0),
        crime_density=payload.get("crime_density", "low"),
    )
    return result
