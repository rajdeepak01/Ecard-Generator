from flask import current_app as app, jsonify, request, abort
from .models import *
from .database import db
from flask_jwt_extended import create_access_token, current_user, jwt_required
from functools import wraps
import random, string

def role_required(required_role):
    def wrapper(fn):
        @wraps(fn)
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
        return jsonify(message = "Wrong username or password"), 400
    
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
        return jsonify("User added successfully"), 201


#dashboard

@app.route("/api/dashboard") #bydefault method get so no need to mension
@jwt_required()
def dashboard():
    if current_user.role == "admin":
        users = len(User.query.filter_by(role = "user").all())
        card_requests = UserCardDetails.query.filter_by(attr_name = "status").all()
        requested = under_verification = verified = generated = 0
        card_request_json = []
        for detail in card_requests:
            detail_dict = {}
            detail_dict["username"] = detail.bearer.username
            detail_dict["cardname"] = detail.cardname
            detail_dict["status"]   = detail.attr_val

            if detail.attr_val == "requested":
                requested += 1
            if detail.attr_val == "under_verification":
                under_verification += 1
            if detail.attr_val == "verified":
                verified += 1
            if detail.attr_val == "generated":
                generated +=1
            card_request_json.append(detail_dict)

        return jsonify({
            "role" :current_user.role,
            "admin_name" : current_user.username,
            "users" : users,
            "card_requests" : requested,
            "under_verification" : under_verification,
            "verified" : verified,
            "card_generated" : generated,
            "available_cards" : 4,
            "card_requested_details" : card_request_json
        })
    else:
        user_card_details = UserCardDetails.query.filter_by(attr_name = "status", user_id = current_user.id).all()
        available_cards = []
        card_requests = []
        for detail in user_card_details:
            detail_dict = {}
            if detail.attr_val == "generated":
                detail_dict["cardname"] = detail.cardname
                available_cards.append(detail_dict)
            else:
                detail_dict["cardname"] = detail.cardname
                detail_dict["status"]   = detail.attr_val
                card_requests.append(detail_dict)
        return jsonify({
            "role" : current_user.role,
            "username" : current_user.username,
            "available_cards" : available_cards,
            "card_requests" : card_requests
        })   
@app.route("/api/generate/<string:cardname>/<int:user_id>")
@role_required("admin")
def generate(cardname, user_id):
    detail = UserCardDetails.query.filter_by(user_id = user_id, cardname = cardname, attr_name = "status").first()
    detail.attr_val = "generated"
    db.session.commit()

    key = ""
    if cardname == "aadhar":
        key = random.randint(10**11, 10**12-1)
    
    elif cardname == "pan":
        first_part = ''.join(random.choices(string.ascii_uppercase, k=5))
        middle_part = ''.join(random.choices(string.digits, k=2))
        last_part = ''.join(random.choices(string.digits, k = 7))
        key = first_part + "-" + middle_part + "-" + last_part
    
    elif cardname == "driving":
        part1 = ''.join(random.choice(string.ascii_uppercase, k = 2))
        part2 = ''.join(random.choices(string.digits, k=2))
        part3 = ''.join(random.choices(string.digits, k = 7))
        key = part1 + "-" + part2 + "-2025" + part3
    else:
        first_part = ''.join(random.choice(string.ascii_uppercase, k = 3))
        last_part = ''.join(random.choices(string.digits, k = 7))
        key = first_part + "-" + last_part
    
    usercarddetails1 = UserCardDetails(attr_name = "key", attr_val=key, cardname=cardname, user_id=current_user.id)
    db.session.add(usercarddetails1)
    db.session.commit()
    return {
        "message": f"{cardname} card created for user: {user_id}",
        "key" : key
    }

#user api

@app.route('/api/request/<string:cardname>', methods=["POST"])
@role_required("user")
def request_card(cardname):
    if cardname == "aadhar":
        fullname = request.json.get("fullname", None)
        dob = request.json.get("dob", None)
        address = request.json.get("address", None)
        gender = request.json.get("gender", None)
        ph = request.json.get("ph", None)

        attr1 = UserCardDetails(attr_name = "fullname", attr_val = fullname, cardname = cardname, user_id = current_user.id)
        attr2 = UserCardDetails(attr_name = "dob", attr_val = dob, cardname = cardname, user_id = current_user.id)
        attr3 = UserCardDetails(attr_name = "address", attr_val = address, cardname = cardname, user_id = current_user.id)
        attr4 = UserCardDetails(attr_name = "gender", attr_val = gender, cardname = cardname, user_id = current_user.id)
        attr5 = UserCardDetails(attr_name = "ph", attr_val = ph, cardname = cardname, user_id = current_user.id)
        attr6 = UserCardDetails(attr_name = "status", attr_val = "requested", cardname = cardname, user_id = current_user.id)

        db.session.add_all([attr1, attr2, attr3, attr4, attr5, attr6])
        db.session.commit()
    elif cardname == "pan":
        fullname = request.json.get("fullname", None)
        dob      = request.json.get("dob", None)
        ph       = request.json.get("ph", None)

        attr1 = UserCardDetails(attr_name = "fullname", attr_val = fullname, cardname=cardname, user_id = current_user.id)
        attr2 = UserCardDetails(attr_name = "dob", attr_val = dob, cardname = cardname, user_id = current_user.id)
        attr3 = UserCardDetails(attr_name = "ph", attr_val = ph, cardname = cardname, user_id = current_user.id)
        attr4 = UserCardDetails(attr_name = 'status', attr_val = "requested", cardname = cardname, user_id = current_user.id)

        db.session.add_all([attr1, attr2, attr3, attr4])
        db.session.commit()

    elif cardname == "voter":
        fullname = request.json.get("fullname", None)
        dob      = request.json.get("dob", None)
        ward     = request.json.get("ward", None)
        ph       = request.json.get("ph", None)

        attr1 = UserCardDetails(attr_name = "fullname", attr_val = fullname, cardname=cardname, user_id = current_user.id)
        attr2 = UserCardDetails(attr_name = "dob", attr_val = dob, cardname = cardname, user_id = current_user.id)
        attr3 = UserCardDetails(attr_name = "ph", attr_val = ph, cardname = cardname, user_id = current_user.id)
        attr4 = UserCardDetails(attr_name = "ward", attr_val = ward, cardname = cardname, user_id = current_user.id)
        attr5 = UserCardDetails(attr_name = 'status', attr_val = "requested", cardname = cardname, user_id = current_user.id)

        db.session.add_all(attr1, attr2, attr3, attr4, attr5)
        db.session.commit() 
    
    else:
        fullname = request.json.get("fullname", None)
        v_no      = request.json.get("dob", None)
        ph       = request.json.get("ph", None)

        attr1 = UserCardDetails(attr_name = "fullname", attr_val = fullname, cardname=cardname, user_id = current_user.id)
        attr2 = UserCardDetails(attr_name = "v_no", attr_val = v_no, cardname = cardname, user_id = current_user.id)
        attr3 = UserCardDetails(attr_name = "ph", attr_val = ph, cardname = cardname, user_id = current_user.id)
        attr4 = UserCardDetails(attr_name = 'status', attr_val = "requested", cardname = cardname, user_id = current_user.id)

        db.session.add_all(attr1, attr2, attr3, attr4)
        db.session.commit()
    return jsonify(message = f"requested for {cardname} made successfully!")