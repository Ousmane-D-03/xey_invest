from sqlalchemy import Column, Integer, String, Date, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime
from enum import Enum

class DistributionStatus(Enum):
    EN_ATTENTE = "en_attente"
    VALIDEE = "validée"
    EXECUTEE = "executée"

class Distribution(Base):
    __tablename__ = "distributions"

    id = Column(Integer, primary_key=True, index=True)
    dateDistribution = Column(Date, nullable=False)
    statut = Column(Enum(DistributionStatus), default=DistributionStatus.EN_ATTENTE, nullable=False)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"), nullable=False)

    campaign = relationship("Campaign", back_populates="distributions")