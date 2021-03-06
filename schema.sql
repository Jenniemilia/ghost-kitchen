CREATE TABLE restaurants 
	(id SERIAL PRIMARY KEY, name TEXT, phone TEXT, email TEXT, description TEXT);
CREATE TABLE styles 
	(id SERIAL PRIMARY KEY, restaurant_id  INTEGER REFERENCES restaurants, style TEXT);
CREATE TABLE users 
	(id SERIAL PRIMARY KEY, name TEXT UNIQUE, password TEXT, role INTEGER);
CREATE TABLE reviews 
	(id SERIAL PRIMARY KEY, restaurant_id INTEGER REFERENCES restaurants, user_id INTEGER REFERENCES users, comment TEXT, 
	stars INTEGER, created TIMESTAMP, visible BOOLEAN);
CREATE TABLE menu 
	(id SERIAL PRIMARY KEY, restaurant_id INTEGER REFERENCES restaurants, dish TEXT, price FLOAT);
CREATE TABLE favorites
	(id SERIAL PRIMARY KEY, restaurant_id INTEGER REFERENCES restaurants, user_id INTEGER REFERENCES users, choice BOOLEAN);
CREATE TABLE orders
	(ID SERIAL PRIMARY KEY, restaurant_id INTEGER REFERENCES restaurants, user_id INTEGER REFERENCES users, created TIMESTAMP);
CREATE TABLE DELIVERY 
	(ID SERIAL PRIMARY KEY, order_id INTEGER REFERENCES orders, dish_id INTEGER REFERENCES menu);