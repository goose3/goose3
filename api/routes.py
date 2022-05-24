from flask import Blueprint
from .views import extract, health_check, redis_health_check, temproute

# set method as endpoint

# Create the blueprint for this app
api = Blueprint("api", __name__, url_prefix="/api")

# Add the view as route; methods like GET, POST, PUT will automatically route to class methods with parameters
api.add_url_rule("extract.json", view_func=extract, methods=["GET"])
api.add_url_rule("health", view_func=health_check, methods=["GET"])
api.add_url_rule("redis", view_func=redis_health_check, methods=["GET"])
api.add_url_rule("ping", view_func=temproute, methods=["GET"])
