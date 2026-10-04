from fastapi import APIRouter, HTTPException

from app.schemas import CheckInRequest, CountdownRequest, FinishSafeWalkRequest, RiskRequest, RiskResponse, SafeWalkCreateRequest
from app.services.risk_service import calculate_risk
from app.services.safewalk_service import create_safewalk_session, finish_safewalk, get_history_for_user, record_checkin, record_countdown

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


@router.post("/start")
def start_safewalk(payload: SafeWalkCreateRequest):
    risk_result = calculate_risk(
        payload.time_of_day,
        payload.day_type,
        payload.incident_count,
        payload.environment_activity,
    )

    session_id = create_safewalk_session(payload.model_dump(), risk_result)

    return {
        "session_id": session_id,
        "message": "SafeWalk started",
        "risk_level": risk_result["level"],
        "risk_score": risk_result["risk_score"],
        "recommendation": risk_result["recommendation"],
    }


@router.post("/countdown")
def set_countdown(payload: CountdownRequest):
    try:
        result = record_countdown(payload.session_id, payload.user_id, payload.countdown_seconds)
        return result
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/checkin")
def check_in(payload: CheckInRequest):
    try:
        result = record_checkin(payload.session_id, payload.user_id, payload.status, payload.message)
        return result
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/finish")
def finish_session(payload: FinishSafeWalkRequest):
    try:
        result = finish_safewalk(payload.session_id, payload.user_id, payload.status, payload.notes)
        return result
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
