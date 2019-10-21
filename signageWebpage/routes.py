from signageWebpage import sw
from flask import render_template
import scrape
import renderLogic


@sw.route("/storytime")
def storytime():
    room = "Storytime Room"
    date = scrape.get_assabet_date()
    events = scrape.get_events_now(room)
    noEvents = renderLogic.no_events_check(events)
    return render_template("events.html", room=room, today=date, events=events, noEvents=noEvents)


@sw.route("/community")
def community():
    room = "Community Meeting Room"
    date = scrape.get_assabet_date()
    events = scrape.get_events_now(room)
    noEvents = renderLogic.no_events_check(events)
    return render_template("events.html", room=room, today=date, events=events, noEvents=noEvents)


@sw.route("/small")
def small():
    room = "Small Meeting Room"
    date = scrape.get_assabet_date()
    events = scrape.get_events_now(room)
    noEvents = renderLogic.no_events_check(events)
    return render_template("events.html", room=room, today=date, events=events, noEvents=noEvents)