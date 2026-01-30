from __future__ import annotations

from datetime import date
import os
from typing import Any

from flask import Flask, abort, redirect, render_template, request, url_for

app = Flask(__name__)

EVENTS: list[dict[str, Any]] = [
    {
        "slug": "hackforge-2026",
        "title": "HackForge 2026",
        "tagline": "48-hour hackathon for builders, designers, and problem-solvers.",
        "type": "Hackathon",
        "dates": "Feb 14–16, 2026",
        "venue": "Innovation Lab, Block C",
        "registration_deadline": "Feb 10, 2026",
        "registration_link": "https://example.com/register/hackforge-2026",
        "highlights": [
            "Team size: 2–4",
            "Tracks: AI, Web, Mobile, IoT, Open Innovation",
            "Prizes + internships for top teams",
        ],
        "rules": [
            "Bring a valid college ID for entry.",
            "Projects must be built during the hackathon window.",
            "External libraries/APIs are allowed; cite sources.",
            "No plagiarism or reuse of previously-built projects.",
            "Respect venue guidelines and code of conduct.",
        ],
        "coordinators": [
            {"name": "Aarav Mehta", "role": "Lead Coordinator", "phone": "+91 90000 00001", "email": "aarav.mehta@college.edu"},
            {"name": "Isha Sharma", "role": "Registrations", "phone": "+91 90000 00002", "email": "isha.sharma@college.edu"},
        ],
        "schedule": [
            {"day": "Day 1", "date": "Feb 14", "items": [
                {"time": "09:00", "title": "Check-in & Breakfast", "location": "Main Lobby"},
                {"time": "10:30", "title": "Opening Ceremony", "location": "Auditorium"},
                {"time": "11:30", "title": "Hacking Starts", "location": "Innovation Lab"},
                {"time": "18:30", "title": "Mentor Hours", "location": "Lab Floor"},
            ]},
            {"day": "Day 2", "date": "Feb 15", "items": [
                {"time": "09:30", "title": "Checkpoint Demos", "location": "Innovation Lab"},
                {"time": "13:00", "title": "Lunch", "location": "Cafeteria"},
                {"time": "19:00", "title": "Lightning Talks", "location": "Auditorium"},
            ]},
            {"day": "Day 3", "date": "Feb 16", "items": [
                {"time": "09:00", "title": "Submissions Deadline", "location": "Online"},
                {"time": "10:30", "title": "Final Presentations", "location": "Auditorium"},
                {"time": "13:30", "title": "Awards & Closing", "location": "Auditorium"},
            ]},
        ],
    },
    {
        "slug": "tech-talk-cloud-native",
        "title": "Tech Talk: Cloud-Native 101",
        "tagline": "A practical session on containers, CI/CD, and deployment basics.",
        "type": "Talk",
        "dates": "Mar 02, 2026",
        "venue": "Seminar Hall 2",
        "registration_deadline": "Feb 28, 2026",
        "registration_link": "https://example.com/register/cloud-native-101",
        "highlights": [
            "Live demos with Docker + GitHub Actions",
            "Q&A with industry speaker",
            "Certificate of participation",
        ],
        "rules": [
            "Seats are limited; registration is mandatory.",
            "Please arrive 10 minutes early.",
            "Maintain decorum during Q&A.",
        ],
        "coordinators": [
            {"name": "Riya Verma", "role": "Event Coordinator", "phone": "+91 90000 00003", "email": "riya.verma@college.edu"},
        ],
        "schedule": [
            {"day": "Session", "date": "Mar 02", "items": [
                {"time": "15:00", "title": "Welcome & Intro", "location": "Seminar Hall 2"},
                {"time": "15:15", "title": "Cloud-Native Concepts", "location": "Seminar Hall 2"},
                {"time": "16:10", "title": "Break", "location": "Outside Hall"},
                {"time": "16:20", "title": "CI/CD Demo", "location": "Seminar Hall 2"},
                {"time": "17:10", "title": "Q&A", "location": "Seminar Hall 2"},
            ]},
        ],
    },
]


def get_event(slug: str) -> dict[str, Any] | None:
    for e in EVENTS:
        if e["slug"] == slug:
            return e
    return None


@app.context_processor
def inject_globals() -> dict[str, Any]:
    today = date.today()
    return {"site_name": "Event Flow", "year": today.year}


@app.get("/")
def home() -> str:
    selected_slug = request.args.get("event")
    selected_event = get_event(selected_slug) if selected_slug else None
    return render_template("index.html", events=EVENTS, selected_event=selected_event)


@app.get("/event/<slug>")
def event_detail(slug: str) -> str:
    event = get_event(slug)
    if not event:
        abort(404)
    return redirect(url_for("home", event=slug) + "#event-details")


@app.errorhandler(404)
def not_found(_: Exception) -> tuple[str, int]:
    return render_template("404.html"), 404


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="127.0.0.1", port=port, debug=True)
