import csv
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


def insert_from_console():
    username = input("Enter username: ").strip()
    phone = input("Enter phone: ").strip()

    command = """
    INSERT INTO phonebook (username, phone)
    VALUES (%s, %s)
    """
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(command, (username, phone))
        print("Contact added successfully.")
    except Exception as error:
        print("Error inserting contact:", error)


def insert_from_csv(filename='contacts.csv'):
    command = """
    INSERT INTO phonebook (username, phone)
    VALUES (%s, %s)
    ON CONFLICT (phone) DO NOTHING
    """
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            with get_connection() as conn:
                with conn.cursor() as cur:
                    for row in reader:
                        if len(row) >= 2:
                            cur.execute(command, (row[0], row[1]))
        print("Contacts imported from CSV successfully.")
    except Exception as error:
        print("Error importing CSV:", error)


def update_contact():
    search_value = input("Enter username or phone of contact to update: ").strip()
    choice = input("What do you want to update? (1-name, 2-phone): ").strip()

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                if choice == '1':
                    new_name = input("Enter new username: ").strip()
                    cur.execute("""
                        UPDATE phonebook
                        SET username = %s
                        WHERE username = %s OR phone = %s
                    """, (new_name, search_value, search_value))
                    print("Username updated successfully.")

                elif choice == '2':
                    new_phone = input("Enter new phone: ").strip()
                    cur.execute("""
                        UPDATE phonebook
                        SET phone = %s
                        WHERE username = %s OR phone = %s
                    """, (new_phone, search_value, search_value))
                    print("Phone updated successfully.")
                else:
                    print("Invalid choice.")
    except Exception as error:
        print("Error updating contact:", error)


def query_contacts():
    print("1 - Show all contacts")
    print("2 - Search by username")
    print("3 - Search by phone prefix")
    choice = input("Choose option: ").strip()

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                if choice == '1':
                    cur.execute("SELECT * FROM phonebook ORDER BY id")
                elif choice == '2':
                    name = input("Enter username to search: ").strip()
                    cur.execute("""
                        SELECT * FROM phonebook
                        WHERE username ILIKE %s
                        ORDER BY id
                    """, (f"%{name}%",))
                elif choice == '3':
                    prefix = input("Enter phone prefix: ").strip()
                    cur.execute("""
                        SELECT * FROM phonebook
                        WHERE phone LIKE %s
                        ORDER BY id
                    """, (f"{prefix}%",))
                else:
                    print("Invalid choice.")
                    return

                rows = cur.fetchall()
                if rows:
                    for row in rows:
                        print(row)
                else:
                    print("No contacts found.")
    except Exception as error:
        print("Error querying contacts:", error)


def delete_contact():
    value = input("Enter username or phone to delete: ").strip()

    command = """
    DELETE FROM phonebook
    WHERE username = %s OR phone = %s
    """
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(command, (value, value))
        print("Contact deleted successfully.")
    except Exception as error:
        print("Error deleting contact:", error)


def menu():
    while True:
        print("\n--- PHONEBOOK MENU ---")
        print("1. Create table")
        print("2. Insert contact from console")
        print("3. Import contacts from CSV")
        print("4. Update contact")
        print("5. Query contacts")
        print("6. Delete contact")
        print("0. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == '1':
            create_table()
        elif choice == '2':
            insert_from_console()
        elif choice == '3':
            insert_from_csv()
        elif choice == '4':
            update_contact()
        elif choice == '5':
            query_contacts()
        elif choice == '6':
            delete_contact()
        elif choice == '0':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == '__main__':
    menu()