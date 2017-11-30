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
                c = cleanup(i)
                if(c["name"] != ""):
                        d[c["name"]] = ""
                        #d[c["name"]] = d[c["info"]]
        return d

def cleanup(i):
        useless = ["salt", "pepper", "optional"]
        for u in useless:
                if u in i:
                        return { "name" : ""}
        return { "name" : i}

'''
print cleanup("salt and pepper to taste")
d = {}
ingreds = ["salt and pepper to taste"]
for i in ingreds:
        c = cleanup(i)
        if(c["name"] != ""):
                d[c["name"]] = ""
print d
'''

for x in range(4):
        print getIngreds(35382 + x)

#getIngreds(35382)
#getRecipeIDs(getRecipes(['cheese', 'bread']))

'''
def recipe_title(json):
	return json['title']

def recipe_source_url(json):
	return json['source_url']

#give a recipe Id (received from the search_json), function uses a get request to receive json and returns that json
def recipe_json(recipeID):
	api_link = "http://food2fork.com/api/get?key=%s&rId=" % getKey()
	api_link += str(recipeID)
	return api_to_json(api_link)['recipe']

#creates a dictionary of the ingredients from a recipe in the format {ingredient_name:[amount, unit_of_measurement]}
def get_ingredients_dict(recipeID):
	dic = {}
	for ingredient in recipe_json(recipeID)['ingredients']:
		ing_list = ingredient.split(' ')
		removable_parts = ing_list[0].encode("utf-8") + " " + ing_list[1].encode("utf-8")
		dic[ingredient[len(removable_parts)+1:].encode("utf-8")] = [ing_list[0].encode("utf-8"), ing_list[1].encode("utf-8")]
	return dic

if __name__ == "__main__":
        print 1
	#print search_json(['cheese', 'bread'])
	#print recipe_json(35382)
	#print get_ingredients_dict(35382)
'''
