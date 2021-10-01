from db import db
from flask import session

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

def get_reviews(restaurant_id):
	sql = """SELECT u.name, r.stars, r.comment FROM users u, reviews r WHERE r.user_id=u.id 
	AND r.restaurant_id=:restaurant_id ORDER BY r.id"""
	return db.session.execute(sql, {"restaurant_id" :restaurant_id}).fetchall()
	pass

def add_reviews(restaurant_id, user_id, stars, comment):
	sql = """INSERT INTO reviews (restaurant_id, user_id, stars, comment) VALUES (:restaurant:id, :user_id, 
	:stars, :comment)"""
	db.session.execute(sql, {"restaurant_id":restaurant_id,"user_id":user_id, "stars":stars, "comment":comment})
	db.session.commit()

def get_restaurant_menu(restaurant_id):
	sql = """SELECT menu.dish, menu.price FROM menu WHERE menu.restaurant_id= 
	:restaurant_id"""
	result = db.session.execute(sql, {"restaurant_id": restaurant_id})
	return result.fetchall()


def get_query(query): 
	sql = """SELECT restaurants.name, restaurants.description FROM restaurants, styles WHERE 
	styles.restaurant_id = restaurants.id AND style ILIKE :query"""
	result = db.session.execute(sql, {"query": "%"+query+"%"})
	result = result.fetchall()
	return result




