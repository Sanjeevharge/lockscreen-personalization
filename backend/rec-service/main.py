from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class RecommendationRequest(BaseModel):
    user_id: str


@app.post("/recommendation/next")
async def get_next_recommendation(request: RecommendationRequest):
    # In a real app, this would involve candidate generation, ranking, and a bandit layer.
    # For now, we'll just return a dummy recommendation.
    return {
        "content_id": "123",
        "title": "The Future of AI",
        "body": "This is an article about the future of AI.",
        "image_url": "https://images.unsplash.com/photo-1620712943543-959636a68270?q=80&w=2070&auto=format&fit=crop",
        "category": "Tech",
        "publisher": "AI Today",
        "published_at": "2025-11-22T12:00:00Z",
        "language": "en",
        "explanation": "Because you liked Tech + Short reads in the evening",
        "strategy": "epsilon_greedy",
    }
