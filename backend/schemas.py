from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

#Schema pentru datele de intrare (ce primim de la Flutter cand se creeaza un cont)
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str #parola in clar care trebuie criptata la trimiterea in models.py

#Schema pentru datele de iesire (ce trimitem noi inapoi catre aplicatie)
class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime

    #clasa interna care ii spune lui Pydantic sa stie sa citeasca direct dintr-un model SQLAlchemy
    class Config:
        from_attributes = True