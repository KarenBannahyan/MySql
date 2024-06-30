import mysql.connector
from mysql.connector import errorcode
def connect_to_server():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="200777"
    )
def connect_to_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="200777",
        database="numbers_db"
    )
def setup_database():
    connection = None
    cursor = None
    try:
        connection = connect_to_server()
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS numbers_db")
        connection.database = 'numbers_db'
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS numbers_table (
                id INT AUTO_INCREMENT PRIMARY KEY,
                number INT
            )
        """)
        print("База данных и таблица проверены/созданы.")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Ошибка в имени пользователя или пароле")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("База данных не существует и не может быть создана")
        else:
            print(err)
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
def add_number(number):
    connection = None
    cursor = None
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO numbers_table (number) VALUES (%s)", (number,))
        connection.commit()
        print(f"Число {number} добавлено с ID {cursor.lastrowid}.")
    except mysql.connector.Error as err:
        print("Ошибка:", err)
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
def update_number(id, new_number):
    connection = None
    cursor = None
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        cursor.execute("UPDATE numbers_table SET number = %s WHERE id = %s", (new_number, id))
        connection.commit()
        if cursor.rowcount > 0:
            print(f"Число с ID {id} обновлено до {new_number}.")
        else:
            print(f"Число с ID {id} не найдено.")
    except mysql.connector.Error as err:
        print("Ошибка:", err)
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
def main():
    setup_database()
    while True:
        print("\nВыберите действие:")
        print("1. Добавить число")
        print("2. Изменить число по ID")
        print("3. Выйти")
        choice = input("Ваш выбор: ")
        if choice == '1':
            try:
                number = int(input("Введите число: "))
                add_number(number)
            except ValueError:
                print("Ошибка: Введите корректное число.")
        elif choice == '2':
            try:
                id = int(input("Введите ID: "))
                new_number = int(input("Введите новое число: "))
                update_number(id, new_number)
            except ValueError:
                print("Ошибка: Введите корректные данные.")
        elif choice == '3':
            print("Выход...")
            break
        else:
            print("Неверный выбор, попробуйте снова.")
if __name__ == "__main__":
    main()
