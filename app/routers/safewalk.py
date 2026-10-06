from fastapi import APIRouter, HTTPException, Depends
from app.routers.auth import get_current_user
from app.schemas import (
    CheckInRequest,
    CountdownRequest,
    FinishSafeWalkRequest,
    SafeWalkCreateRequest,
)
from app.services.ai_risk_engine import RealTimeRiskEngine
from app.services.safewalk_service import (
    create_safewalk_session,
    finish_safewalk,
    get_history_for_user,
    record_checkin,
    record_countdown,
)

router = APIRouter()


@router.post("/start")
def start_safewalk(payload: SafeWalkCreateRequest, user_id: str = Depends(get_current_user)):
    """
    Start a SafeWalk session with AI risk assessment.
    """
    engine = RealTimeRiskEngine()
    risk_result = engine.compute_dynamic_risk(
        time_of_day=payload.time_of_day,
        day_type=payload.day_type,
        environment_activity=payload.environment_activity,
        incident_count=payload.incident_count,
    )

    session_id = create_safewalk_session(user_id, payload.model_dump(), risk_result)

    return {
        "session_id": session_id,
        "message": "SafeWalk started with AI risk assessment",
        "risk_level": risk_result["risk_level"],
        "risk_score": risk_result["risk_score"],
        "incident_probability": risk_result["incident_probability"],
        "recommended_action": risk_result["recommended_action"],
        "recommendation": risk_result["recommendation"],
    }


@router.post("/countdown")
def set_countdown(
    payload: CountdownRequest, user_id: str = Depends(get_current_user)
):
    try:
        result = record_countdown(payload.session_id, user_id, payload.countdown_seconds)
        return result
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/checkin")
def check_in(payload: CheckInRequest, user_id: str = Depends(get_current_user)):
    try:
        result = record_checkin(payload.session_id, user_id, payload.status, payload.message)
        return result
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/finish")
def finish_session(payload: FinishSafeWalkRequest, user_id: str = Depends(get_current_user)):
    try:
        result = finish_safewalk(payload.session_id, user_id, payload.status, payload.notes)
        return result
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
