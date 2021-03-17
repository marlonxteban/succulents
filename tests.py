import os
import unittest
import json
import sys
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from database.model import db, setup_db, Family, Succulent


class SucculentsApiTests(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "succulents_test"
        self.database_path = "postgres://{}@{}/{}".format(
            'postgres:admin', 'localhost:5432', self.database_name)
        self.app.config["SQLALCHEMY_DATABASE_URI"] = self.database_path
        self.db = db
        setup_db(self.app)
        with self.app.app_context():
            #self.db = db
            #self.db.init_app(self.app)
            self.db.create_all()
            #import pdb; pdb.set_trace()
            self.populatedb(self.db)

    def tearDown(self):
        with self.app.app_context():
            # drop tables
            Succulent.__table__.drop(self.db.engine)
            Family.__table__.drop(self.db.engine)

    """
    Populate database with example data
    """

    def populatedb(self, db):
        family1 = Family(name="cactus", environment="hot",
                         weather="dry",
                         diferentiator="spikes")
        succulent1 = Succulent(name="cactus1", family_id=1, life_time=2)
        succulent2 = Succulent(name="cactus2", family_id=1, life_time=5)
        family2 = Family(name="burro's taik", environment="indoors",
                         weather="dry",
                         diferentiator="shape that resembles a tail")
        succulent3 = Succulent(name="burrito1", family_id=2, life_time=1)
        succulent4 = Succulent(name="burrote2", family_id=2, life_time=3)
        family3 = Family(name="araceaea", environment="tropic",
                         weather="various",
                         diferentiator="stores water until rainfall resumes")
        succulent5 = Succulent(name="zz", family_id=3, life_time=1)

        succulents1 = [succulent1, succulent2]
        succulents2 = [succulent3, succulent4]
        succulents3 = [succulent5]

        family1.succulents = succulents1
        family2.succulents = succulents2
        family3.succulents = succulents3

        try:
            db.session.add(family1)
            db.session.add(family2)
            db.session.add(family3)
            db.session.commit()
        except Exception:
            db.session.rollback()
            print(sys.exc_info())

    def test_get_families(self):
        response = self.client().get("/families")
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["total"], 3)
        self.assertTrue(lambda x: x["name"] ==
                        "cactus" in data["families"])


if __name__ == "__main__":
    unittest.main()
