from flask import Flask, render_template, request
from utils.recipe_func import *
from utils.nutri_func import *
import requests
import json

app = Flask(__name__)

def findRecipes(info):
       recipes = getRecipes(info["search"])
       recipeIDs = getRecipeIDs(recipes)

       diff = {}
       for rID in recipeIDs:
              ingreds = getIngreds(rID)
              rDiff = calcDiff(ingreds, info)
              print rDiff
              '''
              if len(diff) < 3:
                     diff[rDiff] = rID
              elif rDiff < max(diff):
                     del diff[max(diff)]
                     diff[rDiff] = rID
       return diff
       chosen = []
       chosen1 = recipeIDs[differences.index(min(differences))]
       differences.pop(differences.index(min(differences)))
       chosen2 = recipeIDs[differences.index(min(differences))]
       differences.pop(differences.index(min(differences)))
       chosen3 = recipeIDs[differences.index(min(differences))]
       differences.pop(differences.index(min(differences)))

       return chosen
       '''
       
@app.route('/', methods=['GET','POST'])
def root():
       if request.method == 'POST':
              info = getInfo()
              findRecipes(info)
              return render_template('temp.html', search = info['search'])
       else:
              return render_template('index.html')

def getInfo():
       info = {'protein': -1, 'carb': -1, 'fat': -1}
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
        
