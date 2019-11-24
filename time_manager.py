class TimeManager:

    def __init__(self):
        self._eventFlags = []
        self._conflictEvents = []
        self._freeTime = []
        self._initialDay = []
        self._finalDay = []
        self._meridianOffset = []

    def checkConflict(self, starttime, endtime, busyIntervals=[{}]):
        eventStart = self.timeToMinutes(starttime, 0)
        eventEnd = self.timeToMinutes(endtime, 0)
        for i in range(len(busyIntervals)):
            busyStart = self.timeToMinutes(busyIntervals[i].get("start"), 0)
            busyEnd = self.timeToMinutes(busyIntervals[i].get("end"), 0)
            if busyStart <= eventStart <= busyEnd:
                self._conflictEvents.append([busyIntervals[i], {"start": starttime, "end": endtime}])
            elif busyStart <= eventEnd <= busyEnd:
                self._conflictEvents.append([busyIntervals[i], {"start": starttime, "end": endtime}])
        if self._conflictEvents is not []:
            return True
        else:
            return False

    # Legend:  Y - year
    #          M - month
    #          D - day
    #          H - hour
    #          M - minute
    #          S - seconds
    #          X - offset hour
    #          C - offset minute
    # Format:  YYYY-MM-DDTHH:MM:SS-XX:CC
    def timeToMinutes(self, time, beginning, days=1):
        # splits date from time
        timeConvertion = time.split("T")
        # sets initial date (lower boundary)
        if beginning > 0:
            self._initialDay = self.dateToIntList(timeConvertion[0])
            dayOffset = 1
        # sets final date (upper boundary)
        elif beginning < 0:
            self._finalDay = self.dateToIntList(timeConvertion[0])
            dayOffset = 1
        else:
            if days > 1:
                dayDistance = self.dateOffset(self.dateToIntList(timeConvertion[0]))
                dayOffset = days - dayDistance
            else:
                dayOffset = 1
        timeConvertion = timeConvertion[1]
        timeConvertion = timeConvertion.split("-")
        self._meridianOffset = timeConvertion[1]
        timeConvertion = timeConvertion[0].split(":")

        for i in range(len(timeConvertion)-1):
            timeConvertion[i] = int(timeConvertion[i])
        x = timeConvertion[0]*60
        y = timeConvertion[1]
        minutes = x + y
        for j in range((days - dayOffset)):
            minutes += 1440
        return minutes

    def dateToIntList(self, date):
        dateConversion = date.split("-")
        for i in range(dateConversion.length()):
            dateConversion[i] = int(dateConversion[i])
        return dateConversion

    def dateOffset(self, date):
        yearDiff = date[0] - self._initialDay[0]
        if yearDiff == 1:
            dayDistance = date[2] + 31 - self._initialDay[2]
        else:
            monthDiff = date[1] - self._initialDay[1]
            if monthDiff == 1:
                if self._initialDay[1] in {4, 6, 9, 11}:
                    dayDistance = date[2] + 30 - self._initialDay[2]
                elif self._initialDay[1] in {1, 3, 5, 7, 8, 10}:
                    dayDistance = date[2] + 31 - self._initialDay[2]
                elif (self._initialDay[1] % 4) == 0:
                    dayDistance = date[2] + 29 - self._initialDay[2]
                else:
                    dayDistance = date[2] + 28 - self._initialDay[2]
            else:
                dayDistance = date[2] - self._initialDay[2]
        return dayDistance

    def minutesToTime(self, firstSattarts, time):
        x = 0

    def createEvent(self):
        x=0

    def checkAvailability(self):
        x=0
