from flask import current_app as app, jsonify, request, abort
from .models import *
from .database import db
from flask_jwt_extended import create_access_token, current_user, jwt_required

def role_required(required_role):
    def wrapper(fn):
        @jwt_required()
        def decorator(*args, **kwargs):
            if current_user.role != required_role:
                return jsonify(message = "Youre not authorized"), 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper

@app.route('/api/login', methods=['POST'])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    user = User.query.filter_by(username = username).one_or_none()
    if not user or not user.password == password:
        return jsonify("Wrong username or password"), 401
    
    access_tocken = create_access_token(identity=user)
    return jsonify(access_tocken=access_tocken)

@app.route("/api/register", methods=['POST'])
def register():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    email    = request.json.get('email', None)

    this_user = User.query.filter_by(username=username).first()

    if this_user:
        return jsonify("User already exist"), 400
    else:
        user = User(username=username, password=password, email=email)
        db.session.add(user)
        db.session.commit()
        return jsonify("User added successfully")

@app.route("/api/user_home")
@role_required('user')
def user_home():

    card_details = UserCardDetails.query.filter_by(user_id = current_user.id).all()
    card_json = []
    for card in card_details:
        card_dict = {}
        card_dict["atr_name"] = card.attr_name
        card_dict['attr_val'] = card.attr_val
        card_dict['cardname'] = card.cardname
        card_json.append(card_dict)

    return jsonify(card_json)

@app.route("/api/request/<cardname>", methods = ['POST'])
@jwt_required()
def requested_card(cardname):
    if cardname == "aadhar":
        pass
    elif cardname == "pan":
        fullname = request.json.get("fullname", None)
        dob = request.json.get("dob", None)
        ph = request.json.get("ph", None)
        en1 = UserCardDetails(attr_name = "fullname", attr_val = fullname, cardname = cardname, user_id = current_user.id)
        en2 = UserCardDetails(attr_name = "dob", attr_val = dob, cardname = cardname, user_id = current_user.id)
        en3 = UserCardDetails(attr_name = "ph", attr_val = ph, cardname = cardname, user_id = current_user.id)
        db.session.ad
    elif cardname == "voter":
        pass
    elif cardname == "driving":
        pass


#dashboard

# @app.route('/dashboard')
# @jwt_required()
# def dashboard():
#     if current_user.role == "admin":
#         return "Welcome to admin dashboard"
#     else:
#         return "Welcome to User dashboard!"
    
# @app.route("/onlyadmin")
# @role_required("admin")
# def admin_endpoint():
#     return "Only admins are allowed"

# def decorator_name():
#     def wrapper(func):
#         funct()
#         return func
#     return wrapper

# @decorator_name()

# def decorator_name(argument):
#     def wrapper(func):
#         def decor(*args, **kwargs)
#             return func(*args, **kwargs)
#         # aditional functionality
#         return decor
#     return wrapper

# @decorator_name("argument")
