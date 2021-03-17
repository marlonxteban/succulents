from flask import Flask, request, jsonify, abort
from database.model import setup_db, Family, Succulent
from config import config
import json


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    setup_db(app)

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

    return app


app = create_app()

if __name__ == '__main__':
    app.run()
