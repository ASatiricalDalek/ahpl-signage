# Room Availability Signage 
The room availability signage is a custom Python Flask application which runs on an Apache2 web 
server on an Ubuntu 18.04 LTS server (SignageServer). Its purpose is to display all the events, 
and their times, for the day in a particular room. Any computer, such as a Raspberry Pi, 
can then connect to the web page at the proper URL to display that room’s events.

The Room Availability Signage application assumes that the Library is running the Assabet event
system as it relies on information about how that system organizes its online calendar to pull
the signage.

The Room Availability Signage application was developed by Connor McNamara, Technology Coordinator
at the Auburn Hills Public Library.


# Change Log
1/15/2020 -
* Added support for events located in multiple rooms

11/4/2019 - 

* Fixed an issue on Linux systems where the leading 0 was not being correctly scrubbed from the date 
leading to a problem where the screen would not display events for single-diget days
* Updated documentation 
* Added logging support to the application, particularly the scrape code
* Updated Small Meeting room to Small Conference Room to match rebranding
* Updated Storytime Room to Activity Room to match rebranding  


# Prerequisites
As mentioned above, the application assumes that all of the events in question are located on the
[Assabet event system](https://www.assabetinteractive.com/). In addition, all events must be 
visible on the public calendar. Any events that are restricted to staff view only will not appear
on the signage schedule.

# Helpful Tutorials
Bits and pieces of the following tutorials and documentation were used in the creation of this application:

[Beautiful Soup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

[Deploying Flask on Apache with WSGI](https://www.codementor.io/abhishake/minimal-apache-configuration-for-deploying-a-flask-app-ubuntu-18-04-phu50a7ft)
 
[Flask and WSGI 2](https://www.bogotobogo.com/python/Flask/Python_Flask_HelloWorld_App_with_Apache_WSGI_Ubuntu14.php)

[The Flask Mega Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)

[Jinja2 Template Documentation](https://jinja.palletsprojects.com/en/2.10.x/templates/)


# Python Code

For specific, line-by-line details of the code, please refer to the code’s comments. This document will provide a high-level overview and explain logic and flow, in addition to assumptions made about the data we are scraping. 

## Dependencies

[Flask](https://palletsprojects.com/p/flask/) 

Flask is a framework for writing Python code to create web based applications. It, in conjunction with semi-traditional HTML and JavaScript, handles displaying our web pages and serving the Python code over the internet. Semi-Traditional is important because Flask does leverage the Jinija2 template engine for HTML pages, which allows for more flexibility but has its own syntax. See the HTML section of this document for more details.

[Requests](https://pypi.org/project/requests/2.7.0/)

Requests is a very simple module which retrieves HTML from a given link. We use requests to scrape the Assabet event page for our full event listings.

[BeautifulSoup4](https://pypi.org/project/beautifulsoup4/)

BeautifulSoup4 is a Python module which parses HTML. It forms the backbone of a lot of the work we will be doing. 


## init.py and signage.py

These two files are structural and don’t contain any real code. Signage.py is the file that flask looks to when it starts running, which imports the application. That application is defined in init.py where we define sw as a flask instance. After that definition is done, we import the routes file, which contains all the Flask logic.

## Routes.py

Routes defines all of the URLs that our Flask application can respond to, and what to do when one of those URLs is hit. For this application, we define three URLs, each as a function with a different decorator. 

Let’s look at an example function from this section:

```python
@sw.route("/storytime")
def storytime():
    room = "Storytime Room"
    date = scrape.get_assabet_date()
    events = scrape.get_events_now(room)
    noEvents = renderLogic.no_events_check(events)
    return render_template("events.html", room=room, today=date, events=events, noEvents=noEvents)
``` 
Here, we are defining a URL of /storytime, and when that URL is hit, the Flask application will execute the function associated with that decorator. In this case, that is storytime(). So when we navigate to *server address*/storytime, the storytime function is run.

Using this logic, we can copy these functions and create multiple pages on our web application that each reference a different room in the Assabet system.

Below this is the “room” variable, which defines what room we are looking for events in. This must match the room as it appears in Assabet, including case. 

We define a few more variables using functions from other files, more on that in a bit, and then return a render_template. This means that this function will return an HTML page that we specify. We also pass a bunch of variables that will be fed into this HTML page (See Jinja2 documentation above for more on this)

## Adding a New Room

If we wanted to add a new room, we can do so very easily from Routes.py. All we need is the name of the room as it appears in the Assabet event system (more on this in the Scrape section). Let’s assume that we have a room called “New Room” in Assabet. To add this room to our webapp, and thus display its daily events on a screen, we would just need to copy an existing function, modify its decorator to whatever URL we want, and change the room variable to match the new room. So for our room called new room, our added function might look like this:

```python
@sw.route("/new-room")
def storytime():
    room = "New Room"
    date = scrape.get_assabet_date()
    events = scrape.get_events_now(room)
    noEvents = renderLogic.no_events_check(events)
    return render_template("events.html", room=room, today=date, events=events, noEvents=noEvents)
```
On line 1, we changed the decorator to /new-room, which means our URL for this page will be:
*server address*/new-room (obviously replace server address with the IP address the application is running on, or localhost if you are testing on your machine). The other change we make here is on line 3, where we change the value of the room variable to “New Room”. Now, the application will search for any events in the room labeled “New Room” for the current day when that URL is navigated to. Neat! 

Note that Python is case sensitive, so if your room is labeled "new room” in Assabet, and you enter “New Room” here, the application will not work. 

On line 1, we changed the decorator to /new-room, which means our URL for this page will be:
10.0.50.36/new-room (obviously replace this IP with the IP address the application is running on, or localhost if you are testing on your machine). The other change we make here is on line 3, where we change the value of the room variable to “New Room”. Now, the application will search for any events in the room labeled “New Room” for the current day when that URL is navigated to. Neat! 

Note that Python is case sensitive, so if your room is labeled "new room” in Assabet, and you enter “New Room” here, the application will not work. 


## renderLogic.py

This file only has one function in it which is designed to check if a given list of events is empty. This is used in Routes.py by passing a list of events for the room on the specified day. If the list has a length of 0 (that is, there are no events) this function returns true, otherwise it returns false. The HTML page uses this information to determine whether or not to display a table of events. 


## event.py

This file defines the Python event object created for this application. This is used in conjunction with the scrape file to create an object that contains all of the attributes of an event that we need to use. This includes the name, date, time, and room the event takes place in. These objects are created in the scrape file and a list of those objects is then returned to be displayed on the screen.

By default, all of these fields are set to none, which allows us to create an empty event object and populate it as we parse that information. 

## scrape.py

The majority of the code for the room availability signage application is in here. The commenting is rather thorough throughout the scrape file as well, so this document will just hit the hightlights. It is here that we pull the HTML content from Assabet using requests, parse through it with BeautifulSoup, use that information to create Pythonic event objects, and then return a list of those objects to routes which then renders the information to the screen. 

While the most common use case for this application is displaying events for the current day, code in the scrape file is written to be as modular as possible. The primary function, which is called in routes.py, is get_events_now, which will get all the events for the current day in whatever room is specified when the function is called. 

However, each of the functions this function calls can be called independently, and a different month or day can be passed to pull events from any arbitrary point in time. 

The print_events function can be used to print out a list of events and all of their properties, properly labeled, for troubleshooting purposes. It is not used in production. 

### How it Scrapes

The application works based on the way Assabet generates event entries in code, and how it formats URLs. For instance, for the Auburn Hills event pages, the event URL is always presented in this fashion: 

https://auburn-hills.assabetinteractive.com/calendar/*year*-*month*/event-listing/
Using this information, we use the DateTime library to get the current year and the current month, format that month to be a full month name, and then use that information to generate a URL which will display a list of events for that month. This is done in the get_assabet_month_year() function.

After we have generated this URL, we can pull all the events for that month, as seen in the get_month_events function. This function takes in a month and year (again, modularity!) and gets all the events for that month. We start by using request to get all the HTML on that page. We next run this HTML through the BeautifulSoup parser to find all of the divs with the “Listing-Event” class. This effectively gives us a list of all the events for the month, but it is still in ugly HTML format and contains a lot of unnecessary information. 

Within this div, the only h2 tag is the event title, so we can get the event title simply by pulling out the first H2 tag we find. If we don’t find any H2 tags, then there are no events that day. If we do find an H2 tag, we make a new Python object to store the event, and then append this event to the list of events that will contain all the month’s events in friendly, Python format. 

The relevant information is contained in spans, event-day, event-time, and event-location-location. We use the .string option to return just the inner string (the bit between the tag) as opposed to the entire element.

With a list of Python objects representing all of our events for the month, it’s a simple matter to filter this down further. The get_day_events and get_events_in_room functions do the filtering you would expect, looping through the list of events we just got and returning their own, shorter lists, based on that criteria. 

Assabet displays the date in “day, month date” format (IE: Wednesday, October 23). With this knowledge, we can get today’s date and put it into a format that matches Assabet’s. This is done in the get_assabet_date() function. This is then passed to get_day_events to get the current events for today. If you want to use a different day, you can always pass in a string in the above format to get events for that day from a list.

get_events_in_room functions almost identically, but in most cases the room is actually supplied in the route.py file. This is why it is vital to have the room string in the functions of route.py match exactly to the room name in Assabet. That value is simply passed into this function where it is compared against all the room properties of our Python objects.