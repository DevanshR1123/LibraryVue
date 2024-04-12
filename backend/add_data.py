import pandas as pd
import numpy as np
from requests import get, post


books_data = pd.read_csv("data/books.csv")
sections_data = pd.read_csv("data/sections.csv")

admin = {
    "email": "test.admin@example.com",
    "password": "password",
}

res = post("http://localhost:5000/login?include_auth_token", json=admin, headers={"Content-Type": "application/json"})
user = res.json()
token = user["response"]["user"]["authentication_token"]

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
