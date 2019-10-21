from signageWebpage import sw
from flask import render_template
import scrape


@sw.route("/")
@sw.route("/index")
def index():
    date = scrape.get_assabet_date()
    mevents = scrape.get_month_events()
    tevents = scrape.get_todays_events(date, mevents)
    revents = scrape.get_events_in_room("Community Meeting Room", tevents)
    return render_template("cmr.html", today=date, events=revents)
