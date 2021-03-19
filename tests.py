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
            self.db.create_all()
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
        family4 = Family(name="test one", environment="test",
                         weather="all",
                         diferentiator="this family will die")

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
            db.session.add(family4)
            db.session.commit()
        except Exception:
            db.session.rollback()
            print(sys.exc_info())

    """
    Families endpoints tests
    """

    def test_get_families(self):
        response = self.client().get("/families")
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["total"], 4)
        self.assertTrue(lambda x: x["name"] ==
                        "burrito1" in data["families"])
        # print(list(data["families"]))

    def test_422_delete_family_with_succulents(self):
        error_message = "There are succulents asociated with the family."
        response = self.client().delete("/families/1")
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 422)
        self.assertFalse(data["success"])
        self.assertEqual(error_message, data["message"])

    def test_404_delete_not_existing_family(self):
        error_message = "resource not found"
        response = self.client().delete("/families/1000")
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertFalse(data["success"])
        self.assertEqual(error_message, data["message"])

    def test_delete_family(self):
        response = self.client().delete("/families/4")
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["deleted"], 4)
        self.assertEqual(data["remaining_families"], 3)
        self.assertEqual(data["remaining_succulents"], 5)

    def test_create_family(self):
        new_family = {
            "name": "super family",
            "environment": "wet",
            "weather": "rainy",
            "differentiator": "super plants"
        }

        response = self.client().post("/families", json=new_family)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data["success"])
        self.assertTrue(data["total_families"], 5)
        self.assertEqual(data["created"], 5)

    def test_400_missing_differentiator(self):
        error_message = "name and differentiator are required."
        new_family = {
            "name": "super family 2",
            "environment": "wet",
            "weather": "rainy",
        }

        response = self.client().post("/families", json=new_family)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertFalse(data["success"])
        self.assertEqual(error_message, data["message"])

    """
    Succulents endpoints tests
    """

    def test_get_succulents(self):
        response = self.client().get("/succulents")
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["total"], 5)
        self.assertTrue(lambda x: x["name"] ==
                        "cactus" in data["succulents"])
        # print(list(data["succulents"]))

    def test_404_delete_not_existing_succulent(self):
        error_message = "resource not found"
        response = self.client().delete("/succulents/1000")
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertFalse(data["success"])
        self.assertEqual(error_message, data["message"])

    def test_delete_succulent(self):
        response = self.client().delete("/succulents/5")
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["deleted"], 5)
        self.assertEqual(data["remaining_succulents"], 4)

    def test_create_succulent(self):
        new_succulent = {
            "name": "super succulent",
            "family_id": 2,
            "life_time": 3,
        }

        response = self.client().post("/succulents", json=new_succulent)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data["success"])
        self.assertTrue(data["total_succulents"], 6)
        self.assertEqual(data["created"], 6)

    def test_400_missing_name(self):
        error_message = "name and family_id are required."
        new_family = {
            "family_id": 2,
            "life_time": 3,
        }

        response = self.client().post("/succulents", json=new_family)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertFalse(data["success"])
        self.assertEqual(error_message, data["message"])


if __name__ == "__main__":
    unittest.main()
