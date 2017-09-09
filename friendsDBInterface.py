import sqlite3

def makeFriendsTable(conn):
    try:
        conn.execute('''CREATE TABLE IF NOT EXISTS friends (
                        id          INT PRIMARY KEY     NOT NULL,
                        name        TEXT                NOT NULL,
                        dob         DATE                NOT NULL,
                        address     TEXT);''')

    except Error as e:
        print(e)

    finally:
        conn.close()

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


print("Welcome to the Friends Database Interface!")
print("(Type Q to quit at any time)\n")

while True:
    print("\nThe applicable options are: U - Update Info, G - Get Info, A - Add Info")
    resp = prompt("What would you like to do? ","uga")

    if(resp == 'u'):
        print("\nUpdate Info Options:")

    elif(resp == 'g'):
        print("\nGet Info Options:")

    elif(resp == 'a'):
        print("\nAdd Info Options:")

    else:
        break


#conn = sqlite3.connect('db\myFriends.db')
#makeFriendsTable(conn)
