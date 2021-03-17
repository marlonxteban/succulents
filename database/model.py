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

    def __init__(self, name, environment, weather, diferentiator):
        self.name = name
        self.environment = environment
        self.weather = weather
        self.differentiator = diferentiator

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'environment': self.environment,
            'weather': self.weather,
            'differentiator': self.differentiator
        }


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

    def __init__(self, name, family_id, life_time):
        self.name = name
        self.family_id = family_id
        self.life_time = life_time

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'family_id': self.family_id,
            'life_time': self.life_time,
        }
