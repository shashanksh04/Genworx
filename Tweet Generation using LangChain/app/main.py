from fastapi import FastAPI
from app.schemas import TweetRequest, TweetResponse
from app.core import tweet_chain

app = FastAPI(title="Tweet Generator API")

@app.get("/")
def read_root():
    return {"message": "Welcome to Tweet Generator API"}

@app.post("/generate_tweet/")
def generate_tweet(request: TweetRequest):
    tweet = tweet_chain.invoke({"topic": request.topic})
    return tweet