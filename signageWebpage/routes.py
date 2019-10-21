from signageWebpage import sw
from flask import render_template
import scrape


@sw.route("/")
@sw.route("/index")
def index():
    room = "Storytime Room"
    date = scrape.get_assabet_date()
    events = scrape.get_events_now(room)
    # TODO: Don't display canceled events
    return render_template("cmr.html", room=room, today=date, events=events)
