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
                #cleanup(i)
                '''
                c = cleanup(i)
                if(c["name"] != ""):
                        d[c["name"]] = ""
                        #d[c["name"]] = d[c["info"]]
                '''
        return d

def cleanup(i):
        useless = ["salt", "pepper", "optional"]
        for u in useless:
                if u in i:
                        return { "name" : ""}
        while "(" in i:
                ssnip = i.find("(")
                esnip = i.find(")")
                i = i[0:ssnip] + i[esnip:]
                i = i.replace(")", " ")

        while "\n" in i:
                i = i.replace("\n", "")

        

        print i
        return { "name" : i}


for x in range(10):
        getIngreds(35382 + x)
'''
cleanup("2 jalapenos, diced (seed them is you prefer less heat)")
'''
'''
a = ["1 (9 inch) pie shell, pre-baked",
     "2 jalapenos, diced (seed them is you prefer less heat)",
     "2 tablespoons jerk seasoning paste (your favorite brand or see below)",
     "1 pound white fish fillets (I used tilapia)",
     "2 pounds short ribs (trimmed)",
     "4 cloves garlic (chopped)",
     "1 inch ginger (grated)",
     "4 green onions (sliced)",
     "1/2 onion (grated)",
     "1 Asian pear (grated)",
     "1 tablespoon sesame seeds (toasted and crushed)",
     "2 green onions (sliced)",
     "1(4 ounce)package cream cheese (room temperature)",
     "1/4 cup grated parmigiano reggiano (grated)",
     "1/4 cup mozzarella (grated)",
     "1/4 cup grated parmigiano reggiano (grated)",
     "2 strips bacon (cut into bite sized pieces, optional)",
     "1 green onion (sliced)",
     "1 teaspoon sesame seeds (toasted)",
     "2 strips of bacon (cut into 1/2 inch pieces)",
     "2 green onions (chopped)"]

for x in a:
        cleanup(x)
'''
#getIngreds(35382)
#getRecipeIDs(getRecipes(['cheese', 'bread']))

'''
def recipe_title(json):
	return json['title']

def recipe_source_url(json):
	return json['source_url']

#creates a dictionary of the ingredients from a recipe in the format {ingredient_name:[amount, unit_of_measurement]}
def get_ingredients_dict(recipeID):
	dic = {}
	for ingredient in recipe_json(recipeID)['ingredients']:
		ing_list = ingredient.split(' ')
		removable_parts = ing_list[0].encode("utf-8") + " " + ing_list[1].encode("utf-8")
		dic[ingredient[len(removable_parts)+1:].encode("utf-8")] = [ing_list[0].encode("utf-8"), ing_list[1].encode("utf-8")]
	return dic
'''
