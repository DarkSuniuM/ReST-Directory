from flask import Blueprint

sites = Blueprint('sites', __name__, url_prefix='/sites/')

from . import views