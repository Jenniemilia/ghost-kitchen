from app import app
from flask import redirect, render_template, request

import users, restaurants
 

@app.route("/")
def index():
	return render_template("index.html", restaurants = restaurants.get_all_restaurants())



#Lisää tarkistus onko Admin jolloin lisää toimintoja
@app.route("/login", methods=["get", "post"])
def login():
	if request.method == "GET":
		return render_template("login.html")
	if request.method == "POST":
		username = request.form["username"]
		password = request.form["password"]
		if users.login(username, password):
			return redirect("/")
	return render_template("error.html", message="Väärä käyttäjätunnus tai salasana")
			
	
		
			

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")



@app.route("/register", methods=["get","post"])
def register():
	if request.method == "GET":
		return render_template("register.html")
	if request.method == "POST":
		username = request.form["username"]
		if len(username) < 3 or len(username) > 25:
			return render_template("error.html", message = "Tunnuksessasi tulisi olla 3-25 merkkiä, kokeile uudelleen")
		password1 = request.form["password1"]
		password2 = request.form["password2"]
		if password1 != password2:
			return render_template("error.html", message="Salasanat eivät täsmää, tarkista oikeinkirjoitus ja yritä uudestaan!")
		
		role = request.form["role"]
		if role not in ("1", "2"):
			return render_template("error.html", message="Tällaista käyttäjää ei ole olemassa")
		if not users.register(username, password1, role):
			return render_template("error.html", message="Rekisteröinti ei jostain syystä onnistunut, yritä uudelleen")
	return redirect("/")

#Ravintolan hakutoiminto, lisää vielä niin että listus toimii ja tulee näkyviin etusivulle
@app.route("/result")
def result():
	query = request.args["query"]
	result = restaurants.get_query(query)
	return render_template("result.html", query=query, result = result)
	

@app.route("/homepage/<int:restaurant_id>")
def homepage(restaurant_id):
	restaurant = restaurants.get_restaurant_info(restaurant_id)
	menu = restaurants.get_restaurant_menu(restaurant_id)
	info = restaurants.get_restaurant_info(restaurant_id)
	reviews = restaurants.get_review(restaurant_id)
	return render_template("homepage.html", reviews= reviews, id = restaurant_id, restaurant=restaurant, menu=menu, info=info)


@app.route("/ownerpage/<int:restaurant_id>")
def ownerpage(restaurant_id):
	restaurant = restaurants.get_restaurant_info(restaurant_id)
	menu = restaurants.get_restaurant_menu(restaurant_id)
	info = restaurants.get_restaurant_info(restaurant_id)

	return render_template("ownerpage.html", id = restaurant_id, restaurant=restaurant, menu=menu, info=info)


@app.route("/userpage<int:user_id>")
def userpage(user_id):
	user = users.get_user_info(user_id)

	return render_template("userpage", id=user_id, user= user)
	pass


@app.route("/review", methods=["post"])
def review():
	users.require_role(1)
	users.check_csrf()
	restaurant_id=request.form["restaurant_id"]
	stars = int(request.form["stars"])
	if stars < 1 or stars > 5:
		return render_template("error.html", message="Valitettavasti arvostelussa oli virheellinen määrä tähtiä, yritä uudelleen")

	comment = request.form["comment"]
	if comment == "":
		comment = " - "

	restaurants.add_review(restaurant_id, users.user_id(), stars, comment)
	return redirect("/homepage/" + str(restaurant_id))

#ravintoloitsija voi lisätä ravintoloita
@app.route("/add", methods=["get", "post"])
def add_restaurant():
	users.require_role(2)
	pass

@app.route("/remove", methods=["get", "post"])
def remove_restaurant():
	users.require_role(2)
	pass


