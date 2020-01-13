import requests
from bs4 import BeautifulSoup
import datetime
from signageWebpage.event import event as ev
import logging
import platform


if platform.system() == "Windows":
    logging.basicConfig(filename="flaskdebug.log", level=logging.DEBUG)
elif platform.system() == "Linux":
    logging.basicConfig(filename="/var/www/ahpl-signage/flaskdebug.log", level=logging.DEBUG)


def get_assabet_date():
    # Assabet displays the date in the "Day, Month Date" format. We get today's date in that format here
    logging.debug("Getting Assabet Friendly date")
    today = datetime.datetime.now()
    # Linux and Windows require different format options to remove the leading zero, so depending on OS choose the
    os = platform.system()
    if os == "Windows":
        logging.debug("Windows OS Detected, removing leading 0 according to Win specifications")
        assabetDate = today.strftime("%A") + ", " + today.strftime("%B") + " " + today.strftime("%#d")
    elif os == "Linux":
        logging.debug("Linux OS Detected, removing leading 0 according to Linux specifications")
        assabetDate = today.strftime("%A") + ", " + today.strftime("%B") + " " + today.strftime("%-d")
    logging.debug("Assabet date: " + str(assabetDate))
    return assabetDate


def get_assabet_month_year():
    # the month and year is used in the URL to determine which month we want to scrape
    logging.debug("Getting month and year")
    today = datetime.datetime.now()
    month = today.strftime("%B")
    logging.debug("Assabet Month " + str(month))
    year = today.year
    logging.debug("Assabet Year " + str(year))
    return month, year


def get_month_events(month, year):
    # Get the event listing page for the current month and year
    # We get the year and month from the get_assabet_month_year function, or pass arbitrarily
    logging.debug("Getting URL")
    url = "https://auburn-hills.assabetinteractive.com/calendar/{}-{}/event-listing/".format(year, month)
    logging.debug("Scraping URL: " + url)
    response = requests.get(url)

    # Scrape the event page for this month
    soupParse = BeautifulSoup(response.text, "html.parser")
    # Get all the Divs which contain the event listings
    eventListings = soupParse.findAll('div', class_="listing-event")
    # Loop through those divs to get the appropriate information for a single event
    events = []
    for listing in eventListings:
        # Create empty event object
        thisEvent = ev()
        # Event titles are always h2 in the HTML
        eventName = listing.find('h2')
        # Create new python event object
        # If eventName is none, there are no events for that day
        if eventName is not None:
            logging.debug("Event found")
            thisEvent.eventName = eventName.string
            logging.debug(str(thisEvent.eventName))
            thisEvent.eventDate = listing.find('span', class_="event-day").string
            logging.debug(str(thisEvent.eventDate))
            thisEvent.eventTime = listing.find('span', class_="event-time").string
            # This causes formatting issues with the log due to the - character
            # logging.debug(str(thisEvent.eventTime))
            rooms = listing.find_all('span', class_="event-location-location")
            # An event can be in multiple rooms, which we store in a list
            stringRooms = []
            for room in rooms:
                stringRooms.append(room.next)
            thisEvent.eventRoom = stringRooms
            # thisEvent.eventRoom = listing.find('span', class_="event-location-location").string
            logging.debug(str(thisEvent.eventRoom))
            # Add this event to our list of event objects
            events.append(thisEvent)
    return events


# Note that today is a string in the same format as Assabet's dates (ex: Tuesday, October 22)
# Use the get_assabet_date() function to return today's date in this format
def get_day_events(today, events):
    daysEvents = []
    logging.debug("Getting events for today")
    logging.debug("Today is: " + today)
    for event in events:
        logging.debug("Event date is " + str(event.eventDate))
        if event.eventDate == today:
            logging.debug(str(event.eventDate) + " equals " + str(today))
            daysEvents.append(event)
        else:
            logging.debug(str(event.eventDate) + " does not equal " + str(today))
    return daysEvents


def get_events_in_room(room, events):
    roomsEvents = []
    logging.debug("Getting events in room " + str(room))
    for event in events:
        logging.debug("Event room is: " + str(event.eventRoom))
        logging.debug("Searching for room: " + str(room))
        # Check the list of rooms to see if the current room is listed. An event can be in multiple rooms
        if room in event.eventRoom:
            logging.debug("Rooms match")
            roomsEvents.append(event)
        else:
            logging.debug("Our room, " + str(room) + " does not equal event's room " + str(event.eventRoom))
    return roomsEvents

# Debug function
def get_specific_event(eventName, events):
    for event in events:
        if event.eventName == eventName:
            return event
    return "Event Not Found"


# "Helper" function to perform the most common use case for the program - getting events for today in specified room
# Most often, call this function directly
def get_events_now(room):
    assabetMonthYear = get_assabet_month_year()
    assabetDate = get_assabet_date()
    events = get_month_events(assabetMonthYear[0], assabetMonthYear[1])
    devents = get_day_events(assabetDate, events)
    finalEvents = get_events_in_room(room, devents)
    return finalEvents


# For populating the list with fake events for testing purposes
# Specify the number of fake events you want and the room they're in
def get_fake_events(numberOfEvents, room):
    fakeEvents = []
    for i in range(0, numberOfEvents):
        newEvent = ev()
        newEvent.eventName = "Test Event with Really Long Title " + str(i)
        newEvent.eventTime = "10:30\u201412:30"
        newEvent.add_room(room)
        newEvent.eventDate = get_assabet_date()
        fakeEvents.append(newEvent)
    return fakeEvents


def print_events(events):
    if len(events) == 0:
        print("No events")
    else:
        for event in events:
            print("Name: ", event.eventName)
            for room in event.eventRoom:
                print("Room: ", room)
            print("Date: ", event.eventDate)
            print("Time: ", event.eventTime)
            print("")
