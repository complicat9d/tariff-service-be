import sqlalchemy as sa

from db.models import Base


class User(Base):
    __tablename__ = "user"

    id = sa.Column(sa.Integer, primary_key=True)
    username = sa.Column(sa.String, nullable=False, unique=True)
    password = sa.Column(sa.String, nullable=False)
