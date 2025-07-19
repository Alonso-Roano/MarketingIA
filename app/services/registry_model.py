from app.services.model_service import ModelService
from app.schemas.marketing_schema import *
import threading

MODEL_CONFIG = {
    "marketing_impressions": {
        "excel_path":"app\common\data\marketing_data.csv",
        "model_path": "app/models/impressions/current_model.pkl",
        "dataset": "marketing_data.csv",
        "input_fields": ['no_of_days', 'approved_budget', 'ext_service_name', 'channel_name', 'weekday_cat', 'media_cost_usd'],
        "target_field": "impressions",
        "schema": Impressions,
        "metadata": {
            "nombre": "Regresor impresiones",
            "descripcion": "Predice la cantidad de impresiones que tendra una campaña publicitaria",
            "campos_esperados": ['no_of_days', 'approved_budget', 'ext_service_name', 'channel_name', 'weekday_cat', 'media_cost_usd'],
            "tipo_modelo": "Random Forest Regressor"
        },
        "model_type": "random_forest_regressor",
        "train_enabled": False
    },
    "marketing_clicks": {
        "excel_path":"app\common\data\marketing_data.csv",
        "model_path": "app/models/clicks/current_model.pkl",
        "dataset": "marketing_data.csv",
        "input_fields": ['no_of_days', 'approved_budget', 'ext_service_name', 'channel_name', 'weekday_cat', 'impressions', 'media_cost_usd'],
        "target_field": "clicks",
        "schema": Clicks,
        "metadata": {
            "nombre": "Regresor clicks",
            "descripcion": "Predice la cantidad de clicks que tendra una campaña publicitaria",
            "campos_esperados": ['no_of_days', 'approved_budget', 'ext_service_name', 'channel_name', 'weekday_cat', 'impressions', 'media_cost_usd'],
            "tipo_modelo": "Random Forest Regressor"
        },
        "model_type": "random_forest_regressor",
        "train_enabled": False
    },
    "marketing_media_cost": {
        "excel_path":"app\common\data\marketing_data.csv",
        "model_path": "app/models/media_cost/current_model.pkl",
        "dataset": "marketing_data.csv",
        "input_fields": ['no_of_days', 'approved_budget', 'ext_service_name', 'channel_name', 'weekday_cat', 'impressions', 'clicks'],
        "target_field": "media_cost_usd",
        "schema": MediaCostUSD,
        "metadata": {
            "nombre": "Regresor costo real",
            "descripcion": "Predice el presupuesto real por dia que tendra una campaña publicitaria",
            "campos_esperados": ['no_of_days', 'approved_budget', 'ext_service_name', 'channel_name', 'weekday_cat', 'impressions', 'clicks'],
            "tipo_modelo": "Random Forest Regressor"
        },
        "model_type": "random_forest_regressor",
        "train_enabled": False
    },
    "marketing_no_days": {
        "excel_path":"app\common\data\marketing_data.csv",
        "model_path": "app/models/no_days/current_model.pkl",
        "dataset": "marketing_data.csv",
        "input_fields": ['clicks', 'impressions', 'media_cost_usd', 'approved_budget', 'ext_service_name_enc', 'channel_name_enc', 'weekday_cat_enc'],
        "target_field": "no_of_days",
        "schema": NoOfDays,
        "metadata": {
            "nombre": "Regresor numero de dias",
            "descripcion": "Predice el numero de dias que durara una campaña publicitaria",
            "campos_esperados": ['clicks', 'impressions', 'media_cost_usd', 'approved_budget', 'ext_service_name_enc', 'channel_name_enc', 'weekday_cat_enc'],
            "tipo_modelo": "Random Forest Regressor"
        },
        "model_type": "random_forest_regressor",
        "train_enabled": False
    },
    "marketing_budget": {
        "excel_path":"app\common\data\marketing_data.csv",
        "model_path": "app/models/budget/current_model.pkl",
        "dataset": "marketing_data.csv",
        "input_fields": ['clicks', 'impressions', 'no_of_days', 'media_cost_usd', 'ext_service_name_enc', 'channel_name_enc', 'weekday_cat_enc'],
        "target_field": "approved_budget",
        "schema": ApprovedBudget,
        "metadata": {
            "nombre": "Regresor presupuesto",
            "descripcion": "Predice el presupuesto maximo de una campaña publicitaria",
            "campos_esperados": ['clicks', 'impressions', 'no_of_days', 'media_cost_usd', 'ext_service_name_enc', 'channel_name_enc', 'weekday_cat_enc'],
            "tipo_modelo": "Random Forest Regressor"
        },
        "model_type": "random_forest_regressor",
        "train_enabled": False
    },
    "marketing_external_service": {
        "excel_path":"app\common\data\marketing_data.csv",
        "model_path": "app/models/media_service/current_model.pkl",
        "dataset": "marketing_data.csv",
        "input_fields": ['clicks', 'impressions', 'no_of_days', 'approved_budget', 'channel_name_enc', 'weekday_cat_enc'],
        "target_field": "ext_service_name",
        "schema": ExtService,
        "metadata": {
            "nombre": "Regresor servicio externo",
            "descripcion": "Predice que servicio externo usar en una campaña publicitaria",
            "campos_esperados": ['clicks', 'impressions', 'no_of_days', 'approved_budget', 'channel_name_enc', 'weekday_cat_enc'],
            "tipo_modelo": "Random Forest"
        },
        "model_type": "random_forest",
        "train_enabled": False
    },
    "marketing_week_day": {
        "excel_path":"app\common\data\marketing_data.csv",
        "model_path": "app/models/week_day/current_model.pkl",
        "dataset": "marketing_data.csv",
        "input_fields": ['clicks', 'impressions', 'no_of_days', 'approved_budget', 'ext_service_name_enc', 'channel_name_enc'],
        "target_field": "weekday_cat",
        "schema": WeekdayCat,
        "metadata": {
            "nombre": "Regresor dia de la semana",
            "descripcion": "Predice que dia de la semana hacer una campaña publicitaria",
            "campos_esperados": ['clicks', 'impressions', 'no_of_days', 'approved_budget', 'ext_service_name_enc', 'channel_name_enc'],
            "tipo_modelo": "Random Forest"
        },
        "model_type": "random_forest",
        "train_enabled": False
    },
    "marketing_chanel_name": {
        "excel_path":"app\common\data\marketing_data.csv",
        "model_path": "app/models/chanel/current_model.pkl",
        "dataset": "marketing_data.csv",
        "input_fields": ['clicks', 'impressions', 'no_of_days', 'approved_budget', 'ext_service_name_enc', 'weekday_cat_enc'],
        "target_field": "channel_name",
        "schema": ChannelName,
        "metadata": {
            "nombre": "Regresor canal de comunicacion",
            "descripcion": "Predice que canal de comunicacion usar en una campaña publicitaria",
            "campos_esperados": ['clicks', 'impressions', 'no_of_days', 'approved_budget', 'ext_service_name_enc', 'weekday_cat_enc'],
            "tipo_modelo": "Random Forest"
        },
        "model_type": "random_forest",
        "train_enabled": False
    }
}

MODEL_REGISTRY = {}

_modeles_cargados = False
_lock = threading.Lock()
_modeles_cargados_count = 0
_modeles_totales = 0

import threading
import traceback

def cargar_modelos():
    def _wrapper():
        try:
            print("[INIT] Cargando modelos de IA...")
            global MODEL_REGISTRY, _modeles_cargados, _modeles_cargados_count, _modeles_totales

            with _lock:
                _modeles_cargados_count = 0
                _modeles_totales = len(MODEL_CONFIG)

                for nombre_modelo, config in MODEL_CONFIG.items():
                    servicio = ModelService(
                        model_path=config["model_path"],
                        excel_path=config["excel_path"],
                        input_fields=config["input_fields"],
                        target_field=config["target_field"],
                        metadata=config["metadata"]
                    )
                    MODEL_REGISTRY[nombre_modelo] = {
                        "service": servicio,
                        "schema": config["schema"],
                        "input_fields": config["input_fields"],
                        "target_field": config["target_field"],
                        "dataset": config.get("dataset", None),
                        "model_type": config.get("model_type", None),
                        "train_enabled": config.get("train_enabled", False),
                    }
                    _modeles_cargados_count += 1
                    print(f"[LOAD] Cargando modelos: {_modeles_cargados_count}/{_modeles_totales}")

                _modeles_cargados = True
                print("[INIT] Modelos de IA cargados.")
        except Exception as e:
            print(f"[ERROR] en cargar_modelos: {e}")
            traceback.print_exc()

    hilo = threading.Thread(target=_wrapper, name="CargaModelosIA", daemon=True)
    hilo.start()

def estan_modelos_listos():
    with _lock:
        return _modeles_cargados

def progreso_carga_modelos():
    with _lock:
        return _modeles_cargados_count, _modeles_totales
