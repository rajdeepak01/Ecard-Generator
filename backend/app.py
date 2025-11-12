from flask import Flask
from application.config import LocalDevelopmentConfig
from application.database import db
from application.models import *
from application.security import jwt
from flask_cors import CORS

app = None

def create_app():
    app = Flask(__name__)
    app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)
    jwt.init_app(app)
    CORS(app)
    app.app_context().push()
    return app

app = create_app()  
from application.routes import *

if __name__ == "__main__":
    # db.create_all()
    # db.session.add(User(username="batman", email="admin@admin.com", password="1234", role="admin"))
    # db.session.add(User(username="panther", email="panther@user.com", password="12"))
    # db.session.commit()
    # print("Database Created successfully!!!!!")
    
    # table = UserCardDetails(attr_name="adhar", attr_val="22HE2R", cardname = "Adhar Card", user_id = 2)
    # db.session.add(table)
    # db.session.commit()
    # print("Data Created!")
    
    app.run()

