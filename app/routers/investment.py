from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth import get_current_user
from app.models.investment import Investment, InvestmentStatus
from app.models.campaign import Campaign, CampaignStatus
from app.schemas.investment import InvestmentDetailResponse, InvestmentListByCampaignResponse, InvestmentListByUserResponse, InvestmentListResponse, CreateInvestment
from typing import List
from app.models.user import User, Role
from fastapi import APIRouter, Depends, HTTPException, status
from datetime import datetime



router = APIRouter()

@router.post("/investments", response_model=InvestmentDetailResponse)
async def create_investement(investment: CreateInvestment, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not authenticated")
    
    if current_user.role != Role.INVESTOR:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to create investements")
    
    
    campaign = db.query(Campaign).filter(Campaign.id == investment.campaign_id).first()
    if not campaign:
        raise HTTPException(404, "Campaign not found")


    if campaign.statut != CampaignStatus.ACTIVE:
        raise HTTPException(400, "Campaign is not active")
    
    
    parts_vendues = sum(i.nombrePartAchetees for i in campaign.investments)

    
    parts_restantes = campaign.nombreTotalParts - parts_vendues

    
    if investment.nombrePartAchetees > parts_restantes:
        raise HTTPException(400, "Pas assez de parts disponibles")
        
    
    new_investment = Investment(
        nombrePartAchetees=investment.nombrePartAchetees,
        user_id=current_user.id,
        campaign_id=investment.campaign_id,
        statut=InvestmentStatus.EN_ATTENTE,
        dateInvestissement=datetime.utcnow()
    )
    db.add(new_investment)
    db.commit()
    db.refresh(new_investment)
    return new_investment



                    
@router.get("/investments", response_model=List[InvestmentListResponse])
async def get_investments(db: Session = Depends(get_db)):
    investments = db.query(Investment).all()
    return investments

@router.get("/investments/user/{user_id}", response_model=List[InvestmentListByUserResponse])
async def get_investments_by_user(user_id: int, db: Session = Depends(get_db)):
    investments = db.query(Investment).filter(Investment.user_id == user_id).all()
    return investments

@router.get("/investments/campaign/{campaign_id}", response_model=List[InvestmentListByCampaignResponse])
async def get_investments_by_campaign(campaign_id: int, db: Session = Depends(get_db)):
    investments = db.query(Investment).filter(Investment.campaign_id == campaign_id).all()
    return investments

@router.get("/investments/{investment_id}", response_model=InvestmentDetailResponse)
async def get_investment(investment_id: int, db: Session = Depends(get_db)):
    investment = db.query(Investment).filter(Investment.id == investment_id).first()
    if not investment:
        raise HTTPException(status_code=404, detail="Investment not found")
    return investment
