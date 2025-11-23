from App.blueprint import create_app
from App.blueprint.models import db 

#call the development section
New_app = create_app('DevelopmentConfig')

#Create the table
with New_app.app_context():
    db.create_all()

New_app.run()
