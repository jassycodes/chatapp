from flask import Flask, render_template, request, Response, make_response, jsonify, json
from flask import redirect, url_for 
import requests
import os
import re
import html
import sqlite3
from datetime import datetime, date
import time

app = Flask(__name__)

connection = sqlite3.connect('data/chatapp.db')
c = connection.cursor()

#auto creates current time particular to the timezone that they're in
CURRENT_TIME = time.strftime('%H:%M:%S')

# c.execute('''DROP TABLE IF EXISTS chats''')

	# (id INTEGER PRIMARY KEY AUTOINCREMENT, message VARCHAR(500) NOT NULL, date_posted default CURRENT_DATE, time_posted default TIME('now', 'localtime'), FOREIGN KEY(user_id) REFERENCES users(id), FOREIGN KEY(username) REFERENCES users(username))''')

c.execute('''CREATE TABLE IF NOT EXISTS chats 
			 (id INTEGER PRIMARY KEY AUTOINCREMENT, message VARCHAR(500) NOT NULL, date_posted default CURRENT_DATE, [timestamp] default timestamp, user_id, username, FOREIGN KEY(user_id) REFERENCES users(id), FOREIGN KEY(username) REFERENCES users(username))''')

# c.execute("INSERT INTO chats(message, username, timestamp) VALUES(?, ?, ?);", ("This is a sample message", "jasssss", CURRENT_TIME))

c.execute('''CREATE TABLE IF NOT EXISTS message 
			 (id INTEGER PRIMARY KEY AUTOINCREMENT, message VARCHAR(300) NOT NULL, date_posted default CURRENT_DATE, sender_id INTEGER, receiver_id INTEGER, FOREIGN KEY(sender_id) REFERENCES users(id), FOREIGN KEY(receiver_id) REFERENCES users(id))''')

c.execute('''CREATE TABLE IF NOT EXISTS users
			 (id INTEGER PRIMARY KEY AUTOINCREMENT, username VARCHAR(50) NOT NULL, password VARCHAR(12) NOT NULL, fname text, lname text, birthday date)''')

# c.execute("CREATE TABLE IF NOT EXISTS chats(id INTEGER PRIMARY KEY AUTOINCREMENT, message VARCHAR(500) NOT NULL, date_posted default CURRENT_DATE NOT NULL, [timestamp] default timestamp NOT NULL, FOREIGN KEY(username) REFERENCES users(username))")

# c.execute("INSERT INTO users(username, password, fname) VALUES(?,?,?);", ("jassycodes", "polygloter03", "Jasmine"))
# c.execute("INSERT INTO users(username, password, fname) VALUES(?,?,?);", ("morsal11", "polygloter11", "Morsal"))

connection.commit()
connection.close()

@app.route("/chat")
def chatapp():
	username = request.cookies.get('sessionID')
	return render_template('index.html', username=username)

@app.route("/register")
def registerPage():
	return render_template('register.html')


@app.route("/register", methods=['POST'])
def registerTwitter():
	username = request.form.get('username')
	password = request.form.get('pword')

	status = ""
	connection = sqlite3.connect('data/twitter.db')
	c = connection.cursor()

	userFound = True

	c.execute("SELECT username FROM users WHERE username=?",(username,))
	
	if c.fetchone() is tuple:
		username_in_db = c.fetchone()[0]
		if username_in_db != username:
			userFound = False
			c.execute("INSERT INTO users(username, password) VALUES(?,?);", (username, password))
			status = "Succesfully created your account!"
		else:
			userFound = True
			status = "'" + username + "' already exists"
	else:
		userFound = False
		c.execute("INSERT INTO users(username, password) VALUES(?,?);", (username, password))
		status = "Succesfully created your account!"

	connection.commit()
	connection.close()

	return render_template('register.html', status_CreateUser=status)

@app.route("/clearmessages", methods=['POST'])
def clearmessages():
	#access the database
	connection = sqlite3.connect('data/chatapp.db')
	c = connection.cursor()

	#remove the table
	c.execute('''DROP TABLE IF EXISTS chats''')
	#create same table again
	c.execute('''CREATE TABLE IF NOT EXISTS chats 
			 (id INTEGER PRIMARY KEY AUTOINCREMENT, message VARCHAR(500) NOT NULL, date_posted default CURRENT_DATE, [timestamp] default timestamp, user_id, username, FOREIGN KEY(user_id) REFERENCES users(id), FOREIGN KEY(username) REFERENCES users(username))''')

	connection.commit()
	connection.close()

	return "MESSAGES SUCCESSFULLY DELETED"

@app.route("/login")
def loginTwitter():
	return render_template('login.html')

@app.route("/logout")
def logoutTwitter():
	print("attempting to delete cookie")
	
	resp = make_response(redirect('/login'))
	resp.set_cookie('userID', '', expires=0)

	return resp


@app.route("/login-user", methods=['POST'])
def loginUser():
	username = request.form.get('username')
	password = request.form.get('pword')

	status = ""
	connection = sqlite3.connect('data/chatapp.db')
	c = connection.cursor()

	userFound = False

	print('login GET')
	c.execute("SELECT username FROM users WHERE username='{}'".format(username))

	fetch = c.fetchone()
	print(type(fetch))
	if type(fetch) is tuple:
		#print("Object exists")
		username_in_db = fetch[0]
		resp = ''
		if username_in_db == username:
			userFound = True
			c.execute("SELECT password FROM users WHERE username=?",(username,))
			password_in_db = c.fetchone()[0]
			connection.commit()
			connection.close()

			if password == password_in_db:
				status = "Succesfully logged in"
				loggedIn = True
				resp = make_response(redirect('/chat'))
				resp.set_cookie('sessionID', username)
				return resp
			else:
				status = "Wrong password"
				resp = make_response(render_template('login.html', status_LogIn=status))
				return resp
	else:
		status = "'" + username + "' doesn't exist"
		resp = make_response(render_template('login.html', status_LogIn=status))
		return resp

@app.route("/")
def redirectToLogin():

	return redirect('/login')

@app.route("/getchats", methods=['GET'])
def fetchall():
	print("/getchats")
	username = request.cookies.get('sessionID')
	print(request.cookies)
	
	if request.cookies['sessionID'] == username:
		connection = sqlite3.connect('data/chatapp.db')
		c = connection.cursor()

		c.execute("SELECT * FROM chats")
		messageList = c.fetchall()

		print(messageList)
			
		connection.commit()
		connection.close()

		return jsonify(messageList)

@app.route("/sample")
def sample():
	return render_template('samplechat.html')

@app.route("/sendtochatbox", methods=['POST'])
def send():
	print("/sendtochatbox")
	# user = request.form.get('username')
	user = request.cookies.get('sessionID') #username from the log in screen

	message = request.form.get('message')

	connection = sqlite3.connect('data/chatapp.db')
	c = connection.cursor()

	#assigning a variable userFound as False .. we're assuming that we haven't found the user
	userFound = False 
	username_verified = "" #a variable where we hold the verified username
	user_fname = "" #name of user based off of the users table
	user_id = 0 #getting id based off of the users table
	error_msg = "" #error message

	#query for checking if username exists in the database
	c.execute("SELECT username FROM users WHERE username='{}'".format(user))

	if c.fetchone() is not None:
		c.execute("SELECT username FROM users WHERE username='{}'".format(user))
		username_verified = c.fetchone()[0] #[username] -> c.fetchone() != string of the username, will always be a list
		print("username_verified: ")
		print(username_verified) 
		userFound = True
		c.execute("SELECT fname FROM users WHERE username='{}'".format(username_verified)) #getting first name
		user_fname = c.fetchone()[0]
		c.execute("SELECT id FROM users WHERE username='{}'".format(username_verified))
		user_id = c.fetchone()[0]
	else:
		print("Empty")
		error_msg = " no username '" + user + "' found"

	if userFound == True:
		# c.execute("INSERT INTO message(message, user_id, username) VALUES(?,?,?);", (message, user_id, username_verified))
		c.execute("INSERT INTO chats(message, timestamp, user_id, username) VALUES(?, ?, ?, ?);", (message, CURRENT_TIME, user_id, username_verified))
		connection.commit()
		connection.close()
		print("Adding message: " + message + " by: " + user_fname + " with the username: " + username_verified)
		return json.dumps({'status':'OK','message': message, 'username': username_verified, 'name': user_fname });
	else:
		print(user + "not found in the database")
		return json.dumps({'status':'OK','error_msg': error_msg });

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



