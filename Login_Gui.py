import customtkinter as ctk
from tkinter import Canvas
import sqlite3
from create_account_GUI import *
from forgot_password_gui import *
import hashlib
from games_menu_gui import *
from CTkMessagebox import *
from PIL import Image
import os
import pygame

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
        self.master.minsize(850,700)
        self.master.maxsize(850,700)

        
        # load icon and images
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.image_filename = ["bg_image.jpg", "email.jpg", "lock.jpg", "google.png", "hide.png", "view.png", "add.png", "arrows.png"]
        self.image_paths = {name: os.path.join(self.script_dir, "images", name) for name in self.image_filename}
        self.unlock_opened = False

        # creating main frame
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        self.main_frame = ctk.CTkFrame(master)
        self.main_frame.grid(row=0,column=0,sticky="nsew")

        # creating left and right grids
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)

        self.left_frame = ctk.CTkFrame(self.main_frame,corner_radius=0)
        self.left_frame.grid(row=0,column=0,sticky="nsew")
        self.right_frame = ctk.CTkFrame(self.main_frame,corner_radius=0,fg_color="white")
        self.right_frame.grid(row=0,column=1,sticky="nsew")

        # creating left frame widgets Image
        self.left_frame_image = ctk.CTkImage(Image.open(self.image_paths["bg_image.jpg"]), size=(440,705))
        self.left_frame_image_label = ctk.CTkLabel(self.left_frame, text="", image=self.left_frame_image)
        self.left_frame_image_label.place(relx=0.49,rely=0.5,anchor="center")

        # creating right frame grid 
        self.right_frame.grid_rowconfigure(0, weight=1)
        self.right_frame.grid_rowconfigure(1, weight=1)
        self.right_frame.grid_rowconfigure(2, weight=1)
        self.right_frame.grid_rowconfigure(3, weight=1)
        self.right_frame.grid_columnconfigure(0, weight=1)

        # creating right frame actual frames
        self.top_welcome_frame = ctk.CTkFrame(self.right_frame,corner_radius=0,fg_color="white",border_color=None)
        self.top_welcome_frame.grid(row=0,column=0,sticky="nsew")
        self.top_email_username_frame = ctk.CTkFrame(self.right_frame,corner_radius=0,fg_color="white",border_color=None)
        self.top_email_username_frame.grid(row=1,column=0,sticky="nsew")
        self.top_password_frame = ctk.CTkFrame(self.right_frame,corner_radius=0,fg_color="white",border_color=None)
        self.top_password_frame.grid(row=2,column=0,sticky="nsew")
        self.top_bottom_frame = ctk.CTkFrame(self.right_frame,corner_radius=0,fg_color="white",border_color=None)
        self.top_bottom_frame.grid(row=3,column=0,sticky="nsew")

        # creating welcome frame widgets
        #copyrights
        self.copyrights_label = ctk.CTkLabel(self.top_welcome_frame,text="© 2025 Alexandros Zevgitis\nAll Rights Reserved.",font=("Times New Roman",12,"bold","underline"),text_color="black")
        self.copyrights_label.place(relx=0.8,rely=0.1,anchor="center")
        self.welcome_header = ctk.CTkLabel(self.top_welcome_frame, text="Welcome To The Mini Games!", text_color="#430386", font=("Times New Roman", 25, "bold", "underline"))
        self.welcome_header.place(relx=0.5,rely=0.65,anchor="center")
        self.sing_in_top_label = ctk.CTkLabel(self.top_welcome_frame,text="Sing in to your account!",text_color="black",font=("Times New Roman",20,"bold"))
        self.sing_in_top_label.place(relx=0.36,rely=0.95,anchor="center")

        # creating email username widgets
        self.email_username_label = ctk.CTkLabel(self.top_email_username_frame,text="Email: ", text_color="#430386", font=("Times New Roman",20,"bold"))
        self.email_username_label.place(relx=0.32,rely=0.45,anchor="center")
        self.email_username_icon = ctk.CTkImage(Image.open(self.image_paths["email.jpg"]), size=(30,25))
        self.email_username_icon_label = ctk.CTkLabel(self.top_email_username_frame, text="", image=self.email_username_icon)
        self.email_username_icon_label.place(relx=0.19,rely=0.45,anchor="center")
        self.email_username_entry = ctk.CTkEntry(self.top_email_username_frame, width=250,placeholder_text="Enter your email...", placeholder_text_color="black",fg_color="transparent", border_color="#430386", text_color="black")
        self.email_username_entry.place(relx=0.45,rely=0.65,anchor="center")

        # creating password widgets
        self.show_password_var = ctk.BooleanVar()
        self.password_label = ctk.CTkLabel(self.top_password_frame, text="Password:",text_color="#430386", font=("Times New Roman",20,"bold"))
        self.password_label.place(relx=0.35,rely=0.15,anchor="center")
        self.password_icon = ctk.CTkImage(Image.open(self.image_paths["lock.jpg"]), size=(30,25))
        self.password_icon_label = ctk.CTkLabel(self.top_password_frame,text="",image=self.password_icon)
        self.password_icon_label.place(relx=0.19,rely=0.15,anchor="center")
        self.password_entry = ctk.CTkEntry(self.top_password_frame,width=250,placeholder_text="Enter your password...",placeholder_text_color="black",fg_color="transparent",border_color="#430386",show="*", text_color="black")
        self.password_entry.place(relx=0.45,rely=0.35,anchor="center")
        self.show_image = ctk.CTkImage(Image.open(self.image_paths["view.png"]),size=(25,20))
        self.hide_image = ctk.CTkImage(Image.open(self.image_paths["hide.png"]),size=(25,20))
        self.show_hide_password_label = ctk.CTkLabel(self.top_password_frame,text="",image=self.show_image,cursor="hand2")
        self.show_hide_password_label.place(relx=0.78,rely=0.35,anchor="center")
        # bind label with click
        self.show_hide_password_label.bind("<Button-1>", self.toggle_password)
        self.is_viewing = True
        # forgot password label
        self.forgot_password_label = ctk.CTkLabel(self.top_password_frame,text="Forgot Password?", text_color="blue",cursor="hand2",font=("Times New Roman",15,"bold"),fg_color="transparent")
        self.forgot_password_label.place(relx=0.61,rely=0.5,anchor="center")
        self.password_entry.lift()
        # bind forgot password
        self.forgot_password_label.bind("<Button-1>", lambda event: self.forgot_password(self.master))

        # creating bottom grid widgets
        self.login_button = ctk.CTkButton(self.top_bottom_frame, text="Login", width=260,height=30,border_color="white",fg_color="#430386",font=("Times New Roman",20,"bold"),hover=None,cursor="hand2",command=self.on_login_button_click)
        self.login_button.place(relx=0.45,rely=0.1,anchor="center")
        self.master.bind("<Return>",lambda event=None: self.on_login_button_click())
        self.create_acc_icon = ctk.CTkImage(Image.open(self.image_paths["add.png"]),size=(25,20))
        self.create_account_button = ctk.CTkButton(self.top_bottom_frame,text="Create An Account",image=self.create_acc_icon,width=260,height=30,border_color="white",fg_color="#430386",font=("Times New Roman",20,"bold"),hover=None,cursor="hand2",compound="left",command=lambda: self.create_account(self.master))
        self.create_account_button.place(relx=0.45,rely=0.35,anchor="center")

        # creating swipe button
        self.arrow_icon = ctk.CTkImage(Image.open(self.image_paths["arrows.png"]),size=(30,30))
        self.swipe_frame = ctk.CTkFrame(self.top_bottom_frame,width=300,height=50,corner_radius=20,fg_color="transparent",border_color="#430386",border_width=3)
        self.swipe_frame.place(relx=0.455,rely=0.65,anchor="center")
        self.swipe_button = ctk.CTkButton(self.swipe_frame,width=120,height=30,corner_radius=20,text="Swipe to Unlock",image=self.arrow_icon,font=("Times New Roman",16,"bold"),hover=None,cursor="hand2",fg_color="#430386",compound="right")
        self.swipe_button.place(x=97,y=25,anchor="center")
        self.swipe_button.bind("<Button-1>", self.start_drag)
        self.swipe_button.bind("<B1-Motion>", self.login_swipe)
        self.swipe_button.bind("<ButtonRelease-1>", self.stop_swipe)
        pygame.mixer.init()

    def toggle_password(self, event):
        # toggle password visibility
        if self.is_viewing:
            self.show_hide_password_label.configure(image=self.hide_image)
            self.password_entry.configure(show="")
        else:
            self.show_hide_password_label.configure(image=self.show_image)
            self.password_entry.configure(show="*")
        self.is_viewing = not self.is_viewing

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
        username = self.email_username_entry.get().strip()
        entered_password = self.password_entry.get().strip()

        if not username or not entered_password:
            CTkMessagebox(title="Error", message="Both fields are required!!!", icon="cancel")
            return None
        
        connect = sqlite3.connect("login.db")
        cursor = connect.cursor()

        cursor.execute("SELECT username FROM users WHERE username = ?", (username,))
        existing_user = cursor.fetchone()

        if not existing_user:
            CTkMessagebox(title="Error", message="Username do not found in database. Please try again with your correct username", icon="warning")
            connect.close()
            return None
        
        cursor.execute("SELECT tries FROM users WHERE username = ?", (username,))
        stored_tries = cursor.fetchone()
        if stored_tries:
            stored_tries = stored_tries[0]
        else:
            CTkMessagebox(title="Error", message="Error retrieving user data", icon="warning")
            connect.close()
            return None

        if stored_tries < 3:
            cursor.execute("SELECT hash_password, salt FROM users WHERE username = ?", (username,))
            password_result = cursor.fetchone()

            if password_result:
                stored_hashed_password, stored_salt = password_result

                entered_hashed_password = hashlib.sha256((entered_password + stored_salt).encode()).hexdigest()

            if entered_hashed_password == stored_hashed_password:
                cursor.execute("UPDATE users SET tries = ? WHERE username = ?", (new_tries, username))
                # CTkMessagebox(title="Success", message="Login successfully!", icon="check")
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
            return None
        
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

                # root = ctk.CTk()
                # game_menu_window = GameMenu(root, username, username_points)  # Pass parameters
                # root.mainloop()
                self.show_loading_screen(username, username_points)

                # self.master.destroy()  # Destroy login window after menu closes
        except Exception as e:
            CTkMessagebox(title="Error", message=f"An unexpected error occurred: {str(e)}", icon="cancel")
            print(e)

    def show_loading_screen(self, username, username_points):
        # Create a new top-level window for loading screen
        loading_screen = ctk.CTkToplevel(self.master)
        loading_screen.geometry("400x200")
        loading_screen.title("Loading...")

        # Make the window non-resizable and centered
        loading_screen.resizable(False, False)
        loading_screen.grab_set()  # Prevent interaction with other windows

        # **Get screen width and height**
        screen_width = loading_screen.winfo_screenwidth()
        screen_height = loading_screen.winfo_screenheight()

        # **Set window width & height**
        win_width = 400
        win_height = 200

        # **Calculate center position**
        x_position = (screen_width // 2) - (win_width // 2)
        y_position = (screen_height // 2) - (win_height // 2)

        # **Set window geometry (Centered)**
        loading_screen.geometry(f"{win_width}x{win_height}+{x_position}+{y_position}")  

        # Add a loading label
        loading_label = ctk.CTkLabel(loading_screen, text="Loading...", font=("Arial", 24, "bold"))
        loading_label.pack(pady=50)

        # Add a progress bar (optional)
        progress = ctk.CTkProgressBar(loading_screen)
        progress.pack(pady=10, fill="x", padx=20)
        progress.start()
        loading_screen.after(3500, lambda: switch_to_game(loading_screen, username, username_points))

        # **Fade effect (Optional)**
        def fade_in(opacity=0.1):
            if opacity <= 1.0:
                loading_screen.attributes("-alpha", opacity)
                loading_screen.after(50, fade_in, opacity + 0.1)  # Increase opacity
            else:
                # Once fully visible, wait then switch to game menu
                loading_screen.after(3500, lambda: switch_to_game(loading_screen, username, username_points))

        def switch_to_game(loading_win, username, username_points):
            loading_win.destroy()  # Close loading screen

            # Open the game menu
            root = ctk.CTk()
            game_menu_window = GameMenu(root, username, username_points)
            root.mainloop()

            self.master.destroy()

        fade_in()  # Start fade-in animation

    def start_drag(self, event):
        self.start_x = event.x
        if self.swipe_button.winfo_x() != 97:
            return 

    def login_swipe(self, event):
        new_x = self.swipe_button.winfo_x() + (event.x - self.start_x)

        new_x = max(97, min(new_x, 200))

        self.swipe_button.place(x=new_x, y=25)
        if new_x == 200 and not self.unlock_opened:
            self.unlock_opened = True
            new_x = 97
            self.swipe_button.place(x=new_x, y=25)
            pygame.mixer.music.load("./sounds_effect/unlock_sound.mp3")
            pygame.mixer.music.play()
            self.unlock_credentials()

    def stop_swipe(self, event):
        new_x = self.swipe_button.winfo_x() + (event.x - self.start_x)
        new_x = max(97, min(new_x, 200))

        if new_x < 200:
            new_x = 97
            self.swipe_button.place(x=new_x, y=25)

    def unlock_credentials(self):
        unlock_screen = ctk.CTkToplevel(self.master)
        unlock_screen.transient(self.master)
        unlock_screen.geometry("400x200")
        unlock_screen.title("Unlock Window")
        unlock_screen.configure(fg_color="white")


        unlock_screen.resizable(False, False)
        unlock_screen.grab_set() 

        screen_width = unlock_screen.winfo_screenwidth()
        screen_height = unlock_screen.winfo_screenheight()

        win_width = 400
        win_height = 200

        x_position = (screen_width // 2) - (win_width // 2)
        y_position = (screen_height // 2) - (win_height // 2)

        unlock_screen.geometry(f"{win_width}x{win_height}+{x_position}+{y_position}") 

        unlock_screen_welcome_label = ctk.CTkLabel(unlock_screen,text="Enter Username & you 4 digit code...",font=("Times New Roman",20,"bold"),text_color="black")
        unlock_screen_welcome_label.place(relx=0.5,rely=0.2,anchor="center")
        unlock_screen_username_entry = ctk.CTkEntry(unlock_screen,width=200,height=30,placeholder_text="Enter your username",placeholder_text_color="black",text_color="black",border_color="#430386",fg_color="transparent")
        unlock_screen_username_entry.place(relx=0.5,rely=0.4,anchor="center")
        digit_entry_widget1 = ctk.CTkEntry(unlock_screen,width=50,height=50,text_color="white",border_color="#430386",font=("Times New Roman",30), justify="center")
        digit_entry_widget1.place(relx=0.2,rely=0.7,anchor="center")
        digit_entry_widget2 = ctk.CTkEntry(unlock_screen,width=50,height=50,text_color="white",border_color="#430386",font=("Times New Roman",30), justify="center")
        digit_entry_widget2.place(relx=0.4,rely=0.7,anchor="center")
        digit_entry_widget3 = ctk.CTkEntry(unlock_screen,width=50,height=50,text_color="white",border_color="#430386",font=("Times New Roman",30), justify="center")
        digit_entry_widget3.place(relx=0.6,rely=0.7,anchor="center")
        digit_entry_widget4 = ctk.CTkEntry(unlock_screen,width=50,height=50,text_color="white",border_color="#430386",font=("Times New Roman",30), justify="center")
        digit_entry_widget4.place(relx=0.8,rely=0.7,anchor="center")

        def on_keyrelease(event, next_entry=None):
            if len(event.widget.get()) == 1:
                if next_entry:
                    next_entry.focus_set()

            if len(digit_entry_widget4.get()) == 1:
                self.master.destroy()

        digit_entry_widget1.bind("<KeyRelease>", lambda event: on_keyrelease(event, digit_entry_widget2))
        digit_entry_widget2.bind("<KeyRelease>", lambda event: on_keyrelease(event, digit_entry_widget3))
        digit_entry_widget3.bind("<KeyRelease>", lambda event: on_keyrelease(event, digit_entry_widget4))
        digit_entry_widget4.bind("<KeyRelease>", on_keyrelease)        


if __name__ == "__main__":
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")

    print_database()
    root = ctk.CTk()
    app = LoginForm(root)
    root.mainloop()
