from flask import session
from db import db

#from random import randint

def get_restaurant_id():
	return session.get("restaurant_id", 0)

def get_all_restaurants():
	sql = "SELECT id, name, description FROM restaurants"
	result = db.session.execute(sql)
	return result.fetchall()

def get_restaurant_info(restaurant_id):
	sql = """SELECT name, phone, email, description FROM restaurants WHERE 
	id=:restaurant_id"""
	result = db.session.execute(sql, {"restaurant_id": restaurant_id})
	return result.fetchone()

def get_review(restaurant_id):
	sql = """SELECT r.id, u.name, r.stars, r.comment, r.created FROM users u, reviews r WHERE r.user_id=u.id 
	AND r.restaurant_id=:restaurant_id AND r.visible=TRUE ORDER BY r.id"""
	return db.session.execute(sql, {"restaurant_id" :restaurant_id}).fetchall()

def get_top_review():
	sql = """SELECT restaurants.name, CAST(AVG(stars)AS INTEGER) as avg_stars FROM restaurants, reviews WHERE 
	reviews.restaurant_id=restaurants.id GROUP by restaurants.name ORDER BY avg_stars desc LIMIT 3"""
	return db.session.execute(sql).fetchall()
	

def add_review(restaurant_id, user_id, stars, comment):
	sql = """INSERT INTO reviews (restaurant_id, user_id, stars, comment, created) VALUES (:restaurant_id, 
	:user_id, :stars, :comment, NOW())"""
	db.session.execute(sql, {"restaurant_id":restaurant_id, "user_id":user_id, "stars":stars, "comment":comment})
	db.session.commit()

def get_restaurant_menu(restaurant_id):
	sql = """SELECT menu.dish, menu.price FROM menu WHERE menu.restaurant_id= 
	:restaurant_id AND menu.visible=TRUE"""
	result = db.session.execute(sql, {"restaurant_id": restaurant_id})
	return result.fetchall()

def get_menu_id(restaurant_id):
	sql="""SELECT menu.id, menu.dish, menu.price FROM menu WHERE menu.restaurant_id=
	:restaurant_id AND menu.visible=TRUE"""
	result = db.session.execute(sql, {"restaurant_id": restaurant_id})
	return result.fetchall()


def get_query(query): 
	sql = """SELECT DISTINCT restaurants.id, restaurants.name, restaurants.description FROM restaurants, 
	styles WHERE styles.restaurant_id = restaurants.id AND style ILIKE :query"""
	result = db.session.execute(sql, {"query": "%"+query+"%"})
	result = result.fetchall()
	return result

def get_styles():
	sql = "SELECT DISTINCT style FROM styles"
	result = db.session.execute(sql)
	return result

def add_restaurant(name, phone, email, description):
	sql = """INSERT INTO restaurants restaurant.name, restaurant.phone, restaurant.style, restaurant.descriprion VALUES 
	(:name, :phone, :email, :description)"""
	db.session.execute(sql, {"name":name, "phone":phone, "email":email, "description":description })
	db.session.commit()

def remove_dish(menu_id):
	sql = "UPDATE menu SET visible=FALSE WHERE menu.id=:menu_id"
	db.session.execute(sql, {"menu_id":menu_id})
	db.session.commit()

def add_dish(restaurant_id, dish, price):
	sql = """INSERT INTO menu (restaurant_id, dish, price, visible) VALUES (:restaurant_id, 
	:dish, :price, TRUE)"""
	db.session.execute(sql, {"restaurant_id":restaurant_id, "dish":dish, "price":price})
	db.session.commit()

def remove_comment(reviews_id):
	sql = "UPDATE reviews SET visible=FALSE WHERE reviews.id=:reviews_id"
	db.session.execute(sql, {"reviews_id":reviews_id})
	db.session.commit()
	
	

