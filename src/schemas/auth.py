from pydantic import BaseModel
from pydantic import BaseModel
class LoginRequest(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None


class UserResponse(BaseModel):
    email: str
    full_name: str | None = None
    is_active: bool

    model_config = {
        "from_attributes": True
    }

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse
