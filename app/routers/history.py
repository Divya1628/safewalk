from fastapi import APIRouter, Depends
from app.routers.auth import get_current_user
from app.services.safewalk_service import get_history_for_user

router = APIRouter()


@router.get("/")
def get_history(user_id: str = Depends(get_current_user)):
    return {"user_id": user_id, "sessions": get_history_for_user(user_id)}
