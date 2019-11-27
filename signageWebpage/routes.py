from signageWebpage import sw, scrape, renderLogic
from flask import render_template
import logging



@sw.route("/storytime")
def storytime():
    room = "Activity Room"
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
    room = "Small Conference Room"
    logging.info("Getting events for " + str(room))
    date = scrape.get_assabet_date()
    logging.info("Event date " + str(date))
    logging.info("Getting events")
    events = scrape.get_events_now(room)
    logging.info("Checking to see if events were found...")
    noEvents = renderLogic.no_events_check(events)
    return render_template("events.html", room=room, today=date, events=events, noEvents=noEvents)

@sw.route("/")
def all():
    scr = "Small Conference Room"
    cr = "Community Room"
    ar = "Activity Room"
    logging.info("Getting events for all rooms")
    date = scrape.get_assabet_date()
    logging.info("Event date " + str(date))
    logging.info("Getting events")
    scrEvents = scrape.get_events_now(scr)
    crEvents = scrape.get_events_now(cr)
    arEvents = scrape.get_events_now(ar)
    logging.info("Checking to see if events were found...")
    scrNoEvents = renderLogic.no_events_check(scrEvents)
    crNoEvents = renderLogic.no_events_check(crEvents)
    arNoEvents = renderLogic.no_events_check(arEvents)
    return render_template("AllRooms.html", today=date, scrEvents=scrEvents, crEvents=crEvents, arEvents=arEvents,
                           scrNoEvents=scrNoEvents, arNoEvents=arNoEvents, crNoEvents=crNoEvents)
