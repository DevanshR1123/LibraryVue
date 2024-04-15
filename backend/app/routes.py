import matplotlib.pyplot as plt
import pandas as pd
from requests import get
import seaborn as sb

from app.models import Book, User, db, user_datastore
from app.utils import get_books_data, get_issues_data, get_sections_data

from flask import current_app as app
from flask import render_template_string, request, send_file, send_from_directory
from flask_security import (
    auth_required,
    current_user,
    hash_password,
    roles_accepted,
    roles_required,
)

GRAPH_DIR = app.config["GRAPH_DIR"]


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


@app.get("/graph/by-section/book-count")
def graph_by_section():
    books = get_books_data()
    plt.figure(figsize=(8, 6))
    sb.countplot(
        data=books,
        x="section",
        order=books["section"].value_counts().index,
        palette="tab10",
        hue="section",
        legend=False,
    )
    plt.title("Number of books per section")
    plt.ylabel("Number of books")
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig(f"{GRAPH_DIR}/graph_by_section.png")
    return send_file(f"{GRAPH_DIR}/graph_by_section.png")


@app.get("/graph/by-section/active-issue-count")
def graph_by_section_active_issue_count():
    books = get_books_data()
    plt.figure(figsize=(8, 6))
    sb.countplot(
        data=books[books["total_active_issues"] > 0],
        x="section",
        order=books[books["total_active_issues"] > 0]["section"].value_counts().index,
        palette="tab10",
        hue="section",
        legend=False,
    )
    plt.title("Number of active issues per section")
    plt.ylabel("Number of books")
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig(f"{GRAPH_DIR}/graph_by_section.png")
    return send_file(f"{GRAPH_DIR}/graph_by_section.png")


@app.get("/graph/by-section/total-issue-count")
def graph_by_section_total_issue_count():
    books = get_books_data()
    plt.figure(figsize=(8, 6))
    sb.countplot(
        data=books[books["total_issues"] > 0],
        x="section",
        order=books[books["total_issues"] > 0]["section"].value_counts().index,
        palette="tab10",
        hue="section",
        legend=False,
    )
    plt.title("Number of total issues per section")
    plt.ylabel("Number of books")
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig(f"{GRAPH_DIR}/graph_by_section.png")
    return send_file(f"{GRAPH_DIR}/graph_by_section.png")


@app.get("/graph/issues/time-series")
def graph_issues_time_series():
    issues = get_issues_data()
    plt.figure(figsize=(8, 6))
    sb.countplot(
        data=issues,
        x="issue_date",
        palette="tab10",
        hue="issue_date",
        legend=False,
    )
    plt.title("Number of issues per day")
    plt.ylabel("Number of issues")
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig(f"{GRAPH_DIR}/graph_issues_time_series.png")
    return send_file(f"{GRAPH_DIR}/graph_issues_time_series.png")


@app.get("/graph/by-year")
def graph_by_year():
    books = get_books_data()
    plt.figure(figsize=(8, 6))
    sb.countplot(
        data=books,
        x="year",
        palette="tab10",
        hue="year",
        legend=False,
    )
    plt.title("Number of books per year")
    plt.ylabel("Number of books")
    plt.tight_layout()
    plt.savefig(f"{GRAPH_DIR}/graph_by_year.png")
    return send_file(f"{GRAPH_DIR}/graph_by_year.png")


@app.get("/stats")
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
        "top_5_most_issued_sections": books.groupby("section")["total_issues"].sum().nlargest(5).to_dict(),
        "top_5_most_issued_books": books.sort_values("total_issues", ascending=False)
        .head(5)[["title", "total_issues"]]
        .to_dict(orient="records"),
    }
    return stats
