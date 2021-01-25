import Person_Model
from collections import defaultdict
relations = {"Son": defaultdict(lambda: 'other household member', {"Sister-in-law":"Aunt","Grandson":"Nephew","Granddaughter":"Niece","Servant":"Servant",
                    "Adopted daughter":"Adopted Sister", "Adopted Son":"Adopted Brother","Head":"Father","Wife":"Mother","Son":"Brother","Daughter":"Sister",
                    "Brother":"Uncle","Sister":"Aunt", "Father":"Grandfather","Mother":"Grandmother","Boarder":"Boarder"}),
             
             "Daughter": defaultdict(lambda: 'other household member', {"Sister-in-law":"Aunt","Grandson":"Nephew","Granddaughter":"Niece","Servant":"Servant",
                         "Adopted daughter":"Adopted Sister", "Adopted Son":"Adopted Brother","Head":"Father","Wife":"Mother","Son":"Brother","Daughter":"Sister",
                         "Brother":"Uncle","Sister":"Aunt", "Father":"Grandfather","Mother":"Grandmother","Boarder":"Boarder"}),
             
             "Wife": defaultdict(lambda: 'other household member', {"Sister-in-law":"Sister","Grandson":"Grandson","Granddaughter":"Granddaughter","Servant":"Servant",
                     "Adopted daughter":"Adopted daughter", "Adopted Son":"Adopted Son","Head":"Husband","Wife":"SELF","Son":"Son","Daughter":"Daughter",
                     "Brother":"Brother-in-law","Sister":"Sister-in-law", "Father":"Father-in-law","Mother":"Mother-in-law","Boarder":"Boarder"}),
             
             "Head": defaultdict(lambda: 'other household member', {"Sister-in-law":"Sister-in-law","Grandson":"Grandson","Granddaughter":"Granddaughter",
                     "Servant":"Servant","Adopted daughter":"Adopted daughter", "Adopted Son":"Adopted Son","Head":"SELF","Wife":"Wife","Son":"Son",
                     "Daughter":"Daughter","Brother":"Brother","Sister":"Sister","Father":"Father", "Mother":"Mother","Boarder":"Boarder"}),
             
             "Brother": defaultdict(lambda: 'other household member', {"Grandson":"Great Grandnephew","Granddaughter":"Great GrandNiece","Servant":"Servant",
                        "Head":"Brother","Wife":"Sister-in-law","Son":"Nephew","Daughter":"Niece","Brother":"Brother","Sister":"Sister","Father":"Father",
                        "Mother":"Mother","Boarder":"Boarder"}),
             
             "Sister": defaultdict(lambda: 'other household member', {"Grandson":"Great Grandnephew","Granddaughter":"Great GrandNiece","Servant":"Servant",
                       "Head":"Brother","Wife":"Sister-in-law","Son":"Nephew","Daughter":"Niece","Brother":"Brother","Sister":"Sister","Father":"Father",
                       "Mother":"Mother","Boarder":"Boarder"}),
             
             "Father": defaultdict(lambda: 'other household member', {"Sister-in-law":"Daughter-in-law","Grandson":"Great Grandson",
                       "Granddaughter":"Great Granddaughter","Servant":"Servant", "Adopted daughter":"Adopted Granddaughter","Adopted Son":"Adopted Grandson",
                       "Head":"Son","Wife":"Daughter-in-law","Son":"Grandson", "Daughter":"Granddaughter","Brother":"Son","Sister":"Daughter","Father":"SELF",
                       "Mother":"Wife","Boarder":"Boarder"}),
             
             "Mother": defaultdict(lambda: 'other household member', {"Sister-in-law":"Daughter-in-law","Grandson":"Great Grandson",
                       "Granddaughter":"Great Granddaughter","Servant":"Servant", "Adopted daughter":"Adopted Granddaughter","Adopted Son":"Adopted Grandson",
                       "Head":"Son","Wife":"Daughter-in-law","Son":"Grandson", "Daughter":"Granddaughter","Brother":"Son","Sister":"Daughter","Father":"Husband",
                       "Mother":"SELF","Boarder":"Boarder"}),
             
             "Adopted daughter": defaultdict(lambda: 'other household member', {"Servant":"Servant","Head":"Foster Father","Wife":"Foster Mother",
                       "Son":"Foster Brother","Daughter":"Foster Sister", "Boarder":"Boarder"}),
             
             "Adopted Son": defaultdict(lambda: 'other household member', {"Servant":"Servant","Head":"Foster Father","Wife":"Foster Mother","Son":"Foster Brother",
                       "Daughter":"Foster Sister", "Boarder":"Boarder"}),
             
             "Granddaughter": defaultdict(lambda: 'other household member', {"Sister-in-law":"Great Aunt","Grandson":"Brother","Granddaughter":"Sister",
                              "Servant":"Servant","Head":"Grandfather", "Wife":"Grandmother","Son":"Uncle","Daughter":"Aunt","Brother":"Great-Uncle",
                              "Sister":"Great-Aunt","Father":"Great Grandfather", "Mother":"Great Grandmother","Boarder":"Boarder"}),
             
             "Grandson": defaultdict(lambda: 'other household member', {"Sister-in-law":"Great Aunt","Grandson":"Brother","Granddaughter":"Sister","Servant":"Servant",
                              "Head":"Grandfather", "Wife":"Grandmother","Son":"Uncle","Daughter":"Aunt","Brother":"Great-Uncle","Sister":"Great-Aunt",
                              "Father":"Great Grandfather", "Mother":"Great Grandmother","Boarder":"Boarder"}),
             
             "Sister-in-law": defaultdict(lambda: 'other household member', {"Sister-in-law":"Sister","Grandson":"Great Grandnephew","Granddaughter":"Great Grandniece",
                              "Servant":"Servant", "Head":"Brother-in-law","Wife":"Sister","Son":"Nephew","Daughter":"Niece", "Boarder":"Boarder"}),
             
             "Boarder": defaultdict(lambda: 'other household member', {"Boarder":"Boarder"}),

             "unknown": defaultdict(lambda: 'other household member')
             
             }

class Model:
    def __init__(self,person=None,documentName="FamilySearchDocs.txt"):
        if not person:
            self.person = Person_Model.Person()
        else:
            self.person = person
            
        self.doc = documentName
        
    # Gets information from the text file
    def runFile(self):
        self.file = open(self.doc,"r")
        #Model.familySearch(file)
                
    # Add the name on the census record of the individual
    def fsNameAdd(self, names):
        for n in range(0,len(names)):
            if n == 0:
                self.person.addName("First",names[n])
            elif n == len(names)-1:
                self.person.addName("Last",names[n])
            else:
                self.person.addName("Middle",names[n])

    # Returns the relationship to the person
    def fsHouseholdAdd(self, personInfo,relationToHead):
        personInfo = personInfo.split("\t")
        if personInfo[1].lower() == "self":
            personInfo[1] = "Head"
        try:
            return relations[relationToHead][personInfo[1]]
        except:
            return "Error"
                        
    def familySearch(self): # for familysearch text documents
        valid = "None"
        relationToHead = birthplace = "unknown"
        household = []
        for line in self.file:
            if valid == "None": # if line doesn't indicate anything of the next's contents
                if "Name:" in line and not "Affiliate" in line:
                    valid = "Name"
                elif "Event Date:" in line or "Event Year:" in line:
                    valid = "Year"
                elif "Event Place:" in line or "Event Place (Original):" in line:
                    valid = "Location"
                elif "Relationship to Head of Household:" in line:
                    valid = "Relation"
                elif "Role" in line:
                    valid = "Household"
                elif "Citing this Record" in line:
                    valid = "Citation"
                elif "Gender:" in line:
                    valid = "Gender"
                elif "Church of Jesus Christ of Latter-day Saints logo" in line:
                    valid = "End"
                    
            if valid == "Name":
                tempName = ' '.join(line.split()[1:len(line)-1])
                self.fsNameAdd(line.split()[1:]) # list of names ie first and last
                valid = "None"

            elif valid == "Year":
                year = int(line.split()[2])
                valid = "None"

            elif valid == "Location":
                location = line[line.index(":")+2:len(line)-1] # removes \n
                valid = "None"

            elif valid == "Relation":
                relationToHead = ' '.join(line[0:len(line)-1].split()[5:]) # removes \n
                if relationToHead == "Self":
                    relationToHead = "Head"
                    
                valid = "None"

            elif valid == "Household":
                if "Birthplace" in line: # still on the initiating line with Household, Role, etc
                    pass
                elif "\t" in line: # these lines always have tabs
                    if tempName in line:
                        birthPlace = line.split("\t")[len(line.split("\t"))-1]
                    household.append(self.fsHouseholdAdd(line,relationToHead))
                else:
                    # remove an extra relationship
                    # ie say relation is son; When son is appended, head's son to head's son = brother, so remove a brother; always one extra
                    household.remove(relations[relationToHead][relationToHead])
                    valid = "None"
            elif valid == "Gender":
                self.person.gender = line[0:len(line)-1].split()[1] # removes \n
                valid = "None"
            elif valid == "Citation" and not "Citing this Record" in line:
                citation = line[0:len(line)-1] # removes \n
                self.person.addRes(year,household,location,citation)
                if not birthPlace == "unknown":
                    self.person.addEvent("BirthPlace",birthPlace[0:len(birthPlace)-1],citation,year)
                # reset everything to it's default
                year = location = citation = ""
                household = []
                relationToHead = "unknown"
                valid = "None"
        
