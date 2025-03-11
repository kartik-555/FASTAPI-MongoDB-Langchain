from pydantic import BaseModel, EmailStr, Field

class SignUpRequest(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    password: str

class SignUpResponse(BaseModel):
    status: str
    username: str
    email: EmailStr
    first_name: str
    last_name: str

class LoginRequest(BaseModel):
    identifier: str  # email or username
    password: str

class LoginResponse(BaseModel):
    status: str
    token: str

class Message(BaseModel):
    message: str

class ResponseMessage(BaseModel):
    response: str

class ErrorMessage(BaseModel):
    error: str