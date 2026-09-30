from datetime import datetime as dt
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
            print(f"Login successful! Welcome, {users[username]["position"]} {username}.")
            position = users[username]["position"]
            loginSucceded = True
            break
        elif attempt == 3:
            raise err.LoginError(f"Login failed.\n")
        else:
            raise err.AuthenticationError(f"Incorrect password. Attempt {attempt} of 3. Try again.")
    except err.AuthenticationError as e:
        print(e)
    except err.LoginError as e:
        print(e)
        break
    finally:
        attempt += 1

menu = set[rstr.Menu]()
stock = dict[rstr.Ingredient, np.int64]()
record = dict[str, dict[str, np.int64]]()

loadDataSucceded = False
if loginSucceded:
    try:
        with open("data/menu_price.json", encoding="utf-8") as f:
            prices = dict(json.load(f))

        with open("data/menu_ingredient.json", encoding="utf-8") as f:
            for name, ingredients_raw in json.load(f).items():
                ingredients = dict[rstr.Ingredient, np.int64]()
                for i in ingredients_raw:
                    ingredients[rstr.Ingredient(i)] = ingredients_raw[i]
                menu.add(rstr.Menu(name, prices[name], ingredients))

        with open("data/ingredient_amount.json", encoding="utf-8") as f:
            for ing, amt in json.load(f).items():
                stock[ing] = amt

        with open("data/amount.json", encoding="utf-8") as f:
            record = dict(json.load(f))
        
    except Exception as e:
        print(f"Error loading data files: {e}")
    else:
        loadDataSucceded = True
        # print(f"Loaded {len(menu)} menu items and stock successfully.")
        # print("Menu:")
        # for m in menu:
        #     print(f"  {m}")

        # print("\nStock:")
        # for s in stock:
        #     print(f"  {s} : {stock[s]}")

        # print("\nOrders:")
        # for o in record:
        #     print(f"  {o}: {record[o]}")

#main
while loginSucceded and loadDataSucceded:
    raw = input("\nSelect action (-1 - 4, 0 for help, -1 for exit): ")

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
            print("1 - Record data\n2 - View statistics\n3 - Manage stock")
        case 1:
            # records data
            print("Record data")
            while True:
                raw = input("\nEnter the date for this data (format: YYYY-MM-DD, Enter nothing for today): ")
                try:
                    rdate = dt.fromisoformat(raw) if raw != "" else dt.today().date()
                    break
                except Exception as e:
                    print(f"Invalid date: {e}")
            
            print("\nRecord item sale by entering the format \"<menu name> <amount sold>\".\nCancel by entering \"c\".\nStop by entering nothing.")
            print(f"Menu:\n  {", ".join([m.Name for m in sorted(menu)])}")
            drecord = {}
            while True:
                raw = input("  ").strip()
                if raw == "" or raw == "c":
                    break

                try:
                    item, amount = raw.split(" ")
                    if item not in menu:
                        raise ValueError(f"Item \"{item}\" doesn't exist.")
                    amount = int(amount)
                    if amount < 1:
                        raise ValueError(f"Amount sold has to be positive.")
                except Exception as e:
                    print(f"Invalid record: {e}")
                else:
                    if item in drecord:
                        overw = ""
                        while overw not in {"y", "n"}:
                            overw = input("Item is already in this record. Did you want to overwrite (y/n)?: ").lower()
                        if overw == "y":
                            drecord[item] = amount
                    else:
                        drecord[item] = amount

            if raw != "c" and len(drecord) > 0:
                record[rdate.isoformat()] = drecord
                with open("data/amount.json", "w", encoding = "utf-8") as amtfs:
                    amtfs.write(json.dumps(record, indent = 4, ensure_ascii = False))

                print(f"Data recorded\nDate {rdate.isoformat()}:")
                for r in drecord:
                    print(f"  {r}: {drecord[r]}")
            else:
                print("Action cancelled")
        case 2:
            # view statistics
            pass
        case 3:
            # manage stock - only accesible to managers
            pass
