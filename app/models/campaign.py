from sqlalchemy import Column, Integer, String, Enum as SqlEnum , Date, Float 
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime, date
from enum import Enum
from sqlalchemy import ForeignKey
from app.models.investment import Investment
from app.models.distribution import Distribution

class CampaignStatus(Enum):
    EN_ATTENTE = "en_attente"
    ACTIVE = "active"
    FINANCEE = "financee"
    CLOTUREE = "cloturee"
    SUSPENDUE = "suspendue"


class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    sector = Column(String, nullable=False)
    goal_amount = Column(Float, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    status = Column(SqlEnum(CampaignStatus), default=CampaignStatus.EN_ATTENTE, nullable=False)
    unit_price = Column(Float, nullable=False)
    total_parts = Column(Integer, nullable=False)
    yield_rate = Column(Float, nullable=False)
    repayment_duration = Column(Integer, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    investments = relationship("Investment", back_populates="campaign")
    distributions = relationship("Distribution", back_populates="campaign")
    owner = relationship("User", back_populates="campaigns")



