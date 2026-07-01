from pydantic import BaseModel
from datetime import datetime
from backend.models.distribution import DistributionStatus


class CreateDitribution(BaseModel):
    campaign_id: int

class DistributionListResponse(BaseModel):
    id:int
    dateDistribution: datetime
    statut:  DistributionStatus
    campaign_id: int

    class Config:
        orm_mode = True

class DistributionDetailResponse(DistributionListResponse):
    campaign_title: str | None = None
    
    class Config:
        orm_mode = True