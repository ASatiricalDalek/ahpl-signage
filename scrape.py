import requests
from bs4 import BeautifulSoup
import datetime

today = datetime.datetime.now()
month = today.strftime("%B")
year = today.year

# Assabet displays the date in the "Day, Month Date" format. We get today's date in that format here
assabetDate = today.strftime("%A") + ", " + today.strftime("%B") + " " + today.strftime("%#d")


def find_link_with_text(tag):
    h2 = tag.findAll('h2')
    print(h2)
    return h2


# Get the event listing page for the current month and year
url = "https://auburn-hills.assabetinteractive.com/calendar/{}-{}/event-listing/".format(year, month)
response = requests.get(url)

# Scrape the event page for this month
soupParse = BeautifulSoup(response.text, "html.parser")
# Get all the Divs which contain the event listings
eventListings = soupParse.findAll('div', class_="listing-event")
# Loop through those divs to get the appropriate information for a single event
# TODO: Create a Python object for events and place this loop in a function that will return an instance of that object
for listing in eventListings:
    eventName = find_link_with_text(listing)
    print(eventName)
    eventDay = listing.find('span', class_="event-day").string
    print(eventDay)
    eventTime = listing.find('span', class_="event-time").string
    print(eventTime)
    eventRoom = listing.find('span', class_="event-location-location").string
    print(eventRoom)



# print(soupParse.prettify())
# print(eventDays)



# testSoup = BeautifulSoup('<span class="event-day"> Wednesday, October 16 </span>', features="html.parser")
# tag = testSoup.span

# spans = soupParse.findAll('span')

