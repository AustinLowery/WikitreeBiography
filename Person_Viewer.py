import Person_Model
from collections import defaultdict
class Viewer:
    def __init__(self,person):
        self.person = person
    def printAll(self):
        self.printGraveInformation()
    def printGraveInformation(self):
        numberNoters = defaultdict(lambda: 'th')
        numberNoters['1'], numberNoters['2'], numberNoters['3'] = 'st','nd','rd' 
        
        if len(self.person.names["First"]) > 1: # Only one first name can be assigned
            print("Type which first name to include (type in a number):\n",
                  *[str(self.person.names["First"].index(item)+1)+"."+item+"\n" for item in self.person.names["First"]])
            self.person.idealNames["First"] = self.person.names["First"][int(input("Response: "))-1]
        else: # if only one, just use that one
            self.person.idealNames["First"] = self.person.names["First"][0]

        if "Middle" not in self.person.names:
            self.person.idealNames["Middle"] = []
        elif len(self.person.names["Middle"]) > 1: # Multiple middle names can be assigned, but which ones should?
            print("Type which middles names to include (type in a string of numbers followed by a space):\n",
                  *[str(self.person.names["Middle"].index(item)+1)+"."+item+"\n" for item in self.person.names["Middle"]])
            self.person.idealNames["Middle"] = [self.person.names["Middle"][index-1] for index in list(map(int,input("Response: ").split()))]
        elif "Middle" in self.person.names: # if only one, just use that one
            self.person.idealNames["Middle"] = self.person.names["Middle"]
            
        if len(self.person.names["Last"]) > 1: # Only one last name can be assigned
            print("Type which last name to include (type in a number):\n",
                  *[str(self.person.names["Last"].index(item)+1)+"."+item+"\n" for item in self.person.names["Last"]])
            self.person.idealNames["Last"] = self.person.names["Last"][int(input("Response: "))-1]
        else:
            self.person.idealNames["Last"] = self.person.names["Last"][0]
        print()
        
        # Every month's abreviation mapped to their full word
        convertMonth = {"JAN":"January","FEB":"February","MAR":"March","APR":"April",
                        "JUN":"June","JUL":"July","AUG":"August","SEP":"September",
                        "OCT":"October","NOV":"November","DEC":"December"}
        if len(self.person.dates["Birth"]) == 3:
            monthB = self.person.dates["Birth"][1]
            # makes months into their full form if not already
            if monthB.upper() in convertMonth:
                monthB = convertMonth[monthB.upper()]
        if len(self.person.dates["Death"]) == 3:
            monthD = self.person.dates["Death"][1]
            if monthD.upper() in convertMonth:
                monthD = convertMonth[monthD.upper()]
                
        #try:
        print(self.person.idealNames["First"], # first name
              *self.person.idealNames["Middle"], # middle names
              self.person.idealNames["Last"],end=" ") # last name

        if len(self.person.dates["Birth"]) == 1:
            print("was born in the year",self.person.dates["Birth"][0])
        elif len(self.person.dates["Birth"]) == 3:
            print("was born the",self.person.dates["Birth"][0]+numberNoters[self.person.dates["Birth"][0][-1]],
                  "of",monthB+",",self.person.dates["Birth"][2],end="") # birth date
##        except:
##            print("Current knowledge of birth of this individual is unknown.")

        if "BirthPlace" in self.person.events:
            # Prints grave citation and birth place w/ citation if the birthplace is given
            print('<!--\n\n---><ref name="Grave">'+self.person.citation+'</ref><!--\n\n-->',"in",self.person.events["BirthPlace"][0]+
                  '.<!--\n\n--><ref name="I'+str(self.person.events["BirthPlace"][2])[1:len(str(self.person.events["BirthPlace"][2]))]+'">'+ # citation
                  self.person.events["BirthPlace"][1]+'</ref><!--\n\n-->')
        else: # Prints grave citation
            print('.<!--\n\n---><ref name="Grave">'+self.person.citation+'</ref><!--\n\n-->',end=" ")

        if len(self.person.dates["Death"]) == 1:
            print(self.person.idealNames["First"],"passed away in the year",
                  self.person.dates["Death"][0],"and",end=" ") # death date
        if len(self.person.dates["Death"]) == 3:
            print(self.person.idealNames["First"],"passed away the",
                  self.person.dates["Death"][0]+numberNoters[self.person.dates["Death"][0][-1]],"of",monthD+",",
                  self.person.dates["Death"][2],"and",end=" ") # death date
        else:
            print("he" if self.person.gender == "Male" else "she",end=" ")
            
        # Prints cemetery
        print("was buried in",self.person.cemetery["Cemetery"],"in",self.person.cemetery["City"]+",",
              self.person.cemetery["County"],",",self.person.cemetery["State"]+
              '.<!--\n\n--><ref name="Grave"/>')


if __name__ == '__main__':
    person = Person_Model.Person()

    person.addName("First","John")
    person.addName("Middle","Jacob")
    person.addName("Middle","George")
    person.addName("Last","JingleheimerSchmit")

    person.gender = "Male"

    person.citation = "Austin Lowery. First Hand Recollection. 13 Nov 2019."

    person.addDate("Birth",["APR","20","1970"])
    person.addDate("Death",["DEC","23","2013"])

    person.addCemetery("Cemetery","New Hope Cemetery")
    person.addCemetery("City","Charlotte")
    person.addCemetery("County","Mecklenburg")
    person.addCemetery("State","North Carolina")

    view = Viewer(person)
    view.printAll()



    

