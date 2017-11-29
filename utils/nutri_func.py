import requests, json

def getKey():
    f = open("govkey","r")
    key = f.read()
    f.close()
    return key

def addDetails(ingreds):
    for i in ingreds:
        ndbno = getID(i)
        nutrients = getNutri(ndbno)#getNutri(ndbno, ingreds[i][0], ingreds[i][1])
        ingreds[i] += [ndbno]
    return ingreds

def getID(ingred):
    link = "https://api.nal.usda.gov/ndb/search/?format=json&ds=Standard+Reference&q=raw %s&api_key=%s" % (ingred, getKey())
    r = requests.get(link)
    d = r.json()
    if 'errors' in d:
        return -1
    return d['list']['item'][0]['ndbno']

def calcNutr(amount, unit):
    return amount * unit

#def getNutri(ID, amount, unit):
def getNutri(ID):
    link = "https://api.nal.usda.gov/ndb/reports?ndbno=%s&type=b&format=json&api_key=%s" % (ID, getKey())
    print link
    r = requests.get(link)
    d = r.json()
    if 'errors' in d:
        return [0, 0, 0]
    nutrients = d['report']['food']['nutrients']
    for n in nutrients:
        print n['name']
    '''
    protein = calcNutr(amount,)
    carbs = calcNutr(amount,)
    fats = calcNutr(amount,)
    return [protein, carbs, fats]
    '''

stuff = {"apple":[], 'orange':[]}
print addDetails(stuff)

'''
https://api.nal.usda.gov/ndb/search/?format=xml&ds=Standard+Reference&q=apples&api_key=DEMO_KEY

needs to be raw for ingredients
ie. apple returns croissant, apple
BUT if we search raw apple,
actually returns the apple we want
if we search raw apple croissant (??) it works too

use standard reference
b/c otherwise the other give you 4k pages

filter out babyfoods? 8 pgs
beef products 20 pgs
breakfast cereals 8 pgs	
baked goods 18 pgs
	
really only ones we need are:
dairy and eggs
cereal grains and pasta
etc.

give peeps an option to search up a brand thing tho
'''
