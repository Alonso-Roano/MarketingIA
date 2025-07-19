endpoints = {
    "auth": {
        "signup": {"method": "POST", "url": "/auth/v1/signup"},
        "login": {"method": "POST", "url": "/auth/v1/token?grant_type=password"},
        "refresh": {"method": "POST", "url": "/auth/v1/token?grant_type=refresh_token"},
        "logout": {"method": "POST", "url": "/auth/v1/logout"},
        "user": {"method": "GET", "url": "/auth/v1/user"},
    },
    "landing": {
        "listar": {"method": "GET", "url": "/functions/v1/landing"},
        "obtener": {"method": "GET", "url": "/functions/v1/landing/{id}"},
        "crear": {"method": "POST", "url": "/functions/v1/landing"},
        "actualizar": {"method": "PUT", "url": "/functions/v1/landing/{id}"},
        "eliminar": {"method": "DELETE", "url": "/functions/v1/landing/{id}"},
    },
    "project": {
        "listar": {"method": "GET", "url": "/functions/v1/project"},
        "obtener": {"method": "GET", "url": "/functions/v1/project/{id}"},
        "crear": {"method": "POST", "url": "/functions/v1/project"},
        "actualizar": {"method": "PUT", "url": "/functions/v1/project/{id}"},
        "eliminar": {"method": "DELETE", "url": "/functions/v1/project/{id}"},
    },
    "projectData": {
        "listar": {"method": "GET", "url": "/functions/v1/project-data"},
        "obtener": {"method": "GET", "url": "/functions/v1/project-data/{id}"},
        "crear": {"method": "POST", "url": "/functions/v1/project-data"},
        "actualizar": {"method": "PUT", "url": "/functions/v1/project-data/{id}"},
        "eliminar": {"method": "DELETE", "url": "/functions/v1/project-data/{id}"},
    },
    "projectPrediction": {
        "listar": {"method": "GET", "url": "/functions/v1/project-prediction"},
        "obtener": {"method": "GET", "url": "/functions/v1/project-prediction/{id}"},
        "crear": {"method": "POST", "url": "/functions/v1/project-prediction"},
        "actualizar": {"method": "PUT", "url": "/functions/v1/project-prediction/{id}"},
        "eliminar": {"method": "DELETE", "url": "/functions/v1/project-prediction/{id}"},
    }
}
