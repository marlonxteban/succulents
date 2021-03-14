from flask import Flask, request, jsonify, abort
from .database.model import setup_db
from .config import config
import json

app = Flask(__name__)
app.config.from_object(config)
setup_db(app)


if __name__ == '__main__':
    app.run()
