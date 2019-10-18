import requests

### FINDAGRAVE URL HERE ###
grave = "https://www.findagrave.com/memorial/63007774/sarah-frances-lowery"
###

class Person:
    names = {}
    residencies = {}
    gender = "None"
    citation = "None"
    dates = {}
    cemetery = {}
    events = {}
    def addRes(self,year,household,location,citation): # Residencies
        self.residencies[year] = [household,location,citation]
        self.residencies = dict(sorted(self.residencies.items())) # Sorts dictionary by year
    def addName(self,nameType,name): # Different Names
        if nameType not in self.names:
            self.names[nameType] = [name]
        elif name not in self.names[nameType]:
            self.names[nameType].append(name)
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
        
person = Person()
# Relationships based on their relationship to the head; if you're the head's son, then when the record mentions a sister, it is the sons aunt
relations = {"Son":{"Grandson":"Nephew","Granddaughter":"Neice","Servant":"Servant","Adopted daughter":"Adopted Sister","Adopted Son":"Adopted Brother","Head":"Father","Wife":"Mother","Son":"Brother","Daughter":"Sister","Brother":"Uncle","Sister":"Aunt","Father":"Grandfather","Mother":"Grandmother","Boarder":"Boarder"},
             "Daughter":{"Grandson":"Nephew","Granddaughter":"Neice","Servant":"Servant","Adopted daughter":"Adopted Sister","Adopted Son":"Adopted Brother","Head":"Father","Wife":"Mother","Son":"Brother","Daughter":"Sister","Brother":"Uncle","Sister":"Aunt","Father":"Grandfather","Mother":"Grandmother","Boarder":"Boarder"},
             "Wife":{"Grandson":"Grandson","Granddaughter":"Granddaughter","Servant":"Servant","Adopted daughter":"Adopted daughter","Adopted Son":"Adopted Son","Head":"Husband","Wife":"SELF","Son":"Son","Daughter":"Daughter","Brother":"Brother-in-law","Sister":"Sister-in-law","Father":"Father-in-law","Mother":"Mother-in-law","Boarder":"Boarder"},
             "Head":{"Grandson":"Grandson","Granddaughter":"Granddaughter","Servant":"Servant","Adopted daughter":"Adopted daughter","Adopted Son":"Adopted Son","Head":"SELF","Wife":"Wife","Son":"Son","Daughter":"Daughter","Brother":"Brother","Sister":"Sister","Father":"Father","Mother":"Mother","Boarder":"Boarder"},
             "Brother":{"Grandson":"Great Grandnephew","Granddaughter":"Great Grandneice","Servant":"Servant","Adopted daughter":"Adopted Neice","Adopted Son":"Adopted Nephew","Head":"Brother","Wife":"Sister-in-law","Son":"Nephew","Daughter":"Neice","Brother":"Brother","Sister":"Sister","Father":"Father","Mother":"Mother","Boarder":"Boarder"},
             "Sister":{"Grandson":"Great Grandnephew","Granddaughter":"Great Grandneice","Servant":"Servant","Adopted daughter":"Adopted Neice","Adopted Son":"Adopted Nephew","Head":"Brother","Wife":"Sister-in-law","Son":"Nephew","Daughter":"Neice","Brother":"Brother","Sister":"Sister","Father":"Father","Mother":"Mother","Boarder":"Boarder"},
             "Father":{"Grandson":"Great Grandson","Granddaughter":"Great Granddaughter","Servant":"Servant","Adopted daughter":"Adopted Granddaughter","Adopted Son":"Adopted Grandson","Head":"Son","Wife":"Daughter-in-law","Son":"Grandson","Daughter":"Granddaughter","Brother":"Son","Sister":"Daughter","Father":"SELF","Mother":"Wife","Boarder":"Boarder"},
             "Mother":{"Grandson":"Great Grandson","Granddaughter":"Great Granddaughter","Servant":"Servant","Adopted daughter":"Adopted Granddaughter","Adopted Son":"Adopted Grandson","Head":"Son","Wife":"Daughter-in-law","Son":"Grandson","Daughter":"Granddaughter","Brother":"Son","Sister":"Daughter","Father":"Husband","Mother":"SELF","Boarder":"Boarder"},
             "Adopted daughter":{"Grandson":"Adopted Nephew","Granddaughter":"Adopted Neice","Servant":"Servant","Head":"Foster Father","Wife":"Foster Mother","Son":"Foster Brother","Daughter":"Foster Sister","Brother":"Foster Uncle","Sister":"Foster Aunt","Father":"Foster Grandfather","Mother":"Foster Grandmother","Boarder":"Boarder"},
             "Adopted Son":{"Grandson":"Adopted Nephew","Granddaughter":"Adopted Neice","Servant":"Servant","Head":"Foster Father","Wife":"Foster Mother","Son":"Foster Brother","Daughter":"Foster Sister","Brother":"Foster Uncle","Sister":"Foster Aunt","Father":"Foster Grandfather","Mother":"Foster Grandmother","Boarder":"Boarder"},
             "Granddaughter":{"Grandson":"Brother","Granddaughter":"Sister","Servant":"Servant","Head":"Grandfather","Wife":"Grandmother","Son":"Uncle","Daughter":"Aunt","Brother":"Uncle","Sister":"Grea-Aunt","Father":"Great Grandfather","Mother":"Great Grandmother","Boarder":"Boarder"},
             "Grandson":{"Grandson":"Brother","Granddaughter":"Sister","Servant":"Servant","Head":"Foster Father","Wife":"Foster Mother","Son":"Foster Brother","Daughter":"Foster Sister","Brother":"Foster Uncle","Sister":"Foster Aunt","Father":"Foster Grandfather","Mother":"Foster Grandmother","Boarder":"Boarder"},
             }


# Gets the string between two characters in a string
def getBetween(n,a,b):
    return n[n.index(a)+len(a):n[n.index(a):len(n)].index(b)+n.index(a)]


# Prints the household for a census
def printHouse(household):
    seen = []

    if person.gender == "Male": # gets the pronoun for a person
        pronoun = "his"
    elif person.gender == "Female":
        pronoun = "her"
    else:
        pronoun = "their"

    statement = []
    for x in range(len(household)):
        # if there's more than one of that relation to the person and it hasn't been seen, print "(# in house) (relation)s" ie "3 sisters"
        if household.count(household[x]) > 1 and household[x] not in seen:
            statement.append(str(household.count(household[x]))+" "+household[x].lower()+'s')
            seen.append(household[x]) # relation has been added
        # if there's only one relation for that person, print "(pronoun) (relation)" ie "his father"
        elif household[x] not in seen:
            statement.append(pronoun+" "+household[x].lower())
            seen.append(household[x])
            
    if len(statement) > 1: # "and" is only needed when there's more than one person
        statement.insert(len(statement)-1,"and") # insert an "and" before the last relation

    for x in range(len(statement)):
        # commas don't go after the last element and when an "and" is listed,
        # otherwise it'd be "his father, his mother, and, his son," instead of "his father, his mother, and his son"
        if x < len(statement)-2:
            print(statement[x]+",",end=" ")
        else:
            print(statement[x],end=" ")
    
# Add the name on the census record of the individual
def fsNameAdd(names):
    for n in range(0,len(names)):
        if n == 0:
            person.addName("First",names[n])
        elif n == len(names)-1:
            person.addName("Last",names[n])
        else:
            person.addName("Middle",names[n])

# Returns the relationship to the person
def fsHouseholdAdd(personInfo,relationToHead):
    personInfo = personInfo.split("\t")
    if personInfo[1] == "Self":
        personInfo[1] = "Head"
    return relations[relationToHead][personInfo[1]]
                    
def familySearch(contents): # for familysearch text documents
    valid = "None"
    relationToHead = "unknown"
    household = []
    for line in file:
        if valid == "None": # if line doesn't indicate anything of the next's contents
            if "Name:" in line:
                valid = "Name"
            elif "Event Date:" in line:
                valid = "Year"
            elif "Event Place:" in line:
                valid = "Location"
            elif "Relationship to Head of Household:" in line:
                valid = "Relation"
            elif "Role" in line:
                valid = "Household"
            elif "Citing this Record" in line:
                valid = "Citation"
            elif "Gender:" in line:
                valid = "Gender"
            elif "Church of Jesus Christ of Latter-day Saints" in line:
                valid = "End"
                
        elif valid == "Name":
            tempName = line[0:len(line)-1]
            fsNameAdd(line.split()) # list of names ie first and last
            valid = "None"

        elif valid == "Year":
            year = int(line)
            valid = "None"

        elif valid == "Location":
            location = line[0:len(line)-1] # removes \n
            valid = "None"

        elif valid == "Relation":
            relationToHead = line[0:len(line)-1] # removes \n
            if relationToHead == "Self":
                relationToHead = "Head"
                
            valid = "None"

        elif valid == "Household":
            if "\t" in line: # these lines always have tabs
                if tempName in line:
                    birthPlace = line.split("\t")[len(line.split("\t"))-1]
                household.append(fsHouseholdAdd(line,relationToHead))
            else:
                # remove an extra relationship
                # ie say relation is son; When son is appended, head's son to head's son = brother, so remove a brother; always one extra
                household.remove(relations[relationToHead][relationToHead])
                valid = "None"
        elif valid == "Citation":
            citation = line[0:len(line)-1] # removes \n
            valid = "None"
        elif valid == "Gender":
            person.gender = line[0:len(line)-1] # removes \n
            valid = "None"
        elif valid == "End":
            person.addRes(year,household,location,citation)
            person.addEvent("BirthPlace",birthPlace[0:len(birthPlace)-1],citation,year)
            # reset everything to it's default
            year = location = citation = ""
            household = []
            relationToHead = "unknown"
            valid = "None"

def graveCitation(citation): # Removes a lot of html junk in the citation
    while "  " in citation:
        citation = citation.replace("  "," ")
    
    citation = citation.replace("<em>","")
    citation = citation.replace("</em>","")
    citation = citation.replace('<a href="https://www.findagrave.com">',"")
    citation = citation.replace('</a>',"")
    citation = citation.replace('<span id="dateHolder"></span>',"today")
    citation = citation.replace('&ndash;','-') # dash value
    citation = citation.replace('<a href="'+grave+'">','['+grave+" ")
    citation = citation.replace('\n',"")
    citation = citation.replace("&#x2F;&#x2F;","//")
    citation = citation.replace("\t","")
    citation = citation.replace(", citing","], citing")

    contributor = citation[citation.index("<a href='https://www.findagrave.com/user/profile/"):len(citation)] # last bits of string
    contributor = getBetween(contributor,"<a href='https://www.findagrave.com/user/profile/","'>")
    citation = citation.replace("<a href='https://www.findagrave.com/user/profile/"+contributor+"'>","["+"https://www.findagrave.com/user/profile/"+contributor+" ")
    citation = citation.replace(contributor+")",contributor+"])")

    return citation

def findAGrave(url):
    name1 = 'class="img-responsive center-block" alt=" '
    name2 = '" id="profileImage"'
    name = getBetween(url,name1,name2).split()

    # Adds given names
    person.addName("First",name[0])
    print(person.names)
    for x in range(1,len(name)-1): # for everything not first name or last name
        if "<I>" not in name[x].upper(): # no italics indicate middle name
            person.addName("Middle",name[x])
        else:
            person.addName("Maiden",getBetween(name[x],">","<"))
    person.addName("Last",name[len(name)-1])

    birth1 = '<td><time id="birthDateLabel" class="info" itemprop="birthDate">'
    birth2 = '</time>'
    person.addDate("Birth",getBetween(url,birth1,birth2).split())

    death1 = '<td><span id="deathDateLabel" class="info middot" itemprop="deathDate">'
    death2 = '(aged '
    try:
        person.addDate("Death",getBetween(url,death1,death2).split())
    except:
        person.addDate("Death",["unknown"])

    span = '</span>'    

    # All cemetery information
    cemetery = '<span id="cemeteryNameLabel" itemprop="name">'
    cemetery = getBetween(url,cemetery,span)
    person.addCemetery("Cemetery",cemetery)

    city = '<span id="cemeteryCityName" itemprop="addressLocality">'
    city = getBetween(url,city,span)
    person.addCemetery("City",city)

    county = '<span id="cemeteryCountyName">'
    county = getBetween(url,county,span)
    person.addCemetery("County",county)

    state = '<span id="cemeteryStateName" itemprop="addressRegion">'
    state = getBetween(url,state,span)
    person.addCemetery("State",state)

    citation1 = '<div id="citationInfo">'
    citation2 = '</div>'
    citationVal = getBetween(url,citation1,citation2)
    person.citation = graveCitation(citationVal)
    

### Adds all class information for person
r = requests.get(grave)
textedUrl = r.text
findAGrave(textedUrl)

file = open("FamilySearchDocs.txt","r")
familySearch(file)

###

### Prints out all the information below
def printCensus(firstName):
    # Residencies
    print("==Residencies==")
    for x in person.residencies.keys():
        print("In",str(x)+",",person.names["First"][firstName-1],"was living with",end=" ")
        printHouse(person.residencies[x][0])
        print("in",person.residencies[x][1]+'.<!--\n\n--><ref name="I'+str(x)[1:len(str(x))]+'">'+person.residencies[x][2]+'</ref><!--\n\n--> ',end="")
def printGraveInfo(firstName,middleName,lastName):
    convertMonth = {"JAN":"January","FEB":"February","MAR":"March","APR":"April","JUN":"June","JUL":"July","AUG":"August","SEP":"September","OCT":"October","NOV":"November","DEC":"December"}
    monthB = person.dates["Birth"][1]
    monthD = person.dates["Birth"][1]
    # makes months into their full form if not already
    if monthB.upper() in convertMonth:
        monthB = convertMonth[monthB.upper()]
    if monthD.upper() in convertMonth:
        monthD = convertMonth[monthD.upper()]

    print(person.names["First"][firstName-1],*[person.names["Middle"][item-1] for item in middleName],person.names["Last"][lastName-1],end=" ") # full name
    print("was born the",person.dates["Birth"][0]+"th of",monthB+",",person.dates["Birth"][2],end="") # birth date

    if "BirthPlace" in person.events:
        # Prints grave citation and birth place w/ citation
        print('<!--\n\n---><ref name="Grave">'+person.citation+'</ref><!--\n\n-->',"in",person.events["BirthPlace"][0]+'.<!--\n\n--><ref name="I'+str(person.events["BirthPlace"][2])[1:len(str(person.events["BirthPlace"][2]))]+'">'+person.events["BirthPlace"][1]+'</ref><!--\n\n-->')
    else: # Prints grave citation
        print('.<!--\n\n---><ref name="Grave">'+person.citation+'</ref><!--\n\n-->',end=" ")

    try:
        print(person.names["First"][firstName-1],"passed away the",person.dates["Death"][0]+"th of",monthD+",",person.dates["Death"][2],"and",end=" ") # death date
    except:
        print("He",end=" ")
    # Prints cemetery
    print("was buried in",person.cemetery["Cemetery"],"in",person.cemetery["City"]+",",person.cemetery["County"],",",person.cemetery["State"]+'.<!--\n\n--><ref name="Grave"/>')






    
if len(person.names["First"]) > 1: # Only one first name can be assigned
    print("Type which first name to include (type in a number):\n",*[str(person.names["First"].index(item)+1)+"."+item+"\n" for item in person.names["First"]])
    firstName = int(input("Response: "))
else: # if only one, just use that one
    firstName = 0
if len(person.names["Middle"]) > 1: # Multiple middle names can be assigned, but which ones should?
    print("Type which middles names to include (type in a string of numbers followed by a space):\n",*[str(person.names["Middle"].index(item)+1)+"."+item+"\n" for item in person.names["Middle"]])
    middleName = list(map(int,input("Response: ").split()))
elif "Middle" in person.names: # if only one, just use that one
    middleName = [1]
else: # if no middle name
    middleName = []
if len(person.names["Last"]) > 1: # Only one last name can be assigned
    print("Type which last name to include (type in a number):\n",*[str(person.names["Last"].index(item)+1)+"."+item+"\n" for item in person.names["Last"]])
    lastName = int(input("Response: "))
else:
    lastName = 0
print()

# Prints the grave record
printGraveInfo(firstName,middleName,lastName)
# Prints the census record
printCensus(firstName)
###
