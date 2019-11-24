class Decoder:

    def __init__(self):
        self._createCommands = {"make event", "new event", "make new event", "create event", "create new event", "create an event"}
        self._availabilityCommands = {"check free time", "when am i free", "when am i available", "when am i open", "availability", "check availability"}
        self._getterCommands = {"describe event", "describe the event", "next event", "upcoming event", "get event info", "event details", "get info"}

    def decodeInstruction(self, searchterm):
        if searchterm in self._createCommands:
            return 1
        elif searchterm in self._availabilityCommands:
            return 2
        elif searchterm in self._getterCommands:
            return 3
        else:
            return 0
