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
        d = {}
        for i in ingreds:
                print i
                #cleanup(i)
                '''
                c = cleanup(i)
                if(c["name"] != ""):
                        d[c["name"]] = ""
                        #d[c["name"]] = d[c["info"]]
                '''
        return d

def cleanup(i):
        info = {"name":"", "info":[0, ""]}

        #removing useless
        useless = ["salt", "pepper", "optional"]
        for u in useless:
                if u in i:
                        return info
        #end removing useless
                
        #removing all (...)
        while "(" in i:
                ssnip = i.find("(")
                esnip = i.find(")")
                i = i[0:ssnip] + i[esnip:]
                i = i.replace(")", " ")
        #end removing all (...)
        
        i = rmxtraWS(i)
        
        #parsing for amount
        esnip = i.find(" ")
        if '/' in i:
                info["info"][0] = frac_float(i[:esnip])
        else:
                info["info"][0] = float(i[:esnip])
        i = i[esnip:]
        #end parsing for amount
        
        if "green onion" in i:
                info["name"] = "green onion"
                info["info"][1] = "stalk"
        print i
        print info

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
        i = " ".join(i.split())
        return i
        
cleanup("1 cup flour")
cleanup("2 green onions (chopped)")
cleanup("1 (4 ounce) package cream cheese (room temperature)")
'''
for x in range(10):
        getIngreds(35382 + x)

cleanup("2 jalapenos, diced (seed them is you prefer less heat)")
'''


'''
def recipe_title(json):
	return json['title']

def recipe_source_url(json):
	return json['source_url']
'''
