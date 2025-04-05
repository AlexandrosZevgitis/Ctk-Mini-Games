import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
import sqlite3
import hashlib
import uuid
import os
from PIL import Image
import tkinter as tk
import re

class CreateAccount():  

    def __init__(self,master):
        self.master = master
        self.master.title("Create An Account")
        self.master.minsize(400,400)
        self.master.maxsize(600,600)
        self.master.configure(fg_color="white")

        # load icon and images
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.image_filename = ["add.png", "hide.png", "view.png"]
        self.image_paths = {name: os.path.join(self.script_dir, "images", name) for name in self.image_filename}


        # Create an account header
        self_add_icon = ctk.CTkImage(Image.open(self.image_paths["add.png"]), size=(35,30))
        self.create_account_header = ctk.CTkLabel(self.master, text="Create An Account",image=self_add_icon, font=("Times New Roman", 35),compound="left",text_color="#430386")
        self.create_account_header.place(relx=0.5, rely=0.15, anchor="center")

        # email entry
        self.email_entry = ctk.CTkEntry(self.master, width=200, font=("Times New Roman", 15), placeholder_text="Example@email.com",placeholder_text_color="black",fg_color="transparent",border_color="#430386",text_color="black")
        self.email_entry.place(relx=0.5, rely=0.3, anchor = "center")
        self.email_entry.bind("<FocusOut>",self.on_email_focus_out)

        # username entry
        self.username_entry = ctk.CTkEntry(self.master, width=200,font=("Times New Roman", 15),placeholder_text="Enter Username...",placeholder_text_color="black",fg_color="transparent",border_color="#430386",text_color="black")
        self.username_entry.place(relx=0.5,rely=0.4,anchor="center")

        # password entry and toggle checkbox
        self.show_image = ctk.CTkImage(Image.open(self.image_paths["view.png"]),size=(35,30))
        self.hide_image = ctk.CTkImage(Image.open(self.image_paths["hide.png"]),size=(35,30))
        self.show_hide_label_icon = ctk.CTkLabel(self.master, text="",image=self.show_image,cursor="hand2")
        self.show_hide_label_icon.place(relx=0.765, rely=0.55, anchor="w")
        self.password_entry = ctk.CTkEntry(self.master, width=200, font=("Times New Roman", 15), placeholder_text="Password...", show="*",placeholder_text_color="black",fg_color="transparent",border_color="#430386",text_color="black")
        self.password_entry.place(relx=0.5, rely=0.5, anchor = "center")
        # repeat password entry
        self.repeat_password_entry = ctk.CTkEntry(self.master, width=200, font=("Times New Roman", 15), placeholder_text="Confirm Password...", show="*",placeholder_text_color="black",fg_color="transparent",border_color="#430386",text_color="black")
        self.repeat_password_entry.place(relx=0.5, rely=0.6, anchor = "center")
        # draw 3 lines for password strength
        self.pwd_line1 = tk.Canvas(self.master, width=62, height=3, bg="black", highlightthickness=0)
        self.pwd_line1.place(relx=0.34,rely=0.65, anchor="center")
        self.pwd_line2 = tk.Canvas(self.master, width=62, height=3, bg="black", highlightthickness=0)
        self.pwd_line2.place(relx=0.5,rely=0.65, anchor="center")
        self.pwd_line3 = tk.Canvas(self.master, width=62, height=3, bg="black", highlightthickness=0)
        self.pwd_line3.place(relx=0.66,rely=0.65, anchor="center")
        # label to show weak-medium-strong
        self.pwd_strength_label = ctk.CTkLabel(self.master,text="Strong",font=("Times New Roman",14,"bold"),text_color="black")
        self.pwd_strength_label.place(relx=0.81,rely=0.65,anchor="center")
        self.password_entry.bind("<KeyRelease>", self.check_password_strength)
        # bind label with click
        self.show_hide_label_icon.bind("<Button-1>", self.toggle_password)
        self.is_viewing = True

        # 4 digit code for fast login
        self.digit_code_login = ctk.CTkEntry(self.master,width=200,font=("Times New Roman",15),placeholder_text="Enter 4 Digit Code...",placeholder_text_color="black",fg_color="transparent",border_color="#430386",text_color="black")
        self.digit_code_login.place(relx=0.5,rely=0.7,anchor="center")
        self.digit_code_login.bind("<KeyRelease>",self.check_digit_code)

        # create account button 
        self.create_account_button = ctk.CTkButton(self.master, text="Create Account", width=200, font=("Times New Roman", 15), corner_radius=50, cursor="hand2", command=self.create_account,fg_color="#430386")
        self.create_account_button.place(relx=0.5, rely=0.8, anchor="center")

    def on_email_focus_out(self,event):
        email = self.email_entry.get().strip()

        # Check if email contains '@'
        if "@" not in email:
            self.email_entry.delete(0,"end")
            self.email_entry.configure(placeholder_text="Email must contain @",placeholder_text_color="red")  # Ensure text color is black
            self.email_entry.configure(text_color="black")
            return None
        else:
            pass

        
    def create_account(self):
        email = self.email_entry.get().strip()
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        repeat_password = self.repeat_password_entry.get().strip()
        code = self.digit_code_login.get()

        if not email and not username and not password and not repeat_password and not code:
            self.email_entry.configure(placeholder_text="All fields are required!!",placeholder_text_color="red")
            self.username_entry.configure(placeholder_text="All fields are required!!",placeholder_text_color="red")
            self.password_entry.configure(placeholder_text="All fields are required!!",placeholder_text_color="red")
            self.repeat_password_entry.configure(placeholder_text="All fields are required!!",placeholder_text_color="red")
            self.digit_code_login.configure(placeholder_text="All fields are required!!",placeholder_text_color="red")
            return None

        # Check if username is provided
        if not username:
            self.username_entry.configure(placeholder_text="Username is required!", placeholder_text_color="red")
            return None

        # Check if passwords match
        if password and repeat_password:
            if password != repeat_password:
                self.password_entry.delete(0, "end")
                self.repeat_password_entry.delete(0, "end")
                self.password_entry.configure(placeholder_text="Passwords don't match!", placeholder_text_color="red")
                self.repeat_password_entry.configure(placeholder_text="Passwords don't match!", placeholder_text_color="red")
                return None
        else:
            self.password_entry.configure(placeholder_text="All fields are required!!",placeholder_text_color="red")
            self.repeat_password_entry.configure(placeholder_text="All fields are required!!",placeholder_text_color="red")

        # Check if the code is 4 digits
        if len(code) != 4 or not code.isdigit():
            self.digit_code_login.delete(0, "end")
            self.digit_code_login.configure(placeholder_text="4 digit code is required!", placeholder_text_color="red")
            return None

        # Check if the email or username already exists
        if self.check_email_or_username(email, username):
            return None

        salt = uuid.uuid4().hex
        hashed_password = hashlib.sha256((password+salt).encode()).hexdigest()

        connect_login = sqlite3.connect("users.db")
        cursor = connect_login.cursor()
        cursor.execute("INSERT INTO users (email,username,hash_password,salt,code) VALUES (?,?,?,?,?)",(email,username,hashed_password,salt,code))
        connect_login.commit()
        connect_login.close()
        connect_game = sqlite3.connect("game.db")
        cursor_game = connect_game.cursor()
        cursor_game.execute("INSERT INTO game (username) VALUES (?)",(username,))
        connect_game.commit()
        connect_game.close()

        self.master.after(1000,self.master.destroy)

    def toggle_password(self, event):
        # toggle password visibility
        if self.is_viewing:
            self.show_hide_label_icon.configure(image=self.hide_image)
            self.password_entry.configure(show="")
            self.repeat_password_entry.configure(show="")
        else:
            self.show_hide_label_icon.configure(image=self.show_image)
            self.password_entry.configure(show="*")
            self.repeat_password_entry.configure(show="*")
        self.is_viewing = not self.is_viewing

    def check_password_strength(self, event):
        self.pwd_strength = self.password_entry.get().strip()

        # Reset the lines to their default state
        self.pwd_line1.config(bg="black")
        self.pwd_line2.config(bg="black")
        self.pwd_line3.config(bg="black")

        # Only lowercase + digits -> weak
        if re.match("^[a-z0-9]+$", self.pwd_strength):
            self.pwd_line1.config(bg="red")
            self.pwd_line2.config(bg="black")
            self.pwd_line3.config(bg="black")
            self.pwd_strength_label.configure(text="Weak")

        # Only uppercase + digits -> weak
        elif re.match("^[A-Z0-9]+$", self.pwd_strength):
            self.pwd_line1.config(bg="red")
            self.pwd_line2.config(bg="black")
            self.pwd_line3.config(bg="black")
            self.pwd_strength_label.configure(text="Weak")

        # Lowercase + uppercase + digits -> medium
        elif re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z0-9]+$", self.pwd_strength):
            self.pwd_line1.config(bg="red")
            self.pwd_line2.config(bg="#d1b604")
            self.pwd_line3.config(bg="black")
            self.pwd_strength_label.configure(text="Medium")

        # Lowercase + uppercase + digits + special characters -> strong
        elif re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+={}\[\]:;,.<>?/~`|-]).+$", self.pwd_strength):
            self.pwd_line1.config(bg="red")
            self.pwd_line2.config(bg="#d1b604")
            self.pwd_line3.config(bg="#23d104")
            self.pwd_strength_label.configure(text="Strong")

        # Lowercase + digits + special characters (but NO uppercase) -> medium
        elif re.match(r"^(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*()_+={}\[\]:;,.<>?/~`|-])(?!.*[A-Z]).+$", self.pwd_strength):
            self.pwd_line1.config(bg="red")
            self.pwd_line2.config(bg="#d1b604")
            self.pwd_line3.config(bg="black")
            self.pwd_strength_label.configure(text="Medium")

        # Uppercase + digits + special characters -> medium (after ensuring it's not strong)
        elif re.match(r"^(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+={}\[\]:;,.<>?/~`|-])[A-Za-z0-9!@#$%^&*()_+={}\[\]:;,.<>?/~`|-]+$", self.pwd_strength):
            self.pwd_line1.config(bg="red")
            self.pwd_line2.config(bg="#d1b604")
            self.pwd_line3.config(bg="black")
            self.pwd_strength_label.configure(text="Medium")

        else:
            # Password does not match any criteria (this is for invalid input or empty password)
            self.pwd_line1.config(bg="red")
            self.pwd_line2.config(bg="black")
            self.pwd_line3.config(bg="black")
            self.pwd_strength_label.configure(text="Weak")

    def check_digit_code(self,event=None):
        current_text = self.digit_code_login.get()
        new_text = ""

        # Keep only digits
        for char in current_text:
            if char.isdigit():
                new_text += char

        # Limit to max 4 digits
        new_text = new_text[:4]

        # If something changed, update the Entry
        if new_text != current_text:
            self.digit_code_login.delete(0, "end")
            self.digit_code_login.insert(0, new_text)

    def check_email_or_username(self,email,username):
        connect_login = sqlite3.connect("users.db")
        cursor = connect_login.cursor()
        
        cursor.execute("SELECT email, username FROM users WHERE email = ? and username = ?", (email,username))

        result = cursor.fetchone()
    
        if result:
            # Check if the email or username exists and set the appropriate placeholder text
            if result[0] == email:  # Check if the email already exists
                self.email_entry.configure(placeholder_text="Email already exists!", placeholder_text_color="red")
                connect_login.close()
                return True
            if result[1] == username:  # Check if the username already exists
                self.username_entry.configure(placeholder_text="Username already exists!", placeholder_text_color="red")
                connect_login.close()
                return True


if __name__ == "__main__":
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    app = CreateAccount(root)
    root.mainloop()        
