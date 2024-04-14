from operator import le
import pandas as pd
import numpy as np
from requests import get, post


books_data = pd.read_csv("data/books.csv")
sections_data = pd.read_csv("data/sections.csv")


def get_user(email, password):
    return post(
        "http://localhost:5000/login?include_auth_token",
        json={"email": email, "password": password},
        headers={"Content-Type": "application/json"},
    ).json()["response"]["user"]


def get_token(email, password):
    return get_user(email, password)["authentication_token"]


admin = {
    "email": "library.admin@example.com",
    "password": "password",
}

librarian = {
    "email": "the.librarian@example.com",
    "password": "password",
}

users = [
    {
        "email": "alice.user@example.com",
        "password": "password",
    },
    {
        "email": "bob.user@example.com",
        "password": "password",
    },
    {
        "email": "charlie.user@example.com",
        "password": "password",
    },
]

token = get_token(admin["email"], admin["password"])

sections_to_id = {}


for s, d in sections_data.itertuples(index=False):
    res = post(
        "http://localhost:5000/sections",
        headers={"Authentication-Token": token},
        files={"image": open(f"data/Sections/{s}.jpeg", "rb")},
        data={"name": s, "description": d},
    )
    sections_to_id[s] = res.json()["id"]

    if "message" in res.json():
        print(res.json()["message"])

print("Sections added")
for image, pdf, title, description, author, section, year, isbn in books_data.itertuples(index=False):
    res = post(
        "http://localhost:5000/books",
        headers={"Authentication-Token": token},
        files={"image": open(f"data/Covers/{image}.jpeg", "rb"), "content": open(f"data/Books/{pdf}.pdf", "rb")},
        data={
            "title": title,
            "description": description,
            "author": author,
            "section_id": sections_to_id[section],
            "year": year,
            "isbn": isbn,
        },
    )

    if "message" in res.json():
        print(res.json()["message"])

print("Books added")

sections = get("http://localhost:5000/sections").json()
books = get("http://localhost:5000/books").json()


issue_requests = []

for user in users:
    user_data = get_user(user["email"], user["password"])
    user["id"] = user_data["id"]
    user["token"] = user_data["authentication_token"]

    issued_books = np.random.choice(books, 5, replace=False)
    for book in issued_books:
        issue = post(
            f"http://localhost:5000/issues/{book['id']}",
            headers={"Authentication-Token": user["token"]},
        ).json()
        issue_requests.append(issue)
        if "message" in issue:
            print(issue["message"])

    print("Issue requests added", len(issued_books), user["email"])

    ratings = np.random.randint(1, 6, len(books))
    for book, rating in zip(books, ratings):
        post(
            f"http://localhost:5000/ratings/{book['id']}",
            headers={"Authentication-Token": user["token"], "Content-Type": "application/json"},
            json={"rating": int(rating)},
        )

print("User data added")


librarian["id"] = get_user(librarian["email"], librarian["password"])["id"]
librarian["token"] = get_token(librarian["email"], librarian["password"])

approve_issues = np.random.choice(issue_requests, 10, replace=False)
print("Approving issues", len(approve_issues))
for issue in approve_issues:
    approve = post(
        f"http://localhost:5000/librarian/issues/{issue['id']}",
        headers={"Authentication-Token": librarian["token"]},
    )

    if "message" in approve.json():
        print(approve.json()["message"])

print("Issues approved")


print("Data added successfully")
