from flask import Blueprint

ajax = Blueprint('ajax', __name__)

from . import views
