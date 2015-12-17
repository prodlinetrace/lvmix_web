from flask import Blueprint

variants = Blueprint('variants', __name__)

from . import routes
