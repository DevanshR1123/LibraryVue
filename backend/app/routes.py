from flask import current_app as app, render_template_string, request
from flask_security import auth_required, hash_password
from app.models import db, user_datastore, Book


@app.route("/")
def home():
    return render_template_string("Hello Home")


@app.post("/book")
@auth_required("token")
def add_book():
    data = request.get_json()
    title = data.get("title")
    author = data.get("author")
    section_id = data.get("section_id")
    description = data.get("description")
    content = data.get("content")
    image = data.get("image")

    book = Book(
        title=title,
        author=author,
        section_id=section_id,
        description=description,
        content=content,
        image=image,
    )
    db.session.add(book)
    db.session.commit()
    return {"message": "Book added successfully"}


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
