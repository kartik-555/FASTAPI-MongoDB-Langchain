from fastapi import FastAPI
from app import auth,llm

app = FastAPI()

app.include_router(auth.router)
app.include_router(llm.router)

@app.get("/")
async def read_root():
    return {
        "message": "Welcome to the FastAPI WebSocket and Authentication example. Use a JWT token to start a chat with the Groq API. Developed by Kartik Verma."
    }