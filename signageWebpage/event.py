class event:
    # Variables are set to none by default, allowing us to declare an empty object and then fill it later
    def __init__(self, eventName = None, eventDate = None, eventTime = None, eventRoom = None):
        self.eventName = eventName
        self.eventDate = eventDate
        self.eventTime = eventTime
        self.eventRoom = eventRoom
