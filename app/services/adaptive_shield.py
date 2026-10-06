from datetime import datetime
from typing import Any, Dict, List
from enum import Enum
import json


class AlertType(str, Enum):
    NORMAL_SOS = "normal_sos"
    COVERT_DURESS = "covert_duress"
    SILENT_ALERT = "silent_alert"
    PANIC_BUTTON = "panic_button"


class RiskSignal:
    """
    Monitors real-time risk signals from multiple sources.
    """

    @staticmethod
    def analyze_risk_signals(
        heart_rate: int,
        movement_pattern: str,
        gps_deviation: float,
        check_in_missed: bool,
        response_time: int,
    ) -> Dict[str, Any]:
        """
        Analyze risk signals from wearables and sensors.
        Returns risk level and anomaly details.
        """
        signals = []
        risk_score = 0

        # Heart rate analysis
        if heart_rate > 130:
            signals.append({"type": "elevated_heart_rate", "value": heart_rate, "severity": "high"})
            risk_score += 25
        elif heart_rate > 110:
            signals.append({"type": "elevated_heart_rate", "value": heart_rate, "severity": "medium"})
            risk_score += 15

        # Movement pattern analysis
        movement_risk = {
            "stationary": 30,
            "erratic": 35,
            "running": 20,
            "slow": 15,
            "normal": 0,
        }
        move_val = movement_risk.get(movement_pattern.lower(), 10)
        if move_val > 0:
            signals.append({"type": "unusual_movement", "pattern": movement_pattern, "severity": "high" if move_val > 20 else "medium"})
        risk_score += move_val

        # GPS deviation (off-route)
        if gps_deviation > 0.5:  # km
            signals.append({"type": "route_deviation", "deviation_km": gps_deviation, "severity": "high"})
            risk_score += 25
        elif gps_deviation > 0.2:
            signals.append({"type": "minor_deviation", "deviation_km": gps_deviation, "severity": "medium"})
            risk_score += 10

        # Missed check-in
        if check_in_missed:
            signals.append({"type": "missed_checkin", "response_time_sec": response_time, "severity": "critical"})
            risk_score += 40
        elif response_time > 600:  # 10 minutes
            signals.append({"type": "delayed_response", "response_time_sec": response_time, "severity": "high"})
            risk_score += 20

        return {
            "risk_score": min(risk_score, 100),
            "signals": signals,
            "detected_at": datetime.utcnow().isoformat(),
        }


class CameraSignal:
    """
    Processes computer vision signals from device camera.
    Detects threats using edge AI.
    """

    @staticmethod
    def analyze_camera_feed(
        person_count: int,
        threat_detected: bool,
        face_recognition_match: bool,
        lighting_level: int,
        movement_direction: str,
    ) -> Dict[str, Any]:
        """
        Analyze camera feed for threats.
        Returns threat assessment and recommendations.
        """
        threats = []
        threat_score = 0

        # Person count analysis
        if person_count > 3:
            threats.append({"type": "crowded_surroundings", "count": person_count, "severity": "low"})
            threat_score += 5
        elif person_count == 0:
            threats.append({"type": "isolated_environment", "count": 0, "severity": "medium"})
            threat_score += 15

        # Direct threat detection (object detection, weapon detection)
        if threat_detected:
            threats.append({"type": "potential_threat", "severity": "critical"})
            threat_score += 50

        # Face recognition (if known threat/stalker)
        if face_recognition_match:
            threats.append({"type": "known_threat_detected", "severity": "critical"})
            threat_score += 45

        # Lighting analysis
        if lighting_level < 20:
            threats.append({"type": "low_lighting", "level": lighting_level, "severity": "medium"})
            threat_score += 12

        # Movement direction (towards user)
        if movement_direction == "towards_user":
            threats.append({"type": "approaching_threat", "direction": movement_direction, "severity": "high"})
            threat_score += 30

        return {
            "threat_score": min(threat_score, 100),
            "threats": threats,
            "analyzed_at": datetime.utcnow().isoformat(),
        }


class UserInput:
    """
    Processes explicit user inputs and gesture-based commands.
    """

    @staticmethod
    def process_user_command(
        command_type: str,
        gesture: str = None,
        voice_command: str = None,
        button_press: str = None,
    ) -> Dict[str, Any]:
        """
        Process user input commands.
        Supports:
        - Panic button
        - Voice commands
        - Gesture-based alerts (e.g., double tap)
        - SOS sequences
        """
        response = {"command_type": command_type, "timestamp": datetime.utcnow().isoformat()}

        if button_press == "panic_button":
            response["action"] = "immediate_sos"
            response["alert_type"] = AlertType.PANIC_BUTTON.value
            response["urgency"] = "critical"

        elif gesture == "triple_tap":
            response["action"] = "covert_alert"
            response["alert_type"] = AlertType.COVERT_DURESS.value
            response["urgency"] = "high"
            response["silent_mode"] = True

        elif gesture == "shake":
            response["action"] = "emergency_sos"
            response["alert_type"] = AlertType.NORMAL_SOS.value
            response["urgency"] = "critical"

        elif voice_command and "help" in voice_command.lower():
            response["action"] = "voice_sos"
            response["alert_type"] = AlertType.NORMAL_SOS.value
            response["urgency"] = "critical"
            response["voice_command"] = voice_command

        return response


class AdaptiveSafetyShield:
    """
    Core adaptive safety shield that fuses multiple signal sources.
    Makes dynamic decisions: Normal SOS vs Covert Duress alerts.
    """

    def __init__(self):
        self.risk_signal_weight = 0.35
        self.camera_signal_weight = 0.40
        self.user_input_weight = 0.25

    def fuse_signals(
        self,
        risk_signals: Dict[str, Any],
        camera_signals: Dict[str, Any],
        user_input: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        """
        Fuse all three signal sources into a unified safety decision.
        """
        # Weighted fusion
        fused_score = (
            risk_signals.get("risk_score", 0) * self.risk_signal_weight
            + camera_signals.get("threat_score", 0) * self.camera_signal_weight
        )

        # If user explicitly triggered, override with user input
        if user_input and "action" in user_input:
            fused_score = 100 if "sos" in user_input["action"].lower() else fused_score

        return {
            "fused_threat_score": round(fused_score, 1),
            "risk_signals": risk_signals.get("signals", []),
            "camera_signals": camera_signals.get("threats", []),
            "user_input": user_input,
            "fused_at": datetime.utcnow().isoformat(),
        }

    def make_safety_decision(
        self,
        fused_signals: Dict[str, Any],
        is_covert_mode: bool = False,
    ) -> Dict[str, Any]:
        """
        Make final safety decision: Normal SOS or Covert Duress.
        """
        score = fused_signals.get("fused_threat_score", 0)
        user_input = fused_signals.get("user_input", {})

        # Check for explicit user input
        if user_input and "action" in user_input:
            if "covert" in user_input.get("action", "").lower():
                return self._generate_covert_alert(fused_signals)
            elif "sos" in user_input.get("action", "").lower():
                return self._generate_normal_sos(fused_signals)

        # Automatic decision based on threat score
        if score >= 80:
            # High threat detected
            if is_covert_mode:
                return self._generate_covert_alert(fused_signals)
            else:
                return self._generate_normal_sos(fused_signals)
        elif score >= 50:
            # Medium threat
            return self._generate_warning(fused_signals)
        else:
            # Low threat
            return self._generate_all_clear(fused_signals)

    def _generate_normal_sos(
        self, fused_signals: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate normal SOS alert.
        Loud, visible, immediate response expected.
        """
        return {
            "alert_type": AlertType.NORMAL_SOS.value,
            "alert_mode": "LOUD_AND_VISIBLE",
            "priority": "CRITICAL",
            "actions": [
                "ACTIVATE_SIREN",
                "SEND_SMS_TO_CONTACTS",
                "SHARE_LIVE_LOCATION",
                "RECORD_VIDEO",
                "CALL_EMERGENCY_SERVICES",
            ],
            "notification": "EMERGENCY ALERT: Immediate help needed. Emergency services notified.",
            "contact_notification": "LOUD",
            "location_sharing": "PUBLIC",
            "fused_signals": fused_signals,
            "triggered_at": datetime.utcnow().isoformat(),
        }

    def _generate_covert_alert(
        self, fused_signals: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate covert duress alert (SILENT ALERT).
        No device notifications, no audible alerts.
        Only trusted contacts are silently notified.
        """
        return {
            "alert_type": AlertType.COVERT_DURESS.value,
            "alert_mode": "SILENT_AND_COVERT",
            "priority": "CRITICAL",
            "actions": [
                "SILENT_LOCATION_TRACKING",
                "DISCRETE_SMS_TO_TRUSTED_CONTACTS",
                "BACKGROUND_VIDEO_RECORDING",
                "ENCRYPTED_CALL_TO_POLICE",
            ],
            "notification": "SILENT ALERT: Duress detected. Trusted contacts notified silently.",
            "contact_notification": "SILENT",
            "location_sharing": "ENCRYPTED_ONLY",
            "device_visibility": "NO_NOTIFICATIONS",
            "perpetrator_detection": True,
            "fused_signals": fused_signals,
            "triggered_at": datetime.utcnow().isoformat(),
        }

    def _generate_warning(
        self, fused_signals: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate warning alert (elevated monitoring).
        """
        return {
            "alert_type": "warning",
            "alert_mode": "MONITORING",
            "priority": "HIGH",
            "actions": [
                "INCREASE_CHECK_IN_FREQUENCY",
                "NOTIFY_TRUSTED_CONTACTS",
                "RECORD_LOCATION_CONTINUOUSLY",
            ],
            "notification": "Safety elevated to HIGH alert. Monitoring intensified.",
            "contact_notification": "SUBTLE",
            "fused_signals": fused_signals,
            "triggered_at": datetime.utcnow().isoformat(),
        }

    def _generate_all_clear(
        self, fused_signals: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate all-clear status (normal operation).
        """
        return {
            "alert_type": "all_clear",
            "alert_mode": "NORMAL",
            "priority": "LOW",
            "actions": ["CONTINUE_NORMAL_MONITORING"],
            "notification": "All clear. SafeWalk continues normally.",
            "contact_notification": "NONE",
            "fused_signals": fused_signals,
            "triggered_at": datetime.utcnow().isoformat(),
        }


class DuressCommandDecoder:
    """
    Detects covert duress commands hidden in normal behavior.
    Examples:
    - Specific phrases in check-in messages
    - Unusual check-in timing patterns
    - Specific emoji sequences
    """

    DURESS_TRIGGERS = {
        "phrases": [
            "i am okay",
            "all good here",
            "nothing to report",
            "feeling safe",
        ],
        "trigger_words": [
            "help",
            "stuck",
            "danger",
            "threat",
        ],
        "emoji_sequences": [
            "🔴🔴🔴",  # Three red circles
            "😟🔒📍",  # Threat + lock + location
        ],
    }

    @staticmethod
    def detect_duress_command(check_in_message: str) -> Dict[str, Any]:
        """
        Analyze check-in message for hidden duress signals.
        """
        message_lower = check_in_message.lower()
        duress_detected = False
        indicators = []

        # Check for trigger words
        for word in DuressCommandDecoder.DURESS_TRIGGERS["trigger_words"]:
            if word in message_lower:
                duress_detected = True
                indicators.append({"type": "trigger_word", "word": word})

        # Check for unusual "safe" phrases when conditions are dangerous
        for phrase in DuressCommandDecoder.DURESS_TRIGGERS["phrases"]:
            if phrase in message_lower:
                indicators.append({"type": "potential_code_phrase", "phrase": phrase})

        # Check for emoji sequences
        for emoji_seq in DuressCommandDecoder.DURESS_TRIGGERS["emoji_sequences"]:
            if emoji_seq in check_in_message:
                duress_detected = True
                indicators.append({"type": "emoji_distress_signal", "sequence": emoji_seq})

        return {
            "duress_detected": duress_detected,
            "indicators": indicators,
            "original_message": check_in_message,
            "analyzed_at": datetime.utcnow().isoformat(),
        }
