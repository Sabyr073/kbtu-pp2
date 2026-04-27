import psycopg2
import json
import csv
from config import load_config


def get_connection():
    config = load_config()
    return psycopg2.connect(**config)


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


def search_contacts_console():
    query = input("Enter search query: ").strip()

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM search_contacts(%s)", (query,))
                rows = cur.fetchall()

                if rows:
                    for row in rows:
                        print(row)
                else:
                    print("No contacts found.")

    except Exception as error:
        print("Error searching contacts:", error)


def add_phone_console():
    name = input("Enter contact name: ").strip()
    phone = input("Enter phone: ").strip()
    phone_type = input("Enter phone type (home/work/mobile): ").strip()

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("CALL add_phone(%s, %s, %s)", (name, phone, phone_type))

        print("Phone added successfully.")

    except Exception as error:
        print("Error adding phone:", error)


def move_to_group_console():
    name = input("Enter contact name: ").strip()
    group_name = input("Enter new group name: ").strip()

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("CALL move_to_group(%s, %s)", (name, group_name))

        print("Contact moved successfully.")

    except Exception as error:
        print("Error moving contact:", error)

def filter_by_group_console():
    group_name = input("Enter group name: ").strip()

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT
                        c.id,
                        c.name,
                        c.email,
                        c.birthday,
                        g.name AS group_name
                    FROM contacts c
                    JOIN groups g ON c.group_id = g.id
                    WHERE g.name ILIKE %s
                    ORDER BY c.name
                """, (group_name,))

                rows = cur.fetchall()

                if rows:
                    for row in rows:
                        print(row)
                else:
                    print("No contacts found in this group.")

    except Exception as error:
        print("Error filtering by group:", error)

def search_by_email_console():
    email = input("Enter email search text: ").strip()

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT
                        id,
                        name,
                        email,
                        birthday,
                        group_id,
                        created_at
                    FROM contacts
                    WHERE email ILIKE %s
                    ORDER BY name
                """, (f"%{email}%",))

                rows = cur.fetchall()

                if rows:
                    for row in rows:
                        print(row)
                else:
                    print("No contacts found with this email.")

    except Exception as error:
        print("Error searching by email:", error)


def sort_contacts_console():
    print("Sort by:")
    print("1. Name")
    print("2. Birthday")
    print("3. Date added")

    choice = input("Choose option: ").strip()

    if choice == "1":
        order_column = "name"
    elif choice == "2":
        order_column = "birthday"
    elif choice == "3":
        order_column = "created_at"
    else:
        print("Invalid option.")
        return

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(f"""
                    SELECT
                        c.id,
                        c.name,
                        c.email,
                        c.birthday,
                        g.name AS group_name,
                        c.created_at
                    FROM contacts c
                    LEFT JOIN groups g ON c.group_id = g.id
                    ORDER BY {order_column}
                """)

                rows = cur.fetchall()

                if rows:
                    for row in rows:
                        print(row)
                else:
                    print("No contacts found.")

    except Exception as error:
        print("Error sorting contacts:", error)


def paginated_contacts_console():
    limit = 3
    offset = 0

    while True:
        try:
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT
                            c.id,
                            c.name,
                            c.email,
                            c.birthday,
                            g.name AS group_name,
                            c.created_at
                        FROM contacts c
                        LEFT JOIN groups g ON c.group_id = g.id
                        ORDER BY c.id
                        LIMIT %s OFFSET %s
                    """, (limit, offset))

                    rows = cur.fetchall()

                    print(f"\n--- Page, offset = {offset} ---")

                    if rows:
                        for row in rows:
                            print(row)
                    else:
                        print("No contacts on this page.")

            command = input("next / prev / quit: ").strip().lower()

            if command == "next":
                offset += limit
            elif command == "prev":
                offset = max(0, offset - limit)
            elif command == "quit":
                break
            else:
                print("Invalid command.")

        except Exception as error:
            print("Error in pagination:", error)
            break


def export_to_json(filename="contacts.json"):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT
                        c.id,
                        c.name,
                        c.email,
                        c.birthday,
                        g.name AS group_name,
                        c.created_at
                    FROM contacts c
                    LEFT JOIN groups g ON c.group_id = g.id
                    ORDER BY c.id
                """)

                contacts = cur.fetchall()
                data = []

                for contact in contacts:
                    contact_id = contact[0]

                    cur.execute("""
                        SELECT phone, type
                        FROM phones
                        WHERE contact_id = %s
                    """, (contact_id,))

                    phones = cur.fetchall()

                    data.append({
                        "id": contact[0],
                        "name": contact[1],
                        "email": contact[2],
                        "birthday": str(contact[3]) if contact[3] else None,
                        "group": contact[4],
                        "created_at": str(contact[5]),
                        "phones": [
                            {"phone": phone[0], "type": phone[1]}
                            for phone in phones
                        ]
                    })

        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

        print(f"Contacts exported to {filename}")

    except Exception as error:
        print("Error exporting to JSON:", error)

def import_from_json(filename="contacts.json"):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)

        with get_connection() as conn:
            with conn.cursor() as cur:
                for item in data:
                    name = item["name"]
                    email = item.get("email")
                    birthday = item.get("birthday")
                    group_name = item.get("group") or "Other"
                    phones = item.get("phones", [])

                    # проверка на дубликат
                    cur.execute("SELECT id FROM contacts WHERE name = %s", (name,))
                    existing = cur.fetchone()

                    if existing:
                        choice = input(
                            f"Contact {name} already exists. skip/overwrite? "
                        ).strip().lower()

                        if choice == "skip":
                            continue
                        elif choice == "overwrite":
                            cur.execute("DELETE FROM contacts WHERE name = %s", (name,))
                        else:
                            print("Invalid choice. Skipping.")
                            continue

                    # группа
                    cur.execute("""
                        INSERT INTO groups (name)
                        VALUES (%s)
                        ON CONFLICT (name) DO NOTHING
                    """, (group_name,))

                    cur.execute("SELECT id FROM groups WHERE name = %s", (group_name,))
                    group_id = cur.fetchone()[0]

                    # контакт
                    cur.execute("""
                        INSERT INTO contacts (name, email, birthday, group_id)
                        VALUES (%s, %s, %s, %s)
                        RETURNING id
                    """, (name, email, birthday, group_id))

                    contact_id = cur.fetchone()[0]

                    # телефоны
                    for phone_item in phones:
                        cur.execute("""
                            INSERT INTO phones (contact_id, phone, type)
                            VALUES (%s, %s, %s)
                        """, (
                            contact_id,
                            phone_item["phone"],
                            phone_item["type"]
                        ))

        print("Contacts imported from JSON successfully.")

    except Exception as error:
        print("Error importing from JSON:", error)

def import_from_csv(filename="contacts.csv"):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            with get_connection() as conn:
                with conn.cursor() as cur:
                    for row in reader:
                        name = row["name"]
                        email = row["email"]
                        birthday = row["birthday"]
                        group_name = row["group"]
                        phone = row["phone"]
                        phone_type = row["type"]

                        # группа
                        cur.execute("""
                            INSERT INTO groups (name)
                            VALUES (%s)
                            ON CONFLICT (name) DO NOTHING
                        """, (group_name,))

                        cur.execute("""
                            SELECT id FROM groups WHERE name = %s
                        """, (group_name,))
                        group_id = cur.fetchone()[0]

                        # контакт
                        cur.execute("""
                            INSERT INTO contacts (name, email, birthday, group_id)
                            VALUES (%s, %s, %s, %s)
                            RETURNING id
                        """, (name, email, birthday, group_id))

                        contact_id = cur.fetchone()[0]

                        cur.execute("""
                            SELECT id FROM contacts WHERE name = %s
                        """, (name,))
                        contact_id = cur.fetchone()[0]

                        # телефон
                        cur.execute("""
                            INSERT INTO phones (contact_id, phone, type)
                            VALUES (%s, %s, %s)
                            ON CONFLICT (phone) DO NOTHING
                        """, (contact_id, phone, phone_type))

        print("Contacts imported from CSV successfully.")

    except Exception as error:
        print("Error importing CSV:", error)


def menu():
    while True:
        print("\n--- TSIS1 PHONEBOOK MENU ---")
        print("1. Load schema.sql")
        print("2. Load procedures.sql")
        print("3. Search contacts")
        print("4. Add phone to contact")
        print("5. Move contact to group")
        print("6. Filter by group")
        print("7. Search by email")
        print("8. Sort contacts")
        print("9. Paginated contacts")
        print("10. Export to JSON")
        print("11. Import from JSON")
        print("12. Import from CSV")
        print("0. Exit")    

        choice = input("Choose option: ").strip()

        if choice == "1":
            execute_sql_file("schema.sql")
        elif choice == "2":
            execute_sql_file("procedures.sql")
        elif choice == "3":
            search_contacts_console()
        elif choice == "4":
            add_phone_console()
        elif choice == "5":
            move_to_group_console()
        elif choice == "6":
            filter_by_group_console()
        elif choice == "7":
            search_by_email_console()
        elif choice == "8":
            sort_contacts_console()
        elif choice == "9":
            paginated_contacts_console()
        elif choice == "10":
            export_to_json()
        elif choice == "11":
            import_from_json()
        elif choice == "12":
            import_from_csv()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    menu()