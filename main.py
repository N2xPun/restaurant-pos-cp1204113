from datetime import date as dt
import json
import numpy as np
import matplotlib.pyplot as plt
import modules.restaurant as rstr
import modules.errorHandling as err

def saveStock(stock: dict[rstr.Ingredient, np.int64], path: str):
    with open(path, "w", encoding = "utf-8") as sfs:
        sfs.write(json.dumps(dict([(i.Name, int(stock[i])) for i in stock]), indent = 4, ensure_ascii = False))

def saveMenu_price(menu: set[rstr.Menu],path: str):
    with open(path, "w", encoding = "utf-8") as sfs:
        sfs.write(json.dumps(dict([(i.Name, int(i.Price)) for i in menu]), indent = 4, ensure_ascii = False))

#json don't know int.64 and rstr.Ingredient
#def __init__(self, name: str, price: np.int64, ingredients: dict[Ingredient, np.int64] = {}):
def saveMenu_ingredient(menu: set[rstr.Menu],path: str): 
    with open(path, "w", encoding = "utf-8") as sfs:
        sfs.write( 
            json.dumps(
                dict( [(i.Name, dict([(k.Name,int(v)) for k,v in i.Ingredients.items()])) for i in menu] ), 
                indent=4, 
                ensure_ascii=False
                )
            )

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
position = "Cashier"
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
prices = dict[str, np.int64]()

loadDataSucceded = False
if loginSucceded:
    try:
        with open("data/menu_price.json", encoding="utf-8") as f:
            prices = dict(json.load(f))
            prices = dict(map(lambda p : (p, np.int64(prices[p])), prices))

        with open("data/menu_ingredient.json", encoding="utf-8") as f:
            for name, ingredients_raw in json.load(f).items():
                ingredients = dict[rstr.Ingredient, np.int64]()
                for i in ingredients_raw:
                    ingredients[rstr.Ingredient(i)] = ingredients_raw[i]
                menu.add(rstr.Menu(name, prices[name], ingredients))

        with open("data/ingredient_amount.json", encoding="utf-8") as f:
            for ing, amt in json.load(f).items():
                stock[rstr.Ingredient(ing)] = amt

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
    raw = input("\nSelect action (-1 - 6, 0 for help, -1 to exit): ")

    try:
        act = int(raw)
        if act < -1 or act > 6:
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
            print("""1 - Record data
2 - View statistics
3 - Manage stock
4 - Add a new menu item
5 - Check stock & Low stock alert.
6 - Quick trends
0 - Show this help message
-1 - Exit program""")
        case 1:
            # records data
            print("Record data")
            while True:
                raw = input("\nEnter the date for this data (format: YYYY-MM-DD, Enter nothing for today): ")
                try:
                    rdate = dt.fromisoformat(raw) if raw != "" else dt.today()
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
                    amount = np.int64(amount)
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
            while True:
                print("\nView statistics\n1 - Overall Revenue Statistics\n2 - Daily Revenue Statistics\n0 - Back")
                try:
                    graph_choice = int(input("Select graph: "))
                    if graph_choice not in {0, 1, 2}:
                        raise ValueError("Choose 0, 1, or 2.")
                except ValueError as e:
                    print(f"Invalid choice: {e}")
                    continue

                if graph_choice == 0:
                    break
                if graph_choice == 1:
                    from graph_statistic import show_daily_revenue
                    show_daily_revenue(record, prices)

                elif graph_choice == 2:
                    from graph_dailyday import show_menu_sales
                    show_menu_sales(record, prices)
                    
        case 3:
            # manage stock - only accesible to managers
            if position != "Manager":
                print("You do not have the permission to manage stock.")
                continue

            print("\nStock Management")
            while True:
                try:
                    raw = input("\nSelect action for stock management (-1 - 4, 0 for help, -1 to exit): ")
                    act = int(raw)
                    if act < -1 or act > 5:
                        raise ValueError("Action is out of range")
                except Exception as e:
                    print(f"Invalid action\n{e}")
                    continue
                match act:
                    case -1:
                        # Stock management complete.
                        print("Stock management complete.")
                        break
                    case 0:
                        print("1 - Stock an ingredient.\n2 - Remove some of an ingredient.\n3 - Add a new ingredient.\n4 - Remove an ingredient.\n0 - Show this help message.\n-1 - Exit stock management.")
                    case 1:
                        # Stock an ingredient.
                        print("Stock an ingredient.")
                        try:
                            print(f"Ingredients:\n  {", ".join([i.Name for i in sorted(stock)])}")
                            ingre, raw_quantity = input("Ingredient and quantity (format: <ingredient name> <quantity>): ").split(" ")
                            ingre = rstr.Ingredient(ingre)
                            if ingre not in stock:
                                raise KeyError(f"{ingre} not in stock.")
                            quantity = np.int64(raw_quantity)
                            if quantity < 0 :
                                raise err.QuantityError(f"Please enter the ingredient quantity as a positive integer.")
                        except Exception as e:
                            print(f"Invalid ingredient\n{e}")
                        else:
                            stock[ingre] += quantity
                            saveStock(stock, "data/ingredient_amount.json")
                            print(f"Stocked {quantity} {ingre}.")
                    case 2:
                        # Remove some of an ingredient.
                        print("Remove some of an ingredient.")
                        print(f"Ingredients:\n  {", ".join([i.Name for i in sorted(stock)])}")
                        try:
                            ingre, raw_quantity = input("Ingredient and quantity (format: <ingredient name> <quantity>): ").split(" ")
                            ingre = rstr.Ingredient(ingre)
                            if ingre not in stock:
                                raise KeyError(f"{ingre} not in stock.")
                            quantity = np.int64(raw_quantity)
                            if stock[ingre] - quantity < 0:
                                raise err.StockError(f"Insufficient ingredient. There are only {stock[ingre]} of {ingre}, but tried to throw out {quantity}.")
                        except Exception as e:
                            print(f"Invalid ingredient\n{e}")
                        else:
                            stock[ingre] -= quantity
                            saveStock(stock, "data/ingredient_amount.json")
                            print(f"Removed {quantity} {ingre}.")
                    case 3:
                        # Add a new ingredient.
                        print("Add a new ingredient.")
                        try:
                            ingre, raw_quantity = input("Ingredient and quantity (format: <ingredient name> <quantity>): ").split(" ")
                            ingre = rstr.Ingredient(ingre)
                            if ingre in stock:
                                raise err.StockError(f"{ingre} already in stock.")
                            quantity = np.int64(raw_quantity)
                            if quantity < 0 :
                                raise err.QuantityError(f"Please enter the ingredient quantity as a positive integer.")
                        except Exception as e:
                            print(f"Invalid ingredient\n{e}")
                        else:
                            stock[ingre] = quantity
                            saveStock(stock, "data/ingredient_amount.json")
                            print(f"Added {quantity} {ingre}.")
                    case 4:
                        # Remove ingredients.
                        print("Remove an ingredient.")
                        print(f"Ingredients:\n  {", ".join([i.Name for i in sorted(stock)])}")
                        try:
                            ingre = rstr.Ingredient(input("Ingredient: "))
                            if ingre not in stock:
                                raise KeyError(f"{ingre} not in stock.")
                        except Exception as e:
                            print(f"Invalid ingredient\n{e}")
                        else:
                            del stock[ingre]
                            saveStock(stock, "data/ingredient_amount.json")
                            print(f"Removed {ingre}.")
        case 4:
            # Add a new menu item - only accesible to managers
            if position != "Manager":
                print("You do not have the permission to Add a new menu item.")
                continue

            print("\nAdd a new menu item")
            while True:
                try:
                    name = input("\nMenu name (enter nothing to cancel): ")
                    if name == "":
                        print("Finished adding the new menu item.")
                        break
                    
                    price = np.int64(input("Price: "))

                    if name in menu:
                        raise ValueError(f"Menu item \"{name}\" already exists.")
                    if price < 0:
                        raise ValueError("Price cannot be negative.")

                    ingredients = {}
                    print(f"Ingredients:\n  {", ".join([i.Name for i in sorted(stock)])}")
                    print("Menu's ingredients (format: <Ingredient name> <quantity>) (enter nothing to finish) (c for cancel):")
                    while True:
                        raw = input("  ")
                        if raw.lower() == "c":
                            print("cancel")
                            break
                        if raw == "":
                            if len(ingredients) == 0:
                                raise ValueError("Menu must have some ingredients") 
                            break

                        ingre, quantity = raw.split()
                        ingre = rstr.Ingredient(ingre)
                        quantity = np.int64(quantity)

                        if ingre not in stock:
                            print(f"{ingre} not in stock.")
                            continue

                        if quantity <= 0:
                            print("Quantity must be positive.")
                            continue

                        ingredients[ingre] = quantity

                    menu.add(rstr.Menu(name, price, ingredients))

                    saveMenu_price(menu, "data/menu_price.json")
                    print("Menu prices saved successfully.")
                    saveMenu_ingredient(menu, "data/menu_ingredient.json")
                    print("Menu ingredients saved successfully.")
                    print(f"Added menu item {name}.")

                except Exception as e:
                    print(f"Invalid menu item\n{e}")

        case 5:
            #Check stock & Low stock alert.
            print("\nCheck stock & Low stock alert.")
            sorted_stock = dict(sorted(stock.items(),key = lambda x:x[1]))
            low_stock = dict[rstr.Ingredient, np.int64]()
            for k,v in sorted_stock.items():
                print(f"{k}: {v}",end=" , ")
                if v < 20:
                    low_stock[k] = v
            if len(low_stock) == 0:
                print("\n\nNo ingredients are low in stock.")
            else:
                print("\n\nLow stock alert.")
                for k,v in low_stock.items():
                    print(f"There are only {v} of {k} left")

        case 6:
            # Quick trends
            print("Sales trend from the last 5 days")
            trecord = sorted(record, key = dt.fromisoformat)[-5:]
            tally = dict[str, np.int64]()
            for r in trecord:
                for i in record[r]:
                    if i not in tally:
                        tally[i] = np.int64(0)
                    tally[i] += record[r][i]

            sktally = sorted(tally, key = lambda k : tally[k], reverse = True)
            plt.rcParams["font.family"] = "Tahoma"
            plt.bar(sktally, [tally[sk] for sk in sktally])
            plt.title("Last 5 days sales")
            plt.xlabel("Menu item")
            plt.xticks(rotation = 45)
            plt.ylabel("Sales")

            plt.show()
