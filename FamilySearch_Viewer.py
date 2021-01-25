import FamilySearch_Model
import Person_Model
from collections import defaultdict
class Viewer:
    def __init__(self,person=None):
        if not person:
            self.person = Person_Model.Person()
        else:
            self.person = person
        
    # Prints the household for a census
    def printHouse(self, household):
        seen = []

        if self.person.gender == "Male": # gets the pronoun for a person
            pronoun = "his"
        elif self.person.gender == "Female":
            pronoun = "her"
        else:
            pronoun = "their"

        statement = []

        others = household.count("other household member")
        household = list(filter(lambda a: a != "other household member", household))
        household += others * ["other household member"]
        
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
                
    # Prints out all census information
    def printCensus(self):
        # Residencies
        print("==Residencies==")
        for x in self.person.residencies.keys():
            print("In",str(x)+",",self.person.idealNames["First"],"was living with",end=" ")
            self.printHouse(self.person.residencies[x][0])
            print("in",self.person.residencies[x][1]+'.<!--\n\n--><ref name="I'+str(x)[1:len(str(x))]+'">'+self.person.residencies[x][2]+'</ref><!--\n\n--> ',end="")

if __name__ == '__main__':
    model = FamilySearch_Model.Model()
    model.runFile()
    model.familySearch()

    view = Viewer(model.person)
    
    if len(view.person.names["First"]) > 1: # Only one first name can be assigned
        print("Type which first name to include (type in a number):\n",*[str(
            view.person.names["First"].index(item)+1)+"."+item+"\n" for item in view.person.names["First"]])
        model.person.idealNames["First"] = model.person.names["First"][int(input("Response: "))-1]
    else: # if only one, just use that one
        model.person.idealNames["First"] = model.person.names["First"][0]

    if "Middle" not in view.person.names:
        middleName = []
        
    elif len(view.person.names["Middle"]) > 1: # Multiple middle names can be assigned, but which ones should?
        print("Type which middles names to include (type in a string of numbers followed by a space):\n",*[str(
            view.person.names["Middle"].index(item)+1)+"."+item+"\n" for item in view.person.names["Middle"]])
        model.person.idealNames["Middle"] = model.person.names["Middle"][list(map(int,input("Response: ").split()))]
    elif "Middle" in view.person.names: # if only one, just use that one
        model.person.idealNames["Middle"] = model.person.names["Middle"][0]
        
    if len(view.person.names["Last"]) > 1: # Only one last name can be assigned
        print("Type which last name to include (type in a number):\n",*[str(
            view.person.names["Last"].index(item)+1)+"."+item+"\n" for item in view.person.names["Last"]])
        model.person.idealNames["Last"] = model.person.names["Last"][int(input("Response: "))-1]
    else:
        model.person.idealNames["Last"] = model.person.names["Last"][0]
    print()

    view.printCensus()





    

