import FindAGrave_Viewer
import FamilySearch_Viewer
import FamilySearch_Model

print("FindAGrave URL: ")
url = input()
if url:
    viewer = FindAGrave_Viewer.FindAGraveView(url)
    viewer.generateProfile()
    model = FamilySearch_Model.Model(viewer.person)
else:
    model = FamilySearch_Model.Model()
model.runFile()
model.familySearch()

view = FamilySearch_Viewer.Viewer(model.person)

if url:
    viewer.printAll()
view.printCensus()
print("\n\n==Sources==\n<references/>\n")

# Uncomment the below line to acknowledge this code in the credits. While not required, it is appreciated.
#print("\n==Acknowledgements==\nThis Biography was made with the help of Austin Lowery's Auto-Biography Generator ©2021")
