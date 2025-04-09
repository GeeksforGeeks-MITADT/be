from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json
import uuid
import os

app = FastAPI()

EVENTS_FILE = "events.json"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health_check():
    return {"status": "✅ API is live"}

@app.get("/events")
def get_events():
    with open(EVENTS_FILE, "r") as f:
        data = json.load(f)
    return data["events"]

@app.post("/events")
async def add_event(req: Request):
    body = await req.json()

    if body.get("apiKey") != "admin123":
        raise HTTPException(status_code=401, detail="Unauthorized")

    with open(EVENTS_FILE, "r") as f:
        data = json.load(f)

    new_event = {
        "id": str(uuid.uuid4()),
        "title": body["title"],
        "description": body["description"],
        "category": body["category"],
        "date": body["date"],
        "time": body["time"],
        "duration": body.get("duration", ""),
        "location": body.get("location", ""),
        "speaker": body.get("speaker", ""),
        "prerequisites": body["prerequisites"],
    }

    data["events"].append(new_event)

    with open(EVENTS_FILE, "w") as f:
        json.dump(data, f, indent=2)

    return new_event
