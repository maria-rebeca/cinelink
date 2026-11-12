from fastapi import FastAPI, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from database import get_db
from fastapi import HTTPException
import models
import schemas
import crud
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="CineLink API")
@app.get("/")
def read_root():
    return {"message":"Serverul CineLink este online si functional"}
@app.get("/test_db")
def test_database_conection(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"message":"Conexiunea la PostgreSQL a reusit"}
    except Exception as e:
        raise HTTPException(status_code=503, detail="Baza de date nu este disponibila")

@app.post("/users/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Creeaza un cont nou de utilizator."""
    
    db_user_email = crud.get_user_by_email(db, email=user.email)
    if db_user_email:
        raise HTTPException(status_code=400, detail="Acest email este deja inregistrat!")
        
    db_user_username = crud.get_user_by_username(db, username=user.username)
    if db_user_username:
        raise HTTPException(status_code=400, detail="Acest username este deja ocupat!")
        
    return crud.create_user(db=db, user=user)