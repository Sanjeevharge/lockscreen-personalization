import httpx
from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

REC_SERVICE_URL = "http://rec-service:8000"
EVENT_SERVICE_URL = "http://event-service:8000"


class InteractionEvent(BaseModel):
    user_id: str
    content_id: str
    event_type: str  # e.g., "impression", "like", "dislike", "skip"


@app.get("/recommendation/next")
async def get_next_recommendation(user_id: str):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{REC_SERVICE_URL}/recommendation/next", json={"user_id": user_id}
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code, detail=e.response.text
            )


@app.post("/events/interaction")
async def post_interaction(event: InteractionEvent):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{EVENT_SERVICE_URL}/events", json=event.dict()
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code, detail=e.response.text
            )
