import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

#citeste fisierul .env (parametru implicit pt ca am denumit conventional) 
#si pune continutul lui in variabilele de mediu ale procesului (de asta am importat pachetul os)
load_dotenv()

#os.getenv citeste valoarea variabilei date ca paramaetru. Daca variabila
#nu exista, returneaza None
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

#engine-ul nu deschide imediat o conexiune, ci tine un pool de conexiuni
#pool de conexiuni = grup de conexiuni deschise si reutilizabile
#pt ca deschiderea unei conexiuni la fiecare cerere ar fi lenta
#exista o singura instanta engine pentru toata aplicatia
engine = create_engine(SQLALCHEMY_DATABASE_URL)

#SessionLocal este o clasa, sessionmaker este o fabrica de sesiuni
#o sesiune este o conversatie cu baza de date (interogari, adaugari, modificari)
#sessionmaker creeeaza o clasa care produce sesiuni cu setarile
#din paramaetri
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#clasa de baza Base pe care o vor mosteni toate tabelele
Base = declarative_base()

#functie generator
def get_db():
    db = SessionLocal() #creeaza o sesiune noua (apelare constructor)
    try:
        yield db #yield imprumuta sesiunea codului care a cerut-o (de ex main.py), iar functia se opreste aici si asteapta
    finally:
        db.close() #cand codul apelant termina, executia ajunge aici
                   #sesiunea se inchide si conexiunea se intaorce in pool
                   #daca nu incgidem sesiunile, ramanem fara conexiuni si serverul se blocheaza