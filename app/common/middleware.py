from fastapi import Header, HTTPException
from typing import Optional
import httpx
from app.common.settings import TOKEN_URL

def verificar_acceso(authorization: Optional[str] = Header(None, include_in_schema=False)):
    if authorization is None or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token no enviado o mal formato")
    
    token = authorization.split(" ")[1]

    try:
        response = httpx.get(
            TOKEN_URL,
            headers={"Authorization": f"Bearer {token}"},
            timeout=10
        )
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"No se pudo contactar el validador: {str(e)}")

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Token inválido o expirado")

    return response.json()


