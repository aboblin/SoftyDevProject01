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
       for rID in recipeIDs[:10]:
              print rID
              if len(diff) < 3:
                     ingreds = getIngreds(rID)
                     rDiff = calcDiff(ingreds, info)
                     diff[rID] = rDiff
              elif len(diff) == 3 & getSt(info):
                     print diff
                     return diff.keys()
              elif rDiff < max(diff.values()):
                     for key, value in diff.items():
                            if value == max(diff.values()):
                                   del diff[key]
                                   break;
                     ingreds = getIngreds(rID)
                     rDiff = calcDiff(ingreds, info)
                     diff[rID] = rDiff
       return diff.keys()
       
@app.route('/', methods=['GET','POST'])
def root():
       if request.method == 'POST':
              info = getInfo()
              i = findRecipes(info)
              ts = []
              for r in i:
                     ts += getTS(r)
              while len(ts) < 6:
                     ts += ["",""]
              return render_template('recipes.html', recipe_one = ts[0], recipe1url = ts[1], recipe_two = ts[2], recipe2url = ts[3], recipe_three = ts[4], recipe3url = ts[5])
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

def getSt(info):
       return info["protein"] == -1 & info["carb"] == -1 & info["fat"] == -1

if __name__ == '__main__':
	app.run(debug = True)
        
