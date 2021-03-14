from sqlalchemy import Column, String, Integer, create_engine
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import json

db = SQLAlchemy()


def setup_db(app):
    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db)


class Family(db.Model):
    __tablename__ = 'families'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    environment = Column(String, nullable=True)
    weather = Column(String, nullable=True)
    differentiator = Column(String, nullable=False)


class Succulent(db.Model):
    __tablename__ = 'succulents'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    family_id = Column(Integer,
                       db.ForeignKey('families.id', ondelete='CASCADE'))
    life_time = Column(Integer, nullable=True)
    family = db.relationship('Family',
                             backref=db.backref('succulents'),
                             lazy=True)
