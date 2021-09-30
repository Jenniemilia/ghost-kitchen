from db import db
from flask import session

def get_restaurant_id():
	return session.get("restaurant_id", 0)

def get_all_restaurants():
	sql = "SELECT * FROM restaurants"
	result = db.session.execute(sql)
	return result.fetchall()

def get_restaurant_info(restaurant_id):
	sql = """SELECT r.name, r.phone, r.email, r.description, s.style FROM restaurants r, styles s WHERE 
	s.restaurant_id=r.id"""
	result = db.session.execute(sql, {"restaurant_id": restaurant_id})
	return result.fetchall()

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
	sql = """SELECT menu.menu, menu.price FROM restaurants, menu WHERE menu.restaurant_id= 
	restaurant_id"""
	result = db.session.execute(sql, {"restaurant_id": restaurant_id})
	return result.fetchall()




