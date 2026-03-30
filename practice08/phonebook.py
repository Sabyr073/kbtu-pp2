import psycopg2
from config import load_config


def get_connection():
    config = load_config()
    return psycopg2.connect(**config)


def create_table():
    command = """
    CREATE TABLE IF NOT EXISTS phonebook (
        id SERIAL PRIMARY KEY,
        username VARCHAR(100) NOT NULL,
        phone VARCHAR(20) NOT NULL UNIQUE
    )
    """
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(command)
        print("Table phonebook created successfully.")
    except Exception as error:
        print("Error creating table:", error)


def execute_sql_file(filename):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            sql = file.read()

        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql)

        print(f"{filename} executed successfully.")
    except Exception as error:
        print(f"Error executing {filename}:", error)


def search_contacts():
    pattern = input("Enter search pattern: ").strip()
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM search_contacts(%s)", (pattern,))
                rows = cur.fetchall()
                if rows:
                    for row in rows:
                        print(row)
                else:
                    print("No contacts found.")
    except Exception as error:
        print("Error searching contacts:", error)


def upsert_contact():
    username = input("Enter username: ").strip()
    phone = input("Enter phone: ").strip()

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("CALL upsert_contact(%s, %s)", (username, phone))
        print("Upsert completed successfully.")
    except Exception as error:
        print("Error in upsert:", error)


def insert_many_users():
    usernames = []
    phones = []

    print("Enter contacts (leave username empty to stop):")

    while True:
        username = input("Username: ").strip()
        if not username:
            break
        phone = input("Phone: ").strip()

        usernames.append(username)
        phones.append(phone)

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("CALL insert_many_users(%s, %s)", (usernames, phones))
        print("Bulk insert completed successfully.")
    except Exception as error:
        print("Error in bulk insert:", error)


def get_paginated_contacts():
    try:
        limit = int(input("Enter limit: "))
        offset = int(input("Enter offset: "))

        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM get_contacts_paginated(%s, %s)", (limit, offset))
                rows = cur.fetchall()
                if rows:
                    for row in rows:
                        print(row)
                else:
                    print("No contacts found.")
    except Exception as error:
        print("Error in pagination query:", error)


def delete_contact():
    value = input("Enter username or phone to delete: ").strip()

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("CALL delete_contact(%s)", (value,))
        print("Contact deleted successfully.")
    except Exception as error:
        print("Error deleting contact:", error)


def menu():
    while True:
        print("\n--- PRACTICE 08 MENU ---")
        print("1. Create table")
        print("2. Load functions.sql")
        print("3. Load procedures.sql")
        print("4. Search contacts by pattern")
        print("5. Upsert contact")
        print("6. Insert many users")
        print("7. Get contacts with pagination")
        print("8. Delete contact")
        print("0. Exit")

        choice = input("Choose option: ").strip()

        if choice == "1":
            create_table()
        elif choice == "2":
            execute_sql_file("functions.sql")
        elif choice == "3":
            execute_sql_file("procedures.sql")
        elif choice == "4":
            search_contacts()
        elif choice == "5":
            upsert_contact()
        elif choice == "6":
            insert_many_users()
        elif choice == "7":
            get_paginated_contacts()
        elif choice == "8":
            delete_contact()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    menu()