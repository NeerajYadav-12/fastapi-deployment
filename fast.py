from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
import redis

load_dotenv()

r = redis.from_url(
    os.environ["REDIS_URL"],
    decode_responses=True
)
r.set('my_key', 'Hello from Redis! WElome to my world friend!First time I am using Redis with FastAPI')
app = FastAPI(title='my APP', description='This is my first FastAPI app', version='1.0.0')
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
@app.get("/")
def home():
    
    return {"message": "FastAPI running", "name": os.getenv("MY_NAME"), "redis_message": r.get('my_key')}

@app.get('/me')
def me():
    return {"name": "Neeraj", "age": 25, "city": "Bangalore", "message": os.environ["MY_NAME"], "redis_message": r.get('my_key')}

@app.get("/redis-test")
def redis_test():
    r.set("deployment_test", "connected")

    return {
        "redis_value": r.get("deployment_test")
    }