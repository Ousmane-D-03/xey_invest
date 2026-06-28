from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from app.routers import auth
from app.routers import campaign
from app.routers import investment
from app.routers import distribution

def create_tables():
    Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(campaign.router, prefix="/campaign", tags=["campaign"])
app.include_router(investment.router, prefix="/investment", tags=["investement"])
app.include_router(distribution.router, prefix="/distribution", tags=["distribution"])

@app.on_event("startup")
def startup():
    create_tables()