import json, requests

#Input an api_link, returns json of data recieved from the api
def api_to_json(api_link):
	url = requests.get(api_link)
	return url.json()

def search_json(ingredients):
	api_link = "http://food2fork.com/api/search?api=API_KEY&q="
	for ingredient in ingredients:
		 api_link += ingredient + ','
	return api_to_json(api_link)

def recipe_json(recipeID):
	api_link = "http://food2fork.com/api/get?api=API_KEY&rID=" + str(recipeID)
	return api_to_json(api_link)

def get_ingredients(recipeID):
	return recipe_json(recipeID)['ingredients']

def get_source_url(recipeID):
	return recipe_json(recipeID)['source_url']

def get_title(recipeID):
	return recipe_json(recipeID)['title']

def get_publisher(recipeID):
	return recipe_json(recipeID)['publisher']

if __name__ == "__main__":
	print search_json(['cheese', 'bread'])
	print recipe_json(12345)
	print get_ingredients(12345)
	print get_source_url(12345)
	print get_title(12345)
	print get_publisher(12345)