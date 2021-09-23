import requests
import json
import threading
import bs4 as BeautifulSoup
from flask import Flask, request, render_template

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
    return "SCP API"

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

@App.route('/api/scps/<scp>')
def getScp(scp=None):
    if scp.isnumeric():
        SCPLoad = requests.get(f"https://scp-wiki.wikidot.com/scp-{scp}")

        if SCPLoad.ok:
            Soup = BeautifulSoup(SCPLoad.text)
            Soup.prettify()

            Result = {
                "found": False,
                "scp_info": {
                    "item_number": "",
                    "object_class": "",
                    "description": ""
                }
            }

            Div = Soup.find('div', {'id': 'page-content'})
            Children = Div.findChildren("div" , recursive=False)
            for Child in Children:
                return Child
        else:
            return SCPLoad
    else:
        return error(statuses.badRequest.status, statuses.badRequest.description)