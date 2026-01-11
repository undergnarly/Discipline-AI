from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Any

from app.core.config import settings
from app.core.security import create_access_token
from app.db.session import get_db
from app.models.user import User
from app.schemas.google_oauth import GoogleAuthRequest, GoogleAuthResponse
from app.services.google_oauth import GoogleOAuthService

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")
google_oauth_service = GoogleOAuthService()

@router.get("/google/authorize")
async def google_authorize() -> dict:
    """Получить URL для авторизации через Google"""
    return {"authorization_url": google_oauth_service.get_authorization_url()}

@router.post("/google/callback", response_model=GoogleAuthResponse)
async def google_callback(
    request: GoogleAuthRequest,
    db: Session = Depends(get_db)
) -> Any:
    """Обработка callback от Google OAuth"""
    try:
        # Получаем токены
        tokens = await google_oauth_service.get_tokens(request.code)
        
        # Получаем информацию о пользователе
        user_info = await google_oauth_service.get_user_info(tokens.access_token)
        
        # Проверяем существование пользователя
        user = db.query(User).filter(User.google_id == user_info.id).first()
        
        if not user:
            # Создаем нового пользователя
            user = User(
                email=user_info.email,
                username=user_info.email.split("@")[0],
                google_id=user_info.id,
                google_email=user_info.email,
                google_picture=user_info.picture,
                google_access_token=tokens.access_token,
                google_refresh_token=tokens.refresh_token,
                google_token_expiry=datetime.fromtimestamp(
                    datetime.now().timestamp() + tokens.expires_in
                )
            )
            db.add(user)
            db.commit()
            db.refresh(user)
        else:
            # Обновляем токены существующего пользователя
            user.google_access_token = tokens.access_token
            user.google_refresh_token = tokens.refresh_token
            user.google_token_expiry = datetime.fromtimestamp(
                datetime.now().timestamp() + tokens.expires_in
            )
            db.commit()
        
        # Создаем JWT токен
        access_token = create_access_token(data={"sub": user.email})
        
        return GoogleAuthResponse(
            user_info=user_info,
            tokens=tokens
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/google/refresh")
async def refresh_google_token(
    current_user: User = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> Any:
    """Обновить Google токен"""
    user = db.query(User).filter(User.email == current_user.email).first()
    
    if not user or not user.google_refresh_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User not found or no refresh token available"
        )
    
    try:
        tokens = google_oauth_service.refresh_token(user.google_refresh_token)
        
        # Обновляем токены в базе
        user.google_access_token = tokens.access_token
        user.google_refresh_token = tokens.refresh_token
        user.google_token_expiry = datetime.fromtimestamp(
            datetime.now().timestamp() + tokens.expires_in
        )
        db.commit()
        
        return tokens
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        ) 