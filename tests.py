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
        self.owner_token = os.getenv('OWNER_TOKEN')
        self.collaborator_token = os.getenv('COLLABORATOR_TOKEN')
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

    def get_bearer_header(self, token):
        return {'Authorization': f"Bearer {token}"}

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

    def test_get_succulent_family(self):
        expected_name = "burro's taik"
        response = self.client().get("/families/2")
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data["success"])
        self.assertEqual(data["family"]["name"], expected_name)

    def test_404_not_existing_family_detail(self):
        error_message = "resource not found"
        response = self.client().get("/families/3000")
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertFalse(data["success"])
        self.assertEqual(error_message, data["message"])

    def test_422_delete_family_with_succulents(self):
        header = self.get_bearer_header(self.owner_token)
        error_message = "There are succulents asociated with the family."
        response = self.client().delete("/families/1", headers=header)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 422)
        self.assertFalse(data["success"])
        self.assertEqual(error_message, data["message"])

    def test_404_delete_not_existing_family(self):
        header = self.get_bearer_header(self.owner_token)
        error_message = "resource not found"
        response = self.client().delete("/families/1000", headers=header)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertFalse(data["success"])
        self.assertEqual(error_message, data["message"])

    def test_delete_family(self):
        header = self.get_bearer_header(self.owner_token)
        response = self.client().delete("/families/4", headers=header)
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
        header = self.get_bearer_header(self.owner_token)
        response = self.client().post("/families",
                                      headers=header,
                                      json=new_family)
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
        header = self.get_bearer_header(self.owner_token)
        response = self.client().post("/families",
                                      headers=header,
                                      json=new_family)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertFalse(data["success"])
        self.assertEqual(error_message, data["message"])

    def test_404_update_non_existing_family(self):
        new_family = {
            "name": "super family",
            "environment": "wet",
            "weather": "rainy",
            "differentiator": "super plants"
        }
        header = self.get_bearer_header(self.owner_token)
        response = self.client().patch("/families/100",
                                       headers=header,
                                       json=new_family)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertFalse(data["success"])

    def test_update_family(self):
        updated_name = "super updated family"
        updated_family = {
            "name": updated_name,
            "differentiator": "super updated plants"
        }
        header = self.get_bearer_header(self.owner_token)
        response = self.client().patch("/families/4",
                                       headers=header,
                                       json=updated_family)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["updated"]["name"], updated_name)

    def test_404_get_succulents_by_family(self):
        response = self.client().get("/families/1000/succulents")
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertFalse(data["success"])

    def test_get_succulents_by_family(self):
        family_id = 2
        response = self.client().get(f"/families/{family_id}/succulents")
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data["success"])
        self.assertEqual(data["family_id"], family_id)
        self.assertEqual(data["total_succulents"], 2)
        self.assertTrue(lambda x: x["name"] ==
                        "burrote2" in data["succulents"])
        self.assertTrue(lambda x: x["name"] ==
                        "burrito1" in data["succulents"])

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

    def test_get_succulent_detail(self):
        header = self.get_bearer_header(self.collaborator_token)
        expected_name = "burrito1"
        response = self.client().get("/succulents/3", headers=header)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data["success"])
        self.assertEqual(data["succulent"]["name"], expected_name)

    def test_404_not_existing_succulent_detail(self):
        error_message = "resource not found"
        header = self.get_bearer_header(self.collaborator_token)
        response = self.client().get("/succulents/3000", headers=header)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertFalse(data["success"])
        self.assertEqual(error_message, data["message"])

    def test_404_delete_not_existing_succulent(self):
        error_message = "resource not found"
        header = self.get_bearer_header(self.owner_token)
        response = self.client().delete("/succulents/1000", headers=header)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertFalse(data["success"])
        self.assertEqual(error_message, data["message"])

    def test_delete_succulent(self):
        header = self.get_bearer_header(self.owner_token)
        response = self.client().delete("/succulents/5", headers=header)
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
        header = self.get_bearer_header(self.collaborator_token)
        response = self.client().post("/succulents",
                                      headers=header,
                                      json=new_succulent)
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
        header = self.get_bearer_header(self.collaborator_token)
        response = self.client().post("/succulents",
                                      headers=header,
                                      json=new_family)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertFalse(data["success"])
        self.assertEqual(error_message, data["message"])

    def test_404_update_non_existing_succulent(self):
        new_succulent = {
            "name": "super succulent"
        }
        header = self.get_bearer_header(self.collaborator_token)
        response = self.client().patch("/succulents/100",
                                       headers=header,
                                       json=new_succulent)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertFalse(data["success"])

    def test_update_succulent(self):
        updated_name = "super updated succulent"
        updated_succulent = {
            "name": updated_name,
            "life_time": 9
        }
        header = self.get_bearer_header(self.collaborator_token)
        response = self.client().patch("/succulents/5",
                                       headers=header,
                                       json=updated_succulent)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["updated"]["name"], updated_name)
        self.assertEqual(data["updated"]["life_time"], 9)

    """
    RBAC tests role: collaborator
    """

    def test_collabotator_can_not_delete_succulent(self):
        error_message = "Permission not found."
        header = self.get_bearer_header(self.collaborator_token)
        response = self.client().delete("/succulents/1000", headers=header)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 403)
        self.assertFalse(data["success"])
        self.assertEqual(error_message, data["message"])

    def test_collaborator_can_not_create_family(self):
        error_message = "Permission not found."
        new_family = {
            "name": "super family",
            "environment": "wet",
            "weather": "rainy",
            "differentiator": "super plants"
        }
        header = self.get_bearer_header(self.collaborator_token)
        response = self.client().post("/families",
                                      headers=header,
                                      json=new_family)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 403)
        self.assertFalse(data["success"])
        self.assertEqual(error_message, data["message"])

    """
    RBAC tests role: owner
    """

    def test_owner_can_update_succulent(self):
        updated_name = "super updated succulent"
        updated_succulent = {
            "name": updated_name,
            "life_time": 9
        }
        header = self.get_bearer_header(self.owner_token)
        response = self.client().patch("/succulents/5",
                                       headers=header,
                                       json=updated_succulent)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["updated"]["name"], updated_name)
        self.assertEqual(data["updated"]["life_time"], 9)

    def test_owner_can_create_succulent(self):
        new_succulent = {
            "name": "super succulent",
            "family_id": 2,
            "life_time": 3,
        }
        header = self.get_bearer_header(self.owner_token)
        response = self.client().post("/succulents",
                                      headers=header,
                                      json=new_succulent)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data["success"])
        self.assertTrue(data["total_succulents"], 6)
        self.assertEqual(data["created"], 6)


if __name__ == "__main__":
    unittest.main()
