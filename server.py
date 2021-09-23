import requests
import json
import threading
import bs4 as beautifulsoup
from flask import Flask, request, render_template

class statuses:
	class forbidden:
		status = "403"
		description = "You do not have access to this page."

App = Flask('')

@App.route('/')
def home():
    return "SCP API"

def run():
    App.run(host='0.0.0.0',port=8080)

if __name__ == "__main__":
	print("System on")
	Thread = threading.Thread(target=run)
	Thread.start()

@App.route('/api/scps/', methods=['GET'])
def getScp():
	print("get")
	print(request)
	return render_template('errors/error.html', status=statuses.forbidden.status, description=statuses.forbidden.description), 403

@App.route('/api', methods=['GET'])
def loadDocumentation():
	return render_template('documentation/index.html')