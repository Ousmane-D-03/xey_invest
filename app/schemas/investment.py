import enum
from datetime import datetime
from pydantic import BaseModel
from app.models.investment import InvestmentStatus


class CreateInvestment(BaseModel):
    nombrePartAchetees: int
    campaign_id: int


class UpdateInvestment(BaseModel):
    nombrePartAchetees: int | None = None
    dateInvestissement: datetime | None = None
    statut: InvestmentStatus | None = None
    urlContrat: str | None = None
    referenceTransaction: str | None = None
    user_id: int | None = None
    campaign_id: int | None = None

class InvestmentListResponse(BaseModel):
    id: int
    nombrePartAchetees: int
    dateInvestissement: datetime
    statut: InvestmentStatus
    urlContrat: str | None = None
    referenceTransaction: str | None = None
    user_id: int
    campaign_id: int

    class Config:
        orm_mode = True

class InvestmentDetailResponse(InvestmentListResponse):
    pass

class InvestmentStatusResponse(BaseModel):
    id: int
    statut: InvestmentStatus

    class Config:
        orm_mode = True

class InvestmentStatusUpdate(BaseModel):
    statut: InvestmentStatus    

class InvestmentListByUserResponse(BaseModel):
    id: int
    nombrePartAchetees: int
    dateInvestissement: datetime
    statut: InvestmentStatus
    urlContrat: str | None = None
    referenceTransaction: str | None = None
    campaign_id: int

    class Config:
        orm_mode = True

class InvestmentListByCampaignResponse(BaseModel):
    user_id: int

    class Config:
        orm_mode = True     

