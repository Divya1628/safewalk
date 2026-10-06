from fastapi import APIRouter, HTTPException
from app.services.adaptive_shield import (
    AdaptiveSafetyShield,
    CameraSignal,
    DuressCommandDecoder,
    RiskSignal,
    UserInput,
)

router = APIRouter()


@router.post("/analyze-risk-signals")
def analyze_risk_signals(payload: dict):
    """
    Analyze real-time risk signals from wearables and sensors.
    """
    result = RiskSignal.analyze_risk_signals(
        heart_rate=payload.get("heart_rate", 0),
        movement_pattern=payload.get("movement_pattern", "normal"),
        gps_deviation=payload.get("gps_deviation", 0.0),
        check_in_missed=payload.get("check_in_missed", False),
        response_time=payload.get("response_time", 0),
    )
    return result


@router.post("/analyze-camera-feed")
def analyze_camera_feed(payload: dict):
    """
    Analyze camera feed for visual threats using computer vision.
    """
    result = CameraSignal.analyze_camera_feed(
        person_count=payload.get("person_count", 0),
        threat_detected=payload.get("threat_detected", False),
        face_recognition_match=payload.get("face_recognition_match", False),
        lighting_level=payload.get("lighting_level", 100),
        movement_direction=payload.get("movement_direction", "away"),
    )
    return result


@router.post("/process-user-command")
def process_user_command(payload: dict):
    """
    Process user input: panic button, gestures, voice commands.
    """
    result = UserInput.process_user_command(
        command_type=payload.get("command_type", "unknown"),
        gesture=payload.get("gesture"),
        voice_command=payload.get("voice_command"),
        button_press=payload.get("button_press"),
    )
    return result


@router.post("/fuse-signals")
def fuse_signals(payload: dict):
    """
    Fuse all signal sources (risk, camera, user input).
    """
    shield = AdaptiveSafetyShield()

    risk_signals = payload.get(
        "risk_signals",
        {"risk_score": 0, "signals": []},
    )
    camera_signals = payload.get(
        "camera_signals",
        {"threat_score": 0, "threats": []},
    )
    user_input = payload.get("user_input")

    fused = shield.fuse_signals(risk_signals, camera_signals, user_input)
    return fused


@router.post("/safety-decision")
def make_safety_decision(payload: dict):
    """
    Make unified safety decision: Normal SOS vs Covert Duress Alert.
    """
    shield = AdaptiveSafetyShield()

    fused_signals = payload.get("fused_signals", {})
    is_covert_mode = payload.get("is_covert_mode", False)

    decision = shield.make_safety_decision(fused_signals, is_covert_mode)
    return decision


@router.post("/full-safety-assessment")
def full_safety_assessment(payload: dict):
    """
    Complete end-to-end assessment: analyze all signals and make decision.
    Includes covert duress detection.
    """
    shield = AdaptiveSafetyShield()

    # Step 1: Analyze risk signals
    risk_signals = RiskSignal.analyze_risk_signals(
        heart_rate=payload.get("heart_rate", 0),
        movement_pattern=payload.get("movement_pattern", "normal"),
        gps_deviation=payload.get("gps_deviation", 0.0),
        check_in_missed=payload.get("check_in_missed", False),
        response_time=payload.get("response_time", 0),
    )

    # Step 2: Analyze camera signals
    camera_signals = CameraSignal.analyze_camera_feed(
        person_count=payload.get("person_count", 0),
        threat_detected=payload.get("threat_detected", False),
        face_recognition_match=payload.get("face_recognition_match", False),
        lighting_level=payload.get("lighting_level", 100),
        movement_direction=payload.get("movement_direction", "away"),
    )

    # Step 3: Process user input
    user_input = None
    if payload.get("gesture") or payload.get("voice_command") or payload.get("button_press"):
        user_input = UserInput.process_user_command(
            command_type=payload.get("command_type", "gesture"),
            gesture=payload.get("gesture"),
            voice_command=payload.get("voice_command"),
            button_press=payload.get("button_press"),
        )

    # Step 4: Fuse all signals
    fused_signals = shield.fuse_signals(risk_signals, camera_signals, user_input)

    # Step 5: Make safety decision
    is_covert_mode = payload.get("is_covert_mode", False)
    decision = shield.make_safety_decision(fused_signals, is_covert_mode)

    # Step 6: Check for duress commands
    duress_check = {"duress_detected": False}
    if payload.get("check_in_message"):
        duress_check = DuressCommandDecoder.detect_duress_command(
            payload.get("check_in_message")
        )
        if duress_check["duress_detected"]:
            # Override to covert duress alert
            decision = shield.make_safety_decision(
                fused_signals, is_covert_mode=True
            )

    return {
        "assessment_timestamp": payload.get("timestamp"),
        "stage_1_risk_analysis": risk_signals,
        "stage_2_camera_analysis": camera_signals,
        "stage_3_user_input": user_input,
        "stage_4_signal_fusion": fused_signals,
        "stage_5_safety_decision": decision,
        "stage_6_duress_detection": duress_check,
        "final_alert_type": decision.get("alert_type"),
        "final_action": decision.get("actions"),
    }


@router.post("/detect-duress-command")
def detect_duress_command(payload: dict):
    """
    Detect hidden duress commands in check-in messages.
    Supports code phrases and emoji sequences.
    """
    result = DuressCommandDecoder.detect_duress_command(
        payload.get("check_in_message", "")
    )
    return result
