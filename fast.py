
import os

import redis
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

# Redis connection
r = redis.from_url(
    os.getenv("REDIS_URL", "redis://localhost:6379/0"),
    decode_responses=True,
    socket_connect_timeout=2,
    socket_timeout=2
)

app = FastAPI(
    title="my APP",
    description="This is my first FastAPI app",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/")
def home():
    return {
        "message": "FastAPI running",
        "name": os.getenv("MY_NAME", "Neeraj"),
        "redis_message": r.get("my_key")
    }


@app.get("/me")
def me():
    return {
        "name": "Neeraj",
        "age": 25,
        "city": "Bangalore",
        "message": os.getenv("MY_NAME", "Neeraj"),
        "redis_message": r.get("my_key")
    }


@app.get("/redis-test")
def redis_test():
    r.set("my_key", "Hello from Redis! Welcome to my world!")
    r.set("deployment_test", "connected")

    return {
        "redis_value": r.get("deployment_test")
    }


# Basic application health
@app.get("/health")
def health():
    return {"status": "healthy"}


# Application + Redis readiness
@app.get("/ready")
def ready():
    try:
        r.ping()
        return {
            "status": "ready",
            "redis": "connected"
        }
    except redis.RedisError:
        raise HTTPException(
            status_code=503,
            detail="Redis unavailable"
        )
