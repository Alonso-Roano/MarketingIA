from fastapi import FastAPI, Header, HTTPException
from typing import Optional, Dict
import jwt
from app.common.settings import SECRET

app = FastAPI()

def verificar_acceso(
    authorization: Optional[str] = Header(None, include_in_schema=False)
) -> Dict:
    if authorization is None:
        raise HTTPException(status_code=401, detail="Header 'Authorization' no enviado.")
    if not authorization.startswith("Bearer Bearer"):
        raise HTTPException(status_code=401, detail="Header 'Authorization' debe empezar con 'Bearer '.")
    
    token = authorization.split(" ")[2]

    try:
        payload = jwt.decode(
            token,
            SECRET,
            algorithms=["HS256"],
            audience="authenticated"
        )
        return payload

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado.")
    except jwt.InvalidTokenError as e:
        raise HTTPException(status_code=401, detail=f"Token inválido")

def obtener_tokens_autenticacion(
    authorization: Optional[str] = Header(None, include_in_schema=False),
    refresh_token: Optional[str] = Header(None, include_in_schema=False)
) -> tuple[str, str]:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Access token inválido o ausente")
    
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token ausente")
    

    access_token = authorization.replace("Bearer ", "")
    return access_token, refresh_token

