from sqlalchemy import Column, Integer, String, Date, Enum as SqlEnum, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime
from enum import Enum

class InvestmentStatus(Enum):
    EN_ATTENTE = "en_attente"
    CONFIRME = "confirme"
    REMBOURSE = "rembourse"

class Investment(Base):
    __tablename__ = "investments"

    id = Column(Integer, primary_key=True, index=True)
    nombrePartAchetees = Column(Integer, nullable=False)
    dateInvestissement = Column(Date, default=datetime.utcnow, nullable=False)
    statut = Column(SqlEnum(InvestmentStatus), default=InvestmentStatus.EN_ATTENTE, nullable=False)
    urlContrat = Column(String, nullable=True)
    referenceTransaction = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"), nullable=False)

    campaign = relationship("Campaign", back_populates="investments")
    user = relationship("User", back_populates="investments")
