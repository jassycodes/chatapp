from flask import Flask, render_template, request, Response, make_response, jsonify, json
from flask import redirect, url_for 
import requests
import os
import re
import html
import sqlite3
import datetime

app = Flask(__name__)

connection = sqlite3.connect('data/chatapp.db')
c = connection.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS message 
			 (id INTEGER PRIMARY KEY AUTOINCREMENT, message VARCHAR(300) NOT NULL, date_posted default CURRENT_DATE, sender_id INTEGER, receiver_id INTEGER, FOREIGN KEY(sender_id) REFERENCES users(id), FOREIGN KEY(receiver_id) REFERENCES users(id))''')

c.execute('''CREATE TABLE IF NOT EXISTS users
			 (id INTEGER PRIMARY KEY AUTOINCREMENT, username text NOT NULL, password VARCHAR(12) NOT NULL, fname text, lname text, birthday date)''')

# c.execute("INSERT INTO users(username, password, fname) VALUES(?,?,?);", ("jassycodes", "polygloter03", "Jasmine"))
# c.execute("INSERT INTO users(username, password, fname) VALUES(?,?,?);", ("morsal11", "polygloter11", "Morsal"))

connection.commit()
connection.close()

@app.route("/")
def homepage():
	return render_template('index.html')

@app.route("/sample")
def sample():
	return render_template('samplechat.html')

@app.route("/sendmessage", methods=['POST'])
def send():
	sender = request.form.get('sender')
	receiver = request.form.get('receiver')	
	a_message = request.form.get('message')

	print(sender)
	print(receiver)


	connection = sqlite3.connect('data/chatapp.db')
	c = connection.cursor()

	sender_id = 0
	receiver_id = 0
	senderFound = False
	receiverFound = False
	sender_name = ""
	receiver_name = ""
	error_msg = ""

	#query for checking if username sender exists in the database
	c.execute("SELECT id FROM users WHERE username='{}'".format(sender))

	if c.fetchone() is not None:
		c.execute("SELECT id FROM users WHERE username='{}'".format(sender))
		sender_id = c.fetchone()[0]
		print("sender_id: ")
		print(sender_id)
		senderFound = True
		c.execute("SELECT fname FROM users WHERE username='{}'".format(sender))
		sender_name = c.fetchone()[0]
	else:
		print("Empty")
		error_msg = " no username '" + sender + "' found"

	#query for checking if username receiver exists in the database
	c.execute("SELECT id FROM users WHERE username='{}'".format(receiver))
	# print(c.fetchall())
	if c.fetchone() is not None:
		c.execute("SELECT id FROM users WHERE username='{}'".format(receiver))
		receiver_id = c.fetchone()[0]
		print("receiver_id: ")
		print(receiver_id)
		receiverFound = True
		c.execute("SELECT fname FROM users WHERE username='{}'".format(receiver))
		receiver_name = c.fetchone()[0]
	else:
		print("Empty")
		error_msg += " no username '" + receiver + "' found"

	if senderFound == True and receiverFound == True:
		c.execute("INSERT INTO message(message, sender_id, receiver_id) VALUES(?,?,?);", (a_message, sender_id, receiver_id))
		connection.commit()
		connection.close()
		print("adding sender_name: " + str(sender_name) + " and receiver_name: " + receiver_name)
		return json.dumps({'status':'OK','a_message':a_message, 'sender': sender_name, 'receiver': receiver_name });
	else:
		print("either receiver or sender not found in the database")
		return json.dumps({'status':'OK','error_msg': error_msg });





# @app.route('/signUpUser', methods=['POST'])
# def signUpUser():
#     user =  request.form['username'];
#     password = request.form['password'];
#     return json.dumps({'status':'OK','user':user,'pass':password});


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

	


