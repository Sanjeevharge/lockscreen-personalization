from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class InteractionEvent(BaseModel):
    user_id: str
    content_id: str
    event_type: str


@app.post("/events")
async def post_event(event: InteractionEvent):
    # In a real app, this would publish the event to a Kafka topic or a RabbitMQ queue.
    # For now, we'll just print the event to the console.
    print(f"Received event: {event.dict()}")
    return {"status": "ok"}
