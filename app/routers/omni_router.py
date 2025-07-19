from fastapi import APIRouter, Depends, HTTPException
from app.services.omni_service import *
from app.common.middleware import verificar_acceso, obtener_tokens_autenticacion
from app.schemas.master_payload import MasterPayload
from app.services.language_service import extraer_conceptos, predecir_keywords
from app.services.ai21_service import generar_mision_vision_desde_ai21, generar_mision_vision_fake

router = APIRouter(prefix="/omni")

@router.post("/datos")
def omni(payload_maestro: MasterPayload, _: None = Depends(verificar_acceso), tokens: tuple[str, str] = Depends(obtener_tokens_autenticacion)):
    access_token, refresh_token = tokens

    try:
        result_project, new_token = crear_proyecto(
            nombre=payload_maestro.nombre,
            icono=payload_maestro.icono,
            primary_color=payload_maestro.primary_color,
            access_token=access_token,
            refresh_token=refresh_token
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    try:
        result, new_token = crear_project_data(
            access_token=access_token,
            refresh_token=refresh_token,
            body = {
                "descripcion": payload_maestro.description,
                "alcance": payload_maestro.scope,
                "tamaño": payload_maestro.size,
                "no_of_days": payload_maestro.no_of_days,
                "ext_service_name": payload_maestro.ext_service_name,
                "channel_name": payload_maestro.channel_name,
                "approved_budget": payload_maestro.approved_budget,
                "weekday_cat": payload_maestro.weekday_cat,
                "impressions": payload_maestro.impressions,
                "clicks": payload_maestro.clicks,
                "media_cost_usd": payload_maestro.media_cost_usd,
                "rubro": payload_maestro.industry,
                "project_id": result_project["data"]["id"]
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    conceptos = extraer_conceptos(payload_maestro.description, usar_lemma=False)

    keywords = predecir_keywords(conceptos)
    predicciones = ejecutar_todo(payload_maestro.dict())

    mision_vision = generar_mision_vision_desde_ai21(
        payload_maestro.description,
        payload_maestro.industry,
        payload_maestro.size,
        payload_maestro.scope,
        keywords["keywords_predichas_es"]
    )

    contexto = armar_contexto_interpretacion(
        predicciones=predicciones,
        keywords=keywords
    )

    try:
        interpretaciones = interpretar_predicciones_en_contexto(
            predicciones={k: v for k, v in contexto.items() if not k.startswith("descripcion")}, 
            descripcion=payload_maestro.description,
            mision_vision=f"Misión: {mision_vision.mision}, Visión: {mision_vision.vision}"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al interpretar con Gemini: {str(e)}")
    
    try:
        result, new_token = crear_project_prediction(
            access_token=access_token,
            refresh_token=refresh_token,
            body = {
                "project_id": result_project["data"]["id"],
                "mision": mision_vision.mision,
                "vision": mision_vision.vision,
                "no_of_days": int(round(interpretaciones["marketing_no_days"]["prediccion"])),
                "ext_service_name": interpretaciones["marketing_external_service"]["prediccion"],
                "channel_name": interpretaciones["marketing_chanel_name"]["prediccion"],
                "approved_budget": float(interpretaciones["marketing_budget"]["prediccion"]),
                "weekday_cat": interpretaciones["marketing_week_day"]["prediccion"],
                "impressions": int(round(interpretaciones["marketing_impressions"]["prediccion"])),
                "clicks": int(round(interpretaciones["marketing_clicks"]["prediccion"])),
                "media_cost_usd": float(interpretaciones["marketing_media_cost"]["prediccion"]),
                "palabras_clave": ", ".join(interpretaciones["keywords_predichas"]["prediccion"]),

                "interpretacion_no_of_days": interpretaciones["marketing_no_days"]["interpretacion"],
                "interpretacion_ext_service_name": interpretaciones["marketing_external_service"]["interpretacion"],
                "interpretacion_channel_name": interpretaciones["marketing_chanel_name"]["interpretacion"],
                "interpretacion_approved_budget": interpretaciones["marketing_budget"]["interpretacion"],
                "interpretacion_weekday_cat": interpretaciones["marketing_week_day"]["interpretacion"],
                "interpretacion_impressions": interpretaciones["marketing_impressions"]["interpretacion"],
                "interpretacion_clicks": interpretaciones["marketing_clicks"]["interpretacion"],
                "interpretacion_media_cost_usd": interpretaciones["marketing_media_cost"]["interpretacion"],
                "interpretacion_palabras_clave": interpretaciones["keywords_predichas"]["interpretacion"]
            }

        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {
        "succes": True,
        "project_id": result_project["data"]["id"],
        "access_token": new_token,
        "token_updated": new_token != access_token
    }