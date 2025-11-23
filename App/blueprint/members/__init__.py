#blueprint/members/init,py
from flask import Blueprint

members_bp = Blueprint('members_bp', __name__)
from . import routes #always do it underneath the declaration