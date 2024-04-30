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

def update_user(id, new_type, new_gender):
    try:
        global connection
        cursor = connection.cursor()
        update_query = """UPDATE users SET type = ?, gender = ? WHERE id = ?"""
        cursor.execute(update_query, (new_type, new_gender, id))
        connection.commit()
        print(f"User updated successfully: ID {id}, Type {new_type}, Gender {new_gender}")
    except sqlite3.Error as error:
        print(f"Failed to update user {id}: {error}")

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


def get_all_teachers():
    try:
        global connection
        cursor = connection.cursor()
        print("Fetching teacher IDs from database")
        cursor.execute("SELECT id FROM users WHERE type = 1")
        teacher_ids = [row[0] for row in cursor.fetchall()]
        print(f"Teacher IDs fetched: {teacher_ids}")
        return teacher_ids
    except sqlite3.Error as error:
        print("Failed to fetch teacher IDs:", error)
        return []


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
