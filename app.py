from flask import Flask, render_template, request
import requests
import json

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def root():
	#r = requests.get("https://api.nasa.gov/planetary/apod?api_key=CJIKeQKz4nuOpRSiMmW2qWB7qylNrE717O2q30Va")
	#dictionary = r.json()
       if request.method == 'POST':
                return render_template('recipes.html')
       else:
	        return render_template('index.html')

	
if __name__ == '__main__':
	app.run(debug = True)
