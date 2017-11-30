import requests, json

def getKey():
    f = open("../static/govkey","r")
    key = f.read()
    f.close()
    return key

def addDetails(ingreds):
    for i in ingreds:
        ndbno = getID(i)
        nutrients = getNutri(ndbno, ingreds[i][0], ingreds[i][1])
        ingreds[i] += ([ndbno] +  nutrients)
    return ingreds

def getID(ingred):
    link = "https://api.nal.usda.gov/ndb/search/?format=json&ds=Standard+Reference&q=raw %s&api_key=%s" % (ingred, getKey())
    r = requests.get(link)
    d = r.json()
    if 'errors' in d:
        return -1
    return d['list']['item'][0]['ndbno']

def getNutri(ID, amount, unit):
    link = "https://api.nal.usda.gov/ndb/reports?ndbno=%s&type=b&format=json&api_key=%s" % (ID, getKey())
    r = requests.get(link)
    d = r.json()
    if 'errors' in d:
        return [-1, -1, -1]
    nutrients = d['report']['food']['nutrients']
    
    protein = nutrients[2]['measures']
    protein = calcNutr(amount, nutri(protein, unit))

    fats = nutrients[3]['measures']
    fats = calcNutr(amount, nutri(fats, unit))

    carbs = nutrients[4]['measures']
    carbs = calcNutr(amount, nutri(carbs, unit))
    
    return [carbs, protein, fats]

def calcNutr(amount, unit):
    return amount * unit

def nutri(nutrient, unit):
    u = unit
    if(len(unit) >= 3):
        u = unit[0:len(unit)-1]
    for measurement in nutrient:
        print measurement['label']
        if u in measurement['label']:
            return float(measurement['value'])
    return -1

def sumNutri(ingreds):
    ingreds = addDetails(ingreds)
    carbs = 0
    protein = 0
    fats = 0
    broken = []
    for i in ingreds:
        if(ingreds[i][3] > 0):
            carbs += ingreds[i][3]
            protein += ingreds[i][4]
            fats += ingreds[i][5]
        else:
            broken += [i]
    return [carbs, protein, fats, broken]

'''
if __name__ == "__main__":
	stuff = {"apple":[1.4, 'cup'], 'orange':[1.5, 'giant'], 'life':[1, 'giant'],  'yes':[1, 'giant'],  'pepper':[1, 'giant'],  'coconut':[1, 'giant']}
	print addDetails(stuff)
'''

stuff = {"sesame oil":[1, "teaspoon"]}
print addDetails(stuff)
