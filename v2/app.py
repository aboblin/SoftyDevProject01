from flask import Flask, render_template, request
from utils.recipe_func import *
from utils.nutri_func import *
import requests
import json

app = Flask(__name__)

def findRecipes(searchTerms):
       recipes = getRecipes(searchTerms)
       recipeIDs = getRecipeIDs(recipes)

       differences = []

       for recipeID in recipeIDs:
              ingreds = 
              nutrient_info = sumNutri(addDetails(get_ingredients_dict(recipeID)))
              differences.append(abs(nutrient_info[0] - carbamount) + abs(nutrient_info[1] - proteinamount) + abs(nutrient_info[2] - fatamount))
       chosen = []
       chosen1 = recipeIDs[differences.index(min(differences))]
       differences.pop(differences.index(min(differences)))
       chosen2 = recipeIDs[differences.index(min(differences))]
       differences.pop(differences.index(min(differences)))
       chosen3 = recipeIDs[differences.index(min(differences))]
       differences.pop(differences.index(min(differences)))

       return chosen

@app.route('/', methods=['GET','POST'])
def root():
       if request.method == 'POST':
              info = getInfo()
              return render_template('temp.html', search = info['search'])
       else:
              return render_template('index.html')

def getInfo():
       info = {'protein': 0.0, 'carb': 0.0, 'fat': 0.0}
       info['search'] = request.form['food']
       if request.form["protein"] != "":
              info['protein'] = float(request.form["protein"])
       if request.form["carb"] != "":
              info['carb'] = float(request.form['carb'])
       if request.form['fat'] != "":
              info['fat'] = float(request.form['fat'])    
       return info

if __name__ == '__main__':
	app.run(debug = True)
