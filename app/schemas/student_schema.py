from pydantic import BaseModel, model_validator
from typing import Optional
from typing import List

class AcademicLevelData(BaseModel):
    Age: Optional[int] = None
    Gender: Optional[int] = None
    Country_ID: Optional[int] = None

    @model_validator(mode='after')
    def al_menos_uno_requerido(cls, values):
        if all(getattr(values, field) is None for field in ['Age', 'Gender', 'Country_ID']):
            raise ValueError("Se requiere al menos un campo con valor")
        return values

class AvgDailyUsageHoursData(BaseModel):
    Age: Optional[int] = None
    Gender: Optional[int] = None
    Undergraduate: Optional[int] = None
    Graduate: Optional[int] = None
    High_School: Optional[int] = None
    Platform_ID: Optional[int] = None
    Sleep_Hours_Per_Night: Optional[float] = None
    Mental_Health_Score: Optional[float] = None
    Relationship_Status: Optional[int] = None

    @model_validator(mode='after')
    def al_menos_uno_requerido(cls, values):
        if all(getattr(values, field) is None for field in [
            'Age', 'Gender', 'Undergraduate', 'Graduate', 'High_School',
            'Platform_ID', 'Sleep_Hours_Per_Night', 'Mental_Health_Score', 'Relationship_Status'
        ]):
            raise ValueError("Se requiere al menos un campo con valor")
        return values

class MostUsedPlatformData(BaseModel):
    Age: Optional[int] = None
    Gender: Optional[int] = None
    Undergraduate: Optional[int] = None
    Graduate: Optional[int] = None
    High_School: Optional[int] = None
    Sleep_Hours_Per_Night: Optional[float] = None
    Mental_Health_Score: Optional[float] = None
    Relationship_Status: Optional[int] = None

    @model_validator(mode='after')
    def al_menos_uno_requerido(cls, values):
        if all(getattr(values, field) is None for field in [
            'Age', 'Gender', 'Undergraduate', 'Graduate', 'High_School',
            'Sleep_Hours_Per_Night', 'Mental_Health_Score', 'Relationship_Status'
        ]):
            raise ValueError("Se requiere al menos un campo con valor")
        return values

class MentalHealthScoreData(BaseModel):
    Age: Optional[int] = None
    Gender: Optional[int] = None
    Undergraduate: Optional[int] = None
    Graduate: Optional[int] = None
    High_School: Optional[int] = None
    Avg_Daily_Usage_Hours: Optional[float] = None
    Sleep_Hours_Per_Night: Optional[float] = None
    Relationship_Status: Optional[int] = None

    @model_validator(mode='after')
    def al_menos_uno_requerido(cls, values):
        if all(getattr(values, field) is None for field in [
            'Age', 'Gender', 'Undergraduate', 'Graduate', 'High_School',
            'Avg_Daily_Usage_Hours', 'Sleep_Hours_Per_Night', 'Relationship_Status'
        ]):
            raise ValueError("Se requiere al menos un campo con valor")
        return values

class AffectsAcademicPerformanceData(BaseModel):
    Age: Optional[int] = None
    Gender: Optional[int] = None
    Undergraduate: Optional[int] = None
    Graduate: Optional[int] = None
    High_School: Optional[int] = None
    Avg_Daily_Usage_Hours: Optional[float] = None
    Sleep_Hours_Per_Night: Optional[float] = None
    Mental_Health_Score: Optional[float] = None

    @model_validator(mode='after')
    def al_menos_uno_requerido(cls, values):
        if all(getattr(values, field) is None for field in [
            'Age', 'Gender', 'Undergraduate', 'Graduate', 'High_School',
            'Avg_Daily_Usage_Hours', 'Sleep_Hours_Per_Night', 'Mental_Health_Score'
        ]):
            raise ValueError("Se requiere al menos un campo con valor")
        return values

class RelationshipStatusData(BaseModel):
    Age: Optional[int] = None
    Gender: Optional[int] = None
    Undergraduate: Optional[int] = None
    Graduate: Optional[int] = None
    High_School: Optional[int] = None
    Avg_Daily_Usage_Hours: Optional[float] = None
    Sleep_Hours_Per_Night: Optional[float] = None
    Mental_Health_Score: Optional[float] = None

    @model_validator(mode='after')
    def al_menos_uno_requerido(cls, values):
        if all(getattr(values, field) is None for field in [
            'Age', 'Gender', 'Undergraduate', 'Graduate', 'High_School',
            'Avg_Daily_Usage_Hours', 'Sleep_Hours_Per_Night', 'Mental_Health_Score'
        ]):
            raise ValueError("Se requiere al menos un campo con valor")
        return values

class ConflictsOverSocialMediaData(BaseModel):
    Age: Optional[int] = None
    Gender: Optional[int] = None
    Undergraduate: Optional[int] = None
    Graduate: Optional[int] = None
    High_School: Optional[int] = None
    Avg_Daily_Usage_Hours: Optional[float] = None
    Sleep_Hours_Per_Night: Optional[float] = None
    Mental_Health_Score: Optional[float] = None
    Relationship_Status: Optional[int] = None

    @model_validator(mode='after')
    def al_menos_uno_requerido(cls, values):
        if all(getattr(values, field) is None for field in [
            'Age', 'Gender', 'Undergraduate', 'Graduate', 'High_School',
            'Avg_Daily_Usage_Hours', 'Sleep_Hours_Per_Night', 'Mental_Health_Score',
            'Relationship_Status'
        ]):
            raise ValueError("Se requiere al menos un campo con valor")
        return values

class AddictedScoreData(BaseModel):
    Age: Optional[int] = None
    Gender: Optional[int] = None
    Undergraduate: Optional[int] = None
    Graduate: Optional[int] = None
    High_School: Optional[int] = None
    Avg_Daily_Usage_Hours: Optional[float] = None
    Sleep_Hours_Per_Night: Optional[float] = None
    Mental_Health_Score: Optional[float] = None
    Relationship_Status: Optional[int] = None

    @model_validator(mode='after')
    def al_menos_uno_requerido(cls, values):
        if all(getattr(values, field) is None for field in [
            'Age', 'Gender', 'Undergraduate', 'Graduate', 'High_School',
            'Avg_Daily_Usage_Hours', 'Sleep_Hours_Per_Night', 'Mental_Health_Score',
            'Relationship_Status'
        ]):
            raise ValueError("Se requiere al menos un campo con valor")
        return values

class SocialUpdateData(BaseModel):
    Student_ID: int
    Age: Optional[int] = None
    Gender: Optional[int] = None
    Academic_Level: Optional[str] = None
    Country: Optional[str] = None
    Avg_Daily_Usage_Hours: Optional[float] = None
    Most_Used_Platform: Optional[str] = None
    Affects_Academic_Performance: Optional[bool] = None
    Sleep_Hours_Per_Night: Optional[float] = None
    Mental_Health_Score: Optional[float] = None
    Relationship_Status: Optional[int] = None
    Conflicts_Over_Social_Media: Optional[int] = None
    Addicted_Score: Optional[float] = None
    Undergraduate: Optional[int] = None
    Graduate: Optional[int] = None
    High_School: Optional[int] = None
    Platform_ID: Optional[int] = None
    Country_ID: Optional[int] = None

class SocialDataRequest(BaseModel):
    Student_ID: int
    Age: int
    Gender: int
    Academic_Level: str
    Country: str
    Avg_Daily_Usage_Hours: float
    Most_Used_Platform: str
    Affects_Academic_Performance: bool
    Sleep_Hours_Per_Night: float
    Mental_Health_Score: float
    Relationship_Status: int
    Conflicts_Over_Social_Media: int
    Addicted_Score: float
    Undergraduate: int
    Graduate: int
    High_School: int
    Platform_ID: int
    Country_ID: int

class InsertarDatosSocialRequest(BaseModel):
    datos: List[SocialDataRequest]