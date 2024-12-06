import mysql.connector
from rich.console import Console
from rich.table import Table
import hashlib
import os
from dotenv import load_dotenv

def run_query(query, params=None):
    """
    Helper function to easily run queries
    :param query: query to be executed
    :param params: values to be replaced in query
    :return: dictionary with query results
    """
    cursor = connection.cursor(dictionary=True)
    if params is None:
        cursor.execute(query)
    else:
        cursor.execute(query, params)
    return cursor.fetchall()

def hashpass(password):
    """
    Helper function to hash password using SHA_256
    :param password: password to hash
    :return: hashed password
    """
    return hashlib.sha256(password.encode()).hexdigest()

def user_login():
    """
    Prompts user to login using username and password.
    Passwords in database are stored as hash values using SHA_256.
    :return: user_id after successful login
    """
    for i in range(10, 0, -1):
        console.print("Please enter your username and password to log in.", style="bold green")
        username = input("Username: ")
        password = input("Password: ")
        hashed_password = hashpass(password)
        #check database for match
        cursor = connection.cursor(dictionary=True)
        query = """
        SELECT user_id 
        FROM user 
        WHERE username = %s AND password = %s"""
        cursor.execute(query, (username, hashed_password))
        result = cursor.fetchone()

        if result:
            return result["user_id"]
        else:
            console.print(f"Invalid username or password. You have {i} attempts left.", style="bold red")
    print("You have run out of attempts. Exiting.")
    exit(0)

def print_header(text):
    """
    Helper function to print header with title
    :param text: title
    :return: None
    """
    length = len(text)+6
    spaces = (80-length)//2
    console.print("=" * 80, style="bold cyan")
    console.print(' ' * spaces + f"🌟  [bold magenta]{text.upper()}[/bold magenta]  🌟")
    console.print("=" * 80, style="bold cyan")

def print_footer(text):
    """
    Helper function to print footer with instructions
    :param text: instructions
    :return: None
    """
    length = len(text)
    spaces = (80 - length) // 2
    console.print("=" * 80, style="bold cyan")
    console.print(' '*spaces, f"{text}", style="dim")
    console.print("=" * 80, style="bold cyan")


def show_start_screen():
    """
    Prints start screen with initial options as table. [option numbers, name, description]
    :return: None
    """
    print_header("QUERYCRAFTS MARKETPLACE")

    table = Table(show_header=False, box=None)
    table.add_row("[bold]1[/bold]  🏪 Your Stores", "- Manage your stores")
    table.add_row("[bold]2[/bold]  🏙️ Other Stores", "- View other stores and their items")
    table.add_row("[bold]3[/bold]  📝 Want-lists", "- View and manage items in your want-lists")
    table.add_row("[bold]4[/bold]  🛒 Cart", "- View and manage items in your cart")
    table.add_row("[bold]5[/bold]  📦 Bought Items", "- View status of bought items")
    table.add_row("[bold]0[/bold]  🚪 Exit", "- Quit the application")
    console.print(table)

    print_footer("Type the number corresponding to your choice.")


def print_users_stores(user_id):
    """
    Prints stores owned by specified user as table. [store ID, name, description]
    :param user_id: user who owns stores to be printed
    :return: None
    """
    query = """
    SELECT store_id, name, description
    FROM store
    WHERE owner_id = %s"""
    result = run_query(query, [user_id])
    print_header("Your Stores")
    table = Table(show_header=False, box=None)
    table.add_column("Store ID", justify="right", style="cyan", no_wrap=True)
    table.add_column("Name", style="green")
    table.add_column("Description")
    for store in result:
        table.add_row(
            str(store["store_id"]),
            store["name"],
            '-' + store["description"]
        )
    console.print(table)

def print_store_manager_screen(store_id):
    """
    Prints screen for managing store options as table. [option number, managing option]
    :param store_id: store to manage
    :return: None
    """
    #print 1 manage listed stock
    #print 2 manage orders
    query = """
    SELECT name
    FROM store
    WHERE store_id = %s"""
    name = run_query(query, [store_id])[0]['name']
    print_header(f"MANAGE: {name}")
    table = Table(show_header=False, box=None)
    table.add_column("Option number", justify="right", style="cyan", no_wrap=True)
    table.add_column("Manager option", style="green")
    table.add_row("1", "Manage listed stock items")
    table.add_row("2", "Manage orders")
    console.print(table)


def get_price(message="Item price: "):
    """
    Helper function to get float in price format
    :param message: prompt for input
    :return: (float) price
    """
    while True:
        try:
            price = float(input(message))
            formatted_price = round(price, 2)
            return formatted_price
        except:
            print("Invalid input")

def get_int(message="Quantity: "):
    """
    Helper function to get integer for quantity
    :param message: prompt for input
    :return: (int) quantity
    """
    while True:
        try:
            q = int(input(message))
            return q
        except:
            print("Invalid input")

def add_item(store_id):
    """
    Adds item to store, including setting its required attributes.
    :param store_id: Store to add item to
    :return: None
    """
    name = input("Item name: ")
    price = get_price()
    quantity = get_int()
    description = input("(Optional, press enter if none) Item description: ")
    description = description if description else None
    query = """
    INSERT INTO item (name, price, quantity, description, store_id)
    VALUES (%s, %s, %s, %s, %s)"""
    run_query(query, [name, price, quantity, description, store_id])
    connection.commit()

def print_item_editor(item_id):
    """
    Prints item attributes for editing as table. [number option, item attribute or action]
    :param item_id: item to edit
    :return: None
    """
    # print table with options 1-5, 1name, 2description, 3price, 4qantity, 5delete
    query = """
    SELECT name, price, quantity, description
    FROM item
    WHERE item_id = %s"""
    result = run_query(query, [item_id])
    name = result[0]['name']
    price = str(result[0]['price'])
    quantity = str(result[0]['quantity'])
    description = result[0]['description']
    print_header(name)
    table = Table(show_header=False, box=None)
    table.add_column("Option number", justify="right", style="cyan", no_wrap=True)
    table.add_column("Attribute", style="green")
    table.add_column("Value")
    table.add_row("1", "Name", name)
    table.add_row("2", "Description", description)
    table.add_row("3", "Price", price)
    table.add_row("4", "Quantity", quantity)
    table.add_row("5", "Remove", "")
    console.print(table)

def edit_item_name(item_id):
    """
    Edit name of item
    :param item_id: item to edit
    :return: None
    """
    name = input("New item name: ")
    query = """
    UPDATE item
    SET name = %s
    WHERE item_id=%s"""
    run_query(query, [name, item_id])
    connection.commit()

def edit_item_desc(item_id):
    """
    Edit description of item
    :param item_id: item to edit
    :return: None
    """
    description = input("New item description: ")
    query = """
    UPDATE item
    SET description = %s
    WHERE item_id=%s"""
    run_query(query, [description, item_id])
    connection.commit()

def edit_item_price(item_id):
    """
    Edit the price of an item
    :param item_id: item to edit
    :return: None
    """
    price = get_price("New price: ")
    query = """
    UPDATE item
    SET price = %s
    WHERE item_id=%s"""
    run_query(query, [price, item_id])
    connection.commit()

def edit_item_quant(item_id):
    """
    Edit the stock quantity of an item
    :param item_id: item to edit
    :return: None
    """
    quantity = get_int("New quantity: ")
    query = """
    UPDATE item
    SET quantity = %s
    WHERE item_id=%s"""
    run_query(query, [quantity, item_id])
    connection.commit()

def remove_item(item_id):
    """
    Removed item from database, including in cart and want-lists. Not in historical sale data, however.
    :param item_id: item to remove
    :return: None
    """
    query1 = """
    DELETE FROM item
    WHERE item_id = %s"""
    query2 = """
    DELETE FROM wantlist
    WHERE item_id = %s"""
    query3 = """
    DELETE FROM cart
    WHERE item_id = %s"""
    run_query(query3, [item_id])
    run_query(query2, [item_id])
    run_query(query1, [item_id])
    connection.commit()

def print_sales(store_id):
    """
    Prints sales that a store has made in table. [sale ID, buyer username, buyer address, shipped status]
    :param store_id: store whose sales are listed
    :return: None
    """
    query = """
    SELECT name
    FROM store
    WHERE store_id = %s"""
    store_name = run_query(query,[store_id])[0]['name']
    print_header(f"{store_name} orders")
    query = """
    SELECT sale.sale_id, sale.shipped, user.username, address.street_number, address.street, address.city, address.state, address.zip
    FROM (sale JOIN address ON sale.buyer_id = address.user_id) JOIN user ON sale.buyer_id = user.user_id
    WHERE store_id = %s"""
    result = run_query(query, [store_id])
    table = Table(show_header=False, box=None)
    table.add_column("Sale ID", justify="right", style="cyan", no_wrap=True)
    table.add_column("username", style="green")
    table.add_column("address")
    table.add_column("shipped", style="dim")
    for sale in result:
        address = " ".join([str(sale['street_number']), sale['street'], sale['city'], sale['state'], sale['zip']])
        shipped = "Shipped" if sale['shipped'] else "Not Shipped"
        table.add_row(
            str(sale["sale_id"]),
            str(sale["username"]),
            address,
            shipped
        )
    console.print(table)

def ship_sale(sale_id):
    """
    Change shipping status of sale from not shipped to shipped (not vice versa)
    :param sale_id: sale to change shipping status
    :return: None
    """
    query = """
    UPDATE sale
    SET shipped = TRUE
    WHERE shipped = FALSE and sale_id = %s"""
    run_query(query, [sale_id])
    connection.commit()

def print_all_stores(user_id):
    """
    Prints list of all stores that are not owned by user as table. [store ID, name, description]
    :param user_id: user's stores to not include in list
    :return: None
    """
    query = """
    SELECT store_id, name, description
    FROM store
    WHERE owner_id != %s"""
    result = run_query(query, [user_id])

    print_header("Stores")
    table = Table(show_header=False, box=None)
    table.add_column("Store ID", justify="right", style="cyan", no_wrap=True)
    table.add_column("Name", style="green")
    table.add_column("Description")
    for store in result:
        table.add_row(
            str(store["store_id"]),
            store["name"],
            '-'+store["description"]
        )
    console.print(table)

def print_store_items(store_id):
    """
    Prints items listed in specified store as table. [item ID, name, price, stock quantity]
    :param store_id: store that has items to be printed
    :return: None
    """
    # get a table with all the items of the user inputted store_id
    query = """
    SELECT item_id, name, price, quantity
    FROM item
    WHERE store_id = %s"""
    result = run_query(query, [store_id])
    if (len(result) == 0):
        raise Exception("Store not found")

    print_header("Items")
    table = Table(show_header=False, box=None)
    table.add_column("Item ID", justify="right", style="cyan")
    table.add_column("Name", style="green")
    table.add_column("Price")
    table.add_column("Quantity", style='dim')

    for item in result:
        table.add_row(
            str(item["item_id"]),
            item["name"],
            str(item["price"]),
            str(item["quantity"])
        )

    console.print(table)

def print_item(item_id):
    """
    Prints item info in table. [item ID, description, price, stock quantity]
    :param item_id: item to detail
    :return: None
    """
    query = """
    SELECT name, description, price, quantity
    FROM item
    WHERE item_id = %s"""
    result = run_query(query, [item_id])
    if (len(result) == 0):
        raise Exception("Item not found")

    print_header(result[0]['name'])

    table = Table(show_header=False, box=None)
    table.add_column("Item ID", justify="right", style="cyan", no_wrap=True)
    table.add_column("Description", style="green")
    table.add_column("Price")
    table.add_column("Quantity", style='dim')
    table.add_row("", str(result[0]['description']), str(result[0]['price']), str(result[0]['quantity']))

    console.print(table)

def add_to_cart(item_id, quantity, user_id):
    """
    Adds item to user's cart at specific quantity
    :param item_id: item to add to cart
    :param quantity: quantity to add to cart (must not exceed stock quantity)
    :param user_id: user whose adding item to their cart
    :return: None
    """
    # decrement item.quantity by quantity
    query = """
    UPDATE item
    SET quantity = quantity - %s
    WHERE item_id = %s"""
    run_query(query, [quantity, item_id])
    # then add to cart table
    query = """
    INSERT INTO cart (user_id, item_id, quantity)
    VALUES (%s, %s, %s);
    """
    run_query(query, [user_id, item_id, quantity])
    connection.commit()

def print_cart(user_id):
    """
    Prints items in cart of user
    :param user_id: user who owns cart
    :return: None
    """
    query = """
    SELECT cart.item_id, item.name, cart.quantity, item.price
    FROM cart JOIN item ON cart.item_id = item.item_id
    WHERE cart.user_id = %s;"""
    result = run_query(query, [user_id])

    print_header("Cart")
    table = Table(show_header=False, box=None)
    table.add_column("Item ID", justify="right", style="cyan", no_wrap=True)
    table.add_column("Name", style="green")
    table.add_column("Price")
    table.add_column("Quantity", style='dim')
    total = 0
    for item in result:
        total += float(item["price"])*int(item['quantity'])
        table.add_row(
            str(item["item_id"]),
            item["name"],
            str(item["price"]),
            str(item["quantity"])
        )

    table.add_row("","Total:",str(round(total,2)),"")

    console.print(table)

def remove_from_cart(item_id, user_id):
    """
    Remove specific item from user's cart
    :param item_id: item to remove
    :param user_id: user who owns cart to remove item from
    :return: None
    """
    # get quantity
    query = """
    SELECT quantity
    FROM cart
    WHERE item_id = %s AND user_id = %s;"""
    q = run_query(query, [item_id, user_id])[0]['quantity']
    # remove from cart
    query = """
    DELETE FROM cart
    WHERE item_id = %s AND user_id = %s;"""
    run_query(query, [item_id, user_id])
    # then increment item.quantity by quantity
    query = """
    UPDATE item
    SET quantity = quantity + %s
    WHERE item_id = %s"""
    run_query(query, [q, item_id])
    connection.commit()

def clear_cart(user_id):
    """
    Clear's users cart (does not buy items, simply removes)
    :param user_id: user who owns cart to clear
    :return: None
    """
    query = """
    DELETE FROM cart
    WHERE user_id = %s;"""
    run_query(query, [user_id])
    connection.commit()

def buy_cart(user_id):
    """
    Adds items in user's cart to sales (does not include any transaction or pos info)
    :param user_id: user to buy cart of
    :return: None
    """
    query = """
    SELECT item.store_id, cart.item_id, cart.quantity
    FROM cart JOIN item ON cart.item_id = item.item_id
    WHERE cart.user_id = %s;"""
    result = run_query(query, [user_id])
    for tuple in result:
        #insert new sale tuple, if exists, ignore
        query = """
        INSERT IGNORE INTO sale (buyer_id, store_id)
        VALUES (%s, %s);"""
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, [user_id, tuple['store_id']])

        #insert new item_sold tuple
        query = """
        INSERT INTO item_sold (sale_id, item_id, quantity)
        VALUES (%s, %s, %s);"""
        run_query(query, [cursor.lastrowid, user_id, tuple['quantity']])
    connection.commit()
    clear_cart(user_id)

def print_wantlists(user_id):
    """
    Print names of user's want-lists
    :param user_id: owner of walt-lists
    :return: None
    """
    query = """
    SELECT DISTINCT list_name
    FROM wantlist
    WHERE user_id = %s;"""
    result = run_query(query, [user_id])
    print_header("Want-lists")
    table = Table(show_header=False, box=None)
    table.add_column("List name", style="green")
    for list in result:
        table.add_row(list['list_name'])
    console.print(table)

def print_list_items(user_id, list_name):
    """
    Print items is a user's specified want-list
    :param user_id: user to identify want-list
    :param list_name: name of list to print items from
    :return: None
    """
    query = """
    SELECT wantlist.item_id, item.name, item.price
    FROM wantlist JOIN item ON wantlist.item_id = item.item_id
    WHERE wantlist.user_id = %s AND wantlist.list_name = %s;"""
    result = run_query(query, [user_id, list_name])
    if (len(result) == 0):
        raise Exception("Want-list not found")
    print_header(list_name)
    table = Table(show_header=False, box=None)
    table.add_column("Item ID", justify="right", style="cyan", no_wrap=True)
    table.add_column("Name", style="green")
    table.add_column("Price")
    for item in result:
        table.add_row(
            str(item["item_id"]),
            item["name"],
            str(item["price"]),
        )
    console.print(table)

def add_item_to_wantlist(item_id, user_id, list_name):
    """
    Adds item to user's specified want-list
    :param item_id: item to add to list
    :param user_id: user who wants item
    :param list_name: list for item to go in
    :return: None
    """
    # check if given list_name is valid
    query = """
    SELECT list_name
    FROM wantlist
    WHERE list_name = %s AND user_id = %s;"""
    result = run_query(query, [list_name, user_id])
    # if list doesnt exist for that user, error, else add to wantlist
    if (len(result) == 0): #know result is returning something, must be next query
        raise Exception("Want-list not found")
    else:
        query = """
        INSERT INTO wantlist (user_id, item_id, list_name)
        VALUES (%s, %s, %s);"""
        run_query(query, [user_id, item_id, list_name])
        connection.commit()


def remove_item_from_wantlist(item_id, user_id, list_name):
    """
    Removes item from specified user's want-list
    :param item_id: item to be removed
    :param user_id: user who owns list
    :param list_name: list to remove item from
    :return: None
    """
    query = """
    DELETE FROM wantlist
    WHERE item_id = %s AND user_id = %s AND list_name = %s;"""
    run_query(query, [item_id, user_id, list_name])
    connection.commit()

def print_users_orders(user_id):
    """
    Prints user's orders in table. [Sale ID, store purchased from, shipped status]
    :param user_id: primary key for user
    :return: None
    """
    #display all sales
    query = """
    SELECT sale.sale_id, store.name, sale.shipped
    FROM sale JOIN store ON sale.store_id = store.store_id
    WHERE sale.buyer_id = %s;"""
    result = run_query(query, [user_id])
    print_header("Your Orders")
    table = Table(show_header=False, box=None)
    table.add_column("Sale ID", justify="right", style="cyan")
    table.add_column("Store", style="green")
    table.add_column("Shipped")
    for order in result:
        table.add_row(
            "order #:"+str(order['sale_id']),
            "From: "+order['name'],
            ("Shipped" if order['shipped'] else "Not Shipped"),
        )
    console.print(table)

def print_order(sale_id):
    """
    Prints item details of order in table. [item ID, item name, price, quantity]
    :param sale_id: primary key of sale
    :return: None
    """
    #print items, price, quantity, total price, and shipped status of order
    query = """
    SELECT item_sold.item_id, item.name, item.price, item_sold.quantity
    FROM item_sold JOIN item ON item_sold.item_id = item.item_id
    WHERE item_sold.sale_id = %s;"""
    result = run_query(query, [sale_id])
    if (len(result)==0):
        raise ValueError
    print_header("Order#:"+str(sale_id))
    table = Table(show_header=False, box=None)
    table.add_column("Item ID", justify="right", style="cyan")
    table.add_column("Name", style="green")
    table.add_column("Price")
    table.add_column("Quantity", style='dim')
    total_price = 0
    for item in result:
        total_price += item["price"]*item["quantity"]
        table.add_row(
            str(item["item_id"]),
            item["name"],
            str(item["price"]),
            str(item["quantity"]),
        )
    table.add_row("","Total", str(total_price),"")
    query = """
    SELECT shipped
    FROM sale
    WHERE sale_id = %s"""
    shipped = "Shipped" if run_query(query, [sale_id])[0]['shipped'] else "Not Shipped"
    table.add_row("", "Shipped status: ", shipped, "")
    console.print(table)


if __name__ == "__main__":
    try:
        console = Console()

        load_dotenv()

        DB_HOST = os.getenv("DB_HOST")
        DB_USER = os.getenv("DB_USER")
        DB_PASSWORD = os.getenv("DB_PASSWORD")
        DB_NAME = os.getenv("DB_NAME")

        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )

        # get user_id
        user_id = user_login()
        console.clear()
        #if match, display start screen, ready user specific relations
        while(True):
            show_start_screen()
            first_choice = input()
            console.clear()
            if (first_choice == "0"):
                print("exiting program")
                exit(0)
            # user's stores
            elif (first_choice == "1"):
                while(True):
                    print_users_stores(user_id)
                    print_footer("Type the number of the store you would like to manage. Type 0 to go back.")
                    store_choice = input()
                    console.clear()
                    if (store_choice == '0'):
                        console.clear()
                        break
                    else:
                        while(True):
                            # choice is store id, new choice to see listed items or sold items
                            try:
                                print_store_manager_screen(store_choice)
                            except:
                                console.clear()
                                print("Invalid input")
                                break
                            print_footer("Type the number corresponding to your choice. Type 0 to go back.")
                            manager_choice = input()
                            console.clear()
                            # listed items
                            if(manager_choice == '0'):
                                console.clear()
                                break
                            if(manager_choice == '1'):
                                while(True):
                                    print_store_items(store_choice)
                                    print_footer("Type the number of the item you wish to edit. Type 'add' to add an item. Type 0 to go back.")
                                    item_manage_choice = input()
                                    console.clear()
                                    if (item_manage_choice == '0'):
                                        console.clear()
                                        break
                                    elif (item_manage_choice == 'add'):
                                        add_item(store_choice)
                                        console.clear()
                                        print("Item added")
                                        continue
                                    else:
                                        while(True):
                                            try:
                                                print_item_editor(item_manage_choice)
                                            except:
                                                print("Invalid input")
                                                break
                                            print_footer("Type the number corresponding to the attribute to edit it. Type 0 to go back.")
                                            attribute_choice = input()
                                            console.clear()
                                            if (attribute_choice == '0'):
                                                console.clear()
                                                break
                                            elif(attribute_choice == '1'):
                                                edit_item_name(item_manage_choice)
                                                console.clear()
                                                continue
                                            elif(attribute_choice == '2'):
                                                edit_item_desc(item_manage_choice)
                                                console.clear()
                                                continue
                                            elif(attribute_choice == '3'):
                                                edit_item_price(item_manage_choice)
                                                console.clear()
                                                continue
                                            elif (attribute_choice == '4'):
                                                edit_item_quant(item_manage_choice)
                                                console.clear()
                                                continue
                                            elif (attribute_choice == '5'):
                                                remove_item(item_manage_choice)
                                                console.clear()
                                                break
                                            else:
                                                print("Invalid input")
                                                continue
                            # sold items
                            elif (manager_choice == '2'):
                                while(True):
                                    # print sold items with ship status, who bought it, and address
                                    # user can change ship status
                                    print_sales(store_choice)
                                    print_footer("Type the number of the order to see details. Type 0 to go back.")
                                    order_choice = input()
                                    console.clear()
                                    if (order_choice == '0'):
                                        console.clear()
                                        break
                                    else:
                                        while(True):
                                            try:
                                                print_order(order_choice)
                                            except:
                                                console.clear()
                                                print("Invalid input")
                                                break
                                            print_footer("Type 1 to change shipping status. Type 0 to go back.")
                                            ship_choice = input()
                                            if (ship_choice == '0'):
                                                console.clear()
                                                break
                                            elif(ship_choice == '1'):
                                                ship_sale(order_choice)
                                                console.clear()
                                                print("Item shipped")
                                                continue
                                            else:
                                                console.clear()
                                                print("Invalid input")
                                                continue
                            else:
                                console.clear()
                                print("Invalid input")
                                continue
            # DONE other stores
            elif (first_choice == "2"):
                # loop options for other stores
                while(True):
                    #list all stores with ids, type id to enter as customer
                    print_all_stores(user_id)
                    print_footer("Type the number of the store you would like to enter. Type 0 to go back.")
                    store_id_choice = input()
                    console.clear()
                    if (store_id_choice == "0"):
                        break
                    else:
                        while(True):
                            try:
                                print_store_items(store_id_choice) #will throw if bad store_id input
                            except:
                                print("Invalid input")
                                console.clear()
                                break
                            print_footer("Type the number of the item you would like to view. Type 0 to go back.")
                            item_id_choice = input()
                            console.clear()
                            if (item_id_choice == "0"):
                                break
                            else:
                                while(True):
                                    try:
                                        print_item(item_id_choice) #can throw if bad item_id input
                                    except:
                                        print("Invalid input")
                                        break
                                    print_footer("Type 1 to add to cart or 2 to add to want-list. Type 0 to go back.")
                                    add_to_list = input()
                                    if(add_to_list == "0"):
                                        console.clear()
                                        break
                                    elif (add_to_list == "1"):
                                        quant = input("How many items do you want to add? ")
                                        try:
                                            add_to_cart(item_id_choice, quant, user_id) #can throw error if quant puts below 0
                                        except:
                                            print("Invalid input")
                                            continue
                                        print("Item(s) added.")
                                        console.clear()
                                    elif (add_to_list == "2"):
                                        #display want lists
                                        print_wantlists(user_id)
                                        print_footer("Type the name of the list to add it to.")
                                        #ask user which list to add item to
                                        list_choice = input()
                                        try:
                                            add_item_to_wantlist(item_id_choice, user_id, list_choice)
                                            console.clear()
                                            print("Item(s) added.")
                                            continue
                                        except:
                                            console.clear()
                                            print("Invalid input")
                                            continue
                                    else:
                                        print("Invalid input")
                                        console.clear()
                                        continue
            # DONE want lists
            elif (first_choice == "3"):
                while(True):
                    print_wantlists(user_id)
                    print_footer("Type the name of the list to view items. Type 0 to go back.")
                    list_view_choice = input()
                    console.clear()
                    if (list_view_choice == '0'):
                        break
                    else:
                        while(True):
                            try:
                                print_list_items(user_id, list_view_choice)
                            except:
                                print("Invalid input")
                                break
                            print_footer("Type the number of the item you would like to view. Type 0 to go back.")
                            list_item_choice = input()
                            if (list_item_choice == "0"):
                                console.clear()
                                break
                            else:
                                while (True):
                                    try:
                                        print_item(list_item_choice)
                                    except:
                                        print("Invalid input")
                                        console.clear()
                                        break
                                    print_footer("Type 1 to add to cart or 2 to remove from list. Type 0 to go back.")
                                    remove = input()
                                    if (remove == "0"):
                                        console.clear()
                                        break
                                    elif (remove == "1"):
                                        quant = input("How many items do you want to add? ")
                                        try:
                                            add_to_cart(list_item_choice, quant, user_id)  # can throw error if quant puts below 0
                                        except:
                                            print("Invalid input")
                                            console.clear()
                                            continue
                                        print("Item(s) added.")
                                        console.clear()
                                    elif (remove == "2"):
                                        remove_item_from_wantlist(list_item_choice, user_id, list_view_choice)
                                        print("Item removed.")

            # DONE cart
            elif (first_choice == "4"):
                while(True):
                    print_cart(user_id)
                    print_footer("To delete an item from the cart, type its number. To checkout, type 'buy'. Type 0 to go back.")
                    cart_choice = input()
                    if (cart_choice == '0'):
                        console.clear()
                        break
                    elif (cart_choice == 'buy'):
                        buy_cart(user_id)
                        console.clear()
                        break
                    else:
                        try:
                            remove_from_cart(cart_choice, user_id)
                        except:
                            console.clear()
                            print("Invalid input")
                            continue
                        console.clear()
                        continue
            # DONE bough items
            elif (first_choice == "5"):
                # list users orders
                while(True):
                    print_users_orders(user_id)
                    print_footer("Type the order number to view details. Type 0 to go back.")
                    # select order, see details
                    order_choice = input()
                    console.clear()
                    if (order_choice == "0"):
                        break
                    else:
                        while(True):
                            try:
                                print_order(order_choice)
                                print_footer("Type 0 to go back.")
                            except:
                                console.clear()
                                print("Invalid input")
                                break
                            go_back = input()
                            if (go_back == "0"):
                                console.clear()
                                break
                            else:
                                console.clear()
                                print("Invalid input")
                                continue
            else:
                print("Invalid input")
    except mysql.connector.Error as e:
        print(f"Error: {e}")
        connection.rollback()
    finally:
        connection.close()
