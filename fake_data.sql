#passwords hashed using sha_256
INSERT INTO user (username, password, name, email) VALUES
('johndoe7', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 'John Doe', 'johndoe@example.com'), #password123
('seller87654', 'fbb4a8a163ffa958b4f02bf9cabb30cfefb40de803f2c4c346a9d39b3be1b544', 'Jane Doe', 'janedoe@example.com'), #securepass
('alidaly', '13dc8554575637802eec3c0117f41591a990e1a2d37160018c48c9125063838a', 'Alice Smith', 'alice.smith@example.com'), #alicepass
('bob', '65868526cf148ae6c44d1aec28fcd15c86312652a38bc130e776500e067c81d6', 'Bob Johnson', 'bob.johnson@example.com'), #bobsecure
('BJ412', 'e012494d67eeb3d7686fb0eb984cdea526744c008ffd8e0dcbc656fdaf6aeb54', 'Bill Johnson', 'BJ012@example.com'); #billspassword

INSERT INTO address (street_number, street, city, state, zip, user_id) VALUES
(123, 'Main St', 'New York', 'NY', '10001', 1),
(456, 'Broadway Ave', 'New York', 'New York', '10002', 2),
(789, 'Market St', 'San Francisco', 'CA', '94105', 3),
(101, 'Pine St', 'Seattle', 'Washington', '98101', 4),
(101, 'Pine St', 'Seattle', 'Washington', '98101', 5);

INSERT INTO store (name, description, owner_id) VALUES
('John\'s Craft Supplies', 'A haven for all your crafting needs.', 1),
('Jane\'s Boutique', 'Fashion and accessories.', 2),
('Alice\'s Books', 'A collection of the best books.', 3),
('Bob\'s Tools', 'All kinds of tools and hardware.', 4);

INSERT INTO item (name, description, quantity, price, store_id) VALUES
('Acrylic Paint Set', '12 vibrant colors for artists of all levels.', 25, 19.99, 1),
('Paintbrush Set', '10-piece set with various brush sizes.', 30, 14.99, 1),
('Colored Pencils', 'Set of 10 colored pencils.', 50, 4.99, 1),
('Canvas Panels', 'Pack of 5 primed canvas panels.', 20, 12.99, 1),

('Handbag', 'Stylish and durable handbag.', 15, 89.99, 2),
('Cotton Fabric', '100% cotton fabric, 2 yards.', 40, 9.99, 2),
('Sewing Kit', 'Essential sewing tools in a compact kit.', 35, 15.99, 2),
('Embroidery Thread', 'Set of 36 vibrant embroidery threads.', 50, 6.99, 2),
('Quilting Ruler', '12-inch acrylic quilting ruler.', 25, 8.99, 2),
('Dress', 'Elegant evening dress.', 8, 129.99, 2),

('Pride and Prejudice', 'A classic novel by Jane Austen.', 20, 9.99, 3),
('1984', 'Dystopian novel by George Orwell.', 25, 8.99, 3),
('The Great Gatsby', 'A masterpiece by F. Scott Fitzgerald.', 15, 10.99, 3),
('To Kill a Mockingbird', 'Harper Lee\'s Pulitzer Prize-winning novel.', 30, 7.99, 3),
('Moby Dick', 'Herman Melville\'s epic tale of a great white whale.', 10, 12.99, 3),
('War and Peace', 'Leo Tolstoy\'s historical novel.', 8, 14.99, 3),
('The Catcher in the Rye', 'J.D. Salinger\'s coming-of-age story.', 18, 11.99, 3),
('The Hobbit', 'J.R.R. Tolkien\'s fantasy classic.', 22, 13.99, 3),
('Crime and Punishment', 'A psychological drama by Fyodor Dostoevsky.', 12, 14.99, 3),
('The Odyssey', 'Homer\'s ancient Greek epic.', 14, 10.99, 3),

('Hammer', 'Durable steel hammer.', 12, 19.99, 4),
('Wood Carving Tools', '10-piece set for detailed wood carving.', 20, 34.99, 4),
('Plywood Sheets', 'Pack of 3 high-quality plywood sheets.', 15, 49.99, 4),
('Wood Glue', 'Strong adhesive for woodworking projects.', 40, 5.99, 4),
('Sandpaper Pack', 'Set of 20 sheets in varying grits.', 50, 9.99, 4);

INSERT INTO cart (user_id, item_id, quantity) VALUES
(1, 18, 1), -- John added The Hobbit
(1, 6, 10), -- John added ten cotton fabrics
(3, 3, 1); -- bill added colored pencils

INSERT INTO wantlist (user_id, item_id, list_name) VALUES
(1, 7, 'Wish List'), -- John wants a Sewing kit
(1, 21, 'tool wishlist'), -- John wants a hammer 
(2, 2, 'Future Buys'), -- Jane wants a Paintbrush set
(4, 11, 'Books to buy'), -- Bob wants Pride and Prejudice
(4, 12, 'Books to buy'); -- Bob wants 1984

INSERT INTO sale (shipped, buyer_id, store_id) VALUES
(TRUE, 1, 2), -- John bought something from Jane's Boutique
(FALSE, 3, 1); -- Alice bought something from John's crafts

INSERT INTO item_sold (sale_id, item_id, quantity) VALUES
(1, 5, 1), -- John bought one Handbag
(2, 10, 1); -- Alice bought one Dress
