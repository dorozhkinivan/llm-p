from pydantic import BaseModel, EmailStr, Field

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6, description="Пароль должен быть не менее 6 символов")

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"