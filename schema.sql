CREATE TABLE restaurants 
	(id SERIAL PRIMARY KEY, name TEXT, phone TEXT, email TEXT, description TEXT);
CREATE TABLE styles 
	(id SERIAL PRIMARY KEY, restaurants_id REFERENCES style TEXT);
CREATE TABLE users 
	(id SERIAL PRIMARY KEY, username TEXT, password TEXT, admin BOOLEAN);
CREATE TABLE reviews 
	(id SERIAL PRIMARY KEY, restaurant_id INTEGER REFERENCES restaurants, user_id INTEGER REFERENCES users, comment TEXT, starts INTEGER, created TIMESTAMP);
CREATE TABLE menu 
	(id SERIAL PRIMARY KEY, restaurant_id INTEGER REFERENCES restaurants, menu TEXT, price FLOAT);
