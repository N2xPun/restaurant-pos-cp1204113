import modules.restaurant as rstr

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
            pass
