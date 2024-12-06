# QueryCrafts Marketplace

QueryCrafts Marketplace is a proof of concept for a digital marketplace for crafts people to buy and sell their creations through digital storefronts. 

## Installing and Running

The program is a single python script main.py which requires the packages rich, mysql-connector-python, and  python-dotenv, all installable using pip as so:

```bash
pip install rich
```
```bash
pip install mysql-connector-python
```
```bash
pip install python-dotenv
```
I did everything in a coda evironment running python 3.13, though I'm sure older version will run fine.

The database was made and ran using MySQL on MySQL Workbench. I have included the actaul .ibd files in a folder called querycrafts. You could try to connect the existing .idb files, or you could run the two .sql files I have provided: create_schemas.sql for creating the database and schemas, and fake_data.sql for filling it with the same fake data I did. This will recreate exactly what exist in the querycrafts folder. 

For connecting to the database, an environment variable file filled with these variables is necessary at line 694:
```bash
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
```
You will need a host (probably localhost), a username and password, and then a name for database, which will be "querycrafts" if you run my scripts.

## Using and Instructions

The program is a CLI. Almost all interactions are by typing a number to select an option. Sometimes a word must be typed to select. Every action of every screen is explained in the footer. For further walkthrough, see the project report section on Application User Interface.

## Test Queries

The test queries are in this repo as a single .sql file. As stated, I used MySQL to run everything, which means I ran everything on MySQL Workbench, if you would like to do the same. 
