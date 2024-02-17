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
        print(error)

    return connection


def add_user(id, type, gender):
    try:
        global connection
        cursor = connection.cursor()
        insert_query = f"""INSERT INTO users
                              (telegram_id, type, gender) 
                               VALUES 
                              ({tid}, {type}, {gender})"""

        sqlite_execute_query = cursor.execute(insert_query)
        connection.commit()
        print(f"DATABASE add_user SUCCESS: {id}, {type}, {gender}")
    except sqlite3.Error as error:
        print("DATABASE add_user FAILED")
        print(error)


def user_exist(id):
    pass
    # TODO: Шлягеру:
    ## Проверка, находится ли юзер в базе данных в таблице users, по идее return True/False. Если False, то add_user. True - то ничего. Дальше переход к get_user


def get_user(id):
    pass
    # TODO: Шлягеру:
    ## Функция для получения данных о гендере пользователя и его касте (препод, школьник). По идее, возвращает gender, type


def end_connection(database):
    pass
    # TODO: Шлягеру:
    ## Мб функция для остановки подключения к БД после завершения работы проги
