import requests
from typing import Dict, Any, Tuple
from app.services.endpoints import endpoints
from app.common.settings import SUPABASE_ANONKEY, SUPABASE_URL
import logging

REFRESH_URL = f"{SUPABASE_URL}/auth/v1/token?grant_type=refresh_token"

def resolve_endpoint(key: str) -> Dict[str, str]:
    parts = key.split('.')
    ref = endpoints
    for part in parts:
        ref = ref.get(part)
        if ref is None:
            raise ValueError(f'Endpoint "{key}" no encontrado')
    return ref

def api_request(
    key: str,
    access_token: str,
    refresh_token: str,
    params: Dict[str, Any] = {},
    data: Any = None
) -> Tuple[Any, str]:
    try:
        endpoint = resolve_endpoint(key)
        method = endpoint["method"]
        url = endpoint["url"]
        print("[supabase] Endpoint resuelto:", url)

        # Reemplazar {param} en la URL
        path_params = {k: v for k, v in params.items() if f"{{{k}}}" in url}
        for k, v in path_params.items():
            url = url.replace(f"{{{k}}}", str(v))
        query_params = {k: v for k, v in params.items() if k not in path_params}

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
            "apikey": SUPABASE_ANONKEY,
        }

        response = requests.request(
            method,
            f"{SUPABASE_URL}{url}",
            headers=headers,
            params=query_params,
            json=data
        )

        if response.status_code == 401:
            print("[supabase] Token expirado, intentando refresh...")
            refresh_response = requests.post(
                REFRESH_URL,
                headers={
                    "Content-Type": "application/json",
                    "apikey": SUPABASE_ANONKEY,
                },
                json={"refresh_token": refresh_token}
            )

            if not refresh_response.ok:
                raise Exception(f"Refresh token inválido: {refresh_response.text}")

            new_access_token = refresh_response.json().get("access_token")
            if not new_access_token:
                raise Exception("No se recibió un nuevo access_token del refresh")

            headers["Authorization"] = f"Bearer {new_access_token}"
            retry_response = requests.request(
                method,
                f"{SUPABASE_URL}{url}",
                headers=headers,
                params=query_params,
                json=data
            )

            if not retry_response.ok:
                raise Exception(f"Error tras el refresh: {retry_response.status_code} - {retry_response.text}")

            return retry_response.json(), new_access_token

        if not response.ok:
            raise Exception(f"Error en la petición: {response.status_code} - {response.text}")

        return response.json(), access_token

    except requests.exceptions.RequestException as req_err:
        logging.exception("Error de red en api_request:")
        raise Exception(f"Error de red al conectar con Supabase: {str(req_err)}")

    except Exception as e:
        logging.exception("Error general en api_request:")
        raise Exception(f"[api_request] Error inesperado: {str(e)}")