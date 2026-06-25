from pydantic import BaseModel
from datetime import datetime
from app.models.campaign import CampaignStatus


class CreateCampaign(BaseModel):
     title: str
     description: str
     goal_amount: float
     start_date: datetime
     end_date: datetime
     sector: str
     unit_price: float
     total_parts: int
     yield_rate: float
     repayment_duration: int


class UpdateCampaign(BaseModel):
    title: str | None = None
    description: str | None = None
    goal_amount: float | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None
    sector: str | None = None
    unit_price: float | None = None
    total_parts: int | None = None
    yield_rate: float | None = None
    repayment_duration: int | None = None


class CampaignStatusUpdate(BaseModel):
    status: CampaignStatus

class CampaignListResponse(BaseModel):
    id: int
    title: str
    description: str
    goal_amount: float
    start_date: datetime
    end_date: datetime
    status: CampaignStatus

    class Config:
        orm_mode = True

class CampaignDetailResponse(CampaignListResponse):
    investments: list[dict] = []
    distributions: list[dict] = []

class CampaignStatusResponse(BaseModel):
    id: int
    status: str

    class Config:
        orm_mode = True

