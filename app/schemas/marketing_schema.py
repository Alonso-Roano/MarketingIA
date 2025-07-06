from pydantic import BaseModel, model_validator
from typing import Optional

class Impressions(BaseModel):
    no_of_days: Optional[int] = None
    approved_budget: Optional[float] = None
    ext_service_name_DV360: Optional[int] = None
    ext_service_name_Facebook_Ads: Optional[int] = None
    ext_service_name_Google_Ads: Optional[int] = None
    channel_name_Display: Optional[int] = None
    channel_name_Mobile: Optional[int] = None
    channel_name_Search: Optional[int] = None
    channel_name_Social: Optional[int] = None
    channel_name_Video: Optional[int] = None
    weekday_cat_week_day: Optional[int] = None
    weekday_cat_week_end: Optional[int] = None

    @model_validator(mode='after')
    def at_least_one_required(cls, values):
        if all(
            getattr(values, field) is None for field in [
                'no_of_days', 'approved_budget',
                'ext_service_name_DV360', 'ext_service_name_Facebook_Ads', 'ext_service_name_Google_Ads',
                'channel_name_Display', 'channel_name_Mobile', 'channel_name_Search',
                'channel_name_Social', 'channel_name_Video',
                'weekday_cat_week_day', 'weekday_cat_week_end'
            ]
        ):
            raise ValueError("Se requiere al menos un campo con valor")
        return values

class Clicks(Impressions):
    pass

class MediaCostUSD(Impressions):
    pass

class NoOfDays(BaseModel):
    clicks: Optional[int] = None
    impressions: Optional[int] = None
    approved_budget: Optional[float] = None
    ext_service_name_enc: Optional[int] = None
    channel_name_enc: Optional[int] = None
    weekday_cat_enc: Optional[int] = None

    @model_validator(mode='after')
    def at_least_one_required(cls, values):
        if all(
            getattr(values, field) is None for field in [
                'clicks', 'impressions', 'approved_budget',
                'ext_service_name_enc', 'channel_name_enc', 'weekday_cat_enc'
            ]
        ):
            raise ValueError("Se requiere al menos un campo con valor")
        return values

class ApprovedBudget(BaseModel):
    clicks: Optional[int] = None
    impressions: Optional[int] = None
    no_of_days: Optional[int] = None
    ext_service_name_enc: Optional[int] = None
    channel_name_enc: Optional[int] = None
    weekday_cat_enc: Optional[int] = None

    @model_validator(mode='after')
    def at_least_one_required(cls, values):
        if all(
            getattr(values, field) is None for field in [
                'clicks', 'impressions', 'no_of_days',
                'ext_service_name_enc', 'channel_name_enc', 'weekday_cat_enc'
            ]
        ):
            raise ValueError("Se requiere al menos un campo con valor")
        return values

class ExtService(BaseModel):
    clicks: Optional[int] = None
    impressions: Optional[int] = None
    no_of_days: Optional[int] = None
    approved_budget: Optional[float] = None
    channel_name_enc: Optional[int] = None
    weekday_cat_enc: Optional[int] = None

    @model_validator(mode='after')
    def at_least_one_required(cls, values):
        if all(
            getattr(values, field) is None for field in [
                'clicks', 'impressions', 'no_of_days',
                'approved_budget', 'channel_name_enc', 'weekday_cat_enc'
            ]
        ):
            raise ValueError("Se requiere al menos un campo con valor")
        return values

class WeekdayCat(BaseModel):
    clicks: Optional[int] = None
    impressions: Optional[int] = None
    no_of_days: Optional[int] = None
    approved_budget: Optional[float] = None
    ext_service_name_enc: Optional[int] = None
    channel_name_enc: Optional[int] = None

    @model_validator(mode='after')
    def at_least_one_required(cls, values):
        if all(
            getattr(values, field) is None for field in [
                'clicks', 'impressions', 'no_of_days',
                'approved_budget', 'ext_service_name_enc', 'channel_name_enc'
            ]
        ):
            raise ValueError("Se requiere al menos un campo con valor")
        return values

class ChannelName(BaseModel):
    clicks: Optional[int] = None
    impressions: Optional[int] = None
    no_of_days: Optional[int] = None
    approved_budget: Optional[float] = None
    ext_service_name_enc: Optional[int] = None
    weekday_cat_enc: Optional[int] = None

    @model_validator(mode='after')
    def at_least_one_required(cls, values):
        if all(
            getattr(values, field) is None for field in [
                'clicks', 'impressions', 'no_of_days',
                'approved_budget', 'ext_service_name_enc', 'weekday_cat_enc'
            ]
        ):
            raise ValueError("Se requiere al menos un campo con valor")
        return values