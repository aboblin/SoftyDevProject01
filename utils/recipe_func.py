import json, requests
from fractions import Fraction

def getKey():
        f = open('static/key','r')
        key = f.read()
        f.close()
        return key

#input an api_link, returns json recieved from the api
def api_to_json(api_link):
	url = requests.get(api_link)
	return url.json()

#give a list of ingredients, function uses a search request to receive json and returns that json
def search_json(ingredients):
	api_link = "http://food2fork.com/api/search?key=%s&q=" % getKey()
        api_link += ingredients
	return api_to_json(api_link)['recipes']

def recipe_title(json):
	return json['title']

def recipe_source_url(json):
	return json['source_url']

def recipe_id(json):
	return json['recipe_id']

def is_number(string):
	try:
		float(sum(Fraction(s) for s in string.split()))
		return True
	except ValueError:
		return False

def remove_unwanted(string):
        string = string.translate(None, '!@;#$&')
        return string

#give a recipe Id (received from the search_json), function uses a get request to receive json and returns that json
def recipe_json(recipeID):
	api_link = "http://food2fork.com/api/get?key=%s&rId=" % getKey()
	api_link += str(recipeID)
	return api_to_json(api_link)['recipe']

#creates a dictionary of the ingredients from a recipe in the format {ingredient_name:[amount, unit_of_measurement]}
def get_ingredients_dict(recipeID):
        dic = {}
        for ingredient in recipe_json(recipeID)['ingredients']:
		ingredient = remove_unwanted(ingredient.encode("ascii", errors="ignore"))
		while ingredient.find("(") != -1:
                        if ingredient.find(")") != -1:
			        ingredient = ingredient.replace(ingredient[ingredient.find("("): ingredient.find(")")+2], "")
                        else:
                                ingredient = ingredient.replace(ingredient[ingredient.find("("):], "")
		ing_list = ingredient.split(' ')
		#print ing_list
                if len(ing_list) > 2:
		        if is_number(ing_list[1]) and is_number(ing_list[0]):
			        removable_parts = ing_list[0] + " " + ing_list[1] + " " + ing_list[2]
			        dic[ingredient[len(removable_parts)+1:]] = [float(sum(Fraction(s) for s in (ing_list[0]+" "+ing_list[1]).split())), ing_list[2]]
		        elif is_number(ing_list[0]):
			        removable_parts = ing_list[0] + " " + ing_list[1]
			        dic[ingredient[len(removable_parts)+1:]] = [float(sum(Fraction(s) for s in ing_list[0].split())), ing_list[1]]
	                        #print dic
	return dic

if __name__ == "__main__":
	print search_json(['salmon'])
	#print recipe_json(35382)
	print get_ingredients_dict(47746)
