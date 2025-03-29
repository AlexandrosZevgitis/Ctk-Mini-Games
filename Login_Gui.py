import customtkinter as ctk
from tkinter import Canvas
import sqlite3
from create_account_GUI import *
from forgot_password_gui import *
import hashlib
from games_menu_gui import *
from CTkMessagebox import *

# Accounts so far: 
        # user: alex pass: 12345
        # user: nikos pass: 56789
        # user: maria pass: 12345
        # user: teo pass: 56789
        # user: giannis pass: 12345

# SUM 1.700 LINES OF CODE AVERAGE

# connect database
connect = sqlite3.connect("login.db")
cursor = connect.cursor()
connect_game = sqlite3.connect("game.db")
cursor_game = connect.cursor()


cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,              
        username TEXT UNIQUE NOT NULL,
        hash_password TEXT NOT NULL,
        salt TEXT NOT NULL,
        tries INTEGER DEFAULT 0
    )
""")

connect.commit()

# print successful connection upon with database.
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
if cursor.fetchone():
    print("Database connection successful and 'users' table created.")
else:
    print("Failed to create 'users' table.")

def print_database():
    # Connect to the database
    connect = sqlite3.connect("login.db")
    cursor = connect.cursor()

    # Fetch all users
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()

    # Print results
    for row in rows:
        print(row)

    # Close connection
    connect.close()
    

class LoginForm():

    def __init__(self, master):
        self.master = master
        self.master.title("Mini Games")
        self.master.minsize(800, 600)
        self.master.maxsize(800, 600)

        

        # login header
        self.login_header = ctk.CTkLabel(self.master, text="Login Form", font=("Times New Roman", 40))
        self.login_header.place(relx=0.48, rely=0.3, anchor="center")

        # login and password entries for user data
        self.login_name_entry = ctk.CTkEntry(self.master, width=150, font=("Times New Roman", 17), placeholder_text="Username...")
        self.login_name_entry.place(relx=0.48, rely=0.38, anchor="center")
        # password show checkbox
        self.show_password_var = ctk.BooleanVar(value=False)
        self.toggle_password_button = ctk.CTkCheckBox(self.master, text="Show\nPassword", variable=self.show_password_var, command=self.toggle_password)
        self.toggle_password_button.place(relx=0.58, rely=0.44, anchor="w")
        self.login_password_entry = ctk.CTkEntry(self.master, width=150, font=("Times New Roman", 17), placeholder_text="Password...", show="*")
        self.login_password_entry.place(relx=0.48, rely=0.44, anchor="center")

        # login button
        self.login_button = ctk.CTkButton(self.master, text="Login", width = 150, font=("Times New Roman", 17), cursor="hand2", command=self.on_login_button_click, corner_radius=50)
        self.login_button.place(relx=0.48, rely=0.5, anchor="center")
        self.master.bind("<Return>", lambda event: self.on_login_button_click())

        # forgot password and create account labels for handling problems and new users
        self.login_forgot_password_label = ctk.CTkLabel(self.master, text="Reset Password", font=("Times New Roman",  17), text_color="lightblue", cursor="hand2")
        self.login_forgot_password_label.place(relx=0.48, rely=0.55, anchor="center")
        self.login_forgot_password_label.bind("<Button-1>", lambda event: self.open_forgot_password())
        # bind key here to open forgot password gui and functions

        self.login_create_account_label = ctk.CTkLabel(self.master, text="Create an account", font=("Times New Roman",  17), text_color="lightblue", cursor="hand2")
        self.login_create_account_label.place(relx=0.48, rely=0.59, anchor="center")
        # bind key here to open create account gui and functions
        self.login_create_account_label.bind("<Button-1>", lambda event: self.open_create_account())

    def toggle_password(self):
        # toggle password visibility
        if self.show_password_var.get():
            self.login_password_entry.configure(show="")
        else:
            self.login_password_entry.configure(show="*")

    def create_account(self, master):
        create_account_window = ctk.CTkToplevel(master)  # Create a new top-level window
        create_account_window.transient(master)  # Make it a child of the main window
        create_account_window.grab_set()  # Force focus on this window
        CreateAccount(create_account_window)  # Initialize the account creation GUI

    def open_create_account(self):
        self.create_account(self.master)

    def forgot_password(self, master):
        forgot_password_window = ctk.CTkToplevel(master)
        forgot_password_window.transient(master)  # Make it a child of the main window
        forgot_password_window.grab_set()  # Force focus on this window
        Forgot_Password(forgot_password_window)  # Initialize the forgot password GUI

    def open_forgot_password(self):
        self.forgot_password(self.master)

    def login_credentials(self):
        new_tries = 0
        username = self.login_name_entry.get().strip()
        entered_password = self.login_password_entry.get().strip()

        if not username or not entered_password:
            CTkMessagebox(title="Error", message="Both fields are required!!!", icon="cancel")
            return
        
        connect = sqlite3.connect("login.db")
        cursor = connect.cursor()

        cursor.execute("SELECT username FROM users WHERE username = ?", (username,))
        existing_user = cursor.fetchone()

        if not existing_user:
            CTkMessagebox(title="Error", message="Username do not found in database. Please try again with your correct username", icon="warning")
            connect.close()
            return
        
        cursor.execute("SELECT tries FROM users WHERE username = ?", (username,))
        stored_tries = cursor.fetchone()
        if stored_tries:
            stored_tries = stored_tries[0]
        else:
            CTkMessagebox(title="Error", message="Error retrieving user data", icon="warning")
            connect.close()
            return

        if stored_tries < 3:
            cursor.execute("SELECT hash_password, salt FROM users WHERE username = ?", (username,))
            password_result = cursor.fetchone()

            if password_result:
                stored_hashed_password, stored_salt = password_result

                entered_hashed_password = hashlib.sha256((entered_password + stored_salt).encode()).hexdigest()

            if entered_hashed_password == stored_hashed_password:
                cursor.execute("UPDATE users SET tries = ? WHERE username = ?", (new_tries, username))
                CTkMessagebox(title="Success", message="Login successfully!", icon="check")
                connect.commit()
                connect.close()
                return username
            else:
                stored_tries += 1
                cursor.execute("UPDATE users SET tries = ? WHERE username = ?", (stored_tries, username))
                CTkMessagebox(title="Incorrect", message=f"Incorrect credentials.\nPlease try again.\n You have {3 - stored_tries} tries left.", icon="warning")
                connect.commit()
                connect.close()
                return
        else:
            CTkMessagebox(title="Account Locked", message="Account locked! Reset password to unlock your account.", icon="warning")
            connect.close()
            return
        
    def on_login_button_click(self):
        try:
            username = self.login_credentials()

            if username:
                # Connect to SQLite database
                connect = sqlite3.connect("game.db")
                cursor_game_points = connect.cursor()
                cursor_game_points.execute("SELECT points FROM game WHERE username = ?", (username,))
                result = cursor_game_points.fetchone()  # Fetch one record
                connect.close()

                # Extract points (default to 0 if user has no points)
                username_points = result[0] if result else 0

                self.master.withdraw()  # Hide login window
                print(f"Logged in as {username}, Points: {username_points}")

                root = ctk.CTk()
                game_menu_window = GameMenu(root, username, username_points)  # Pass parameters
                root.mainloop()

                self.master.destroy()  # Destroy login window after menu closes
            else:
                self.msg = CTkMessagebox(title="Error", message="Connection Error.\nPlease try again.", icon="warning", option_1="Exit", option_2="Ok")
                if self.msg.get() == "Exit":
                    print("exit")
        except Exception as e:
            CTkMessagebox(title="Error", message=f"An unexpected error occurred: {str(e)}", icon="cancel")
            print(e)


if __name__ == "__main__":
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")

    print_database()
    root = ctk.CTk()
    app = LoginForm(root)
    root.mainloop()
