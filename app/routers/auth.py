from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import timedelta

from app.database import get_async_session
from app.models import User
from app.schemas import UserCreate, UserRead
from app.auth import (
    get_password_hash, verify_password, create_access_token,
    get_current_active_user
)
from app.config import get_settings

settings = get_settings()
router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=UserRead)
async def register(user_data: UserCreate, session: AsyncSession = Depends(get_async_session)):
    # Check if user exists
    result = await session.execute(select(User).where(User.email == user_data.email))
    existing = result.scalar_one_or_none()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create user
    user = User(
        email=user_data.email,
        hashed_password=get_password_hash(user_data.password)
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_async_session)
):
    result = await session.execute(select(User).where(User.email == form_data.username))
    user = result.scalar_one_or_none()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/logout")
async def logout():
    # JWT is stateless, client just discards token
    return {"message": "Successfully logged out"}


@router.get("/me", response_model=UserRead)
async def get_me(current_user: User = Depends(get_current_active_user)):
    return current_user
