import json, requests

def getKey():
        f = open('key','r')
        key = f.read()
        f.close()
        return key
	


#input an api_link, returns json of data recieved from the api
def api_to_json(api_link):
	url = requests.get(api_link)
	return url.json()

def search_json(ingredients):
	api_link = "http://food2fork.com/api/search?key=90c4ebe5b63a775a3d75b20f0dab1906&q="
	for ingredient in ingredients:
		api_link += ingredient + ','
	return api_to_json(api_link)

def recipe_json(recipeID):
	api_link = "http://food2fork.com/api/get?key=90c4ebe5b63a775a3d75b20f0dab1906&rId=" + str(recipeID)
	return api_to_json(api_link)['recipe']

def get_ingredients_dict(recipeID):
	dic = {}
	for ingredient in recipe_json(recipeID)['ingredients']:
		ing_list = ingredient.split(' ')
		removable_parts = ing_list[0].encode("utf-8") + " " + ing_list[1].encode("utf-8")
		dic[ingredient[len(removable_parts)+1:].encode("utf-8")] = [ing_list[0].encode("utf-8"), ing_list[1].encode("utf-8")]
	print dic
		

def get_source_url(recipeID):
	return recipe_json(recipeID)['source_url']

def get_title(recipeID):
	return recipe_json(recipeID)['title']

def get_publisher(recipeID):
	return recipe_json(recipeID)['publisher']

if __name__ == "__main__":
	#print search_json(['cheese', 'bread'])
	#print recipe_json(35382)
	print get_ingredients_dict(35382)
	#print get_source_url(35382)
	#print get_title(35382)
	#print get_publisher(35382)
