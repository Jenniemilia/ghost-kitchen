from app import app
from flask import redirect, render_template, request

import users, restaurants
 

@app.route("/")
def index():
	top_rated = restaurants.get_top_review()
	favorites = users.get_favorites()
	return render_template("index.html", users = users.get_all_users(), restaurants = restaurants.get_all_restaurants(), top_rated=top_rated, favorites=favorites)

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

@app.route("/result")
def result():
	query = request.args["query"]
	if len(query) < 1 or len(query) > 15:
		return render_template("error.html", message = "Hakusanassa on oltava vähintään yksi kirjain, koita uudestaan!")
	result = restaurants.get_query(query)
	return render_template("result.html", query=query, result = result)
	

@app.route("/homepage/<int:restaurant_id>")
def homepage(restaurant_id):
	restaurant = restaurants.get_restaurant_info(restaurant_id)
	menu = restaurants.get_restaurant_menu(restaurant_id)
	info = restaurants.get_restaurant_info(restaurant_id)
	reviews = restaurants.get_review(restaurant_id)
	favorites = users.get_favorites_by_restaurant(restaurant_id)
	user_id=users.user_id()
	return render_template("homepage.html", reviews= reviews, user_id=user_id, id = restaurant_id, restaurant=restaurant, menu=menu, info=info, favorites=favorites)
	

@app.route("/favorite", methods=["post"])
def favorite():
	users.check_csrf
	user_id=users.user_id()
	restaurant_id=request.form["restaurant_id"]
	users.add_favorite(restaurant_id, user_id)
	return redirect("/homepage/" + str(restaurant_id))

@app.route("/not_favorite", methods=["post"])
def not_favorite():
	users.check_csrf
	user_id=users.user_id()
	restaurant_id=request.form["restaurant_id"]
	users.delete_favorite(restaurant_id, user_id)
	return redirect("/homepage/" + str(restaurant_id))
 
@app.route("/ownerpage/<int:restaurant_id>")
def ownerpage(restaurant_id):
	restaurant = restaurants.get_restaurant_info(restaurant_id)
	menu = restaurants.get_menu_id(restaurant_id)
	return render_template("ownerpage.html", id = restaurant_id, menu=menu, restaurant=restaurant)

@app.route("/remove", methods=["post"])
def remove_dish():
	users.require_role(2)
	users.check_csrf()
	restaurant_id=request.form["restaurant_id"]
	menu_id=request.form["menu_id"]
	restaurants.remove_dish(menu_id)
	return redirect("/ownerpage/" + str(restaurant_id))

@app.route("/newdish", methods=["post"])
def new_dish():
	users.require_role(2)
	users.check_csrf()
	restaurant_id=request.form["restaurant_id"]
	dish=request.form["dish"]
	price=request.form["price"]
	restaurants.add_dish(restaurant_id, dish, price)
	return redirect("/")

@app.route("/userpage/<int:user_id>")
def userpage(user_id):
	user_id = users.user_id() 
	user = users.get_user_info(user_id)

	return render_template("userpage.html", user= user)
	
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





