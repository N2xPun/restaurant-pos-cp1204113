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

menu = set[rstr.Menu]()
stock = dict[rstr.Ingredient, np.int64]()
daily_orders = np.ndarray([], dtype = np.int64)

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

        # why are daily orders not name indexed?
        # Also, you don't even know what days are these.
        with open("data/amount.txt", encoding="utf-8") as f:
            daily_orders = np.array(list(map(eval, f.readlines())), dtype = np.int64, ndmin = 2, ndmax = 2)
        
    except Exception as e:
        print(f"Error loading data files: {e}")
    else:
        loadDataSucceded = True
        print(f"Loaded {len(menu)} menu items and stock successfully.")
        print("Menu:")
        for m in menu:
            print(f"  {m}")

        print("\nStock:")
        for s in stock:
            print(f"  {s} : {stock[s]}")

        print("\nOrders:")
        for o in daily_orders:
            print(f"  {o}")

#main
while loginSucceded and loadDataSucceded:
    raw = input("\nSelect action (-1 - 4, 0 for help, -1 for exit): ")

    try:
        act = int(raw)
        if act < -1 or act > 5:
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
            if position != "Manager":
                print("You do not have the authority to manage stock.")
                continue
            print()
            print("Start manage stock")
            while True:
                try:
                    raw = input("\nSelect action for manage stock (-1 - 4, 0 for help, -1 for exit): ")
                    act = int(raw)
                    if act < -1 or act > 5:
                        raise ValueError("Action is out of range")
                except Exception as e:
                    print(f"Invalid action\n{e}")
                    continue
                match act:
                    case -1:
                        # Cancel stock management
                        print("stock management complete.")
                        break
                    case 0:
                        print("1 - Increase ingredients.\n2 - Reduce ingredients.\n3 - Add new ingredients.\n4 - Remove ingredients.")
                    case 1:
                        # Increase ingredients.
                        print("Increase ingredients.")
                        try:
                            ingre,raw_quantity = input("ingredients and quantity [ Ex.พริก,30 ]: ").split(",")
                            if ingre not in stock:
                                raise KeyError(f"{ingre} not in stock.")
                            quantity = int(raw_quantity)
                            if quantity < 0 :
                                raise err.QuantityError(f"Please enter the ingredient quantity as a positive integer.")
                        except KeyError as e:
                            print(f"Invalid action\n{e}")
                        except ValueError:
                            print(f"Invalid action\nPlease enter the ingredient quantity as a positive integer.")
                        except err.QuantityError as e:
                            print(f"Invalid action\n{e}")
                        except Exception:
                            print(f"Invalid action\nInput Error.")
                        else:
                            stock[ingre] += quantity
                            print(f"Increase ingredients succeded.")
                    case 2:
                        # Reduce ingredients.
                        print("Reduce ingredients.")
                        try:
                            ingre,raw_quantity = input("ingredients and quantity [ Ex.พริก,30 ]: ").split(",")
                            if ingre not in stock:
                                raise KeyError(f"{ingre} not in stock.")
                            quantity = int(raw_quantity)
                            if stock[ingre] - quantity < 0:
                                raise err.StockError(f"Insufficient ingredient. There are {stock[ingre]} of {ingre}.")
                        except KeyError as e:
                            print(f"Invalid action\n{e}")
                        except ValueError:
                            print(f"Invalid action\nPlease enter the ingredient quantity as a positive integer.")
                        except err.StockError as e:
                            print(f"Invalid action\n{e}")
                        except Exception:
                            print(f"Invalid action\nInput Error")
                        else:
                            stock[ingre] -= quantity
                            print(f"Reduce ingredients succeded.")
                    case 3:
                        # Add new ingredients.
                        print("Add new ingredients.")
                        try:
                            ingre,raw_quantity = input("ingredients and quantity [ Ex.ไก่,10 ]: ").split(",")
                            if ingre in stock:
                                raise err.StockError(f"{ingre} already in stock.")
                            quantity = int(raw_quantity)
                            if quantity < 0 :
                                raise err.QuantityError(f"Please enter the ingredient quantity as a positive integer.")
                        except err.QuantityError as e:
                            print(f"Invalid action\n{e}")
                        except ValueError:
                            print(f"Invalid action\nPlease enter the ingredient quantity as a positive integer.")
                        except err.StockError as e:
                            print(f"Invalid action\n{e}")
                        except Exception:
                            print(f"Invalid action\nInput Error")
                        else:
                            stock[ingre] = quantity
                            print(f"Add new ingredients succeded.")
                    case 4:
                        # Remove ingredients.
                        print("Remove ingredients.")
                        try:
                            ingre = input("ingredients [ Ex.ไก่ ]: ")
                            if ingre not in stock:
                                raise KeyError(f"{ingre} not in stock.")
                            
                        except KeyError as e:
                            print(f"Invalid action\n{e}")
                        except Exception:
                            print(f"Invalid action\nInput Error")
                        else:
                            del stock[ingre]
                            print(f"Remove ingredients succeded.")



        case 4:
            # add met - only accesible to managers
            pass