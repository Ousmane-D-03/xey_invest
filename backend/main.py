from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from backend.routers import auth
from backend.routers import campaign
from backend.routers import investment
from backend.routers import distribution

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