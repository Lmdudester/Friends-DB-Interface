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

def getInfo(conn):
    print("\nApplicable options are: W - Whole Database, I - Individual's Data")
    resp = prompt("What would you like to view? ", "wi")

    #Whole Database
    if(resp == 'w'):
        try:
            c = conn.execute("SELECT id, name, dob, address FROM friends")
        except Error as e:
            print(e)
            print("Failed to get data from the database...")

        print("")
        for row in c:
            print("Entry #" + str(row[0]))
            print("Name........" + row[1])
            print("DOB........." + row[2])
            print("Address....." + row[3])
            print("")

    #Individual's Data
    elif(resp == 'i'):
        while resp == 'i':
            resp = input("\nWho would you like to get information on? ")
            if(resp == 'q'):
                return 'q'

            try:
                c = conn.execute("SELECT id, name, dob, address FROM friends WHERE name == \'" + resp + "\'")

            except Error as e:
                print(e)
                print("Failed to get data from the database...")

            num = 0
            print("")
            for row in c:
                print("Entry #" + str(row[0]))
                print("Name........" + row[1])
                print("DOB........." + row[2])
                print("Address....." + row[3])
                print("")
                num += 1;

            if(num == 0):
                print("Invalid name...")
                resp = 'i'


    #Quitting
    else:
        return "q"

def updateTime(conn, resp, name, prsnid):
    #Name
    if(resp == 'n'):
        newName =  input("New first and last name for " + name + "? ")
        if newName == 'q':
            return 'q' #user quit

        #By Id
        if(prsnid != -1):
            conn.execute("UPDATE friends SET name = \'" + newName + "\' WHERE id = \'" + str(prsnid) + "\';")
            conn.commit()
            print("\"" + name + "\" updated to \"" + newName +"\" in Database.")
            return 'u' #success

        #By name
        else:
            conn.execute("UPDATE friends SET name = \'" + newName + "\' WHERE name = \'" + name + "\';" )
            conn.commit()
            print("\"" + name + "\" updated to \"" + newName +"\" in Database.")
            return 'u' #success

    #Address
    elif(resp == 'a'):
        address =  input("New address for " + name + "? ")
        if address == 'q':
            return 'q' #user quit

        #By Id
        if(prsnid != -1):
            conn.execute("UPDATE friends SET address = \'" + address + "\' WHERE id = \'" + str(prsnid) + "\';")
            conn.commit()
            print("\"" + name + "'s\" address updated to \"" + address + "\" in Database.")
            return 'u' #success

        #By name
        else:
            conn.execute("UPDATE friends SET address = \'" + address + "\' WHERE name = \'" + name + "\';")
            conn.commit()
            print("\"" + name + "'s\" address updated to \"" + address + "\" in Database.")
            return 'u' #success

    #Date of birth
    elif(resp == 'd'):
        dob = input("Date of birth? (YYYY-MM-DD) ")
        if dob == 'q':
            return 'q' #user quit

        #By Id
        if(prsnid != -1):
            try:
                conn.execute("UPDATE friends SET dob = \'" + dob + "\' WHERE id = \'" + str(prsnid) + "\';")
                conn.commit()
            except Error as e:
                print(e)
                print("Failed to enter data into the database...")
                return 'f'

            print("\"" + name + "'s\" dob updated to \"" + dob + "\" in Database.")
            return 'u' #success

        #By name
        else:
            try:
                conn.execute("UPDATE friends SET dob = \'" + dob + "\' WHERE name = \'" + name + "\';")
                conn.commit()
            except Error as e:
                print(e)
                print("Failed to enter data into the database...")
                return 'f'

            print("\"" + name + "'s\" dob updated to \"" + dob + "\" in Database.")
            return 'u' #success

    else:
        return 'q'

def updateInfo(conn):
    print("\nApplicable options are: N - by Name, E - by Entry Number")
    resp = prompt("How would you like to find the person? ", "ne")

    #Find by Name
    if(resp == 'n'):
        name = input("First and last name? ")
        if(name == 'q'):
            return 'q'
        c = conn.execute("SELECT name, count(*) as num FROM friends WHERE name = \'" + name + "\';")

        row = c.fetchone()

        while(row[1] != 1):
            print("\nInvalid or duplicate name, try again or press q to quit.")
            name = input("First and last name? ")
            if(name == 'q'):
                return 'q'
            c = conn.execute("SELECT count(*) as num FROM friends WHERE name = \'" + name + "\';")
            row = c.fetchone()

        print("\nApplicable options are: N - Name, A - Address, D - DOB")
        resp = prompt("What would you like to update? ", "nad")

        resp = updateTime(conn, resp, row[0], -1)

        return resp

    #Find by Entry Number
    elif(resp == 'e'):
        prsnid = input("Entry Number? ")
        if(prsnid == 'q'):
            return 'q'
        c = conn.execute("SELECT name, count(*) as num FROM friends WHERE id = \'" + prsnid + "\';")

        row = c.fetchone()

        while(row[1] != 1):
            print("\nInvalid or duplicate name, try again or press q to quit.")
            prsnid = input("First and last name? ")
            if(prsnid == 'q'):
                return 'q'
            c = conn.execute("SELECT count(*) as num FROM friends WHERE id = \'" + prsnid + "\';")
            row = c.fetchone()

        print("\nApplicable options are: N - Name, A - Address, D - DOB")
        resp = prompt("What would you like to update? ", "nad")

        resp = updateTime(conn, resp, row[0], prsnid)

        return resp

    #Quitting
    else:
        return q


print("\n__Welcome to the Friends Database Interface!__")
print("(Enter Q to quit at individual letter prompts)\n")

conn = sqlite3.connect('db\myFriends.db')
makeFriendsTable(conn)

while True:
    print("\nThe applicable options are: U - Update Info, G - Get Info, A - Add Info")
    resp = prompt("What would you like to do? ", "uga")

    if(resp == 'u'):
        if(updateInfo(conn) == 'q'):
            break

    elif(resp == 'g'):
        if(getInfo(conn) == 'q'):
            break

    elif(resp == 'a'):
        if(addInfo(conn) == 'q'):
            break

    else:
        break

conn.close()
