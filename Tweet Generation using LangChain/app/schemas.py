from pydantic import BaseModel

class TweetRequest(BaseModel):
    topic: str

class TweetResponse(BaseModel):
    tweet: str
    verification: str