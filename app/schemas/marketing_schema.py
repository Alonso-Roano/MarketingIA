from pydantic import BaseModel, model_validator
from typing import Optional

class Impressions(BaseModel):
    no_of_days: Optional[int] = None
    approved_budget: Optional[float] = None
    ext_service_name: Optional[str] = None
    channel_name: Optional[str] = None
    weekday_cat: Optional[str] = None
    media_cost_usd: Optional[float] = None

    @model_validator(mode='after')
    def at_least_one_required(cls, values):
        if all(
            getattr(values, field) is None for field in ['no_of_days', 'approved_budget', 'ext_service_name', 'channel_name', 'weekday_cat', 'media_cost_usd']
        ):
            raise ValueError("Se requiere al menos un campo con valor")
        return values

class Clicks(BaseModel):
    no_of_days: Optional[int] = None
    approved_budget: Optional[float] = None
    ext_service_name: Optional[str] = None
    channel_name: Optional[str] = None
    weekday_cat: Optional[str] = None
    impressions: Optional[int] = None
    media_cost_usd: Optional[float] = None
    

    @model_validator(mode='after')
    def at_least_one_required(cls, values):
        if all(
            getattr(values, field) is None for field in ['no_of_days', 'approved_budget', 'ext_service_name', 'channel_name', 'weekday_cat', 'impressions', 'media_cost_usd']
        ):
            raise ValueError("Se requiere al menos un campo con valor")
        return values

class MediaCostUSD(BaseModel):
    no_of_days: Optional[int] = None
    approved_budget: Optional[float] = None
    ext_service_name: Optional[str] = None
    channel_name: Optional[str] = None
    weekday_cat_week: Optional[str] = None
    impressions: Optional[int] = None
    clicks: Optional[int] = None
    

    @model_validator(mode='after')
    def at_least_one_required(cls, values):
        if all(
            getattr(values, field) is None for field in ['no_of_days', 'approved_budget', 'ext_service_name', 'channel_name', 'weekday_cat', 'impressions', 'clicks']
        ):
            raise ValueError("Se requiere al menos un campo con valor")
        return values

class NoOfDays(BaseModel):
    clicks: Optional[int] = None
    impressions: Optional[int] = None
    approved_budget: Optional[float] = None
    ext_service_name_enc: Optional[int] = None
    channel_name_enc: Optional[int] = None
    weekday_cat_enc: Optional[int] = None
    media_cost_usd: Optional[float] = None

    @model_validator(mode='after')
    def at_least_one_required(cls, values):
        if all(
            getattr(values, field) is None for field in [
                'clicks', 'impressions', 'approved_budget',
                'ext_service_name_enc', 'channel_name_enc', 'weekday_cat_enc', 'media_cost_usd'
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
    media_cost_usd: Optional[float] = None

    @model_validator(mode='after')
    def at_least_one_required(cls, values):
        if all(
            getattr(values, field) is None for field in [
                'clicks', 'impressions', 'no_of_days',
                'ext_service_name_enc', 'channel_name_enc', 'weekday_cat_enc', 'media_cost_usd'
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