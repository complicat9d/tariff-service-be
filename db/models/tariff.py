import sqlalchemy as sa

from db.models import Base


class Tariff(Base):
    __tablename__ = "tariff"

    id = sa.Column(sa.Integer, primary_key=True)
    cargo_type = sa.Column(sa.String, nullable=False)
    rate = sa.Column(sa.Float, nullable=False)
    date = sa.Column(sa.Date, nullable=False)
