from flask import current_app as app
from flask import render_template_string, request, send_from_directory
from flask_security import (
    hash_password,
    login_required,
    roles_required,
    current_user,
    auth_required,
    permissions_accepted,
    roles_accepted,
)

from app.models import Book, db, user_datastore


@app.route("/")
def home():
    return render_template_string("Welcome to LibraryVue API")


@app.route("/test-api", methods=["GET", "POST", "PUT", "DELETE"])
@auth_required("token")
@roles_accepted("admin", "librarian")
def test_api():

    try:

        if request.method == "GET":
            print("Request args:", request.args)
        elif request.method == "POST":
            # print("Request data:", request.data)
            print("Request form:", request.form)
            # print("Request args:", request.args)
            # print("Request json:", request.json)
            print("Request files:", request.files)

            if request.files:
                file = request.files["file"]
                file.save(f"{app.config['IMAGE_DIR']}/{file.filename}")

    except Exception as e:
        print(e)

    # print(current_user)

    return {"message": "Test API"}


@app.get("/check-auth")
@auth_required("token")
def check_auth():
    return {"message": "Authenticated"}


@app.route("/books/content/<int:id>")
def get_book_content(id):
    book = Book.query.get_or_404(id, "Book not found")
    return send_from_directory(app.config["BOOKS_DIR"], book.content, as_attachment=True)


@app.route("/images/<path:filename>")
def get_image(filename):
    return send_from_directory(app.config["IMAGE_DIR"], filename)


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
