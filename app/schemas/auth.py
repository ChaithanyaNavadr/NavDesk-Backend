from pydantic import BaseModel

# ✅ Request schema for login
class LoginRequest(BaseModel):
    username: str
    password: str

# ✅ Response schema for token
class Token(BaseModel):
    access_token: str
    token_type: str
