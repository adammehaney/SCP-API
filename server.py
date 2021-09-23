import requests
import json
import threading
import random
from bs4 import BeautifulSoup
from flask import Flask, request, render_template, redirect

class statuses:
	class forbidden:
		status = "403"
		description = "You do not have access to this page."
	class badRequest:
		status = "400"
		description = "You did not input a valid SCP name or number!"

App = Flask('')

@App.route('/')
def home():
	return redirect("/api/", code=301)

def run():
	App.run(host='0.0.0.0',port=8080)

def error(status, description):
	return render_template('errors/error.html', status=status, description=description), int(status)

if __name__ == "__main__":
	print("System on")
	Thread = threading.Thread(target=run)
	Thread.start()

# @App.route('/api/scps/', methods=['GET'])
# def getScps():
# 	print("get")
# 	print(request)
# 	return error(statuses.forbidden.status, statuses.forbidden.description)

@App.route('/api/', methods=['GET'])
def loadDocumentation():
	return render_template('documentation/index.html')

@App.route('/api/endpoints', methods=['GET'])
def loadEndpoints():
	return render_template('documentation/endpoints.html')

@App.route('/api/scps/<scp>')
def getScp(scp=None):
	if int(scp):
		SCPLoad = requests.get(f"https://scp-wiki.wikidot.com/scp-{scp}")

		if SCPLoad.ok:
			Soup = BeautifulSoup(SCPLoad.text, 'html.parser')
			Soup.prettify()

			Result = {
				"found": False,
				"scp_info": {
					"item_number": "",
					"object_class": "",
					"description": ""
				}
			}

			Div = Soup.find_all('strong')

			for Child in Div:
				Text = Child.text.strip()
				if Text == "Item #:":
					Result["found"] = True
					Result["scp_info"]["item_number"] = Child.next_sibling.text.strip()

				if Text == "Object Class:":
					Result["scp_info"]["object_class"] = Child.next_sibling.text.strip()

				if Text == "Description:":
					Sibling = Child.parent.find_next_sibling()
					while True:				
						if Sibling.name.strip() != "p":
							break

						Result["scp_info"]["description"] += Sibling.text.strip()

						Sibling = Sibling.find_next_sibling()


			return json.dumps(Result)
		else:
			return SCPLoad
	else:
		return error(statuses.badRequest.status, statuses.badRequest.description)

@App.route('/api/randomscp/')
def randomScp():
	return getScp(random.randrange(6999))