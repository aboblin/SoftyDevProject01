import json, requests

def getKey():
        f = open('../static/key','r')
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
        d = {}
        for i in ingreds:
                print i

def cleanup(i):
        info = {"name":"", "info":[0, ""]}

        #removing useless
        useless = ["optional"]
        for u in useless:
                if u in i:
                        return info
        #end removing useless

        #checking to make sure amount exists
        if not any(char.isdigit() for char in i):
                return info       
                
        #removing all (...)
        while "(" in i:
                ssnip = i.find("(")
                esnip = i.find(")")
                i = i[0:ssnip] + i[esnip:]
                i = i.replace(")", " ")
        #end removing all (...)

        #parsing for amount
        esnip = i.find(" ")
        if '/' in i:
                info["info"][0] = frac_float(i[:esnip])
        else:
                info["info"][0] = float(i[:esnip])
        i = i[esnip:]
        #end parsing for amount

        #cutting off extra
        while "," in i:
                ssnip = i.find(",")
                i = i[:ssnip]
        #end cutting off extra
        
        #remove extra whitespace
        i = rmxtraWS(i)
        
        convert = {"cups":"cup", "cup":"cup", "slices":"slice", "tablespoon":"tablespoon","tablespoons":"tablespoon", "teaspoons":"tsp", "teaspoon":"tsp", "large":"large", "small":"small","slice":"slice", "package":"", "strips":"strips", "strip":"strip", "handful":"cup"}
        special = { "jalapeno":"pepper", "jalapenos":"pepper", "onion":"stalk", "green onion":"stalk", 'jalapeno peppers':"pepper",  "green onions":"stalk"}
        extra = ["of","and","grated","shredded"]
        
        for part in i.split(" "):
                if part in convert:
                        info["info"][1] = convert[part]
                else:
                        if part not in extra:
                                info["name"] += (part + " ")

        info["name"] = info["name"].strip()
                
        if (info["info"][1] == "") & (info["name"] in special):
                info["info"][1] = special[info["name"]]
                
        print c(info)

def c(x):
        return {x['name'] : x['info']}


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
'''
