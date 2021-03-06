from app import app
from flask import redirect, render_template, request, flash

import users, restaurants
 

@app.route("/")
def index():
	top_rated = restaurants.get_top_review()
	user_id = users.user_id()
	favorites = users.get_favorites(user_id)	
	return render_template("index.html",user_id=user_id, users = users.get_all_users(), restaurants = restaurants.get_all_restaurants(), top_rated=top_rated, favorites=favorites)

@app.route("/login", methods=["get", "post"])
def login():
	if request.method == "GET":
		return render_template("login.html")
	if request.method == "POST":
		username = request.form["username"]
		password = request.form["password"]
		if users.login(username, password):
			flash("Kirjautuminen onnistui", "success")
			return redirect("/")
	flash("Väärä käyttäjätunnus tai salasana", "error")	
	return render_template("login.html")			

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
			flash("Tunnuksessasi tulisi olla 3-25 merkkiä, kokeile uudelleen", "error")	
			return render_template("register.html")
		password1 = request.form["password1"]
		password2 = request.form["password2"]
		if password1 != password2:
			flash("Salasanat eivät täsmää, tarkista oikeinkirjoitus ja yritä uudestaan!", "error")
			return render_template("register.html")
		
		role = request.form["role"]
		if role not in ("1", "2"):
			flash("Tällaista käyttäjää ei ole olemassa", "error")
			return render_template("register.html")
		if not users.register(username, password1, role):
			flash("Rekisteröinti ei jostain syystä onnistunut, yritä uudelleen", "error")
			return render_template("register.html")
	return redirect("/")

@app.route("/result")
def result():
	query = request.args["query"]
	if len(query) < 1 or len(query) > 15:
		flash("Hakusanassa on oltava vähintään yksi kirjain, koita uudestaan!", "error")
		return render_template("/result")
	result = restaurants.get_query(query)
	return render_template("result.html", query=query, result = result)
	

@app.route("/homepage/<int:restaurant_id>")
def homepage(restaurant_id):
	menu = restaurants.get_restaurant_menu(restaurant_id)
	info = restaurants.get_restaurant_info(restaurant_id)
	reviews = restaurants.get_review(restaurant_id)
	user_id = users.user_id()
	favorites = users.get_favorites_by_restaurant(restaurant_id, user_id)	
	return render_template("homepage.html", reviews= reviews, user_id=user_id, id = restaurant_id, restaurants=restaurants.get_all_restaurants(), menu=menu, info=info, favorites=favorites)
	

@app.route("/favorite", methods=["post"])
def favorite():
	users.check_csrf
	user_id = users.user_id()
	restaurant_id = request.form["restaurant_id"]
	users.add_favorite(restaurant_id, user_id)
	flash("Ravintola lisätty suosikiksi", "success")
	return redirect("/homepage/" + str(restaurant_id))

@app.route("/not_favorite", methods=["post"])
def not_favorite():
	users.check_csrf
	user_id=users.user_id()
	restaurant_id=request.form["restaurant_id"]
	users.delete_favorite(restaurant_id, user_id)
	flash("Ravintola poistettu suosikeista", "success")
	return redirect("/homepage/" + str(restaurant_id))
 
@app.route("/ownerpage/<int:restaurant_id>")
def ownerpage(restaurant_id):
	restaurant = restaurants.get_restaurant_info(restaurant_id)
	menu = restaurants.get_menu_id(restaurant_id)
	reviews = restaurants.get_review(restaurant_id)
	styles = restaurants.get_styles()
	orders = restaurants.get_orders(restaurant_id)
	top_orders = restaurants.get_top_orders(restaurant_id)
	return render_template("ownerpage.html", id = restaurant_id, menu=menu, restaurant=restaurant, reviews=reviews, styles=styles, orders=orders, top_orders=top_orders)

@app.route("/add_restaurant", methods=["post"])
def add_restaurant():
	users.require_role(2)
	users.check_csrf()
	restaurant_id=request.form["restaurant_id"]
	name=request.form["name"]
	if len(name) < 1 or len(name) > 20:
		flash("Ravintolan nimessä tulee olla 1-20 kirjainta, yritä uudestaan", "error")
		return render_template("/add_restaurant")
	phone=request.form["phone"]
	if len(phone) < 1 or len(phone) > 20:
		flash("Ravintolan puhelinnumerossa tulee olla 1-20 kirjainta, yritä uudestaan", "error")
		return render_template("/add_restaurant")
	email=request.form["email"]
	if len(email) < 1 or len(email) > 50:
		flash("Ravintolan sähköpostissa tulee olla 1-50 kirjainta, yritä uudestaan", "error")
		return render_template("/add_restaurant")
	description=request.form["description"]
	if len(description) < 1 or len(description) > 50:
		flash("Ravintolan kuvauksessa tulee olla 1-50 kirjainta, yritä uudestaan", "error")
		return render_template("/add_restaurant")
	styles=request.form.getlist("style")
	new_style = request.form["new_style"]
	if new_style != "":
		x = new_style.split(", ")
		for i in x:
			styles.append(i)
	restaurants.add_restaurant(name, phone, email, description, styles)
	flash("Ravintolan lisääminen onnistui, kuvan voit lisätä jälkikäteen", "success")
	return redirect("/")

@app.route("/remove", methods=["post"])
def remove_dish():
	users.require_role(2)
	users.check_csrf()
	restaurant_id=request.form["restaurant_id"]
	menu_id=request.form["menu_id"]
	restaurants.remove_dish(menu_id)
	flash("Ruokalaji poistettu", "success")
	return redirect("/ownerpage/" + str(restaurant_id))

@app.route("/newdish", methods=["post"])
def new_dish():
	users.require_role(2)
	users.check_csrf()
	restaurant_id=request.form["restaurant_id"]
	dish=request.form["dish"]
	price=request.form["price"]
	restaurants.add_dish(restaurant_id, dish, price)
	flash("Ruokalajin lisääminen onnistui", "success")
	return redirect("/ownerpage/" + str(restaurant_id))

@app.route("/remove_comment", methods=["post"])
def remove_comment():
	users.require_role(2)
	users.check_csrf()
	restaurant_id=request.form["restaurant_id"]
	reviews_id=request.form["reviews_id"]
	restaurants.remove_comment(reviews_id)
	flash("Kommentin poisto onnistui", "success")
	return redirect("/ownerpage/" + str(restaurant_id))
	
@app.route("/review", methods=["post"])
def review():
	users.require_role(1)
	users.check_csrf()
	restaurant_id=request.form["restaurant_id"]
	stars = int(request.form["stars"])
	if stars < 1 or stars > 5:
		flash("Valitettavasti arvostelussa oli virheellinen määrä tähtiä, yritä uudelleen", "error")
		return redirect("/homepage/" + str(restaurant_id))
	comment = request.form["comment"]
	if comment == "":
		comment = " - "
	restaurants.add_review(restaurant_id, users.user_id(), stars, comment)
	flash("Arvostelun lisäys onnistui", "success")
	return redirect("/homepage/" + str(restaurant_id))

@app.route("/orders", methods=["post"])
def orders():
	user_id = users.user_id()
	restaurant_id=request.form["restaurant_id"]
	if not user_id:
		flash("Kirjaudu sisään niin pääset tekemään tilauksen loppuun", "error")
		return redirect("/homepage/" + str(restaurant_id))
	
	dishes=request.form.getlist("dish")
	restaurants.orders(restaurant_id, user_id, dishes)
	flash("Ruuat laitettu tilaukseen, kiitos!", "success")
	return redirect("/homepage/" + str(restaurant_id))






