from app import app
from db import db
from flask import redirect, render_template, request, session

import users, restaurants


@app.route("/")
def index():
	
	return render_template("index.html", restaurants = restaurants.get_all_restaurants())


@app.route("/login", methods=["GET", "POST"])
def login():
	if request.method == "GET":
		return render_template("login.html")
	if request.method == "POST":
		username = request.form["username"]
		password = request.form["password"]
		if users.login(username, password):
			session["username"] = username
			return redirect("/")
		else:
			return render_template("error.html", message="Väärä käyttäjätunnus tai salasana")

@app.route("/logout")
def logout():
        users.logout()
        return redirect("/")



@app.route("/register", methods=["GET","POST"])
def register():
	if request.method == "GET":
		return render_template("register.html")
	if request.method == "POST":
		username = request.form["username"]
		password1 = request.form["password1"]
		password2 = request.form["password2"]
		if password1 != password2:
			return render_template("error.html", message="Salasanat eivät täsmää, tarkista oikeinkirjoitus ja yritä uudestaan!")
		if users.register(username, password1):
			return redirect("/")
		else:
			return render_template("error.html", message="Rekisteröinti ei onnistunut")



@app.route("/result")
def result():
	query = request.args["query"]
	sql = """SELECT restaurants.name FROM restaurants, styles WHERE 
	styles.restaurants_id = restaurants.id AND style LIKE :query"""
	result = db.session.execute(sql, {"query": "%"+query+"%"})
	restaurants = result.fetchall()
	return render_template("result.html", restaurants=restaurants)

@app.route("/restauranthomepage/<int:restaurants_id>")
def restauranthomepage(restaurants_id):
	info = restaurants.get_info(restaurants_id)
	return render_template("restauranthomepage.html", restaurants_id=restaurants_id, info=info)

