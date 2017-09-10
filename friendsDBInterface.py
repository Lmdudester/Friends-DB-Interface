import sqlite3

def makeFriendsTable(conn):
    try:
        conn.execute('''CREATE TABLE IF NOT EXISTS friends (
                        id          INTEGER PRIMARY KEY AUTOINCREMENT,
                        name        TEXT                                  NOT NULL,
                        dob         DATE                                  NOT NULL,
                        address     TEXT);''')

    except Error as e:
        print(e)
        conn.close()
        exit()

def prompt(prompt, responses):
    try:
        resp = input(prompt).lower()
    except:
        resp = ""

    while len(resp) > 1 or (resp not in responses and resp != "q"):
        print("Invalid Response. Try again.")
        try:
            resp = input(prompt).lower()
        except:
            resp = ""

    return resp

def addInfo(conn):
    resp = "n"
    #Get data to enter
    while resp == "n":
        print("\nPlease answer the following prompts about the person you would like to add: ")
        try:
            name = input("First and last name? ")
            if name == 'q':
                return 'q' #user quit

            dob = input("Date of birth? (YYYY-MM-DD) ")
            if dob == 'q':
                return 'q' #user quit

            address = input("Address? ")
            if address == 'q':
                return 'q' #user quit

            resp = prompt("Is this information correct? (Y/N) ", "yn") #User self-check
            if resp == 'q':
                return 'q' #user quit
        except:
            print("Invalid response...")
            resp = 'n'

    #Enter the data
    try:
        conn.execute("INSERT INTO friends (name, dob, address) values (\'" + name + "\', \'" + dob + "\', \'" + address + "\');")
    except Error as e:
        print(e)
        print("Failed to enter data into the database...")

    conn.commit()
    print("\"" + name + "\" Added to Database.")
    return 'a' #success

print("Welcome to the Friends Database Interface!")
print("(Enter Q to quit at individual letter prompts)\n")

conn = sqlite3.connect('db\myFriends.db')
makeFriendsTable(conn)

while True:
    print("\nThe applicable options are: U - Update Info, G - Get Info, A - Add Info")
    resp = prompt("What would you like to do? ", "uga")

    if(resp == 'u'):
        print("\nUpdate Info Options:")

    elif(resp == 'g'):
        print("\nGet Info Options:")

    elif(resp == 'a'):
        if(addInfo(conn) == 'q'):
            break;

    else:
        break

cur = conn.execute("SELECT name, dob, address FROM friends")

print("")

for row in cur:
    print("Name: " + row[0])
    print("DOB: " + row[1])
    print("Address: " + row[2])
    print("")

conn.close()
