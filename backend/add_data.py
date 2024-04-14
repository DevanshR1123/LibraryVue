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

print("Books added")

sections = get("http://localhost:5000/sections").json()
books = get("http://localhost:5000/books").json()

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

for user in users:
    user_data = get_user(user["email"], user["password"])
    user["id"] = user_data["id"]
    user["token"] = user_data["authentication_token"]
