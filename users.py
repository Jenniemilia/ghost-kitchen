#from os import name
import os
from db import db
from flask import session, abort, request
from werkzeug.security import check_password_hash, generate_password_hash

def user_id():
    return session.get("user_id", 0)

def login(name, password):
    sql = "SELECT password, id, role FROM users WHERE name=:name"
    result = db.session.execute(sql, {"name":name})
    user = result.fetchone()
    if not user:
        return False
    if check_password_hash(user.password, password):
        session["user_id"] = user.id
        session["user_name"] = name
        session["user_role"] = user.role
        session["csrf_token"] = os.urandom(16).hex()
        return True
    return False

def get_all_users():
    sql = "SELECT id, name, password FROM users"
    result = db.session.execute(sql)
    return result.fetchall()

def logout():
    del session["user_name"], session["user_id"], session["user_role"], session["csrf_token"]

def register(name, password, role):
	hash_value = generate_password_hash(password)
	try:
		sql = "INSERT INTO users (name, password, role) VALUES (:name, :password, :role)"
		db.session.execute(sql, {"name":name, "password":hash_value, "role":role})
		db.session.commit()
	except:
		return False
    
	return login(name, password)

def check_csrf():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

def require_role(role):
    if role > session.get("user_role", 0):
        abort(403)

def get_user_info(user_id):
    sql = "SELECT name FROM users WHERE id=:user_id"
    result = db.session.execute(sql, {"user_id":user_id})
    return result.fetchone()

def add_favorite(restaurant_id, user_id):
    sql = """INSERT INTO favorites (restaurant_id, user_id, choice) VALUES 
    (:restaurant_id, :user_id, TRUE)"""
    db.session.execute(sql, {"restaurant_id":restaurant_id, "user_id":user_id})
    db.session.commit()

def delete_favorite(restaurant_id, user_id):
    sql = "UPDATE favorites SET choice= FALSE where resturant_id=:restaurant_id AND user_id=:user_id"
    db.session.execute(sql, {"restaurant_id":restaurant_id, "user_id":user_id})
    db.session.commit()

def get_favorites():
    sql = """SELECT DISTINCT restaurants.name FROM restaurants, favorites WHERE 
    favorites.restaurant_id=restaurants.id AND choice=TRUE"""
    result = db.session.execute(sql)
    return result.fetchall()

def get_favorites_by_restaurant(restaurant_id):
    sql="""SELECT restaurant_id, user_id, choice FROM favorites WHERE restaurant_id=:restaurant_id"""
    result = db.session.execute(sql, {"restaurant_id":restaurant_id})
    return result.fetchall()


