from fastapi import FastAPI, Header, HTTPException, Depends
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

    print(authorization.split(" "))

    try:
        payload = jwt.decode(
            token,
            SECRET,
            algorithms=["HS256"],
            audience="authenticated"
        )
        print("Token válido. Payload decodificado:")
        print(payload)
        return payload

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado.")
    except jwt.InvalidTokenError as e:
        raise HTTPException(status_code=401, detail=f"Token inválido")
