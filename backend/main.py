from fastapi import FastAPI, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from database import get_db
from fastapi import HTTPException

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