import requests
from bs4 import BeautifulSoup
import datetime
from event import event as ev


def get_assabet_date():
    # Assabet displays the date in the "Day, Month Date" format. We get today's date in that format here
    today = datetime.datetime.now()
    assabetDate = today.strftime("%A") + ", " + today.strftime("%B") + " " + today.strftime("%#d")
    return assabetDate


def find_link_with_text(tag):
    h2 = tag.find('h2')
    return h2


def get_month_events():
    today = datetime.datetime.now()
    month = today.strftime("%B")
    year = today.year
    # Get the event listing page for the current month and year
    url = "https://auburn-hills.assabetinteractive.com/calendar/{}-{}/event-listing/".format(year, month)
    response = requests.get(url)

    # Scrape the event page for this month
    soupParse = BeautifulSoup(response.text, "html.parser")
    # Get all the Divs which contain the event listings
    eventListings = soupParse.findAll('div', class_="listing-event")
    # Loop through those divs to get the appropriate information for a single event
    events = []
    for listing in eventListings:
        thisEvent = ev()
        eventName = find_link_with_text(listing)
        # If eventName is none, there are no events for that day
        if eventName is not None:
            thisEvent.eventName = eventName.string
            thisEvent.eventDate = listing.find('span', class_="event-day").string
            thisEvent.eventTime = listing.find('span', class_="event-time").string
            thisEvent.eventRoom = listing.find('span', class_="event-location-location").string
            events.append(thisEvent)
    return events


def get_todays_events(today, events):
    todaysEvents = []
    for event in events:
        if event.eventDate == today:
            todaysEvents.append(event)
    return todaysEvents


def get_events_in_room(room, events):
    roomsEvents = []
    for event in events:
        if event.eventRoom == room:
            roomsEvents.append(event)
    return roomsEvents


def print_events(events):
    if len(events) == 0:
        print("No events")
    else:
        for event in events:
            print("Name: ", event.eventName)
            print("Room: ", event.eventRoom)
            print("Date: ", event.eventDate)
            print("Time: ", event.eventTime)
            print("")


dt = get_assabet_date()
evn = get_month_events()
tde = get_todays_events(dt, evn)
eir = get_events_in_room("Storytime Room", tde)
print_events(eir)

