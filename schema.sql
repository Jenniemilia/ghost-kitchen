CREATE TABLE restaurants 
	(id SERIAL PRIMARY KEY, name TEXT, phone TEXT, email TEXT, description TEXT);
CREATE TABLE styles 
	(id SERIAL PRIMARY KEY, restaurant_id  INTEGER REFERENCES restaurants, style TEXT);
CREATE TABLE users 
	(id SERIAL PRIMARY KEY, name TEXT, password TEXT, role INTEGER);
CREATE TABLE reviews 
	(id SERIAL PRIMARY KEY, restaurant_id INTEGER REFERENCES restaurants, user_id INTEGER REFERENCES users, comment TEXT, stars INTEGER, created TIMESTAMP);
CREATE TABLE menu 
	(id SERIAL PRIMARY KEY, restaurant_id INTEGER REFERENCES restaurants, dish TEXT, price FLOAT);

