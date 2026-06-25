from sqlalchemy import Column, Integer, String, Enum as SqlEnum
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime
from enum import Enum
from app.models.investment import InvestmentStatus
from app.models.campaign import Campaign


class Status(Enum):
    EN_ATTENTE ="en_attente"
    VALIDE = "valide"
    SUSPENDU = "suspendu"

class Role(Enum):
    INVESTOR = "investor"
    PROJECT_OWNER = "project_owner"
    ADMIN = "admin"



class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    status = Column(SqlEnum(Status), default=Status.EN_ATTENTE, nullable=False)
    secteur_activite = Column(String, nullable=True) 
    role = Column(SqlEnum(Role), nullable=False) 

    campaigns = relationship("Campaign", back_populates="owner")
    investments = relationship("Investment", back_populates="user")

    