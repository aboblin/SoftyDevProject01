import json, requests

def getKey():
        f = open('utils/key','r')
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
	for ingredient in ingredients:
		api_link += ingredient + ','
	return api_to_json(api_link)['recipes']

def recipe_title(json):
	return json['title']

def recipe_source_url(json):
	return json['source_url']

def recipe_id(json):
	return json['recipe_id']

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
	print search_json(['cheese', 'bread'])
	print recipe_json(35382)
	print get_ingredients_dict(35382)