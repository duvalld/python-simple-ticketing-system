import sqlite3

DATABASE_NAME = "ticketing_system.db"

# Function for Creating Tables
def create_table(qry):
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        cursor.execute(qry)
        conn.commit()
        cursor.close()
        conn.close()
    except sqlite3.Error as e:
        print(f"Error: {e}")

# Function for user login
def user_login(uname, pword):
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM users WHERE username = ? AND password = ?", (uname, pword))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return row
    except sqlite3.Error as e:
        print(f"Error: {e}")

# Function for adding users
def add_user(name, username, password):
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name, username, password) VALUES (?, ?, ?)", (name, username, password))
        conn.commit()
        cursor.close()
        conn.close()
        print(f"{name} succesfully added to users.")
    except sqlite3.Error as e:
        print(f"Error: {e}")

# Function for adding clients
def add_client(name):
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO clients (name) VALUES (?)", (name,))
        conn.commit()
        cursor.close()
        conn.close()
        print(f"{name} succesfully added to clients.")
    except sqlite3.Error as e:
        print(f"Error: {e}")

# function for viewing users and tickets assigned
def view_users():
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        cursor.execute("""
                    SELECT 
                        users.id
                       ,users.name
                       ,(SELECT COUNT(*) FROM tickets WHERE assigned_to = users.id AND status = 'Open')
                       ,(SELECT COUNT(*) FROM tickets WHERE assigned_to = users.id AND status = 'In Progress')
                       ,(SELECT COUNT(*) FROM tickets WHERE assigned_to = users.id AND status = 'Closed')
                       ,(SELECT COUNT(*) FROM tickets WHERE assigned_to = users.id)
                    FROM users
                       """)
        rows = cursor.fetchall()
        row_headers = f"{'ID':<4} | {'Name':<20} | {'Open':<5} | {'In Progress':<12} | {'Closed':<8} | {'All Tickets Assigned':<20}"
        print(row_headers)
        print(len(row_headers) * "-")
        for row in rows:
            (row_id, row_name, row_open, row_inprog, row_closed, row_all) = row
            print(f"{row_id:<4} | {row_name:<20} | {row_open:<5} | {row_inprog:<12} | {row_closed:<8} | {row_all:<20}")
        print(f"Results: {len(rows)} row(s)\n")
        cursor.close()
        conn.close()
    except sqlite3.Error as e:
        print(f"Error: {e}")

# function for viewing clients and ticket count
def view_clients():
    try:
        print("Clients:")
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        cursor.execute("""
                    SELECT 
                       clients.id
                       ,clients.name
                       ,(SELECT COUNT(*) FROM tickets WHERE client_id = clients.id AND status = 'Open')
                       ,(SELECT COUNT(*) FROM tickets WHERE client_id = clients.id AND status = 'In Progress')
                       ,(SELECT COUNT(*) FROM tickets WHERE client_id = clients.id AND status = 'Closed')
                       ,(SELECT COUNT(*) FROM tickets WHERE client_id = clients.id)
                    FROM clients
                       """)
        rows = cursor.fetchall()
        row_headers = f"{'ID':<4} | {'Name':<30} | {'Open':<5} | {'In Progress':<12} | {'Closed':<8} | {'All Tickets Assigned':<20}"
        print(row_headers)
        print(len(row_headers) * "-")
        for row in rows:
            (row_id, row_name, row_open, row_inprog, row_closed, row_all) = row
            print(f"{row_id:<4} | {row_name:<30} | {row_open:<5} | {row_inprog:<12} | {row_closed:<8} | {row_all:<20}")
        print(f"Results: {len(rows)} row(s)\n")
        cursor.close()
        conn.close()
    except sqlite3.Error as e:
        print(f"Error: {e}")

# function for viewing all tickets
def view_all_tickets():
    try:
        print("Tickets:")
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        cursor.execute("""
                    SELECT
                        tk.id
                        ,tk.title
                        ,tk.description
                        ,created.name
                        ,assigned.name
                        ,cx.name
                        ,tk.created_at
                        ,tk.status
                    FROM tickets as tk
                    LEFT JOIN users as created ON tk.created_by = created.id
                    LEFT JOIN users as assigned ON tk.assigned_to = assigned.id
                    LEFT JOIN clients as cx ON tk.client_id = cx.id
                       """)
        rows = cursor.fetchall()
        row_headers = f"{'ID':<4} | {'Title':<30} | {'Created By':<20} | {'Assigned To':<20} | {'Client':<30} | {'Date Created':<20}  | {'Status':<20}"
        print(row_headers)
        print(len(row_headers) * "-")
        for row in rows:
            (row_id, row_title, row_desc, row_created_by, row_assigned, row_client, row_date, row_status) = row
            print(f"{row_id:<4} | {row_title:<30} | {row_created_by:<20} | {row_assigned:<20} | {row_client:<30} | {row_date:<20}  | {row_status:<20}")
        print(f"Results: {len(rows)} row(s)\n")
        cursor.close()
        conn.close()
    except sqlite3.Error as e:
        print(f"Error: {e}")

# function for viewing specific ticket
def view_ticket(ticket_id):
    try:
        print("Ticket:")
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        cursor.execute("""
                    SELECT
                        tk.id
                        ,tk.title
                        ,tk.description
                        ,tk.body
                        ,created.name
                        ,assigned.name
                        ,cx.name
                        ,tk.created_at
                        ,tk.modified_at
                        ,tk.status
                    FROM tickets as tk
                    LEFT JOIN users as created ON tk.created_by = created.id
                    LEFT JOIN users as assigned ON tk.assigned_to = assigned.id
                    LEFT JOIN clients as cx ON tk.client_id = cx.id
                    WHERE tk.id = ?
                       """, (ticket_id,))
        rows = cursor.fetchall()
        for row in rows:
            (row_id, row_title, row_desc, row_body, row_created_by, row_assigned, row_client, row_date, row_date_modif, row_status) = row
            print(f"Ticket ID: {row_id}")
            print(f"Title: {row_title}")
            print(f"Description: {row_desc}")
            print(f"Body: {row_body}")
            print(f"Created By: {row_created_by}")
            print(f"Assigned To: {row_assigned}")
            print(f"Client: {row_client}")
            print(f"Date Created: {row_date}")
            print(f"Date Modified: {row_date_modif}")
            print(f"Status: {row_status}")
        cursor.close()
        conn.close()
    except sqlite3.Error as e:
        print(f"Error: {e}")

#function for adding new ticket
def add_new_ticket(user_id):
    try:
        title_input = input("Title: ")
        desc_input = input("Description: ")
        body_input = input("Body: ")
        assigned_to_input = int(input("Assigned to (User ID):"))
        client_input = int(input("Client (ID): "))
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        cursor.execute("""
                       INSERT INTO tickets (
                           title
                           ,description
                           ,body
                           ,created_by
                           ,assigned_to
                           ,client_id
                           ,created_at
                           ,modified_at
                           ,status) 
                        VALUES (?, ?, ?, ?, ?, ?, DATETIME('now','localtime'), DATETIME('now','localtime'), 'Open')""", (title_input, desc_input, body_input, user_id, assigned_to_input,client_input))
        conn.commit()
        cursor.close()
        conn.close()
        print(f"{title_input} ticket successfully added.")
    except sqlite3.Error as e:
        print(f"Error: {e}")

# function for adding ticket activity
def add_new_ticket_activity(user_id, ticket_id):
    try:
        activitiy_input = input("Activity: ")
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        cursor.execute("""
                       INSERT INTO ticket_activities (
                           ticket_id
                           ,activity
                           ,created_by
                           ,created_at) 
                        VALUES (?, ?, ?, DATETIME('now','localtime'))""", (ticket_id, activitiy_input, user_id))
        conn.commit()
        cursor.close()
        conn.close()
        print(f"{activitiy_input} ticket_activity successfully added.")
    except sqlite3.Error as e:
        print(f"Error: {e}")

# function for viewing ticket activities
def view_activities(tkt_id):
    try:
        print("Activities:")
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        cursor.execute("""
                    SELECT
                        tk.id
                        ,tk.activity
                        ,created.name
                        ,tk.created_at
                    FROM ticket_activities as tk
                    LEFT JOIN users as created ON tk.created_by = created.id
                    WHERE tk.ticket_id = ?
                       """, (tkt_id,))
        rows = cursor.fetchall()
        row_headers = f"{'ID':<4} | {'Activity':<50} | {'Created By':<20} | {'Date Created':<20}"
        print(row_headers)
        print(len(row_headers) * "-")
        for row in rows:
            (row_id, row_activity, row_created_by, row_date) = row
            print(f"{row_id:<4} | {row_activity:<50} | {row_created_by:<20} | {row_date:<20} ")
        print(f"Results: {len(rows)} row(s)\n")
        cursor.close()
        conn.close()
    except sqlite3.Error as e:
        print(f"Error: {e}")

# function for updating ticket status and add it to ticket activities
def update_ticket_status(tkt_id, usr_id):
    try:
        status_input = input("Status: ")
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        cursor.execute("UPDATE tickets SET status=? WHERE id = ?", (status_input, tkt_id))
        cursor.execute("""
                       INSERT INTO ticket_activities (
                           ticket_id
                           ,activity
                           ,created_by
                           ,created_at)
                        VALUES (?, ?, ?, DATETIME('now','localtime'))""", (tkt_id, f"Change Ticket Status to {status_input}", usr_id))
        conn.commit()
        cursor.close()
        conn.close()
        print(f"Status Changed to {status_input}")
    except sqlite3.Error as e:
        print(f"Error {e}")

# query for users table
users_table_query = """
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY
        ,name TEXT
        ,username TEXT
        ,password TEXT
    )
"""

# query for clients table
clients_table_query = """
    CREATE TABLE IF NOT EXISTS clients(
        id INTEGER PRIMARY KEY
        ,name TEXT
    )
"""

# query for tickets table
tickets_table_query = """
    CREATE TABLE IF NOT EXISTS tickets(
        id INTEGER PRIMARY KEY
        ,title TEXT
        ,description TEXT
        ,body TEXT
        ,created_by INTEGER
        ,assigned_to INTEGER
        ,created_at DATETIME
        ,modified_at DATETIME
        ,status TEXT
        ,client_id INTEGER
    )
"""

# query for ticket activities
ticket_activities_table_query = """
    CREATE TABLE IF NOT EXISTS ticket_activities(
        id INTEGER PRIMARY KEY
        ,ticket_id INTEGER
        ,created_by INTEGER
        ,created_at DATETIME 
        ,activity TEXT
    )
"""
# table query list
table_queries = [users_table_query, clients_table_query, tickets_table_query, ticket_activities_table_query]

# create each table in query list
for query in table_queries:
    create_table(query)

# program start
print("Welcome to Simple Ticketing System")

# user login
login_running = True
while login_running:
    print("User Login:")
    username = input("Username: ")
    password = input("Password: ")
    result = user_login(username, password)
    if result != None:
        login_running = False
        (current_user_id, current_user_name) = result
    else:
        print("Invalid Username and Password")

# main menu
main_menu_running = True
while main_menu_running:
    try:
        menu_input = int(input("Enter 1: Tickets, 2: Users & Clients, 3: Exit: "))
        if menu_input == 1:
            view_all_tickets()
            ticket_menu = int(input("Enter 1: Add New Ticket, 2: Manage_ticket: "))
            if ticket_menu == 1:
                add_new_ticket(current_user_id)
            if ticket_menu == 2:
                ticket_id = int(input("Enter Ticket ID that you want to Manage: "))
                view_ticket(ticket_id)
                view_activities(ticket_id)
                manage_ticket_menu = int(input("Enter 1: Add ticket activity, 2: Change ticket status: "))
                if manage_ticket_menu == 1:
                    add_new_ticket_activity(current_user_id, ticket_id)
                    view_activities(ticket_id)
                elif manage_ticket_menu == 2:
                    update_ticket_status(ticket_id, current_user_id)
                    view_ticket(ticket_id)
                    view_activities(ticket_id)
        elif menu_input == 2:
            view_users()
            view_clients()
        elif menu_input == 3:
            main_menu_running = False
        else:
            print("Invalid Input: Input 1 to 3")
    except ValueError:
        print("Invalid Input: Numerical value only")

       