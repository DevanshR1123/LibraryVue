import numpy as np
import pandas as pd

from app.models import Book, Section, BookIssue, User, Rating, db


def is_valid_isbn(isbn):
    isbn = isbn.replace("-", "").replace(" ", "")
    if len(isbn) not in (10, 13):
        return False

    if len(isbn) == 10:
        try:
            digits = [int(x) if x.isdigit() else 10 for x in isbn]
            check_sum = sum(weight * digit for weight, digit in enumerate(digits[::-1], start=1))
            return check_sum % 11 == 0
        except ValueError:
            return False

    elif len(isbn) == 13:
        try:
            if not isbn.startswith("978"):
                return False
            digits = [int(x) if x.isdigit() else 10 for x in isbn]

            check_sum = sum((3 if weight % 2 else 1) * digit for weight, digit in enumerate(digits))
            return check_sum % 10 == 0
        except ValueError:
            return False

    return False


def get_books_data():
    books: list[Book] = Book.query.all()
    books_dict = [
        {
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "section": book.section.name,
            "year": book.year,
            "issued": book.issued,
            "total_issues": book.total_issues,
            "total_active_issues": book.total_active_issues,
        }
        for book in books
    ]
    df = pd.DataFrame(books_dict)
    return df


def get_sections_data():
    sections: list[Section] = Section.query.all()
    sections_dict = [
        {
            "id": section.id,
            "name": section.name,
            "total_books": len(section.books),
        }
        for section in sections
    ]
    df = pd.DataFrame(sections_dict)
    return df


def get_issues_data():
    issues: list[BookIssue] = BookIssue.query.all()
    issues_dict = [
        {
            "id": issue.id,
            "book_id": issue.book_id,
            "user_id": issue.user_id,
            "granted": issue.granted,
            "active": issue.active,
            "issue_date": issue.issue_date,
            "return_date": issue.return_date,
        }
        for issue in issues
    ]
    df = pd.DataFrame(issues_dict)
    df["issue_date"] = pd.to_datetime(df["issue_date"]).dt.strftime("%Y-%m-%d")
    df["return_date"] = pd.to_datetime(df["return_date"]).dt.strftime("%Y-%m-%d")
    return df
