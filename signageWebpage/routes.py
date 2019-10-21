from signageWebpage import sw
from flask import render_template
import scrape


@sw.route("/storytime")
def storytime():
    room = "Storytime Room"
    date = scrape.get_assabet_date()
    events = scrape.get_events_now(room)
    # TODO: Don't display canceled events
    return render_template("events.html", room=room, today=date, events=events)


@sw.route("/community")
def community():
    room = "Community Meeting Room"
    date = scrape.get_assabet_date()
    events = scrape.get_events_now(room)
    return render_template("events.html", room=room, today=date, events=events)


@sw.route("/small")
def small():
    room = "Small Meeting Room"
    date = scrape.get_assabet_date()
    events = scrape.get_events_now(room)
    return render_template("events.html", room=room, today=date, events=events)