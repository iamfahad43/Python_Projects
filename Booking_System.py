# import hashlib to perform encryption decryption
import hashlib
import sys
import random


# Book Ticket
def book_seat():
    temp_name = input(f"Specify a customer from list below:\n{customers}\n")
    
    print("\nHere is the seating area\n")
    for index, seats in enumerate(seating_area):
        print(index+1, seats)

    user_row = int(input("\nEnter Row:\n"))
    user_seat = int(input("\nEnter Seat:\n"))

    # update in seating area
    seating_area[user_row-1][user_seat-1] = seating_area[user_row-1][user_seat-1] + f"@{temp_name.upper()}"

    print("\nUpdated seating area is:\n")
    for index, seats in enumerate(seating_area):
        print(index+1, seats)



# Release Ticket
def release_seat():
    temp_name = input(f"Specify a customer from list below:\n{customers}\n")
    
    print("\nHere is the seating area details\n")
    for index, seats in enumerate(seating_area):
        print(index+1, seats)

    user_row = int(input("\nEnter Row:\n"))
    user_seat = int(input("\nEnter Seat:\n"))

    # update in seating area
    seating_area[user_row-1][user_seat-1] = seating_area[user_row-1][user_seat-1].replace(f"@{temp_name.upper()}", "") 

    print("\nUpdated seating area is:\n")
    for index, seats in enumerate(seating_area):
        print(index+1, seats)



# Check Remaining Seats
def remaining_seats():

    booked_seats = 0
    total_seats = 0

    for index, seats in enumerate(seating_area):
        total_seats = total_seats + len(seats)
        for testy in seats:
            booked_seats = booked_seats + testy.count("@")

    remaining = total_seats - booked_seats

    print(f"\nRemaining Seats in this flight is/are:\n{remaining}\n")



# Get Flight's Revenue
def get_revenue():

    SD = 70
    FC = SD * 10
    ER = SD * 1.1
    IF = SD * 0.1

    SD_Dict = {"SD": SD, "FC": FC, "ER": ER, "IF": IF}

    cost = 0

    for index, seats in enumerate(seating_area):
            for nest in seats:
                if "@" in nest:
                    tmp = nest.replace("@", "")
                    cost = cost + SD_Dict[tmp[:-1]]
    print(f"\nTotal Revenue of this flight is: {round(cost)}$\n")



# Get Flight's Average Ticket Price
def get_average():

    """
    It will calculate all the sold prices and divided by number of customers
    """

    SD = 70
    FC = SD * 10
    ER = SD * 1.1
    IF = SD * 0.1

    SD_Dict = {"SD": SD, "FC": FC, "ER": ER, "IF": IF}

    cost = 0

    # list to append all the entries with customer
    entries = []

    for index, seats in enumerate(seating_area):

        for nest in seats:
            if "@" in nest:
                entries.append(nest)
                tmp = nest.replace("@", "")
                cost = cost + SD_Dict[tmp[:-1]]
    
    average_ticket_price = cost / len(entries)
    print(f"\nAverage Ticket Price of this flight is: {round(average_ticket_price)}$\n")



# Give Upgrade
def give_upgrade():

    # required user password for authentication
    print("\nAuthentication Required!!!\n")
    # User_Authentication
    user_name = input("Enter a username:\n")
    pass_word = input("Enter password:\n")

    if user_name in user_list:
        if hashlib.sha256(pass_word.encode()).hexdigest() == authentication[user_name]:

            temp_name = input(f"Specify a customer from list below:\n{customers}\n")

            print("\nPick a seat to rellocate:\n")
            for index, seats in enumerate(seating_area[2:]):
                print(index+1, seats)

            user_row = int(input("\nEnter Row:\n"))
            user_seat = int(input("\nEnter Seat:\n"))

            # removing from non-fc seats in seating area
            seating_area[user_row+1][user_seat-1] = seating_area[user_row+1][user_seat-1].replace(f"@{temp_name}", "") 

            # assign new seat
            tmp = random.choice(list(enumerate(seating_area[:2])))
            random_row = tmp[0]
            tmp2 = random.choice(list(enumerate(tmp[1])))
            random_seat = tmp2[0]
            
            if "@" not in seating_area[random_row][random_seat]:
                seating_area[random_row][random_seat] = seating_area[random_row][random_seat] + f"@{temp_name.upper()}"
            else:
                tmp = random.choice(list(enumerate(seating_area[:2])))
                random_row = tmp[0]
                tmp2 = random.choice(list(enumerate(tmp[1])))
                random_seat = tmp2[0]

            print("\nUpdated seating area is:\n")
            for index, seats in enumerate(seating_area):
                print(index+1, seats)
        else:
            print("\nAuthentication Failed!\n")
    else:
        print("\nInvalid User\n")


# Get Flight's Average Ticket Price
def get_highest():

    """
    will display the customer with highest total cost
    """

    SD = 70
    FC = SD * 10
    ER = SD * 1.1
    IF = SD * 0.1

    SD_Dict = {"SD": SD, "FC": FC, "ER": ER, "IF": IF}

    cost = 0

    # list to append all the entries with customer
    entries = []

    for index, seats in enumerate(seating_area):
        for nest in seats:
            if "@" in nest:
                entries.append(nest)
                tmp = nest.replace("@", "")
                cost = cost + SD_Dict[tmp[:-1]]
    
    # saperation of single customer booked seats
    A_entries = []
    B_entries = []
    C_entries = []
    E_entries = []
    F_entries = []
    G_entries = []
    for entry in entries:
      if entry[-1] == "A":
        A_entries.append(entry)
      elif entry[-1] == "B":
        B_entries.append(entry)
      elif entry[-1] == "C":
        C_entries.append(entry)
      elif entry[-1] == "E":
        E_entries.append(entry)
      elif entry[-1] == "F":
        F_entries.append(entry)
      elif entry[-1] == "G":
        G_entries.append(entry)
    
    # Calculating customer cost on behalf of booked ticket
    A_cost = 0
    for a_entity in A_entries:
      A_cost = A_cost + SD_Dict[a_entity.replace("@", "")[:-1]]
    B_cost = 0
    for b_entity in B_entries:
      B_cost = B_cost + SD_Dict[b_entity.replace("@", "")[:-1]]
    C_cost = 0
    for c_entity in C_entries:
      C_cost = C_cost + SD_Dict[c_entity.replace("@", "")[:-1]]
    E_cost = 0
    for e_entity in E_entries:
      E_cost = E_cost + SD_Dict[e_entity.replace("@", "")[:-1]]
    F_cost = 0
    for f_entity in F_entries:
      F_cost = F_cost + SD_Dict[f_entity.replace("@", "")[:-1]]
    G_cost = 0
    for g_entity in G_entries:
      G_cost = G_cost + SD_Dict[g_entity.replace("@", "")[:-1]]


    # printable string
    do_print = ""

    # print the highest total cost of customer
    if A_cost > max(B_cost, C_cost, E_cost, F_cost, G_cost):
      do_print = (f"The Customer A has the highest total cost of {A_cost}$\n")
    elif B_cost > max(A_cost, C_cost, E_cost, F_cost, G_cost):
      do_print = (f"The Customer B has the highest total cost of {B_cost}$\n")
    elif C_cost > max(A_cost, B_cost, E_cost, F_cost, G_cost):
      do_print = (f"The Customer C has the highest total cost of {C_cost}$\n")
    elif E_cost > max(A_cost, B_cost, C_cost, F_cost, G_cost):
      do_print = (f"The Customer E has the highest total cost of {E_cost}$\n")
    elif F_cost > max(A_cost, B_cost, C_cost, E_cost, G_cost):
      do_print = (f"The Customer F has the highest total cost of {F_cost}$\n")
    elif G_cost > max(A_cost, B_cost, C_cost, E_cost, F_cost):
      do_print = (f"The Customer G has the highest total cost of {G_cost}$\n")
    
    print(do_print)
  




if __name__ == "__main__":

    # a list of customers
    customers = ["A", "B", "C", "E", "F", "G"]

    # users
    user_list = ["Ibrahiim43", "Fahad", "yourgenericchan" ]

    # a dict of customers with passwords
    authentication = {"Ibrahiim43": hashlib.sha256("IamIbrahiim43".encode()).hexdigest(), 
                    "Fahad": hashlib.sha256("IamFahad123".encode()).hexdigest(),
                    "yourgenericchan": hashlib.sha256("Iamyourgenericchan32".encode()).hexdigest()}

    # menu list to be shown after successfully logged 

    menu = ["1 - Book a Ticket", "2 - Cancel a Reservation", "3 - Check Remaining Seats", "4 - Calculate Flight's Reveneu",
            "5 - Calculate Average Ticket Price", "6 - Upgrade the Seat", "7 - List the highest total", "8 - Exit the system"]

    # a nested list called seating_area
    seating_area = [['FC', 'FC', 'FC'],
                    ['FC', 'FC', 'FC'],
                    ['ER', 'ER', 'ER', 'ER'],
                    ['SD', 'SD', 'SD', 'SD'],
                    ['IF', 'IF', 'IF', 'IF'],
                    ['SD', 'SD', 'SD', 'SD'],
                    ['ER', 'ER', 'ER', 'ER'],
                    ['ER', 'IF', 'IF', 'ER'],
                    ['SD', 'IF', 'IF', 'ER']]
    
    # User_Authentication
    username = input("Enter a username:\n")
    password = input("Enter password:\n")

    if username in user_list:
        if hashlib.sha256(password.encode()).hexdigest() == authentication[username]:
            
            user_input = 0

            while user_input != 8:

                print("\n")
                for menu_list in menu:
                    print(menu_list)
                
                print("\n")
                user_input = int(input("\nInput the number of your selection:\n"))

                if user_input == 1:
                    book_seat()
                elif user_input == 2:
                    release_seat()
                elif user_input == 3:
                    remaining_seats()
                elif user_input == 4:
                    get_revenue()
                elif user_input == 5:
                    get_average()
                elif user_input == 6:
                    give_upgrade()
                elif user_input == 7:
                    get_highest()
                elif user_input == 8:
                    sys.exit
                else:
                    print("Invalid Choice\n")
        else:
            print("Invalid Password\n")
    else:
        print(f"Enter a valid username from the list below\n{customers}")

            
            
            
