from app.services.model_service import ModelService
from app.schemas.marketing_schema import *

MODEL_REGISTRY = {
    "marketing_impressions": {
        "service": ModelService(
            model_path="app/models/impressions/current_model.pkl",
            excel_path="app/common/data/marketing_data.xlsx",
            input_fields=['no_of_days', 'approved_budget', 'ext_service_name_DV360', 'ext_service_name_Facebook Ads', 'ext_service_name_Google Ads', 
                          'channel_name_Display', 'channel_name_Mobile', 'channel_name_Search', 'channel_name_Social', 'channel_name_Video', 
                          'weekday_cat_week_day', 'weekday_cat_week_end'],
            target_field="impressions",
            metadata={
                "nombre": "Regresor impresiones",
                "descripcion": "Predice la cantidad de impresiones que tendra una campaña publicitaria",
                "campos_esperados": ['no_of_days', 'approved_budget', 'ext_service_name_DV360', 'ext_service_name_Facebook Ads', 
                                     'ext_service_name_Google Ads', 'channel_name_Display', 'channel_name_Mobile', 
                                     'channel_name_Search', 'channel_name_Social', 'channel_name_Video', 'weekday_cat_week_day', 'weekday_cat_week_end'],
                "tipo_modelo": "Random Forest Regressor"
            }
        ),
        "schema": Impressions,
        "input_fields": ['no_of_days', 'approved_budget', 'ext_service_name_DV360', 'ext_service_name_Facebook Ads', 
                                     'ext_service_name_Google Ads', 'channel_name_Display', 'channel_name_Mobile', 
                                     'channel_name_Search', 'channel_name_Social', 'channel_name_Video', 'weekday_cat_week_day', 'weekday_cat_week_end'],
        "target_field": "impressions",
        "dataset": "marketing_data.xlsx",
        "model_path": "impressions",
        "model_type": "random_forest_regressor",
        "train_enabled": False
    },
    "marketing_clicks": {
        "service": ModelService(
            model_path="app/models/clicks/current_model.pkl",
            excel_path="app/common/data/marketing_data.xlsx",
            input_fields=['no_of_days', 'approved_budget', 'ext_service_name_DV360', 'ext_service_name_Facebook Ads', 'ext_service_name_Google Ads', 
                          'channel_name_Display', 'channel_name_Mobile', 'channel_name_Search', 'channel_name_Social', 'channel_name_Video', 
                          'weekday_cat_week_day', 'weekday_cat_week_end'],
            target_field="clicks",
            metadata={
                "nombre": "Regresor clicks",
                "descripcion": "Predice la cantidad de clicks que tendra una campaña publicitaria",
                "campos_esperados": ['no_of_days', 'approved_budget', 'ext_service_name_DV360', 'ext_service_name_Facebook Ads', 
                                     'ext_service_name_Google Ads', 'channel_name_Display', 'channel_name_Mobile', 
                                     'channel_name_Search', 'channel_name_Social', 'channel_name_Video', 'weekday_cat_week_day', 'weekday_cat_week_end'],
                "tipo_modelo": "Random Forest Regressor"
            }
        ),
        "schema": Clicks,
        "input_fields": ['no_of_days', 'approved_budget', 'ext_service_name_DV360', 'ext_service_name_Facebook Ads', 
                                     'ext_service_name_Google Ads', 'channel_name_Display', 'channel_name_Mobile', 
                                     'channel_name_Search', 'channel_name_Social', 'channel_name_Video', 'weekday_cat_week_day', 'weekday_cat_week_end'],
        "target_field": "clicks",
        "dataset": "marketing_data.xlsx",
        "model_path": "clicks",
        "model_type": "random_forest_regressor",
        "train_enabled": False
    },
    "marketing_media_cost": {
        "service": ModelService(
            model_path="app/models/media_cost/current_model.pkl",
            excel_path="app/common/data/marketing_data.xlsx",
            input_fields=['no_of_days', 'approved_budget', 'ext_service_name_DV360', 'ext_service_name_Facebook Ads', 'ext_service_name_Google Ads', 
                          'channel_name_Display', 'channel_name_Mobile', 'channel_name_Search', 'channel_name_Social', 'channel_name_Video', 
                          'weekday_cat_week_day', 'weekday_cat_week_end'],
            target_field="media_cost_usd",
            metadata={
                "nombre": "Regresor costo real",
                "descripcion": "Predice el presupuesto real por dia que tendra una campaña publicitaria",
                "campos_esperados": ['no_of_days', 'approved_budget', 'ext_service_name_DV360', 'ext_service_name_Facebook Ads', 
                                     'ext_service_name_Google Ads', 'channel_name_Display', 'channel_name_Mobile', 
                                     'channel_name_Search', 'channel_name_Social', 'channel_name_Video', 'weekday_cat_week_day', 'weekday_cat_week_end'],
                "tipo_modelo": "Random Forest Regressor"
            }
        ),
        "schema": MediaCostUSD,
        "input_fields": ['no_of_days', 'approved_budget', 'ext_service_name_DV360', 'ext_service_name_Facebook Ads', 
                                     'ext_service_name_Google Ads', 'channel_name_Display', 'channel_name_Mobile', 
                                     'channel_name_Search', 'channel_name_Social', 'channel_name_Video', 'weekday_cat_week_day', 'weekday_cat_week_end'],
        "target_field": "media_cost_usd",
        "dataset": "marketing_data.xlsx",
        "model_path": "media_cost",
        "model_type": "random_forest_regressor",
        "train_enabled": False
    },
    "marketing_no_days": {
        "service": ModelService(
            model_path="app/models/no_days/current_model.pkl",
            excel_path="app/common/data/marketing_data.xlsx",
            input_fields= ['clicks', 'impressions', 'approved_budget','ext_service_name_enc', 'channel_name_enc', 'weekday_cat_enc'],
            target_field="no_of_days",
            metadata={
                "nombre": "Regresor numero de dias",
                "descripcion": "Predice el numero de dias que durara una campaña publicitaria",
                "campos_esperados":  ['clicks', 'impressions', 'approved_budget','ext_service_name_enc', 'channel_name_enc', 'weekday_cat_enc'],
                "tipo_modelo": "Random Forest Regressor"
            }
        ),
        "schema": NoOfDays,
        "input_fields":  ['clicks', 'impressions', 'approved_budget','ext_service_name_enc', 'channel_name_enc', 'weekday_cat_enc'],
        "target_field": "no_of_days",
        "dataset": "marketing_data.xlsx",
        "model_path": "no_days",
        "model_type": "random_forest_regressor",
        "train_enabled": False
    },
    "marketing_budget": {
        "service": ModelService(
            model_path="app/models/budget/current_model.pkl",
            excel_path="app/common/data/marketing_data.xlsx",
            input_fields= ['clicks', 'impressions', 'no_of_days', 'ext_service_name_enc', 'channel_name_enc', 'weekday_cat_enc'],
            target_field="approved_budget",
            metadata={
                "nombre": "Regresor presupuesto",
                "descripcion": "Predice el presupuesto maximo de una campaña publicitaria",
                "campos_esperados": ['clicks', 'impressions', 'no_of_days', 'ext_service_name_enc', 'channel_name_enc', 'weekday_cat_enc'],
                "tipo_modelo": "Random Forest Regressor"
            }
        ),
        "schema": ApprovedBudget,
        "input_fields": ['clicks', 'impressions', 'no_of_days', 'ext_service_name_enc', 'channel_name_enc', 'weekday_cat_enc'],
        "target_field": "approved_budget",
        "dataset": "marketing_data.xlsx",
        "model_path": "budget",
        "model_type": "random_forest_regressor",
        "train_enabled": False
    },
    "marketing_external_service": {
        "service": ModelService(
            model_path="app/models/media_service/current_model.pkl",
            excel_path="app/common/data/marketing_data.xlsx",
            input_fields= ['clicks', 'impressions', 'no_of_days', 'approved_budget', 'channel_name_enc', 'weekday_cat_enc'],
            target_field="ext_service_name",
            metadata={
                "nombre": "Regresor servicio externo",
                "descripcion": "Predice que servicio externo usar en una campaña publicitaria",
                "campos_esperados": ['clicks', 'impressions', 'no_of_days', 'approved_budget', 'channel_name_enc', 'weekday_cat_enc'],
                "tipo_modelo": "Random Forest"
            }
        ),
        "schema": ExtService,
        "input_fields": ['clicks', 'impressions', 'no_of_days', 'approved_budget', 'channel_name_enc', 'weekday_cat_enc'],
        "target_field": "ext_service_name",
        "dataset": "marketing_data.xlsx",
        "model_path": "media_service",
        "model_type": "random_forest",
        "train_enabled": False
    },
    "marketing_week_day": {
        "service": ModelService(
            model_path="app/models/week_day/current_model.pkl",
            excel_path="app/common/data/marketing_data.xlsx",
            input_fields= ['clicks', 'impressions', 'no_of_days', 'approved_budget', 'ext_service_name_enc', 'channel_name_enc'],
            target_field="weekday_cat",
            metadata={
                "nombre": "Regresor dia de la semana",
                "descripcion": "Predice que dia de la semana hacer una campaña publicitaria",
                "campos_esperados": ['clicks', 'impressions', 'no_of_days', 'approved_budget', 'ext_service_name_enc', 'channel_name_enc'],
                "tipo_modelo": "Random Forest"
            }
        ),
        "schema": WeekdayCat,
        "input_fields": ['clicks', 'impressions', 'no_of_days', 'approved_budget', 'ext_service_name_enc', 'channel_name_enc'],
        "target_field": "weekday_cat",
        "dataset": "marketing_data.xlsx",
        "model_path": "week_day",
        "model_type": "random_forest",
        "train_enabled": False
    },
    "marketing_chanel_name": {
        "service": ModelService(
            model_path="app/models/chanel/current_model.pkl",
            excel_path="app/common/data/marketing_data.xlsx",
            input_fields= ['clicks', 'impressions', 'no_of_days', 'approved_budget', 'ext_service_name_enc', 'weekday_cat_enc'],
            target_field="chanel_name",
            metadata={
                "nombre": "Regresor canal de comunicacion",
                "descripcion": "Predice que canal de comunicacion usar en una campaña publicitaria",
                "campos_esperados": ['clicks', 'impressions', 'no_of_days', 'approved_budget', 'ext_service_name_enc', 'weekday_cat_enc'],
                "tipo_modelo": "Random Forest"
            }
        ),
        "schema": WeekdayCat,
        "input_fields": ['clicks', 'impressions', 'no_of_days', 'approved_budget', 'ext_service_name_enc', 'weekday_cat_enc'],
        "target_field": "chanel_name",
        "dataset": "marketing_data.xlsx",
        "model_path": "chanel",
        "model_type": "random_forest",
        "train_enabled": False
    }
}
