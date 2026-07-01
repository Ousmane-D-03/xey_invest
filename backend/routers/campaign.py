from fastapi import APIRouter, Depends, HTTPException, status
from backend.auth import get_current_user
from backend.models.campaign import Campaign, CampaignStatus
from backend.models.user import User, Role
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.schemas.campaigns import CreateCampaign, UpdateCampaign, CampaignListResponse, CampaignDetailResponse, CampaignStatusUpdate, CampaignStatusResponse

router = APIRouter()



@router.post("/campaigns", response_model=CampaignDetailResponse)
def create_campaign(campaign: CreateCampaign, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not authenticated")
    
    if current_user.role != Role.PROJECT_OWNER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to create campaigns")

    
    new_campaign = Campaign(
        title=campaign.title,
        description=campaign.description,
        goal_amount=campaign.goal_amount,
        start_date=campaign.start_date.date(),
        end_date=campaign.end_date.date(),
        sector=campaign.sector,
        unit_price=campaign.unit_price,
        total_parts=campaign.total_parts,
        yield_rate=campaign.yield_rate,
        repayment_duration=campaign.repayment_duration,
        owner_id=current_user.id,
        status=CampaignStatus.EN_ATTENTE,
    )
    db.add(new_campaign)
    db.commit()
    db.refresh(new_campaign)
    return new_campaign

@router.get("/campaigns", response_model=list[CampaignListResponse])
def get_campaigns(db: Session = Depends(get_db)):
    campaigns = db.query(Campaign).all()
    return campaigns


@router.get("/campaigns/{campaign_id}", response_model=CampaignDetailResponse)
def get_campaign(campaign_id: int, db: Session = Depends(get_db)):
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Campaign not found")
    return campaign

@router.put("/campaigns/{campaign_id}", response_model=CampaignDetailResponse)
def update_campaign(campaign_id: int, campaign_update: UpdateCampaign, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):      
    if current_user.role != Role.ADMIN and current_user.role != Role.PROJECT_OWNER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update campaigns")
    
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Campaign not found")
    
    if campaign.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this campaign")
    
    for key, value in campaign_update.dict(exclude_unset=True).items():
        setattr(campaign, key, value)
    
    db.commit()
    db.refresh(campaign)
    return campaign


@router.get("/my-campaigns", response_model=list[CampaignListResponse])
def get_my_campaigns(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    campaigns = db.query(Campaign).filter(Campaign.owner_id == current_user.id).all()
    return campaigns

@router.patch("/campaigns/{campaign_id}/status", response_model=CampaignStatusResponse)
def update_campaign_status(campaign_id: int, status_update: CampaignStatusUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != Role.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update campaign status")
    
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Campaign not found")
    
    campaign.status = status_update.status
    db.commit()
    db.refresh(campaign)
    return {"id": campaign.id, "status": campaign.status.value}