from fastapi import FastAPI
from app import auth,llm

app = FastAPI()

app.include_router(auth.router)
app.include_router(llm.router)
