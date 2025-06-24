from fastapi import Header, HTTPException
from app.common.settings import ACCESS_TOKEN, ADMIN_TOKEN
from typing import Optional

def verificar_acceso(authorization: Optional[str] = Header(None, include_in_schema=False)):
    if authorization is None or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token no enviado o mal formato")
    token = authorization.split(" ")[1]
    if token != ACCESS_TOKEN and token != ADMIN_TOKEN:
        raise HTTPException(status_code=401, detail="Token de acceso inválido")

def verificar_admin(authorization: Optional[str] = Header(None, include_in_schema=False)):
    if authorization is None or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=403, detail="Token no enviado o mal formato")
    token = authorization.split(" ")[1]
    if token != ADMIN_TOKEN:
        raise HTTPException(status_code=401, detail="Token de acceso inválido")


