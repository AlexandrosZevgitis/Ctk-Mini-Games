import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
import sqlite3
import hashlib
import uuid

class CreateAccount():  

    def __init__(self,master):
        self.master = master
        self.master.title("Create An Account")
        self.master.minsize(400,400)
        self.master.maxsize(600,600)


        # Create an account header
        self.create_account_header = ctk.CTkLabel(self.master, text="Create An Account", font=("Times New Roman", 25))
        self.create_account_header.place(relx=0.5, rely=0.3, anchor="center")

        # username entry
        self.username_entry = ctk.CTkEntry(self.master, width=150, font=("Times New Roman", 15), placeholder_text="Username...")
        self.username_entry.place(relx=0.5, rely=0.4, anchor = "center")

        # password entry and toggle checkbox
        self.show_password_var = ctk.BooleanVar(value=False)
        self.toggle_password_button = ctk.CTkCheckBox(self.master, text="Show\nPassword", corner_radius=50, variable=self.show_password_var, command=self.toggle_password)
        self.toggle_password_button.place(relx=0.7, rely=0.5, anchor="w")
        self.password_entry = ctk.CTkEntry(self.master, width=150, font=("Times New Roman", 15), placeholder_text="Password...", show="*")
        self.password_entry.place(relx=0.5, rely=0.5, anchor = "center")
        # repeat password entry and toggle checkbox
        self.repeat_password_entry = ctk.CTkEntry(self.master, width=150, font=("Times New Roman", 15), placeholder_text="Confirm Password...", show="*")
        self.repeat_password_entry.place(relx=0.5, rely=0.6, anchor = "center")

        # create account button 
        self.create_account_button = ctk.CTkButton(self.master, text="Create Account", width=150, font=("Times New Roman", 15), corner_radius=50, cursor="hand2", command=self.create_account)
        self.create_account_button.place(relx=0.5, rely=0.7, anchor="center")
        
    def create_account(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        repeat_password = self.repeat_password_entry.get().strip()

        if not username or not password or not repeat_password:
            CTkMessagebox(title="Error", message="All fields are required!!!", icon="cancel")
            return
            
        if password != repeat_password:
            CTkMessagebox(title="Error", message="Passwords do not match!", icon="warning")
            return
            
        connect = sqlite3.connect("login.db")
        cursor = connect.cursor()

        connect_game = sqlite3.connect("game.db")
        cursor_game = connect_game.cursor()

        cursor.execute("SELECT username FROM users WHERE username = ?", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            CTkMessagebox(title="Error", message="Username already exists!\nPlease try another username.", icon="warning")
            connect.close()
            return
            
        salt = uuid.uuid4().hex
        hashed_password = hashlib.sha256((password + salt).encode()).hexdigest()

        cursor.execute("INSERT INTO users (username, hash_password, salt) VALUES (?, ?, ?)", (username, hashed_password, salt))
        cursor_game.execute("""
                INSERT INTO game (username, mastermind, g_t_n, hangman, r_p_s, points)
                VALUES (?, 0, 0, 0, 0, 100)
            """, (username,))
        connect.commit()
        connect.close()
        connect_game.commit()
        connect_game.close()

        CTkMessagebox(title="Confirm", message="Account created successfully!", icon="check")

        self.master.after(2000, self.master.destroy)

    def toggle_password(self):
        # toggle password visibility
        if self.show_password_var.get():
            self.password_entry.configure(show="")
            self.repeat_password_entry.configure(show="")
        else:
            self.password_entry.configure(show="*")
            self.repeat_password_entry.configure(show="*")




if __name__ == "__main__":
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    app = CreateAccount(root)
    root.mainloop()        
