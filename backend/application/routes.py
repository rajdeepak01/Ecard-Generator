from flask import current_app as app, jsonify, request, abort
from .models import User
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

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    user = User.query.filter_by(username = username).one_or_none()
    if not user or not user.password:
        return jsonify("Wrong username or password"), 401
    
    access_tocken = create_access_token(identity=user)
    return jsonify(access_tocken=access_tocken)

# @app.route("/who_am_i", methods=['GET'])
# @jwt_required()
# def procted():
#     return jsonify(
#         id=current_user.id,
#         username=current_user.username,
#         password=current_user.password,
#         email=current_user.email,
#         role=current_user.role
#     )

#dashboard

@app.route('/dashboard')
@jwt_required()
def dashboard():
    if current_user.role == "admin":
        return "Welcome to admin dashboard"
    else:
        return "Welcome to User dashboard!"
    
@app.route("/onlyadmin")
@role_required("admin")
def admin_endpoint():
    return "Only admins are allowed"

def decorator_name():
    def wrapper(func):
        funct()
        return func
    return wrapper

@decorator_name()

def decorator_name(argument):
    def wrapper(func):
        def decor(*args, **kwargs)
            return func(*args, **kwargs)
        # aditional functionality
        return decor
    return wrapper

@decorator_name("argument")
