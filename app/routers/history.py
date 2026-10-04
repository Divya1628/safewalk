from fastapi import APIRouter

from app.services.safewalk_service import get_history_for_user

router = APIRouter()


@router.get("/{user_id}")
def get_history(user_id: str):
    return {"user_id": user_id, "sessions": get_history_for_user(user_id)}
