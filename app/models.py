from pydantic import BaseModel, EmailStr

class UserInDB(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    username: str
    hashed_password: str
