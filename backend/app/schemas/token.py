from pydantic import BaseModel
import uuid

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class TokenPayload(BaseModel):
    sub: uuid.UUID
    # exp: int # (expiration time) - будет проверяться при декодировании 