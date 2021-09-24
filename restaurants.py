from db import db

def get_all_restaurants():
	sql = "SELECT * FROM restaurants ORDER BY name"
	result = db.session.execute(sql)
	return result.fetchall()


def get_reviews(restaurants_id):
	sql = """SELECT u.name, r.stars, r.comment FROM reviews r, users u WHERE r.users_id=u.id 
	AND r.restaurants_id=:restaurants_id ORDER BY r.id"""
	return db.session.execute(sql, {"restaurants_id" :restaurants_id}).fetchall()

def add_reviews(restaurants_id, users_id, stars, comment):
	sql = """INSERT INTO reviews (restaurants_id, users_id, stars, comment) VALUES (:restaurants:id, :users_id, 
	:stars, :comment)"""
	db.session.execute(sql, {"restaurants_id":restaurants_id,"users_id":users_id, "stars":stars, "comment":comment})
	db.session.commit() 
