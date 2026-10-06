# SafeWalk Backend with Adaptive Safety Shield

A FastAPI backend for SafeWalk with cutting-edge **Adaptive Safety Shield** — multi-source signal fusion and **Covert Duress Alerts**.

## 🛡️ Adaptive Safety Shield Overview

```
         SafeWalk AI
             ↓
   Adaptive Safety Shield
             ↓
    ┌────────┼────────┐
    ↓        ↓        ↓
Risk     Camera    User
Signals  Signals   Input
    ↓        ↓        ↓
    └────────┼────────┘
             ↓
      Safety Decision
             ↓
    ┌────────┴────────┐
    ↓                 ↓
Normal SOS      Covert Duress
                 (Silent Alert)
```

## 🚀 Key Innovation: Covert Duress Alerts

### What is Covert Duress?
When someone is in immediate danger but **cannot openly call for help** (e.g., held at gunpoint, forced into a vehicle, kidnapping scenario), the Adaptive Safety Shield detects this and sends a **SILENT ALERT**:

- **No audible alerts** on device
- **No notifications visible** to perpetrator
- **Silent GPS tracking** activated
- **Encrypted alert** to trusted contacts only
- **Police notified discretely**
- **Background video recording** starts
- **Behavioral analysis** detects duress even if user says "I'm fine"

## 📊 Three Signal Sources

### 1. Risk Signals (Wearables & Sensors)
- Heart rate spikes (stress/fear)
- Unusual movement patterns (erratic, stationary, running)
- GPS deviation from route (forced movement)
- Missed check-ins
- Delayed responses

### 2. Camera Signals (Computer Vision)
- Person count nearby
- Threat detection (weapons, suspicious behavior)
- Face recognition (known threats)
- Lighting level
- Movement direction (approaching/retreating)

### 3. User Input
- Panic button press
- Gesture commands (triple tap for covert)
- Voice commands
- Check-in messages with hidden duress codes

## 🔄 Multi-Stage Decision Process

```
Stage 1: Risk Analysis         → Risk signals scored
Stage 2: Camera Analysis        → Visual threats scored  
Stage 3: User Input Processing  → Commands decoded
Stage 4: Signal Fusion          → Weighted score calculation
Stage 5: Safety Decision        → Alert type determined
Stage 6: Duress Detection       → Code phrases analyzed
```

## 🔐 Hidden Duress Commands

Users can trigger covert alerts through:

### Gestures
- **Triple tap** → Covert Duress Alert (silent)
- **Shake device** → Emergency SOS (loud)
- **Long press** → Panic button

### Voice Commands
- "Help me" → SOS
- "I need assistance" → SOS

### Code Phrases in Check-in Messages
- "`I am okay`" when conditions are dangerous → Duress signal
- "`Nothing to report`" with elevated heart rate → Duress signal
- ✅ Emoji sequences: 🔴🔴🔴, 😟🔒📍

### Message Anomalies
- Delayed check-in (>10 min) + unusual phrasing = duress
- Heart rate spike + "I'm fine" = contradiction detected

## 📡 API Endpoints

### Analyze Risk Signals
```
POST /api/shield/analyze-risk-signals
```

Payload:
```json
{
  "heart_rate": 135,
  "movement_pattern": "erratic",
  "gps_deviation": 0.8,
  "check_in_missed": true,
  "response_time": 900
}
```

Response:
```json
{
  "risk_score": 78.5,
  "signals": [
    {"type": "elevated_heart_rate", "value": 135, "severity": "high"},
    {"type": "unusual_movement", "pattern": "erratic", "severity": "high"},
    {"type": "route_deviation", "deviation_km": 0.8, "severity": "high"},
    {"type": "missed_checkin", "response_time_sec": 900, "severity": "critical"}
  ]
}
```

### Analyze Camera Feed
```
POST /api/shield/analyze-camera-feed
```

Payload:
```json
{
  "person_count": 0,
  "threat_detected": true,
  "face_recognition_match": true,
  "lighting_level": 15,
  "movement_direction": "towards_user"
}
```

Response:
```json
{
  "threat_score": 95.0,
  "threats": [
    {"type": "isolated_environment", "count": 0, "severity": "medium"},
    {"type": "potential_threat", "severity": "critical"},
    {"type": "known_threat_detected", "severity": "critical"},
    {"type": "low_lighting", "level": 15, "severity": "medium"},
    {"type": "approaching_threat", "direction": "towards_user", "severity": "high"}
  ]
}
```

### Process User Command
```
POST /api/shield/process-user-command
```

Payload:
```json
{
  "command_type": "gesture",
  "gesture": "triple_tap"
}
```

Response:
```json
{
  "command_type": "gesture",
  "action": "covert_alert",
  "alert_type": "covert_duress",
  "urgency": "high",
  "silent_mode": true
}
```

### Full Safety Assessment (End-to-End)
```
POST /api/shield/full-safety-assessment
```

Payload:
```json
{
  "timestamp": "2026-10-06T14:45:00Z",
  "heart_rate": 140,
  "movement_pattern": "erratic",
  "gps_deviation": 1.2,
  "check_in_missed": true,
  "response_time": 1200,
  "person_count": 1,
  "threat_detected": true,
  "face_recognition_match": true,
  "lighting_level": 10,
  "movement_direction": "towards_user",
  "check_in_message": "I am okay, nothing to report",
  "is_covert_mode": false
}
```

Response:
```json
{
  "assessment_timestamp": "2026-10-06T14:45:00Z",
  "stage_1_risk_analysis": { ... },
  "stage_2_camera_analysis": { ... },
  "stage_3_user_input": null,
  "stage_4_signal_fusion": { ... },
  "stage_5_safety_decision": {
    "alert_type": "covert_duress",
    "alert_mode": "SILENT_AND_COVERT",
    "priority": "CRITICAL",
    "actions": [
      "SILENT_LOCATION_TRACKING",
      "DISCRETE_SMS_TO_TRUSTED_CONTACTS",
      "BACKGROUND_VIDEO_RECORDING",
      "ENCRYPTED_CALL_TO_POLICE"
    ],
    "notification": "SILENT ALERT: Duress detected. Trusted contacts notified silently.",
    "contact_notification": "SILENT",
    "location_sharing": "ENCRYPTED_ONLY",
    "device_visibility": "NO_NOTIFICATIONS",
    "perpetrator_detection": true
  },
  "stage_6_duress_detection": {
    "duress_detected": true,
    "indicators": [{"type": "potential_code_phrase", "phrase": "i am okay"}]
  },
  "final_alert_type": "covert_duress"
}
```

### Detect Duress Commands
```
POST /api/shield/detect-duress-command
```

Payload:
```json
{
  "check_in_message": "I am okay, nothing to report 🔴🔴🔴"
}
```

Response:
```json
{
  "duress_detected": true,
  "indicators": [
    {"type": "potential_code_phrase", "phrase": "i am okay"},
    {"type": "emoji_distress_signal", "sequence": "🔴🔴🔴"}
  ]
}
```

## 🎯 Decision Tree: Normal SOS vs Covert Duress

```
Threat Score > 80?
├─ YES
│  ├─ User explicitly triggered covert? → COVERT DURESS (SILENT)
│  └─ User triggered normal SOS? → NORMAL SOS (LOUD)
│
├─ NO
│  ├─ Threat Score > 50? → WARNING (MONITORING)
│  └─ Threat Score < 50? → ALL CLEAR (NORMAL)
```

## 🔐 Safety Features

✅ **Multi-signal Fusion** — Risk + Camera + User Input
✅ **Covert Duress Detection** — Silent alerts when threatened
✅ **Behavioral Anomaly** — Detects stress even when user says "I'm fine"
✅ **Duress Code Phrases** — Hidden commands in normal messages
✅ **Gesture Recognition** — Triple tap for covert, shake for emergency
✅ **Voice Command Support** — "Help me" triggers SOS
✅ **Perpetrator Unawareness** — No notifications shown on device
✅ **Encrypted Contacts** — Trusted circle receives silent alerts
✅ **Automated Police Notification** — Silent call to emergency services
✅ **Background Recording** — Video/audio evidence collection

## 📱 Supported Devices

- iOS (iPhone, Apple Watch)
- Android (Smartphones, Wearables)
- Smart Wearables (Fitbit, Garmin, Apple Watch)
- Connected IoT sensors

## 🔧 Tech Stack

- Python 3.8+
- FastAPI
- MongoDB
- Computer Vision (OpenCV, TensorFlow)
- Sensor fusion algorithms
- CORS enabled for mobile apps

## 📖 Setup

1. Create virtual environment
```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Configure `.env`
```bash
cp .env.example .env
```

4. Start MongoDB
```bash
mongod
```

5. Run the app
```bash
uvicorn app.main:app --reload
```

6. Visit API docs
```
http://localhost:8000/docs
```

## 🚨 Emergency Response Flow

### Normal SOS
1. **Loud siren** activates
2. **SMS to all contacts** (loud notification)
3. **Live location shared** publicly
4. **Video recording** starts
5. **Emergency services** auto-dialed

### Covert Duress Alert
1. **Silent operation** — no device notifications
2. **GPS tracked** continuously
3. **Discrete SMS** to trusted contacts only
4. **Background recording** starts
5. **Police notified** via encrypted channel
6. **Perpetrator stays unaware**

## 📊 Weighted Signal Scoring

- **Risk Signals**: 35% weight
- **Camera Signals**: 40% weight
- **User Input**: 25% weight

Final Score = (Risk×0.35) + (Camera×0.40) + (User×0.25)

---

**Built with safety-first principles. When every second counts.**
