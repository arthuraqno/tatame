from pydantic import BaseModel, EmailStr

class UsuarioCreate(BaseModel):
    email : EmailStr
    senha : str
    telefone : str

class UsuarioResponse(BaseModel):
    id: int
    email: str
    role : str
    telefone : str

class LoginRequest(BaseModel):
    email: EmailStr
    senha: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"