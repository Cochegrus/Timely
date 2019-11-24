import datetime

class TimeManager:

    def __init__(self):
        self._eventFlags = []
        self._conflictEvents = []
        self._freeTime = [{}]
        self._initialDay = []
        self._currentDay = ""
        self._meridianOffset = ""

    def checkConflict(self, starttime, endtime, busyIntervals=[{}]):
        eventStart = self.timeToMinutes(starttime)
        eventEnd = self.timeToMinutes(endtime)
        for i in range(len(busyIntervals)):
            busyStart = self.timeToMinutes(busyIntervals[i].get("start"))
            busyEnd = self.timeToMinutes(busyIntervals[i].get("end"))
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
    def timeToMinutes(self, time, flag=0, days=1):
        # splits date from time
        timeConvertion = time.split("T")
        # sets initial date (lower boundary)
        if flag > 0:
            self._initialDay = self.dateToIntList(timeConvertion[0])
            dayOffset = 1
        # sets final date (upper boundary)
        elif flag < 0:
            self._currentDay = timeConvertion[0]
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

        #hours
        x = int(timeConvertion[0])*60
        #minutes
        y = int(timeConvertion[1])
        minutes = x + y
        for j in range((days - dayOffset)):
            minutes += 1440
        return minutes

    # Legend:  Y - year
    #          M - month
    #          D - day
    #          H - hour
    #          M - minute
    #          S - seconds
    #          X - offset hour
    #          C - offset minute
    # Format:  YYYY-MM-DDTHH:MM:SS-XX:CC
    def minutesToTime(self, minutes, day):
        #minutes
        y = str(minutes % 10)
        if len(y) == 1:
            y = "0" + y
        #hours
        x = str((minutes - y) / 60)
        if len(x) == 1:
            x = "0" + x
        timeStr = x + ":" + y + ":" + "00" + "-" + self._meridianOffset

        year = str(self._initialDay[0])
        month = str(self._initialDay[1])
        if len(month) == 1:
            month = "0" + month
        day = str(self._initialDay[2])
        if len(day) == 1:
            day = "0" + day
        dateStr = year + "-" + month + "-" + day
        datetimeStr = dateStr + "T" + timeStr

        return datetimeStr

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

    def createEvent(self, starttime="", endtime="", name="New Event"):
        ## call query
        busyIntervals = [{}]
        if starttime == "" or endtime == "":
            self.allocate(name, starttime, endtime, busyIntervals)
        else:
            possible = self.checkConflict(starttime, endtime, busyIntervals)
            if possible:
                x=0 ## create event on calendar
            else:
                self.resolveConflict(starttime, endtime, name, busyIntervals)

    def checkAvailability(self, starttime="", endtime="", busyIntervals=[{}]):
        if starttime == "" or endtime == "":
            minutes = 60
            back = 0
            done = False
        else:
            lowerBound = self.timeToMinutes(starttime)
            higherBound = self.timeToMinutes(endtime, flag=-1)
            minutes = higherBound - lowerBound
            done = True
            if datetime.date.today() == self._currentDay:
              back = 0
            else:
              back = -1

        previousIni = self._initialDay
        count = 0
        k = 0
        freeStart = 0
        for day in range(back, 3):
            if not done:
                busyStart = self.timeToMinutes(busyIntervals[k].get("start"), flag=1)
                done = True
            else:
                busyStart = self.timeToMinutes(busyIntervals[k].get("start"))
                busyEnd = self.timeToMinutes(busyIntervals[k].get("end"))
            for i in range(360, 1260):
                if busyStart <= i < busyEnd:
                    if (count - minutes) >= 30:
                        newStart = self.minutesToTime(freeStart, day)
                        newEnd = self.minutesToTime(i, day)
                        self._freeTime.append({"start": newStart, "end": newEnd})
                    count = 0
                elif i == busyEnd:
                    k += 1
                    try:
                        busyStart = self.timeToMinutes(busyIntervals[k].get("start"), 0)
                        busyEnd = self.timeToMinutes(busyIntervals[k].get("end"), 0)
                    except IndexError:
                        None
                else:
                    count += 0

                if count == (minutes + 30):
                    freeStart = count

        self._initialDay = previousIni

    def getInfo(self, name):
        x = 0
        #event = service.events().get(calenderId='primary', eventId=name).execute()

    def allocate(self, name, starttime="", endtime="",  busyIntervals=[{}]):
        self.checkAvailability(starttime, endtime,  busyIntervals)

        bestFit = None
        biggestDiff = -1
        for i in range(len(self._freeTime)):
            lowerBoundary = self.timeToMinutes(self._freeTime[i].get("start"))
            higherBoundary = self.timeToMinutes(self._freeTime[i].get("end"))
            diff = higherBoundary - lowerBoundary
            if diff > biggestDiff:
                biggestDiff = diff
                bestFit = i

        ## if bestfit is not None
        ## create event with name=name, starttime = self._freeTime[bestFit].get("start"), endtime = self._freeTime[bestFit].get("end")
        ## return True
        ## else, return False

    def resolveConflict(self, starttime, endtime, name, busyIntervals=[{}]):
        print("The following event(s) have clatched and lashed any their schedule ocurred:\n")
        for i in range(len(self._conflictEvents)):
            print(self.getInfo(name))

        priority = input("Which event takes presedence over them the other?\n")
        priorityEvent = self.getInfo(priority)

        done = self.allocate(priority, priorityEvent.starttime, priorityEvent.endtime, busyIntervals)

        if done:
            return True
        else:
            return self.editEvent(name, starttime, endtime)

    def editEvent(self, name = "", starttime = "", endtime = ""):

        #event = service.events().get(calendarId='primary', eventId=name).execute()
        #if starttime != "":
        #    starttime = event['start'].get(dateTime)
        #if endtime != "":
        #    endtime = event['end'].get(dateTime)
        #service.events().delete(calendarId='primary', eventId=name).execute()
        #new_event = {
        #    'summary': name,
        #    'start': {
        #        'dateTime' = starttime
        #    },
        #    'end': {
        #        'dateTime' = endtime
        #    }
        #}
        #createEvent(self, name, starttime, endtime)
        x=0
