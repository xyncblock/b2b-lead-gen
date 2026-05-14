from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.database import get_async_session
from app.models import Business, User
from app.schemas import BusinessCreate, BusinessUpdate, BusinessRead
from app.auth import get_current_active_user

router = APIRouter(prefix="/api/businesses", tags=["businesses"])


@router.get("/", response_model=List[BusinessRead])
async def list_businesses(
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_active_user)
):
    result = await session.execute(
        select(Business).where(Business.user_id == current_user.id)
    )
    businesses = result.scalars().all()
    return businesses


@router.post("/", response_model=BusinessRead)
async def create_business(
    business_data: BusinessCreate,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_active_user)
):
    business = Business(
        user_id=current_user.id,
        name=business_data.name,
        description=business_data.description,
        target_market=business_data.target_market,
        ideal_customer_profile=business_data.ideal_customer_profile
    )
    session.add(business)
    await session.commit()
    await session.refresh(business)
    return business


@router.get("/{business_id}", response_model=BusinessRead)
async def get_business(
    business_id: int,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_active_user)
):
    result = await session.execute(
        select(Business).where(
            Business.id == business_id,
            Business.user_id == current_user.id
        )
    )
    business = result.scalar_one_or_none()
    if not business:
        raise HTTPException(status_code=404, detail="Business not found")
    return business


@router.patch("/{business_id}", response_model=BusinessRead)
async def update_business(
    business_id: int,
    business_data: BusinessUpdate,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_active_user)
):
    result = await session.execute(
        select(Business).where(
            Business.id == business_id,
            Business.user_id == current_user.id
        )
    )
    business = result.scalar_one_or_none()
    if not business:
        raise HTTPException(status_code=404, detail="Business not found")
    
    update_data = business_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(business, field, value)
    
    await session.commit()
    await session.refresh(business)
    return business


@router.delete("/{business_id}")
async def delete_business(
    business_id: int,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_active_user)
):
    result = await session.execute(
        select(Business).where(
            Business.id == business_id,
            Business.user_id == current_user.id
        )
    )
    business = result.scalar_one_or_none()
    if not business:
        raise HTTPException(status_code=404, detail="Business not found")
    
    await session.delete(business)
    await session.commit()
    return {"message": "Business deleted"}
