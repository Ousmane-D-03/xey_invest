from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime
from enum import Enum

class UserStatus(Enum):
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
    status = Column(Enum(UserStatus), default=UserStatus.EN_ATTENTE, nullable=False)
    secteur_activite = Column(String, nullable=True) 
    role = Column(Enum(Role), nullable=False) 

    campaigns = relationship("Campaign", back_populates="owner")

    