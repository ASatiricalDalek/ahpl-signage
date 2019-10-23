def no_events_check(events):
    # Events is a list of all events for a given day
    # if the length of that list is 0, no events were scheduled for that day
    if len(events) == 0:
        noEvents = "No Events in this Room Today"
    else:
        noEvents = None
    return noEvents
