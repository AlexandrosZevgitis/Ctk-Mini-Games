import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
import sqlite3
import hashlib
import uuid

class Forgot_Password():

    def __init__(self, master):
        self.master = master
        self.master.title("Reset Password")
        self.master.minsize(400,400)
        self.master.maxsize(600,600)

        # Forgot password header
        self.forgot_password_header = ctk.CTkLabel(self.master, text="Reset Password", font=("Times New Roman", 25))
        self.forgot_password_header.place(relx=0.5, rely=0.3, anchor="center")
        
        # Username entry 
        self.username_entry = ctk.CTkEntry(self.master, width=150, font=("Times New Roman", 15), placeholder_text="Username..." )
        self.username_entry.place(relx=0.5, rely=0.4, anchor="center")

        # password checkbox
        self.show_password_var = ctk.BooleanVar(value = False)
        self.toggle_password_button = ctk.CTkCheckBox(self.master, text="Show\nPassword", variable=self.show_password_var, command=self.toggle_password)
        self.toggle_password_button.place(relx=0.7, rely=0.6, anchor="w")

        # Old password entry
        self.old_password_entry = ctk.CTkEntry(self.master, width=150, font=("Times New Roman", 15), placeholder_text="Old Password...", show="*")
        self.old_password_entry.place(relx=0.5, rely=0.5, anchor="center")

        # New password entry
        self.new_password_entry = ctk.CTkEntry(self.master, width=150, font=("Times New Roman", 15), placeholder_text="New Password...", show="*")
        self.new_password_entry.place(relx=0.5, rely=0.6, anchor="center")

        # New password repeat entry
        self.repeat_new_password_entry = ctk.CTkEntry(self.master, width=150, font=("Times new Roman", 15), placeholder_text="Repeat Password...", show="*")
        self.repeat_new_password_entry.place(relx=0.5, rely=0.7, anchor="center")

        # New password confirm button
        self.new_password_confirm_button = ctk.CTkButton(self.master,text="Confirm New Password", width=15, font=("Times New Roman", 15), cursor="hand2", corner_radius=50, command=self.reset_password)
        self.new_password_confirm_button.place(relx=0.5, rely=0.8, anchor="center")

    def toggle_password(self):
        if self.show_password_var.get():
            self.old_password_entry.configure(show="")
            self.new_password_entry.configure(show="")
            self.repeat_new_password_entry.configure(show="")
        else:
            self.old_password_entry.configure(show="*")
            self.new_password_entry.configure(show="*")
            self.repeat_new_password_entry.configure(show="*")

    def reset_password(self):
        username = self.username_entry.get().strip()
        old_password = self.old_password_entry.get().strip()
        new_password = self.new_password_entry.get().strip()
        repeat_password = self.repeat_new_password_entry.get().strip()

        if not username or not old_password or not new_password or not repeat_password:
            CTkMessagebox(title="Error", message="All fields are required!!!", icon="cancel")
            return
        
        connect = sqlite3.connect("login.db")
        cursor = connect.cursor()

        cursor.execute("SELECT tries FROM users WHERE username = ?", (username,))
        stored_tries = cursor.fetchone()
        cursor.execute("SELECT username FROM users WHERE username = ?", (username,))
        existing_user = cursor.fetchone()

        if not existing_user:
            CTkMessagebox(title="Error", message="Username do not found in database. Please try again with your correct username", icon="warning")
            connect.close()
            return
        
        cursor.execute("SELECT salt FROM users WHERE username = ?", (username,))
        old_salt = cursor.fetchone()
        
        if old_salt:
            old_salt = old_salt[0]
        else:
            CTkMessagebox(title="Error", message="Error retrieving salt for user.", icon="warning")
            connect.close()
            return
        
        old_hashed_password = hashlib.sha256((old_password + old_salt).encode()).hexdigest()

        cursor.execute("SELECT hash_password FROM users WHERE username = ?",(username,))
        stored_hashed_password = cursor.fetchone()

        if stored_hashed_password:
            stored_hashed_password = stored_hashed_password[0]
        else:
            CTkMessagebox(title="Error", message="Error retrieving user password", icon="warning")
            connect.close()
            return
        
        if old_hashed_password != stored_hashed_password:
            CTkMessagebox(title="Error", message="Old password is incorrect", icon="warning")
            connect.close()
            return
        
        if new_password != repeat_password:
            CTkMessagebox(title="Error", message="Passwords do not match!", icon="warning")
            connect.close()
            return
        
        stored_tries = 0
        new_salt = uuid.uuid4().hex
        new_hashed_password = hashlib.sha256((new_password + new_salt).encode()).hexdigest()

        cursor.execute("UPDATE users SET hash_password = ?, salt = ?, tries = ? WHERE username = ?", (new_hashed_password, new_salt, stored_tries, username))
        connect.commit()
        connect.close()

        CTkMessagebox(title="Success", message="Password has been reset successfully!", icon="check")

        self.master.after(2000, self.master.destroy)


if __name__ == "__main__":
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    app = Forgot_Password(root)
    root.mainloop()    