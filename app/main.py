from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .models import user, campaign, investment, distribution
from app.routers import auth

def create_tables():
    Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(auth.router, prefix="/auth", tags=["auth"])

@app.on_event("startup")
def startup():
    create_tables()