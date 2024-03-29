from flask import current_app as app
from flask import render_template_string, request
from flask_security import hash_password

from app.models import db, user_datastore


@app.route("/")
def home():
    return render_template_string("Hello Home")


@app.post("/signup")
def signup():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    confirm_password = data.get("confirm_password")
    firstname = data.get("first_name")
    lastname = data.get("last_name")

    if password != confirm_password:
        return {"message": "Passwords do not match"}, 400

    user_datastore.create_user(
        email=email,
        password=hash_password(password),
        firstname=firstname,
        lastname=lastname,
        roles=["user"],
    )
    db.session.commit()
    return {"message": "User created successfully"}
