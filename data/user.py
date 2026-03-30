import sqlalchemy
from .db_session import SqlAlchemyBase
from flask_login import UserMixin
from sqlalchemy import orm, Column


class User(UserMixin, SqlAlchemyBase):
    __tablename__ = 'user'
    id = Column(sqlalchemy.Integer, primary_key=True)
    username = Column(sqlalchemy.String, unique=True)
    email = Column(sqlalchemy.String, unique=True)
    password = Column(sqlalchemy.String)
    places = orm.relationship('Places', back_populates='user')
