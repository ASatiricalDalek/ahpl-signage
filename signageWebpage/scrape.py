import requests
from bs4 import BeautifulSoup
import datetime
from signageWebpage.event import event as ev


def get_assabet_date():
    # Assabet displays the date in the "Day, Month Date" format. We get today's date in that format here
    today = datetime.datetime.now()
    assabetDate = today.strftime("%A") + ", " + today.strftime("%B") + " " + today.strftime("%#d")
    return assabetDate


def get_assabet_month_year():
    # the month and year is used in the URL to determine which month we want to scrape
    today = datetime.datetime.now()
    month = today.strftime("%B")
    year = today.year
    return month, year


def get_month_events(month, year):
    # Get the event listing page for the current month and year
    # We get the year and month from the get_assabet_month_year function, or pass arbitrarily
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
        # Event titles are always h2 in the HTML
        eventName = listing.find('h2')
        # Create new python event object
        # If eventName is none, there are no events for that day
        if eventName is not None:
            thisEvent.eventName = eventName.string
            thisEvent.eventDate = listing.find('span', class_="event-day").string
            thisEvent.eventTime = listing.find('span', class_="event-time").string
            thisEvent.eventRoom = listing.find('span', class_="event-location-location").string
            # Add this event to our list of event objects
            events.append(thisEvent)
    return events


# Note that today is a string in the same format as Assabet's dates (ex: Tuesday, October 22)
# Use the get_assabet_date() function to return today's date in this format
def get_day_events(today, events):
    daysEvents = []
    for event in events:
        if event.eventDate == today:
            daysEvents.append(event)
    return daysEvents


def get_events_in_room(room, events):
    roomsEvents = []
    for event in events:
        if event.eventRoom == room:
            roomsEvents.append(event)
    return roomsEvents


# "Helper" function to perform the most common use case for the program - getting events for today in specified room
# Most often, call this function directly
def get_events_now(room):
    assabetMonthYear = get_assabet_month_year()
    assabetDate = get_assabet_date()
    events = get_month_events(assabetMonthYear[0], assabetMonthYear[1])
    devents = get_day_events(assabetDate, events)
    finalEvents = get_events_in_room(room, devents)
    return finalEvents


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


# dt = get_assabet_date()
# evn = get_month_events("October", "2019")
# tde = get_todays_events(dt, evn)
# eir = get_events_in_room("Storytime Room", tde)
# print_events(eir)

# todayEvents = get_events_now("Community Meeting Room")
# print_events(todayEvents)


