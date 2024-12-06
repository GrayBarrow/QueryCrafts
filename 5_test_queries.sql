# Display user_id given the correct username and hashed password:
SELECT user_id 
FROM user 
WHERE username = 'bob' AND password = '65868526cf148ae6c44d1aec28fcd15c86312652a38bc130e776500e067c81d6';

# gives single cell user_id of 4, which is what bob's is
	# this is 'bobsecure' hashed using SHA_256


# Display cart of John (user_id=1):
SELECT cart.item_id, item.name, cart.quantity, item.price
FROM cart JOIN item ON cart.item_id = item.item_id
WHERE cart.user_id = 1;

# given fake_data.sql, should give two items:
	# item 6, Cotton Fabric, 10 pieces, at 9.99 each
	# item 18, The Hobbit, 1 copy, at 13.99
    

# Display Bob's (user_id=4) wishlist "Books to buy":
SELECT wantlist.item_id, item.name, item.price
FROM wantlist JOIN item ON wantlist.item_id = item.item_id
WHERE wantlist.user_id = 4 AND wantlist.list_name = "Books to buy";

#given fake_data.sql, should give two items:
	# item 11, Pride and Prejudice, at 9.99
    # item 12, 1984, at 8.99
    
    
# Display Alice's (user_id=3) orders:
SELECT sale.sale_id, store.name, sale.shipped
FROM sale JOIN store ON sale.store_id = store.store_id
WHERE sale.buyer_id = 3;

# should give single sale:
	#sale 2, from John's Craft Supplies, it has not shipped yet
    
    
# Display Jane's Boutique's (store_id=2) sales:
SELECT sale.sale_id, sale.shipped, user.username, address.street_number, address.street, address.city, address.state, address.zip
FROM (sale JOIN address ON sale.buyer_id = address.user_id) JOIN user ON sale.buyer_id = user.user_id
WHERE store_id = 2;

# should give single sale:
	# sale 1, it has shipped, buyer is John, address: 123 Main St. New York, NY. 10001