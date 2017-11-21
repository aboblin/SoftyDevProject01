from flask import Flask, render_template
import requests
import json

app = Flask(__name__)

@app.route('/')
def root():
	r = requests.get("https://api.nasa.gov/planetary/apod?api_key=CJIKeQKz4nuOpRSiMmW2qWB7qylNrE717O2q30Va")
	dictionary = r.json()
	return render_template('index.html', pic = dictionary['url'], info = dictionary["explanation"])
	
if __name__ == '__main__':
	app.run(debug = True)