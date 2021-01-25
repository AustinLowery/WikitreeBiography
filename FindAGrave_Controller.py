import FindAGrave_Viewer

print("FindAGrave URL: ")
url = input()
viewer = FindAGrave_Viewer.FindAGraveView(url)
viewer.generateProfile()
viewer.printAll()
