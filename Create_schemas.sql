CREATE DATABASE querycrafts;

USE querycrafts;

CREATE TABLE user (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE address (
    street_number INT NOT NULL,
    street VARCHAR(100) NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(50) NOT NULL,
    zip VARCHAR(5) NOT NULL,
    user_id INT NOT NULL,
    PRIMARY KEY (street_number, street, city, state, zip, user_id),
    FOREIGN KEY (user_id) REFERENCES user(user_id),
    CHECK (zip REGEXP '^[0-9]{5}$')
);

CREATE TABLE store (
    store_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    owner_id INT NOT NULL,
    FOREIGN KEY (owner_id) REFERENCES user(user_id)
);

CREATE TABLE item (
    item_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    quantity INT NOT NULL CHECK (quantity >= 0),
    price DECIMAL(10, 2) NOT NULL CHECK (price >= 0),
    store_id INT NOT NULL,
    FOREIGN KEY (store_id) REFERENCES store(store_id)
);

CREATE TABLE cart (
    user_id INT NOT NULL,
    item_id INT NOT NULL,
    quantity INT NOT NULL CHECK (quantity > 0),
    PRIMARY KEY (user_id, item_id),
    FOREIGN KEY (user_id) REFERENCES user(user_id),
    FOREIGN KEY (item_id) REFERENCES item(item_id)
);

CREATE TABLE wantlist (
    user_id INT NOT NULL,
    item_id INT NOT NULL,
    list_name VARCHAR(100) NOT NULL,
    PRIMARY KEY (user_id, item_id, list_name),
    FOREIGN KEY (user_id) REFERENCES user(user_id),
    FOREIGN KEY (item_id) REFERENCES item(item_id)
);

CREATE TABLE sale (
    sale_id INT AUTO_INCREMENT PRIMARY KEY,
    shipped BOOLEAN DEFAULT FALSE,
    buyer_id INT NOT NULL,
    store_id INT NOT NULL,
    FOREIGN KEY (buyer_id) REFERENCES user(user_id),
    FOREIGN KEY (store_id) REFERENCES store(store_id)
);

CREATE TABLE item_sold (
    sale_id INT NOT NULL,
    item_id INT NOT NULL,
    quantity INT NOT NULL CHECK (quantity > 0),
    PRIMARY KEY (sale_id, item_id),
    FOREIGN KEY (sale_id) REFERENCES sale(sale_id),
    FOREIGN KEY (item_id) REFERENCES item(item_id)
);
