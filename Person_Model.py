class Person:
    names = {}
    idealNames = {}
    residencies = {}
    gender = "None"
    citation = "None"
    dates = {}
    cemetery = {}
    events = {}
    def addRes(self,year,household,location,citation): # Residencies
        self.residencies[year] = [household,location,citation]
        s = sorted(self.residencies.keys())
        self.residencies = dict(zip(s,[self.residencies[x] for x in s])) # Sorts dictionary by year
    def addName(self,nameType,name): # Different Names
        if nameType not in self.names:
            self.names[nameType] = [name]
            self.idealNames[nameType] = name
        elif name not in self.names[nameType]:
            self.names[nameType].append(name)
    def addIdealName(self,nameType,name):
        self.idealNames[nameType] = name
    def addDate(self,dateType,date): # Important dates
        for x in range(len(date)):
            if date[x].isdigit() and not date[0].isdigit():
                temp = date[x]
                date[x] = date[0]
                date[0] = temp
        self.dates[dateType] = date
    def addCemetery(self,dataType,data): # Cemetery Location
        self.cemetery[dataType] = data
    def addEvent(self,eventType,event,citation,year): # Events ie birth places
        self.events[eventType] = [event,citation,year]
