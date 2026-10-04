from datetime import datetime
from typing import Any, Dict, List

from bson import ObjectId

from app.database import db


def create_safewalk_session(payload: Dict[str, Any], risk_result: Dict[str, Any]) -> str:
    session_data = {
        "user_id": payload["user_id"],
        "destination": payload["destination"],
        "time_of_day": payload["time_of_day"],
        "day_type": payload["day_type"],
        "incident_count": payload["incident_count"],
        "environment_activity": payload["environment_activity"],
        "risk_score": risk_result["risk_score"],
        "risk_level": risk_result["level"],
        "recommendation": risk_result["recommendation"],
        "status": "active",
        "countdown_seconds": 10,
        "started_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "checkins": [],
        "history_saved": False,
    }

    session_id = db["safewalk_sessions"].insert_one(session_data).inserted_id
    return str(session_id)


def record_countdown(session_id: str, user_id: str, countdown_seconds: int) -> Dict[str, Any]:
    session = db["safewalk_sessions"].find_one({"_id": ObjectId(session_id), "user_id": user_id})
    if not session:
        raise ValueError("Session not found")

    item = {
        "type": "countdown",
        "seconds": countdown_seconds,
        "recorded_at": datetime.utcnow(),
    }
    db["safewalk_sessions"].update_one(
        {"_id": ObjectId(session_id)},
        {"$set": {"countdown_seconds": countdown_seconds, "updated_at": datetime.utcnow()}, "$push": {"checkins": item}},
    )

    return {"message": "Countdown set", "countdown_seconds": countdown_seconds}


def record_checkin(session_id: str, user_id: str, status: str, message: str = "") -> Dict[str, Any]:
    session = db["safewalk_sessions"].find_one({"_id": ObjectId(session_id), "user_id": user_id})
    if not session:
        raise ValueError("Session not found")

    item = {
        "type": "checkin",
        "status": status,
        "message": message,
        "recorded_at": datetime.utcnow(),
    }
    db["safewalk_sessions"].update_one(
        {"_id": ObjectId(session_id)},
        {"$set": {"updated_at": datetime.utcnow()}, "$push": {"checkins": item}},
    )

    return {"message": "Check-in saved", "status": status}


def finish_safewalk(session_id: str, user_id: str, status: str, notes: str = "") -> Dict[str, Any]:
    session = db["safewalk_sessions"].find_one({"_id": ObjectId(session_id), "user_id": user_id})
    if not session:
        raise ValueError("Session not found")

    final_status = status if status in ["safe", "unsafe", "emergency"] else "safe"
    summary = {
        "session_id": session_id,
        "user_id": user_id,
        "destination": session.get("destination"),
        "risk_level": session.get("risk_level"),
        "status": final_status,
        "notes": notes,
        "finished_at": datetime.utcnow(),
        "history_saved": True,
    }

    db["safewalk_sessions"].update_one(
        {"_id": ObjectId(session_id)},
        {
            "$set": {
                "status": final_status,
                "notes": notes,
                "finished_at": datetime.utcnow(),
                "history_saved": True,
                "updated_at": datetime.utcnow(),
            },
            "$push": {
                "checkins": {
                    "type": "final_status",
                    "status": final_status,
                    "notes": notes,
                    "recorded_at": datetime.utcnow(),
                }
            },
        },
    )

    db["history"].insert_one(summary)
    return {
        "message": "SafeWalk finished and saved to history",
        "status": final_status,
        "session_id": session_id,
    }


def get_history_for_user(user_id: str) -> List[Dict[str, Any]]:
    sessions = list(db["safewalk_sessions"].find({"user_id": user_id}))
    for item in sessions:
        item["_id"] = str(item["_id"])
    return sessions
