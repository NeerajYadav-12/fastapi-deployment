from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
import redis

load_dotenv()

redis_client = redis.Redis(host='redis-server', port=6379, db=0)

redis_client.set('my_key', 'Hello from Redis!')

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
    
    return {"message": "FastAPI running", "name": os.getenv("MY_NAME"), "redis_message": redis_client.get('my_key').decode('utf-8')}

@app.get('/me')
def me():
    return {"name": "Neeraj", "age": 25, "city": "Bangalore", "message": os.environ["MY_NAME"], "redis_message": redis_client.get('my_key').decode('utf-8')}