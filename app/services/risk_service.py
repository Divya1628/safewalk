from datetime import datetime
from typing import Any, Dict


def calculate_risk(
    time_of_day: str,
    day_type: str,
    incident_count: int,
    environment_activity: str,
) -> Dict[str, Any]:
    score = 0
    time_value = (time_of_day or "").strip().lower()
    day_value = (day_type or "").strip().lower()
    env_value = (environment_activity or "").strip().lower()

    time_map = {
        "night": 35,
        "late_night": 40,
        "evening": 20,
        "dusk": 22,
        "morning": 5,
        "daytime": 5,
        "afternoon": 8,
        "midday": 6,
    }
    score += time_map.get(time_value, 10)

    day_map = {
        "weekend": 15,
        "holiday": 18,
        "weekday": 6,
        "workday": 7,
    }
    score += day_map.get(day_value, 8)

    if incident_count >= 10:
        score += 30
    elif incident_count >= 5:
        score += 20
    elif incident_count >= 2:
        score += 10
    else:
        score += 0

    environment_map = {
        "high_activity": 18,
        "low_activity": 8,
        "moderate_activity": 12,
        "remote_area": 25,
        "poor_lighting": 18,
        "weather_risk": 15,
        "crowded_area": 10,
        "isolated_area": 22,
        "well_lit": 0,
    }
    score += environment_map.get(env_value, 8)

    risk_score = min(score, 100)

    if risk_score >= 70:
        level = "HIGH"
        recommendation = (
            "Avoid walking alone. Use safer transport or request company, and share your route with a trusted contact."
        )
    elif risk_score >= 35:
        level = "MEDIUM"
        recommendation = (
            "Stay alert, keep your phone charged, and share your journey with someone you trust."
        )
    else:
        level = "LOW"
        recommendation = (
            "SafeWalk can proceed normally. Continue checking in and keep a basic safety plan in place."
        )

    return {
        "risk_score": risk_score,
        "level": level,
        "recommendation": recommendation,
        "factors": {
            "time_of_day": time_value,
            "day_type": day_value,
            "incident_count": incident_count,
            "environment_activity": env_value,
            "timestamp": datetime.utcnow().isoformat(),
        },
    }
