from flask import Flask, render_template, request
from utils.recipe_func import *
from utils.nutri_func import *
import requests
import json

app = Flask(__name__)

def findRecipes(item):
       recipes=search_json(item)
       if request.form["carb"] == "":
              carbamount = 0
       else:
              carbamount = float(request.form["carb"])
       if request.form["protein"] == "":
              proteinamount = 0
       else:
              proteinamount = float(request.form["protein"])
       if request.form["fat"] == "":
              fatamount = 0
       else:
              fatamount = float(request.form["fat"])
       recipeIDs = []
       for recipe in recipes:
              recipeIDs.append(recipe_id(recipe))
       differences = []
       for recipeID in recipeIDs:
              nutrient_info = sumNutri(addDetails(get_ingredients_dict(recipeID)))
              differences.append(abs(nutrient_info[0] - carbamount) + abs(nutrient_info[1] - proteinamount) + abs(nutrient_info[2] - fatamount))
       chosen = []
       chosen1 = recipeIDs[differences.index(min(differences))]
       chosen.append(chosen1)
       differences.pop(differences.index(min(differences)))
       chosen2 = recipeIDs[differences.index(min(differences))]
       chosen.append(chosen2)
       differences.pop(differences.index(min(differences)))
       chosen3 = recipeIDs[differences.index(min(differences))]
       chosen.append(chosen3)
       differences.pop(differences.index(min(differences)))
       return chosen

@app.route('/', methods=['GET','POST'])
def root():
       if request.method == 'POST':
              search = request.form["food"]
              return render_template('temp.html', search = search)
       else:
              return render_template('index.html')

	
if __name__ == '__main__':
	app.run(debug = True)
