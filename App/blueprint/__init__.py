#file responsible for creating our app
from flask import Flask
from .extensions import ma, limiter, cache
from App.blueprint.members import members_bp
from .models import db #using relative path absoulute pathing will be (app.models)
from flask_swagger_ui import get_swaggerui_blueprint

SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
API_URL = '/static/swagger.yaml'  # Our API URL (can of course be a local resource)

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Your API's Name"
    }
)

def create_app(config_name): #Create the app
    New_app = Flask(__name__) #Initializes the app
    New_app.config.from_object(f'config.{config_name}')

#Adding extensions
    db.init_app(New_app) #adding our db extension to our app
    ma.init_app(New_app)
    limiter.init_app(New_app) #adds the limiter to your app
    cache.init_app(New_app)

#Registering Blueprint
    New_app.register_blueprint(members_bp, url_prefix="/members")
    New_app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL) #Registering our swagger blueprint
    return New_app