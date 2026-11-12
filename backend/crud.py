from sqlalchemy.orm import Session
import models, schemas
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    """Functie utilitara care transforma parola in text intr-un hash ireversibil."""
    return pwd_context.hash(password)

def get_user_by_email(db: Session, email: str):
    """Cauta un utilizator in baza de date dupa email-ul sau."""
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_username(db: Session, username: str):
    """Cauta un utilizator in baza de date dupa username."""
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    """Creeaza un utilizator nou, ii cripteaza parola si il salveaza in baza de date."""
    # Transformam parola primita din aplicatie in hash
    hashed_password = get_password_hash(user.password)
    
    # Construim obiectul SQLAlchemy bazat pe modelul User
    db_user = models.User(
        username=user.username, 
        email=user.email, 
        password_hash=hashed_password
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user