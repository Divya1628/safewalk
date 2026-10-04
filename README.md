# SafeWalk Backend

A FastAPI backend for a SafeWalk safety application with:
- destination risk analysis
- LOW / MEDIUM / HIGH risk calculation
- SafeWalk session start
- countdown and check-in flow
- final "I'm Safe" save to history
- MongoDB data persistence

## Features

- Risk scoring based on time, day, incident data, and environmental conditions
- Recommendation engine for safer travel
- SafeWalk session lifecycle
- Check-in and emergency reporting
- History retrieval for a user

## Tech Stack

- Python
- FastAPI
- MongoDB
- Pydantic

## Setup

1. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Configure environment

```bash
cp .env.example .env
```

4. Start MongoDB locally (if not already running)

```bash
mongod
```

5. Run the app

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## API Overview

### Risk calculation

POST /api/risk/calculate

Example JSON:

```json
{
  "time_of_day": "night",
  "day_type": "weekend",
  "incident_count": 6,
  "environment_activity": "poor_lighting"
}
```

### Start SafeWalk

POST /api/safewalk/start

Example JSON:

```json
{
  "user_id": "user_123",
  "destination": "Downtown Station",
  "time_of_day": "night",
  "day_type": "weekend",
  "incident_count": 6,
  "environment_activity": "poor_lighting"
}
```

### Countdown

POST /api/safewalk/countdown

Example JSON:

```json
{
  "session_id": "<session_id>",
  "user_id": "user_123",
  "countdown_seconds": 10
}
```

### Check-in

POST /api/safewalk/checkin

Example JSON:

```json
{
  "session_id": "<session_id>",
  "user_id": "user_123",
  "status": "safe",
  "message": "I'm Safe"
}
```

### Finish SafeWalk

POST /api/safewalk/finish

Example JSON:

```json
{
  "session_id": "<session_id>",
  "user_id": "user_123",
  "status": "safe",
  "notes": "Reached destination safely."
}
```

### History

GET /api/history/{user_id}

## MongoDB Collections

- safewalk_sessions
- history

## Notes

This backend is designed to be easy to extend for:
- authentication
- SMS notifications
- emergency alerts
- frontend integration
- analytics dashboards
