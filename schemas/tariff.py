from pydantic import BaseModel
import datetime


class TariffBaseSchema(BaseModel):
    cargo_type: str
    date: datetime.date


class TariffSchema(TariffBaseSchema):
    rate: float


class TariffCreateSchema(TariffSchema):
    pass


class TariffUpdateSchema(BaseModel):
    cargo_type: str
    date: datetime.date
    new_rate: float


class TariffDeleteSchema(TariffBaseSchema):
    pass


class InsuranceCalculationSchema(TariffBaseSchema):
    value: float
