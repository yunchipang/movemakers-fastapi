from pydantic import BaseModel, Field, EmailStr, ConfigDict, UUID4

# user
class BaseUser(BaseModel):
    email: EmailStr

class User(BaseUser):
    id: UUID4
    
    model_config = ConfigDict(from_attributes=True)

class CreateUser(BaseUser):
    hashed_password: str = Field(alias="password")

# user login
class UserLogin(BaseModel):
    email: EmailStr
    password: str
