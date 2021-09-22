import requests
import json
import threading
import beautifulsoup
from flask import Flask, request

App = Flask('')

@app.route('/')
def home():
    return "LOHS System Online"

def run():
    app.run(host='0.0.0.0',port=8080)

def keep_alive():
    t = threading.Thread(target=run)
    t.start()

@app.route('/register', methods=['GET'])
def register():
    print(request.json)