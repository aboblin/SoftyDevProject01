from flask import Flask
import json, requests

url = requests.get("http://food2fork.com/api/search?key=90c4ebe5b63a775a3d75b20f0dab1906&q=shredded%20chicken")

print url.json();