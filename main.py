import json
import numpy as np
import modules.restaurant as rstr
import modules.errorHandling as err

#login
users = {}

print("Login")
with open("data/Users.csv") as usersFile:
    raw = usersFile.read().splitlines()[1:]
    for i in raw:
        username, position, password = i.split(",")
        users[username] = {"position": position, "password": password}

while True:
    username = input("Username: ")
    try:
        if username == "":
            raise err.InvalidUsernameError("Username cannot be empty.\n")
        if username not in users:
            raise err.UserNotFoundError(f"Cannot find user '{username}'.\n")
        
    except err.InvalidUsernameError as e:
        print(e)
    except err.UserNotFoundError as e:
        print(e)
    else:
        break
        
attempt = 1
loginSucceded = False
while True:
    password = input("Password: ")
    
    try:
        if password == users[username]["password"]:
            print(f"Login successful! Welcome, {users[username]["position"]} {username}.\n")
            position = users[username]["position"]
            loginSucceded = True
            break
        elif attempt == 3:
            raise err.LoginError(f"Login failed.\n")
        else:
            raise err.AuthenticationError(f"Incorrect password. Attempt {attempt} of 3.\nTry again.\n")
    except err.AuthenticationError as e:
        print(e)
    except err.LoginError as e:
        print(e)
        break
    finally:
        attempt += 1

menu_list = []
stock_dict = {}
daily_orders = []

if loginSucceded:
    try:
        with open("menu_ingredients.txt", "r", encoding="utf-8") as f:
            menu_data = json.load(f)

        with open("menu_price.txt", "r", encoding="utf-8") as f:
            price_data = json.load(f)
            prices = dict(price_data)

        for name, ingredients in menu_data.items():
            menu_list.append({
                "name": name,
                "ingredients": ingredients,
                "price": prices.get(name, 0)
            })

        with open("ingredient_amount.txt", "r", encoding="utf-8") as f:
            stock_dict = json.load(f)

        with open("amount.txt", "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    data = line.strip("[]").split(",")
                    daily_orders.append([int(x.strip()) for x in data])

        print(f"Loaded {len(menu_list)} menu items and stock successfully.\n")

    except Exception as e:
        print(f"Error loading data files: {e}")

#main
while loginSucceded:
    raw = input("Select action (-1 - 4, 0 for help, -1 for exit): ")

    try:
        act = int(raw)
        if act < -1 or act > 4:
            raise ValueError("Action is out of range")
    except Exception as e:
        print(f"Invalid action\n{e}")
        continue

    match act:
        case -1:
            # exit program
            print("Exiting Program")
            break
        case 0:
            # manage stock should only appear to managers when login is implemented
            print("1 - Record today's data\n2 - View statistics\n3 - Manage stock")
        case 1:
            # record today's data
            pass
        case 2:
            # view statistics
            pass
        case 3:
            # manage stock - only accesible to managers
            pass
