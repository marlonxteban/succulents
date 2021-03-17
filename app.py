from flask import Flask, request, jsonify, abort
from database.model import setup_db, Family, Succulent
from flask_cors import CORS
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

    '''
    Error handlers.
    '''
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
