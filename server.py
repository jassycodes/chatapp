from flask import Flask, render_template, request, Response, make_response, jsonify
from flask import redirect, url_for 
import requests
import os
import re
import html
import sqlite3
import datetime

app = Flask(__name__)

# connection = sqlite3.connect('data/travel.db')
# c = connection.cursor()

# connection.commit()
# connection.close()

@app.route("/")
def homepage():
	return render_template('index.html')

@app.route("/randomstring")
def rndmstring():
	return "this is a randomstring";


@app.route("/hackernews", methods=['GET'])
def hacker():
	response = requests.get('https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty')
	top_ten_ids = response.json()[:10]
	print("hello test hackernews")
	print(top_ten_ids)

	top10_titles = []
	stories = []

	for top_id in top_ten_ids:
		response_url = 'https://hacker-news.firebaseio.com/v0/item/{}.json?print=pretty'.format(top_id)
		response = requests.get(response_url)
		stories.append(response.json()) 

	for story in stories:
		top10_titles.append(story['title'])

		top10_titles.sort()
	return jsonify(top10_titles)

@app.route("/random_string")
def rndm_string():
	return "another random string"


if __name__ == '__main__':
   app.run()

	


