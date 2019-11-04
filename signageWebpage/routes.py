from signageWebpage import sw, scrape, renderLogic
from flask import render_template
import logging



@sw.route("/storytime")
def storytime():
    room = "Storytime Room"
    logging.info("Getting events for " + str(room))
    date = scrape.get_assabet_date()
    logging.info("Event date " + str(date))
    logging.info("Getting events")
    events = scrape.get_events_now(room)
    logging.info("Checking to see if events were found...")
    noEvents = renderLogic.no_events_check(events)
    return render_template("events.html", room=room, today=date, events=events, noEvents=noEvents)


@sw.route("/community")
def community():
    room = "Community Room"
    logging.info("Getting events for " + str(room))
    date = scrape.get_assabet_date()
    logging.info("Event date " + str(date))
    logging.info("Getting events")
    events = scrape.get_events_now(room)
    logging.info("Checking to see if events were found...")
    noEvents = renderLogic.no_events_check(events)
    return render_template("events.html", room=room, today=date, events=events, noEvents=noEvents)


@sw.route("/small")
def small():
    room = "Small Meeting Room"
    logging.info("Getting events for " + str(room))
    date = scrape.get_assabet_date()
    logging.info("Event date " + str(date))
    logging.info("Getting events")
    events = scrape.get_events_now(room)
    logging.info("Checking to see if events were found...")
    noEvents = renderLogic.no_events_check(events)
    return render_template("events.html", room=room, today=date, events=events, noEvents=noEvents)