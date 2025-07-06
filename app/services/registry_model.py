from app.services.model_service import ModelService
from app.schemas.student_schema import *
from app.schemas.marketing_schema import *

MODEL_REGISTRY = {
    "academic_level_classifier": {
        "service": ModelService(
            model_path="app/models/academic_level_classifier/current_model.pkl",
            excel_path="app/common/data/students_cleaned.xlsx",
            input_fields=["Age", "Gender", "Country_ID"],
            target_field="Academic_Level",
            metadata={
                "nombre": "Clasificador de Nivel Académico",
                "descripcion": "Clasifica el nivel académico del usuario",
                "campos_esperados": ["Age", "Gender", "Country_ID"],
                "tipo_modelo": "Random Forest"
            }
        ),
        "schema": AcademicLevelData,
        "input_fields": ["Age", "Gender", "Country_ID"],
        "target_field": "Academic_Level",
        "dataset": "students_cleaned.xlsx",
        "model_path": "academic_level_classifier",
        "model_type": "random_forest"
    },
    "avg_daily_usage_regressor": {
        "service": ModelService(
            model_path="app/models/avg_daily_usage_regressor/current_model.pkl",
            excel_path="app/common/data/students_cleaned.xlsx",
            input_fields=[
                "Age", "Gender", "Undergraduate", "Graduate", "High_School",
                "Platform_ID", "Sleep_Hours_Per_Night", "Mental_Health_Score", "Relationship_Status"
            ],
            target_field="Avg_Daily_Usage_Hours",
            metadata={
                "nombre": "Regresor de Uso Diario",
                "descripcion": "Predice las horas de uso diario en redes sociales",
                "campos_esperados": [
                    "Age", "Gender", "Undergraduate", "Graduate", "High_School",
                    "Platform_ID", "Sleep_Hours_Per_Night", "Mental_Health_Score", "Relationship_Status"
                ],
                "tipo_modelo": "Random Forest Regressor"
            }
        ),
        "schema": AvgDailyUsageHoursData,
        "input_fields": [
            "Age", "Gender", "Undergraduate", "Graduate", "High_School",
            "Platform_ID", "Sleep_Hours_Per_Night", "Mental_Health_Score", "Relationship_Status"
        ],
        "target_field": "Avg_Daily_Usage_Hours",
        "dataset": "students_cleaned.xlsx",
        "model_path": "avg_daily_usage_regressor",
        "model_type": "random_forest_regressor"
    },
    "most_used_platform_classifier": {
        "service": ModelService(
            model_path="app/models/most_used_platform_classifier/current_model.pkl",
            excel_path="app/common/data/students_cleaned.xlsx",
            input_fields=[
                "Age", "Gender", "Undergraduate", "Graduate", "High_School",
                "Sleep_Hours_Per_Night", "Mental_Health_Score", "Relationship_Status"
            ],
            target_field="Most_Used_Platform",
            metadata={
                "nombre": "Clasificador de Plataforma Usada",
                "descripcion": "Predice la plataforma de redes sociales más usada",
                "campos_esperados": [
                    "Age", "Gender", "Undergraduate", "Graduate", "High_School",
                    "Sleep_Hours_Per_Night", "Mental_Health_Score", "Relationship_Status"
                ],
                "tipo_modelo": "Random Forest"
            }
        ),
        "schema": MostUsedPlatformData,
        "input_fields": [
            "Age", "Gender", "Undergraduate", "Graduate", "High_School",
            "Sleep_Hours_Per_Night", "Mental_Health_Score", "Relationship_Status"
        ],
        "target_field": "Most_Used_Platform",
        "dataset": "students_cleaned.xlsx",
        "model_path": "most_used_platform_classifier",
        "model_type": "random_forest"
    },
    "mental_health_score_regressor": {
        "service": ModelService(
            model_path="app/models/mental_health_score_regressor/current_model.pkl",
            excel_path="app/common/data/students_cleaned.xlsx",
            input_fields=[
                "Age", "Gender", "Undergraduate", "Graduate", "High_School",
                "Avg_Daily_Usage_Hours", "Sleep_Hours_Per_Night", "Relationship_Status"
            ],
            target_field="Mental_Health_Score",
            metadata={
                "nombre": "Regresor de Salud Mental",
                "descripcion": "Predice el puntaje de salud mental",
                "campos_esperados": [
                    "Age", "Gender", "Undergraduate", "Graduate", "High_School",
                    "Avg_Daily_Usage_Hours", "Sleep_Hours_Per_Night", "Relationship_Status"
                ],
                "tipo_modelo": "Random Forest Regressor"
            }
        ),
        "schema": MentalHealthScoreData,
        "input_fields": [
            "Age", "Gender", "Undergraduate", "Graduate", "High_School",
            "Avg_Daily_Usage_Hours", "Sleep_Hours_Per_Night", "Relationship_Status"
        ],
        "target_field": "Mental_Health_Score",
        "dataset": "students_cleaned.xlsx",
        "model_path": "mental_health_score_regressor",
        "model_type": "random_forest_regressor"
    },
    "affects_academic_performance_classifier": {
        "service": ModelService(
            model_path="app/models/affects_academic_performance_classifier/current_model.pkl",
            excel_path="app/common/data/students_cleaned.xlsx",
            input_fields=[
                "Age", "Gender", "Undergraduate", "Graduate", "High_School",
                "Avg_Daily_Usage_Hours", "Sleep_Hours_Per_Night", "Mental_Health_Score"
            ],
            target_field="Affects_Academic_Performance",
            metadata={
                "nombre": "Impacto en el Rendimiento Académico",
                "descripcion": "Clasifica si el rendimiento académico se ve afectado por el uso de redes",
                "campos_esperados": [
                    "Age", "Gender", "Undergraduate", "Graduate", "High_School",
                    "Avg_Daily_Usage_Hours", "Sleep_Hours_Per_Night", "Mental_Health_Score"
                ],
                "tipo_modelo": "Random Forest"
            }
        ),
        "schema": AffectsAcademicPerformanceData,
        "input_fields": [
            "Age", "Gender", "Undergraduate", "Graduate", "High_School",
            "Avg_Daily_Usage_Hours", "Sleep_Hours_Per_Night", "Mental_Health_Score"
        ],
        "target_field": "Affects_Academic_Performance",
        "dataset": "students_cleaned.xlsx",
        "model_path": "affects_academic_performance_classifier",
        "model_type": "random_forest"
    },
    "relationship_status_classifier": {
        "service": ModelService(
            model_path="app/models/relationship_status_classifier/current_model.pkl",
            excel_path="app/common/data/students_cleaned.xlsx",
            input_fields=[
                "Age", "Gender", "Undergraduate", "Graduate", "High_School",
                "Avg_Daily_Usage_Hours", "Sleep_Hours_Per_Night", "Mental_Health_Score"
            ],
            target_field="Relationship_Status",
            metadata={
                "nombre": "Clasificador de Estado de Relación",
                "descripcion": "Predice el estado de relación del usuario",
                "campos_esperados": [
                    "Age", "Gender", "Undergraduate", "Graduate", "High_School",
                    "Avg_Daily_Usage_Hours", "Sleep_Hours_Per_Night", "Mental_Health_Score"
                ],
                "tipo_modelo": "Random Forest"
            }
        ),
        "schema": RelationshipStatusData,
        "input_fields": [
            "Age", "Gender", "Undergraduate", "Graduate", "High_School",
            "Avg_Daily_Usage_Hours", "Sleep_Hours_Per_Night", "Mental_Health_Score"
        ],
        "target_field": "Relationship_Status",
        "dataset": "students_cleaned.xlsx",
        "model_path": "relationship_status_classifier",
        "model_type": "random_forest"
    },
    "conflicts_over_social_media_classifier": {
        "service": ModelService(
            model_path="app/models/conflicts_over_social_media_classifier/current_model.pkl",
            excel_path="app/common/data/students_cleaned.xlsx",
            input_fields=[
                "Age", "Gender", "Undergraduate", "Graduate", "High_School",
                "Avg_Daily_Usage_Hours", "Sleep_Hours_Per_Night", "Mental_Health_Score",
                "Relationship_Status"
            ],
            target_field="Conflicts_Over_Social_Media",
            metadata={
                "nombre": "Clasificador de Conflictos en Redes",
                "descripcion": "Predice la intensidad de conflictos ocasionados por el uso de redes sociales",
                "campos_esperados": [
                    "Age", "Gender", "Undergraduate", "Graduate", "High_School",
                    "Avg_Daily_Usage_Hours", "Sleep_Hours_Per_Night", "Mental_Health_Score",
                    "Relationship_Status"
                ],
                "tipo_modelo": "Random Forest"
            }
        ),
        "schema": ConflictsOverSocialMediaData,
        "input_fields": [
            "Age", "Gender", "Undergraduate", "Graduate", "High_School",
            "Avg_Daily_Usage_Hours", "Sleep_Hours_Per_Night", "Mental_Health_Score",
            "Relationship_Status"
        ],
        "target_field": "Conflicts_Over_Social_Media",
        "dataset": "students_cleaned.xlsx",
        "model_path": "conflicts_over_social_media_classifier",
        "model_type": "random_forest"
    },
    "addicted_score_regressor": {
        "service": ModelService(
            model_path="app/models/addicted_score_regressor/current_model.pkl",
            excel_path="app/common/data/students_cleaned.xlsx",
            input_fields=[
                "Age", "Gender", "Undergraduate", "Graduate", "High_School",
                "Avg_Daily_Usage_Hours", "Sleep_Hours_Per_Night", "Mental_Health_Score",
                "Relationship_Status"
            ],
            target_field="Addicted_Score",
            metadata={
                "nombre": "Regresor de Adicción a Redes",
                "descripcion": "Predice el nivel de adicción a redes sociales",
                "campos_esperados": [
                    "Age", "Gender", "Undergraduate", "Graduate", "High_School",
                    "Avg_Daily_Usage_Hours", "Sleep_Hours_Per_Night", "Mental_Health_Score",
                    "Relationship_Status"
                ],
                "tipo_modelo": "Random Forest Regressor"
            }
        ),
        "schema": AddictedScoreData,
        "input_fields": [
            "Age", "Gender", "Undergraduate", "Graduate", "High_School",
            "Avg_Daily_Usage_Hours", "Sleep_Hours_Per_Night", "Mental_Health_Score",
            "Relationship_Status"
        ],
        "target_field": "Addicted_Score",
        "dataset": "students_cleaned.xlsx",
        "model_path": "addicted_score_regressor",
        "model_type": "random_forest_regressor"
    },
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
