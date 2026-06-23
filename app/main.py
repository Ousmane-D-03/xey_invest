from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .models import user, campaign, investment, distribution

def create_tables():
    Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.on_event("startup")
def startup():
    create_tables()