import sqlalchemy as sa

from db.models import Base


class Tariff(Base):
    __tablename__ = "tariff"

    cargo_type = sa.Column(sa.String, nullable=False)
    date = sa.Column(sa.Date, nullable=False)
    rate = sa.Column(sa.Float, nullable=False)

    __table_args__ = (sa.PrimaryKeyConstraint(cargo_type, date),)
