import pandas as pd

from application.models import Book, User, db, user_datastore
from application.utils import get_books_data, get_issues_data
from application.cache import cache
from application.celery.tasks import generate_graph, notify_user, generate_report, clean_files

from flask import current_app as app
from flask import render_template_string, request, send_file, send_from_directory
from flask_security import (
    auth_required,
    current_user,
    hash_password,
    roles_accepted,
)

GRAPH_DIR = app.config["GRAPH_DIR"]


@app.route("/")
def home():
    return render_template_string("Welcome to LibraryVue API")


@app.route("/tasks/generate-graph")
def generate_graph_task():
    generate_graph.delay()
    return {"message": "Generate graph task scheduled"}


@app.route("/tasks/notify-user")
def notify_user_task():
    notify_user.delay()
    return {"message": "Notify user task scheduled"}


@app.route("/tasks/generate-report")
def generate_report_task():
    generate_report.delay()
    return {"message": "Generate report task scheduled"}


@app.route("/tasks/clean-files")
def clean_files_task():
    clean_files.delay()
    return {"message": "Clean files task scheduled"}


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


@app.route("/books/<int:id>/content")
def get_book_content(id):
    book = Book.query.get_or_404(id, "Book not found")
    return send_file(f'{app.config["BOOKS_DIR"]}/{book.content}')


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


@app.get("/graph/<graph_name>")
def graph_by_section(graph_name):
    return send_from_directory(GRAPH_DIR, f"{graph_name}.png")


@auth_required("token")
@roles_accepted("admin", "librarian")
@app.get("/stats/library")
@cache.cached(timeout=60)
def stats():
    books = get_books_data()

    stats = {
        "total_users": User.query.filter(User.roles.any(name="user")).count(),
        "total_books": books.shape[0],
        "total_issued": books[books["issued"]].shape[0],
        "total_sections": books["section"].nunique(),
        "total_years": books["year"].nunique(),
        "sections": books["section"].value_counts().to_dict(),
        "years": books["year"].value_counts().to_dict(),
        "issued_books": books[books["issued"]]["section"].value_counts().to_dict(),
        "percentage_issued": books["issued"].mean() * 100,
        "top_5_most_issued_sections": books.groupby("section")["total_issues"]
        .sum()
        .nlargest(5)
        .reset_index()
        .to_dict(orient="records"),
        "top_5_most_issued_books": books.sort_values("total_issues", ascending=False)
        .head(5)[["title", "total_issues"]]
        .to_dict(orient="records"),
    }

    return stats


@auth_required("token")
@roles_accepted("user")
@app.get("/stats/user")
def user_stats():
    user = User.query.get(current_user.id)
    user_books = [issue.book for issue in user.all_issues]

    books_data = pd.DataFrame(
        [
            {
                "id": book.id,
                "title": book.title,
                "author": book.author,
                "section": book.section.name,
                "year": book.year,
            }
            for book in user_books
        ],
        columns=["id", "title", "author", "section", "year"],
    )

    stats = {
        "total_issues": len(user.active_issues),
        "total_books": len(set([issue.book.id for issue in user.all_issues])),
        "total_sections": len(set([issue.book.section.name for issue in user.all_issues])),
        "sections": books_data["section"].value_counts().to_dict(),
        "top_5_most_issued_sections": books_data["section"]
        .value_counts()
        .reset_index()
        .sort_values("count", ascending=False)
        .head(5)
        .to_dict(orient="records"),
        "top_5_most_issued_books": books_data["title"]
        .value_counts()
        .reset_index()
        .sort_values("count", ascending=False)
        .head(5)
        .to_dict(orient="records"),
    }

    print(stats)

    return stats
