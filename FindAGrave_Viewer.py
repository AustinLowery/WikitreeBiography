import FindAGrave_Model
import Person_Model
import Person_Viewer
import requests

class FindAGraveView:
    def __init__(self,url,person=None):
        self.url = requests.get(url).text
        if not person:
            self.person = Person_Model.Person()
        else:
            self.person = person
        self.profile = FindAGrave_Model.Model(self.url,self.person)
    def generateProfile(self):
        self.profile.findAGrave()
    def printAll(self):
        pView = Person_Viewer.Viewer(self.person)
        pView.printAll()

if __name__ == '__main__':
    lincoln = 'https://www.findagrave.com/memorial/627/abraham-lincoln'
    viewer = FindAGraveView(lincoln)
    viewer.generateProfile()
    viewer.printAll()
