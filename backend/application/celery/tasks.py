import os
from datetime import datetime, timedelta

import pandas as pd
import numpy as np
import seaborn as sb
import matplotlib.pyplot as plt

from application.celery.celery import celery
from application.models import Book, Section, User
from application.utils import get_books_data, get_issues_data

from celery.schedules import crontab
from flask import current_app as app

GRAPH_DIR = app.config["GRAPH_DIR"]


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Clean files every 24 hours
    sender.add_periodic_task(crontab(minute=0, hour=0), clean_files.s(), name="clean-files")

    # Notify user every 24 hours
    sender.add_periodic_task(crontab(minute=0, hour=12), notify_user.s(), name="notify-user")

    # Generate report every month
    sender.add_periodic_task(crontab(minute=0, hour=0, day_of_month=1), generate_report.s(), name="generate-report")

    # Generate graph every hour
    sender.add_periodic_task(crontab(minute=0), generate_graph.s(), name="generate-graph")


# Create a Celery task
@celery.task
def clean_files():
    book_images = Book.query.with_entities(Book.image).all()
    book_images = [image[0] for image in book_images]
    book_images = set(book_images)

    book_content = Book.query.with_entities(Book.content).all()
    book_content = [content[0] for content in book_content]
    book_content = set(book_content)

    section_images = Section.query.with_entities(Section.image).all()
    section_images = [image[0] for image in section_images]
    section_images = set(section_images)

    image_dir = app.config["IMAGE_DIR"]
    books_dir = app.config["BOOKS_DIR"]

    cleaned_files = 0

    for file in os.listdir(image_dir):
        if file not in book_images and file not in section_images:
            os.remove(os.path.join(image_dir, file))
            cleaned_files += 1

    for file in os.listdir(books_dir):
        if file not in book_content:
            os.remove(os.path.join(books_dir, file))
            cleaned_files += 1

    print(f"Cleaned {cleaned_files} files")

    return cleaned_files


@celery.task
def notify_user():
    users: list[User] = User.query.filter(
        User.login_count.is_not(None), User.current_login_at.is_not(None), User.roles.any(name="user")
    ).all()
    now = datetime.now()
    for user in users:
        if (user.current_login_at is not None) and (now - user.current_login_at).days >= 1:
            print(f"Sending notification to {user.email} with id {user.current_login_at }")
            # Send notification
    return "Notification sent"


@celery.task
def generate_report():
    for user in User.query.filter(User.roles.any(name="user")).all():
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
        }

        sections = books_data["section"].value_counts().to_frame()

        top_5_most_issued_sections = (
            books_data["section"].value_counts().reset_index().sort_values("count", ascending=False).head(5)
        )
        top_5_most_issued_books = (
            books_data["title"].value_counts().reset_index().sort_values("count", ascending=False).head(5)
        )

        report = f"""
User report for {user.full_name}:

Total issues: {stats["total_issues"]}
Total books: {stats["total_books"]}
Total sections: {stats["total_sections"]}

Explored sections:
{sections}

Top 5 most issued sections:
{top_5_most_issued_sections}

Top 5 most issued books: 
{top_5_most_issued_books}

"""
        print(report)
        # Send report to user


@celery.task
def generate_graph():
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
    plt.savefig(f"{GRAPH_DIR}/by_section_book_count.png")

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
    plt.savefig(f"{GRAPH_DIR}/by_section_active_issue_count.png")

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
    plt.savefig(f"{GRAPH_DIR}/by_section_total_issue_count.png")

    issues = get_issues_data()
    min_date = issues["date_issued"].min()
    max_date = issues["date_issued"].max()
    plt.figure(figsize=(8, 6))
    sb.lineplot(
        data=issues,
        x="date_issued",
        y="total_issues",
        palette="tab10",
        legend=False,
    )
    plt.title("Number of issues per day")
    plt.ylabel("Number of issues")
    plt.xticks(np.arange(min_date, max_date, timedelta(days=7)), rotation=90)
    plt.tight_layout()
    plt.savefig(f"{GRAPH_DIR}/issues_time_series.png")

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
    plt.savefig(f"{GRAPH_DIR}/by_year.png")

    plt.figure(figsize=(8, 6))
    sb.countplot(
        data=books[books["total_active_issues"] > 0],
        x="year",
        palette="tab10",
        hue="year",
        legend=False,
    )
    plt.title("Number of active issues per year")
    plt.ylabel("Number of books")
    plt.tight_layout()
    plt.savefig(f"{GRAPH_DIR}/by_year_active_issues.png")
