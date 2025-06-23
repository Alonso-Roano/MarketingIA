from app.services.model_service import ModelService
from app.schemas.student_schema import AcademicLevelData, AvgDailyUsageHoursData, MostUsedPlatformData, MentalHealthScoreData, AffectsAcademicPerformanceData, RelationshipStatusData, ConflictsOverSocialMediaData, AddictedScoreData

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
    }
}
