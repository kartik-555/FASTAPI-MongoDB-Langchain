from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException, status
from pydantic import ValidationError
from jose import jwt, JWTError
from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from schemas import Message, ResponseMessage, ErrorMessage
from pydantic import BaseModel
from database import db

load_dotenv()

router = APIRouter()
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize Groq LLM
llm = ChatGroq(
    model_name="llama-3.3-70b-versatile",
    temperature=0.3,
    api_key=GROQ_API_KEY
)

async def store_token(token: str):
    await db.tokens.insert_one({"token": token})

async def is_token_used(token: str) -> bool:
    token_entry = await db.tokens.find_one({"token": token})
    return token_entry is not None

# Pydantic model for expected response structure
class LLMResponse(BaseModel):
    response: str

# Define the output parser
parser = JsonOutputParser(pydantic_object=LLMResponse)

# Prompt to enforce JSON structured responses
prompt = ChatPromptTemplate.from_messages([
    ("system", """You are an AI assistant that responds to client messages over a WebSocket connection. Based on the client's message, your response should be a JSON object with the following structure:

- If the question is relevant to the topic:
  {{
    "response": "Your answer to the client's question."
  }}
- If the question is not relevant to the topic:
  {{
    "response": "This question is not relevant to the topic of discussion."
  }}
- If the question requires more details:
  {{
    "response": "Can you provide more context for your question?"
  }}
- If you cannot answer the question:
  {{
    "response": "I'm sorry, but I do not have an answer for that."
  }}

Ensure that your response is always a valid JSON object."""),
("user", "{input}")

])

# Create the LangChain pipeline
chain = prompt | llm | parser

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

async def process_message_with_groq(message: str) -> dict:
    try:
        print(f"Processing message: {message}")
        result = chain.invoke({"input": message})
        return result
    except Exception as e:
        print(f"Error processing message: {str(e)}")
        return {"response": "I'm sorry, but I do not have an answer for that."}

@router.websocket("/ws/{topic}")
async def websocket_endpoint(websocket: WebSocket, topic: str):
    token = websocket.query_params.get("token")
    if not token:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return
    
    if await is_token_used(token):
        await websocket.accept()
        await websocket.send_json({"error": "Token expired"})
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    try:
        verify_token(token)
    except HTTPException:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return
    
    await store_token(token)
    await websocket.accept()
    try:
        while True:
            try:
                data = await websocket.receive_json()
                message = Message(**data)
            except ValidationError:
                error_message = ErrorMessage(
                    error="Invalid message format. Expected a JSON object with a 'message' field."
                )
                await websocket.send_json(error_message.dict())
                continue

            response_data = await process_message_with_groq(message.message)
            response = ResponseMessage(response=response_data["response"])
            await websocket.send_json(response.dict())

    except WebSocketDisconnect:
        print("Client disconnected")