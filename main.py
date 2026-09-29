import modules.restaurant as rstr
import modules.Errorhandling as err

#login
print("Login")
with open("data/User.csv") as datauser:
    datauser2 = datauser.read().splitlines()
    All_User = dict()
    Check_Headling = 1
    for i in datauser2:
        username_temp,position_temp,password_temp = i.split(",")
        if username_temp not in All_User:
            All_User[username_temp] = [position_temp,password_temp]
while True:
    username = input("Username: ")
    try:
        if username == "" :
            raise err.InvalidUsernameError("Error: Username cannot be empty.")
        if username not in All_User:
            raise err.UserNotFoundError(f"Error: User '{username}' does not exist.")
        
    except err.InvalidUsernameError as e:
        print(e)
    except err.UserNotFoundError as e:
        print(e)
    else:
        print("Username verified.")
        break
    finally:
        print("Username verification completed.")
        print()
        
time = 1
while True:

    password = input("Password: ")
    
    try:
        if password == All_User[username][1]:
            print(f"Login successful! Welcome, {All_User[username][0]} {username}.")
            position = All_User[username][0]
            break
        elif time ==3:
            raise err.AccountLockedError(f"Error: Account '{username}' has been locked.")
        elif password != All_User[username][1] :
            raise err.AuthenticationError(f"Error: Incorrect password. Attempt {time} of 3.")

        
    except err.AuthenticationError as e:
        print(e)
        print("Enter password again.")
        
        
    except err.AccountLockedError as e:
        print(e)
        print("Login failed.")
        break
    finally:
        time += 1
        print("Login attempt completed.")
        print()
    




#main
while True:
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
            print(f"manage stock - only accesible to managers")
            if position != "manager":
                print("You do not have access to Manage stock")
                continue
            

            pass
