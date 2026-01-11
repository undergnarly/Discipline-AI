from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class GoogleUserInfo(BaseModel):
    id: str
    email: EmailStr
    verified_email: bool
    name: str
    given_name: str
    family_name: str
    picture: str
    locale: str

class GoogleTokenResponse(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str
    expires_in: int
    scope: str
    id_token: Optional[str] = None

class GoogleAuthResponse(BaseModel):
    user_info: GoogleUserInfo
    tokens: GoogleTokenResponse

class GoogleAuthRequest(BaseModel):
    code: str
    redirect_uri: str 