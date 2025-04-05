import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
import sqlite3
import hashlib
import uuid
import os
from PIL import Image

class Forgot_Password():

    def __init__(self, master):
        self.master = master
        self.master.title("Reset Password")
        self.master.minsize(400,400)
        self.master.maxsize(600,600)
        self.master.configure(fg_color="white")

        # load icon and images
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.image_filename = ["reset_password.png", "hide.png", "view.png"]
        self.image_paths = {name: os.path.join(self.script_dir, "images", name) for name in self.image_filename}

        # Forgot password header and key icon
        self.key_icon = ctk.CTkImage(Image.open(self.image_paths["reset_password.png"]),size=(45,40))
        self.forgot_password_header = ctk.CTkLabel(self.master, text="Set Password", font=("Times New Roman", 50,"bold"),image=self.key_icon,compound="left",text_color="#430386")
        self.forgot_password_header.place(relx=0.47, rely=0.25, anchor="center")
        
        # Username entry 
        self.username_entry = ctk.CTkEntry(self.master, width=170, font=("Times New Roman", 20), placeholder_text="Username...",placeholder_text_color="black",fg_color="transparent",border_color="#430386",text_color="black")
        self.username_entry.place(relx=0.5, rely=0.425, anchor="center")

        # password hide and show
        self.show_image = ctk.CTkImage(Image.open(self.image_paths["view.png"]),size=(35,30))
        self.hide_image = ctk.CTkImage(Image.open(self.image_paths["hide.png"]),size=(35,30))
        self.show_hide_label_icon = ctk.CTkLabel(self.master, text="", image=self.show_image,cursor="hand2")
        self.show_hide_label_icon.place(relx=0.725, rely=0.57, anchor="w")
        # bind label with click
        self.show_hide_label_icon.bind("<Button-1>", self.toggle_password)
        self.is_viewing = True

        # Old password entry
        self.old_password_entry = ctk.CTkEntry(self.master, width=170, font=("Times New Roman", 20), placeholder_text="Old Password...", show="*",placeholder_text_color="black",fg_color="transparent",border_color="#430386",text_color="black")
        self.old_password_entry.place(relx=0.5, rely=0.525, anchor="center")

        # New password entry
        self.new_password_entry = ctk.CTkEntry(self.master, width=170, font=("Times New Roman", 20), placeholder_text="New Password...", show="*",placeholder_text_color="black",fg_color="transparent",border_color="#430386",text_color="black")
        self.new_password_entry.place(relx=0.5, rely=0.625, anchor="center")

        # New password repeat entry
        self.repeat_new_password_entry = ctk.CTkEntry(self.master, width=170, font=("Times new Roman", 20), placeholder_text="Repeat Password...", show="*",placeholder_text_color="black",fg_color="transparent",border_color="#430386",text_color="black")
        self.repeat_new_password_entry.place(relx=0.5, rely=0.725, anchor="center")

        # New password confirm button
        self.new_password_confirm_button = ctk.CTkButton(self.master,text="Reset Password", width=170, font=("Times New Roman", 20), cursor="hand2", corner_radius=50, command=self.reset_password, fg_color="#430386",hover=None)
        self.new_password_confirm_button.place(relx=0.5, rely=0.85, anchor="center")

    def toggle_password(self, event):
        # toggle password visibility
        if self.is_viewing:
            self.show_hide_label_icon.configure(image=self.hide_image)
            self.old_password_entry.configure(show="")
            self.new_password_entry.configure(show="")
            self.repeat_new_password_entry.configure(show="")
        else:
            self.show_hide_label_icon.configure(image=self.show_image)
            self.old_password_entry.configure(show="*")
            self.new_password_entry.configure(show="*")
            self.repeat_new_password_entry.configure(show="*")
        self.is_viewing = not self.is_viewing

    def reset_password(self):
        username = self.username_entry.get().strip()
        old_password = self.old_password_entry.get().strip()
        new_password = self.new_password_entry.get().strip()
        repeat_password = self.repeat_new_password_entry.get().strip()

        if not username and not old_password and not new_password and not repeat_password:
            self.username_entry.configure(placeholder_text="All fields are required!",placeholder_text_color="red")
            self.old_password_entry.configure(placeholder_text="All fields are required!",placeholder_text_color="red")
            self.new_password_entry.configure(placeholder_text="All fields are required!",placeholder_text_color="red")
            self.repeat_new_password_entry.configure(placeholder_text="All fields are required!",placeholder_text_color="red")
            return None
        
        connect = sqlite3.connect("users.db")
        cursor = connect.cursor()

        cursor.execute("SELECT tries FROM users WHERE username = ?", (username,))
        stored_tries = cursor.fetchone()
        cursor.execute("SELECT username FROM users WHERE username = ?", (username,))
        existing_user = cursor.fetchone()

        if not existing_user:
            self.username_entry.configure(placeholder_text="Username not exists!",placeholder_text_color="red")
            connect.close()
            return None
        
        cursor.execute("SELECT salt FROM users WHERE username = ?", (username,))
        old_salt = cursor.fetchone()
        
        if old_salt:
            old_salt = old_salt[0]
        else:
            connect.close()
            return None
        
        old_hashed_password = hashlib.sha256((old_password + old_salt).encode()).hexdigest()

        cursor.execute("SELECT hash_password FROM users WHERE username = ?",(username,))
        stored_hashed_password = cursor.fetchone()

        if stored_hashed_password:
            stored_hashed_password = stored_hashed_password[0]
        else:
            connect.close()
            return None
        
        if old_hashed_password != stored_hashed_password:
            self.old_password_entry.configure(placeholder_text="Incorrect old password!",placeholder_text_color="red")
            connect.close()
            return None
        
        if new_password != repeat_password:
            self.new_password_entry.configure(placeholder_text="Passwords do not match!",placeholder_text_color="red")
            self.repeat_new_password_entry.configure(placeholder_text="Passwords do not match!",placeholder_text_color="red")
            connect.close()
            return
        
        stored_tries = 0
        new_salt = uuid.uuid4().hex
        new_hashed_password = hashlib.sha256((new_password + new_salt).encode()).hexdigest()

        cursor.execute("UPDATE users SET hash_password = ?, salt = ?, tries = ? WHERE username = ?", (new_hashed_password, new_salt, stored_tries, username))
        connect.commit()
        connect.close()

        self.master.after(1000, self.master.destroy)


if __name__ == "__main__":
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    app = Forgot_Password(root)
    root.mainloop()    