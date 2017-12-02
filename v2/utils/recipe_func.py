import json, requests

def getKey():
        f = open('static/key','r')
        key = f.read()
        f.close()
        return key

def getLink(ingreds):
        terms = ""
        for i in ingreds:
                terms += (i + ",")
                api_link = "http://food2fork.com/api/search?key=%s&q=%s" % (getKey(), terms)
        return api_link

def getRecipes(ingreds):
        link = getLink(ingreds)
        r = requests.get(link)
        d = r.json()
        return d['recipes']

def getRecipeIDs(recipes):
        rIDs = []
        for r in recipes:
                rIDs += [r['recipe_id']]
        return rIDs

def getRecipeInfo(rID):
        link = "http://food2fork.com/api/get?key=%s&rId=%s" % (getKey(), rID)
        r = requests.get(link)
        d = r.json()
        return d['recipe']

def getIngreds(rID):
        info = getRecipeInfo(rID)
        ingreds = info['ingredients']
        print ingreds
        d = {}
        for i in ingreds:
                d.update(cleanup(i))
        print d
        return d

def cleanup(i):
        info = {"name":"", "info":[0, ""]}

        #removing useless
        useless = ["optional"]
        for u in useless:
                if u in i:
                        return {"": [0, ""]}
        #end removing useless

        #checking to make sure amount exists
        if not any(char.isdigit() for char in i):
                return {"": [0, ""]}       
                
        #removing all (...)
        while "(" in i:
                ssnip = i.find("(")
                esnip = i.find(")")
                i = i[0:ssnip] + i[esnip:]
                i = i.replace(")", " ")
        #end removing all (...)

        i = i.replace("-", " ")

        try:
                #parsing for amount
                esnip = i.find(" ")
                if '/' in i:
                        info["info"][0] = frac_float(i[:esnip])
                else:
                        info["info"][0] = float(i[:esnip])
                        i = i[esnip:]
                #end parsing for amount
        except:
                return {"": [0, ""]}       

        #cutting off extra
        while "," in i:
                ssnip = i.find(",")
                i = i[:ssnip]
        #end cutting off extra

        while ";" in i:
                ssnip = i.find(";")
                i = i[:ssnip]

        while "or" in i:
                ssnip = i.find("or")
                i = i[:ssnip]
                
        #remove extra whitespace
        i = rmxtraWS(i)
        
        convert = {"cups":"cup", "cup":"cup", "slices":"slice", "tablespoon":"tablespoon","tablespoons":"tablespoon", "teaspoons":"tsp", "teaspoon":"tsp", "large":"large", "small":"small","slice":"slice", "package":"", "strips":"strips", "strip":"strip", "handful":"cup"}
        special = { "jalapeno":"pepper", "jalapenos":"pepper", "onion":"stalk", "green onion":"stalk", 'jalapeno peppers':"pepper",  "green onions":"stalk"}
        extra = ["of","and","grated","shredded", "such", "as"]
        
        for part in i.split(" "):
                if part in convert:
                        info["info"][1] = convert[part]
                else:
                        if part not in extra:
                                info["name"] += (part + " ")

        info["name"] = info["name"].strip(" &#1234567890;")
                
        if (info["info"][1] == "") & (info["name"] in special):
                info["info"][1] = special[info["name"]]

        return {info["name"]:info["info"]}

def frac_float(string):
        split = string.find("/")
        num = string[:split]
        den = string[split + 1:]
        try:
                return float(num)/float(den)
        except:
                return -1

def rmxtraWS(i):
        while "\n" in i:
                i = i.replace("\n", "")
        i = i.strip()
        i = " ".join(i.split())
        return i

'''
for x in range(10):
        getIngreds(35382 + x)

def recipe_title(json):
	return json['title']

def recipe_source_url(json):
	return json['source_url']


a = [
        u'2 cups (250 grams) all- purpose flour',
        u'1/2 teaspoon table salt',
        u'13 tablespoons (185 grams or 1 stick plus 5 tablespoons) cold unsalted butter, diced',
        u'6 tablespoons (90 grams) sour cream or whole Greek yogurt (i.e., a strained',
        u'yogurt)',
        u'1 tablespoon (15 ml) white wine vinegar',
        u'1/4 cup (60 ml) ice water',
        u'1 egg, beaten with 1 tablespoon water, for egg wash',
        u'2 tablespoons (30 ml) olive oil',
        u'4 ounces (115 grams or 3/4 to 1 cup) 1/4-inch-diced pancetta',
        u'1 large or 2 small onions, finely chopped',
        u'1 large carrot, finely chopped',
        u'1 large stalk celery, finely chopped',
        u'Pinch of red pepper flakes',
        u'Salt and freshly ground black pepper',
        u'2 garlic cloves, minced',
        u'Thinly sliced Swiss chard leaves from an 8- to 10-ounce (225- to 285-gram)',
        u'bundle (4 cups); if leaves are very wide, you can halve them lengthwise',
        u'3 1/2 tablespoons (50 grams) butter',
        u'3 1/2 tablespoons (25 grams) all- purpose flour',
        u'3 1/2 cups (765 ml) sodium- free or low- sodium chicken or vegetable broth',
        u'2 cups white beans, cooked and drained, or from one and a third 15.5- ounce',
        u'(440-gram) cans'
]

for x in a:
        print cleanup(x)
'''
