from flask import Flask, request, jsonify, abort
from database.model import setup_db, Family, Succulent
from errors.processError import ProcessError
from flask_cors import CORS
from helpers import familyHelper
from config import config
import json


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    setup_db(app)

    """
    Cors config.
    """

    cors = CORS(app, resources={r"/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,PATCH,DELETE,OPTIONS')
        return response

    """
    Families endpoints
    """

    @app.route('/families')
    def get_families():
        families = Family.query.order_by(Family.id).all()
        return jsonify({
            "status_code": 200,
            "total": len(families),
            "success": True,
            "families": [family.format() for family in families]
        })

    @app.route('/families/<int:id>', methods=["DELETE"])
    def delete_family(id):

        family = Family.query.filter(Family.id == id).one_or_none()

        if not family:
            abort(404)

        if len(family.succulents):
            raise ProcessError({
                'code': 'related_succulents',
                'description':
                'There are succulents asociated with the family.'
            }, 422)

        try:
            family.delete()
            remaining_families = Family.query.count()
            remaining_succulents = Succulent.query.count()

            return jsonify({
                "success": True,
                "deleted": id,
                "remaining_families": remaining_families,
                "remaining_succulents": remaining_succulents
            })
        except Exception:
            abort(422)

    @app.route("/families", methods=["POST"])
    def create_family():
        body = request.get_json()
        # import pdb; pdb.set_trace()

        if not familyHelper.is_valid_family(body):
            raise ProcessError({
                'code': 'invalid_family',
                'description':
                'name and differentiator are required.'
            }, 400)

        name = body.get("name")
        environment = body.get("environment")
        weather = body.get("weather")
        differentiator = body.get("differentiator")

        try:
            last_family = Family.query.order_by(Family.id.desc()).first()
            new_family = Family(name=name,
                                environment=environment,
                                weather=weather,
                                diferentiator=differentiator)
            new_family.id = last_family.id + 1
            new_family.insert()
            total_families = Family.query.count()

            return jsonify({
                "status_code": 200,
                "success": True,
                "created": new_family.id,
                "total_families": total_families
            })
        except Exception:
            abort(422)

    """
    Succulents endpoints
    """

    @app.route('/succulents')
    def get_succulents():
        succulents = Succulent.query.order_by(Succulent.id).all()
        return jsonify({
            "status_code": 200,
            "total": len(succulents),
            "success": True,
            "succulents": [succulent.format()
                           for succulent in succulents]
        })

    @app.route('/succulents/<int:id>', methods=["DELETE"])
    def delete_succulent(id):

        succulent = Succulent.query.filter(Succulent.id == id).one_or_none()

        if not succulent:
            abort(404)

        try:
            succulent.delete()
            remaining_succulents = Succulent.query.count()

            return jsonify({
                "success": True,
                "deleted": id,
                "remaining_succulents": remaining_succulents
            })
        except Exception:
            abort(422)

    '''
    Error handlers.
    '''
    @app.errorhandler(ProcessError)
    def process_error(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error["description"]
        }), error.status_code

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    return app


app = create_app()

if __name__ == '__main__':
    app.run()
