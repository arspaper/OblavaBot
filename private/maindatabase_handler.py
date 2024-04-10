import sqlite3


# gender  1 - Male, 2 - Female
# type  1 - Teacher, 2 - Student

connection = None

def create_connection(database):
    global connection

    try:
        connection = sqlite3.connect(database)
        print("DATABASE CONNECTION SUCCESS")

    except sqlite3.Error as error:

        print("DATABASE CONNECTION FAILED")
        print("---ERROR---")
        print(error)
        print("-----------")

    print()
    return connection


def add_user(id, type, gender):
    try:
        global connection
        cursor = connection.cursor()

        insert_query = """INSERT INTO users
                              (id, type, gender) 
                               VALUES 
                              (?, ?, ?)"""

        cursor.execute(insert_query, (id, type, gender))
        connection.commit()
        print(f"DATABASE add_user SUCCESS: id: {id}, type: {type}, gender: {gender}")

    except sqlite3.Error as error:
        print("DATABASE add_user FAILED")
        print("---ERROR---")
        print(error)
        print("-----------")

    print()


def get_user(id):
    try:
        global connection
        cursor = connection.cursor()

        select_query = f"""SELECT type, gender FROM users WHERE id = ?"""

        cursor.execute(select_query, (id,))
        user = cursor.fetchone()

        print(f"DATABASE get_user SUCCESS")

        if user:
            type, gender = user
            print(f"user exists: id: {id}, type: {type}, gender: {gender}")
            print()
            return type, gender
        else:
            print(f"user does not exist: id: {id}")
            print()
            return None, None

    except sqlite3.Error as error:
        print("DATABASE get_user FAILED")
        print("---ERROR---")
        print(error)
        print("-----------")
    print()
    return None, None


def get_raider(gender):
    try:
        global connection
        cursor = connection.cursor()

        select_query = f"""SELECT id FROM users WHERE gender = ? AND type = 1"""

        cursor.execute(select_query, (gender,))
        user = cursor.fetchone()

        print(f"DATABASE get_raider SUCCESS")

        if user:
            id = user
            print(f"user exists: id: {id}")
            print()
            return id
        else:
            print(f"user does not exist: gender: {gender}")
            print()
            return None

    except sqlite3.Error as error:
        print("DATABASE get_raider FAILED")
        print("---ERROR---")
        print(error)
        print("-----------")
    print()
    return None


def end_connection(database):
    global connection

    try:
        connection.close()
        print("DATABASE DISCONNECT SUCCESS")

    except sqlite3.Error as error:

        print("DATABASE DISCONNECT FAILED")
        print("---ERROR---")
        print(error)
        print("-----------")

    print()


def get_database(database):
    try:
        global connection
        cursor = connection.cursor()

        select_query = f"""SELECT * FROM users"""

        cursor.execute(select_query)
        user = cursor.fetchall()

        print(f"DATABASE get_database SUCCESS")

        print(user)

    except sqlite3.Error as error:

        print("DATABASE get_database FAILED")
        print("---ERROR---")
        print(error)
        print("-----------")

    print()
