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

#cleanup("1 cup flour")
#cleanup("2 green onions (chopped)")
#cleanup("1 (4 ounce) package cream cheese (room temperature)")
#cleanup("2 jalapeno peppers, cut in half lengthwise and seeded")

a = ["2 slices sour dough bread",
     "1 tablespoon tortilla chips, crumbled",
     '1 pizza dough',
     '2 jalapeno peppers, sliced **',
     '4 slices bacon, cut into 1 inch pieces and cooked',
     '1 cup mozzarella, shredded',
     '1 cup cheddar, shredded',
     '1/4 cup buttermilk',
     '1/4 cup mayonnaise',
     '1 jalapeno, stemmed and seeded',
     '1 clove garlic',
     '1 green onion',
     '1/2 lime, juice',
     '1 handful cilantro',
     'salt and pepper to taste',
     '1 (9 inch) pie shell, pre-baked',
     '1/2 cup cream cheese, room temperature',
     '2 jalapenos, diced (seed them is you prefer less heat)',
     '1/2 cup milk',
     '1/2 cup cream',
     '5 large eggs, lightly beaten',
     '1/2 teaspoon smoked paprika',
     '1/8 teaspoon salt',
     '1 jalapeno, sliced',
     '1/2 cup cheddar cheese, grated',
     '2 tablespoons jerk seasoning paste (your favorite brand or see below)',
     '1 pound ground beef',
     '1 cup',
     '4 buns',
     '1 pound white fish fillets (I used tilapia)',
     '1 batch jerk marinade',
     '1 cup jasmine rice',
     '1 cup coconut milk, unsweetened',
     '1 cup water',
     '1 batch banana and pineapple salsa',
     '2 pounds short ribs (trimmed)',
     '1/4 cup soy sauce',
     '2 tablespoons brown sugar',
     '1 tablespoon sesame oil',
     '4 cloves garlic (chopped)',
     '1 inch ginger (grated)',
     '4 green onions (sliced)',
     '1/2 onion (grated)',
     '1 Asian pear (grated)',
     '1 tablespoon sesame seeds (toasted and crushed)',
     '1 cup',
     '2 green onions (sliced)',
     '1 (4 ounce) package cream cheese (room temperature)',
     '1/2 cup sour cream',
     '1/4 cup mayonnaise',
     '1/4 cup grated parmigiano reggiano (grated)',
     '1/4 cup mozzarella (grated)',
     '1/4 cup panko crumbs',
     '1/4 cup grated parmigiano reggiano (grated)',
     '2 eggs',
     '2 strips bacon (cut into bite sized pieces, optional)',
     '1/4 cup',
     '1 tablespoon mayonnaise',
     '1 teaspoon gochujang',
     '1 green onion (sliced)',
     '1 teaspoon sesame seeds (toasted)',
     '2 leaves of lettuce',
     '2 slices of bread',
     '2 strips of bacon (cut into 1/2 inch pieces)',
     '1 cup flour',
     '1/2 cup water',
     '1/2 cup',
     '1 egg',
     '1/2 cup',
     '2 green onions (chopped)']

for x in a:
        cleanup(x)

'''
{'clove garlic': [1.0, '']}
{'lime': [0.5, '']}
{'handful cilantro': [1.0, '']}
{'pound ground beef': [1.0, '']}
{'buns': [4.0, '']}
{'pound white fish fillets': [1.0, '']}
{'batch jerk marinade': [1.0, '']}
{'batch banana pineapple salsa': [1.0, '']}
{'pounds short ribs': [2.0, '']}
{'cloves garlic': [4.0, '']}
{'inch ginger': [1.0, '']}
{'Asian pear': [1.0, '']}
{'green onions': [2.0, '']}
{'package cream cheese': [1.0, '']}
{'leaves lettuce': [2.0, '']}
{'strips bacon': [2.0, '']}
'''

'''
for x in range(10):
        getIngreds(35382 + x)

def recipe_title(json):
	return json['title']

def recipe_source_url(json):
	return json['source_url']
'''
