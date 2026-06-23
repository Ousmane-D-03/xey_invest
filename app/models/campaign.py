from sqlalchemy import Column, Integer, String, Enum as SqlEnum , Date, Float 
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime, date
from enum import Enum
from sqlalchemy import ForeignKey

class CampaignStatus(Enum):
    EN_ATTENTE = "en_attente"
    ACTIVE = "active"
    FINANCEE = "financee"
    CLOTUREE = "cloturee"
    SUSPENDUE = "suspendue"


class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column(Integer, primary_key=True, index=True)
    titre = Column(String, nullable=False)
    description = Column(String, nullable=False)
    secteur = Column(String, nullable=False)
    objectifFinancier = Column(Integer, nullable=False)
    dateDebut = Column(Date, nullable=False)
    dateFin = Column(Date, nullable=False)
    statut = Column(SqlEnum(CampaignStatus), default=CampaignStatus.EN_ATTENTE, nullable=False)
    prixUnitairePart = Column(Integer, nullable=False)
    nombreTotalParts = Column(Integer, nullable=False)
    tauxRendement = Column(Float, nullable=False)
    dureRemboursement = Column(Integer, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    owner = relationship("User", back_populates="campaigns")    



