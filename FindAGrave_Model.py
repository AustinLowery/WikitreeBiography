from datetime import datetime
# Gets the string between two characters in a string
def getBetween(n,a,b):
    try:
        # finds where a is in n and starts string at the end of a
        firstPlacement = n.index(a)+len(a)
        
        # string from a to the end of string; this decreases chance of failure by duplication
        lastPart = n[firstPlacement:len(n)]

        # finds where b is in the substring the adds the indice of the firstPlacement to use in the full string
        lastPlacement = lastPart.index(b)+firstPlacement
        return n[firstPlacement:lastPlacement]
    except:
        #print("Substring Not Found: A:",a," B:",b,"N:",n)
        return ""
class Model:
    def __init__(self,url,person):
        self.url = url
        self.person = person

    def graveCitation(self,citation): # Removes a lot of html junk in the citation
        while "  " in citation:
            citation = citation.replace("  "," ")
        
        citation = citation.replace("<em>","")
        citation = citation.replace("</em>","")
        citation = citation.replace('<a href="https://www.findagrave.com">',"")
        citation = citation.replace('</a>',"")
        citation = citation.replace('<span id="dateHolder"></span>',datetime.today().strftime('%d %B %Y'))
        citation = citation.replace('&ndash;','-') # dash value
        citation = citation.replace(getBetween(citation,'<a href="','">'),'['+getBetween(citation,'<a href="','">')+" ")
        citation = citation.replace('\n',"")
        citation = citation.replace("&#x2F;&#x2F;","//")
        citation = citation.replace("\t","")
        citation = citation.replace(", citing","], citing")

        try:
            contributor = citation[citation.index("<a href='https://www.findagrave.com/user/profile/"):len(citation)] # last bits of string
            contributor = getBetween(contributor,"<a href='https://www.findagrave.com/user/profile/","'>")
            citation = citation.replace("<a href='https://www.findagrave.com/user/profile/"+contributor+"'>","["+"https://www.findagrave.com/user/profile/"+contributor+" ")
            citation = citation.replace(contributor+")",contributor+"])")
        except:
            # FindAGrave is the contributor
            pass

        link = getBetween(citation,'<a href="','">')
        citation = citation.replace(getBetween(citation,'Find a Grave Memorial no. ','>'),str(link+' '))
        citation = citation.replace(str(link+' >'),str(link+' '))

        while "  " in citation:
            citation = citation.replace("  "," ")

        return citation
    
    def findAGrave(self):
        name1 = 'class="img-responsive center-block" alt=" '
        name2 = '" id="profileImage"'
        name = getBetween(self.url,name1,name2)

        if name == "":
            name = getBetween(self.url,name1[:-1],name2).split()
        else:
            name = name.split()

        # Adds given names
        self.person.addName("First",name[0])
        for x in range(1,len(name)-1): # for everything not first name or last name
            if "<I>" not in name[x].upper(): # no italics indicate middle name
                self.person.addName("Middle",name[x])
            else:
                self.person.addName("Maiden",getBetween(name[x],">","<"))
        self.person.addName("Last",name[len(name)-1])

        birth1 = '<td><time id="birthDateLabel" class="info" itemprop="birthDate">'
        birth2 = '</time>'
        self.person.addDate("Birth",getBetween(self.url,birth1,birth2).split())

        death1 = '<td><span id="deathDateLabel" class="info middot" itemprop="deathDate">'
        death2 = '(aged '
        try:
            self.person.addDate("Death",getBetween(self.url,death1,death2).split())
        except:
            self.person.addDate("Death",["unknown"])

        span = '</span>'    

        # All cemetery information
        cemetery = '<span id="cemeteryNameLabel" itemprop="name">'
        cemetery = getBetween(self.url,cemetery,span)
        self.person.addCemetery("Cemetery",cemetery)

        city = '<span id="cemeteryCityName" itemprop="addressLocality">'
        city = getBetween(self.url,city,span)
        self.person.addCemetery("City",city)

        county = '<span id="cemeteryCountyName">'
        county = getBetween(self.url,county,span)
        self.person.addCemetery("County",county)

        state = '<span id="cemeteryStateName" itemprop="addressRegion">'
        state = getBetween(self.url,state,span)
        self.person.addCemetery("State",state)

        citation1 = '<div id="citationInfo">'
        citation2 = '</div>'
        citationVal = getBetween(self.url,citation1,citation2)
        self.person.citation = self.graveCitation(citationVal)
        
