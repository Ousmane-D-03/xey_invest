from fastapi import APIRouter, Depends
from backend.schemas.distributions import CreateDitribution, DistributionListResponse
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.auth import get_current_user
from backend.models.user import User, Role
from fastapi import APIRouter, Depends, HTTPException, status
from datetime import datetime
from backend.models.distribution import DistributionStatus, Distribution
from typing import List
from backend.models.campaign import Campaign

router = APIRouter()

@router.post("/distribution",response_model=DistributionListResponse)
def create_distribution(distribution: CreateDitribution, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not authenticated")
    
    if current_user.role != Role.PROJECT_OWNER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to create investements")
    
    new_distribution = Distribution(
        dateDistribution=datetime.utcnow(),
        statut=DistributionStatus.EN_ATTENTE, 
        campaign_id= distribution.campaign_id
    )

    db.add(new_distribution)
    db.commit()
    db.refresh(new_distribution)
    return new_distribution
    

@router.get("/distributions", response_model=List[DistributionListResponse])
def get_distributions(db: Session = Depends(get_db)):
    distributions = db.query(Distribution).all()
    return distributions 

@router.get("/distributions/{campaign_id}", response_model= List[DistributionListResponse])
def get_distribution_by_campaign(campaign_id: int, db: Session = Depends(get_db)):
    distributions = db.query(Distribution).filter(Distribution.campaign_id == campaign_id ).all()
    return distributions

@router.patch("/distributions/{id}/validate", response_model=List[DistributionListResponse])
def validate_distributiion(id: int ,db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not authenticated")
    
    if current_user.role != Role.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to create investements")
    
    distribution = db.query(Distribution).filter(Distribution.id == id).first()

    if not distribution:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Distribution not found")


    campaign = db.query(Campaign).filter(Campaign.id == distribution.campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")

    total_invested_parts = sum(inv.nombrePartAchetees for inv in campaign.investments)
    total_distribution_amount = total_invested_parts * campaign.prixUnitairePart * campaign.tauxRendement

    repartition = []
    for inv in campaign.investments:
        montant = (inv.nombrePartAchetees / campaign.nombreTotalParts) * total_distribution_amount
        repartition.append({
            "user_id": inv.user_id,
            "montant": montant
        })


    db.commit()
    db.refresh(distribution)
    
    return {"distribution": distribution, "repartition": repartition}



