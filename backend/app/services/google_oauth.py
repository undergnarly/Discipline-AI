from datetime import datetime, timedelta
from typing import Optional
import httpx
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
from app.core.config import settings
from app.schemas.google_oauth import GoogleUserInfo, GoogleTokenResponse

class GoogleOAuthService:
    def __init__(self):
        self.client_id = settings.GOOGLE_CLIENT_ID
        self.client_secret = settings.GOOGLE_CLIENT_SECRET
        self.redirect_uri = settings.GOOGLE_REDIRECT_URI
        self.scopes = [
            "https://www.googleapis.com/auth/userinfo.profile",
            "https://www.googleapis.com/auth/userinfo.email",
            "openid"
        ]

    def get_authorization_url(self) -> str:
        flow = Flow.from_client_config(
            {
                "web": {
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                }
            },
            scopes=self.scopes,
            redirect_uri=self.redirect_uri
        )
        return flow.authorization_url()[0]

    async def get_tokens(self, code: str) -> GoogleTokenResponse:
        flow = Flow.from_client_config(
            {
                "web": {
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                }
            },
            scopes=self.scopes,
            redirect_uri=self.redirect_uri
        )
        
        flow.fetch_token(code=code)
        credentials = flow.credentials
        
        return GoogleTokenResponse(
            access_token=credentials.token,
            refresh_token=credentials.refresh_token,
            token_type=credentials.token_type,
            expires_in=credentials.expiry.timestamp() - datetime.now().timestamp(),
            scope=credentials.scopes[0],
            id_token=credentials.id_token
        )

    async def get_user_info(self, access_token: str) -> GoogleUserInfo:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://www.googleapis.com/oauth2/v2/userinfo",
                headers={"Authorization": f"Bearer {access_token}"}
            )
            response.raise_for_status()
            data = response.json()
            
            return GoogleUserInfo(
                id=data["id"],
                email=data["email"],
                verified_email=data["verified_email"],
                name=data["name"],
                given_name=data["given_name"],
                family_name=data["family_name"],
                picture=data["picture"],
                locale=data["locale"]
            )

    def refresh_token(self, refresh_token: str) -> GoogleTokenResponse:
        credentials = Credentials(
            None,
            refresh_token=refresh_token,
            token_uri="https://oauth2.googleapis.com/token",
            client_id=self.client_id,
            client_secret=self.client_secret
        )
        
        credentials.refresh(Request())
        
        return GoogleTokenResponse(
            access_token=credentials.token,
            refresh_token=credentials.refresh_token,
            token_type=credentials.token_type,
            expires_in=credentials.expiry.timestamp() - datetime.now().timestamp(),
            scope=credentials.scopes[0],
            id_token=credentials.id_token
        ) 