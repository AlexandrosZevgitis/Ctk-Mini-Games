import customtkinter as ctk
import sqlite3
from CTkMessagebox import CTkMessagebox
import random
import time

class MasterMind():

    def __init__(self, master,username,update_callback):
        self.master = master
        self.username = username
        self.update_callback = update_callback
        self.master.title("MasterMind Game")
        self.master.minsize(820, 950)
        self.master.maxsize(820,950)
        self.right_position = 0
        self.wrong_position = 0
        self.tries = 9
        self.color_index = 0
        self.index_i = 39
        self.enable_index = 44
        self.user_color_guesses = []
        self.hint_labels = []
        self.hint_index = 8

        # instances
        self.colors = ["#FFA500", "#FFC0CB", "#FFFFFF", "#00FFFF", 
                "#FFFF00", "#008000", "#FF0000", "#000000"]

        self.color_names = {
            "#FFA500": "Orange",
            "#FFC0CB": "Pink",
            "#FFFFFF": "White",
            "#00FFFF": "Cyan",
            "#FFFF00": "Yellow",
            "#008000": "Green",
            "#FF0000": "Red",
            "#000000": "Black"
            }
        
        self.win_points = 50
        self.loss_points = 25
        
        self.buttons_grid = []
        self.random_color_guesses = []

        self.top_head_label = ctk.CTkLabel(self.master, text="Welcome To the\nMasterMind Game!", font=("Times New Roman", 30, "bold", "underline"))
        self.top_head_label.place(relx=0.76,rely=0.05, anchor="center")

        # create the hint labels
        self.create_hint_labels()

        # create the button color labels
        self.create_button_grid()

        # bottom guess button
        self.bot_guess_button = ctk.CTkButton(self.master,text=f"Make A Guess - Tries Left: {self.tries}", corner_radius=50,width=500,height=70, font=("Times New Roman", 30),command=lambda: self.process_game(username))
        self.bot_guess_button.place(relx=0.5,rely=0.93,anchor="center")

        self.computer_colors()

    def create_hint_labels(self):
        self.distance = 0.13
        for i in range(9):
            label = ctk.CTkLabel(self.master, text=f"[{self.right_position} right position color]\n[{self.wrong_position} wrong position color]", font=("Times New Roman", 20))
            label.place(relx=0.65,rely=self.distance, anchor="center")
            self.hint_labels.append(label)
            self.distance += 0.089

    def update_hint_label(self, index, right_pos, wrong_pos):
        if 0 <= index < len(self.hint_labels):  # Ensure index is within range
            self.hint_labels[index].configure(text=f"[{right_pos} right position color]\n[{wrong_pos} wrong position color]")

    def game_reset(self):

        self.right_position = 0
        self.wrong_position = 0
        self.tries = 9
        self.color_index = 0
        self.index_i = 39
        self.enable_index = 44
        self.user_color_guesses = []
        self.hint_index = 8

        for btn in self.buttons_grid:
            btn.configure(state="normal", fg_color="#1F6AA5")

        self.bot_guess_button.configure(text=f"Make A Guess - Tries Left: {self.tries}")
        
        for i in range(36):
            self.buttons_grid[i].configure(state="disabled", fg_color="grey")

        for label in self.hint_labels:
            label.configure(text="[0 right position color]\n[0 wrong position color]")

        self.computer_colors()

    def print_color_names(self):
        for color in self.random_color_guesses:
            print(self.color_names.get(color, "Unknown color"), end=' ')
        print()

    def print_user_color_guesses(self):
        for color in self.user_color_guesses:
            print(self.color_names.get(color, "Unknown color"), end=' ')
        print()

    def create_button_grid(self):
        total_rows = 10
        total_columns = 6

        start_row = (total_rows - 10) // 2  # Start at middle row
        start_column = (total_columns - 4) // 2  # Start at middle column

        for i in range(40):
            row = start_row + i // 4
            column = start_column + i % 4

            self.button = ctk.CTkButton(self.master, text=f"", corner_radius=50, width=100, height=80, command=lambda i=i: self.button_callback(i),hover=None)
            self.button.grid(row=row, column=column, padx=2, pady=2)

            self.buttons_grid.append(self.button)

        for i in range(36):
            self.buttons_grid[i].configure(state="disabled", fg_color="grey")

    def computer_colors(self):
        self.random_color_guesses = random.sample(self.colors, 4)
            
        for i in range(4):
            self.buttons_grid[i].configure(fg_color=f"{self.random_color_guesses[i]}")

    def print_computer_colors(self):
        for i in range(4):
            self.buttons_grid[i].configure(fg_color=f"{self.random_color_guesses[i]}")

    def button_callback(self, index):
        self.button_pressed_index = index
        self.on_click_change(index)

    def on_click_change(self, index):
        if self.color_index == 8:
            self.color_index = 0
        self.buttons_grid[index].configure(fg_color=self.colors[self.color_index])
        self.color_index += 1

    def find_user_points(self, username):
        # find user points 
        connect = sqlite3.connect("game.db")
        cursor = connect.cursor()
        total_user_points = cursor.execute("SELECT points FROM game WHERE username = ?", (username,))
        result = total_user_points.fetchone()

        if total_user_points:
            total_user_points = result[0]
        else:
            total_user_points = 0
        connect.commit()
        connect.close()

        return total_user_points

    def process_game(self, username):
        connect = sqlite3.connect("game.db")
        cursor = connect.cursor()

        self.right_position = 0
        self.wrong_position = 0
        self.enable_index -= 4
        self.index_i -= 4
        self.user_color_guesses = []
        
        # get the colors of the enable state button in button grid 
        for btn in self.buttons_grid:
            if btn.cget('state') != "disabled":
                if btn.cget('fg_color') in self.colors:
                    self.user_color_guesses.append(btn.cget('fg_color')) 
                else:
                    self.master.winfo_toplevel().grab_release()
                    CTkMessagebox(title="Error", message="All fields required a color.", icon="warning")  
                    self.enable_index += 4
                    self.index_i += 4
                    self.user_color_guesses = [] 
                    return
        
        # checks if the user has give a duplicate color in a row 
        if len(set(self.user_color_guesses)) < len(self.user_color_guesses):
            self.master.winfo_toplevel().grab_release()
            CTkMessagebox(title="Error", message="Duplicate colors are not allowed.\nPlease give unique color combinations.", icon="warning")
            self.enable_index += 4
            self.index_i += 4
            self.user_color_guesses = [] 
            return
                
        print(self.user_color_guesses)
        print("User's color guesses: ", end="")
        self.print_user_color_guesses()
        print(self.random_color_guesses)

        if len(self.user_color_guesses) == 4:
            self.tries -= 1
            self.bot_guess_button.configure(text=f"Make A Guess - Tries Left: {self.tries}")
            if self.user_color_guesses == self.random_color_guesses:
                cursor.execute("UPDATE game SET points = points + ?, mastermind = mastermind + ? WHERE username = ?", (self.win_points,1,username))
                connect.commit()
                total_user_points = self.find_user_points(username)
                connect.close()
                self.master.winfo_toplevel().grab_release()
                self.msg = CTkMessagebox(title="Congratulations", message=f"Congratulations. You won {self.win_points} points.\nYou are now a MasterMind.\nTotal points: {total_user_points} points.",icon="check",option_1="Exit Game", option_2="Play Again")
                if self.msg.get() == "Exit Game":
                    self.update_callback(self.username)
                    self.master.destroy()
                else:
                    self.master.after(1000, self.game_reset)
            elif self.tries == 0:
                self.print_computer_colors()
                time.sleep(1)
                cursor.execute("UPDATE game SET points = points - ? WHERE username = ?", (self.loss_points, username))
                connect.commit()
                total_user_points = self.find_user_points(username)
                connect.close()
                self.master.winfo_toplevel().grab_release()
                self.msg = CTkMessagebox(title="Game Over", message=f"Too bad you lost {self.loss_points} points.\nBetter luck next time.\nTotal Points: {total_user_points} points.",icon="cancel",option_1="Exit Game", option_2="Play Again")
                if self.msg.get() == "Exit Game":
                    self.update_callback(self.username)
                    self.master.destroy()
                else:
                    self.master.after(1000, self.game_reset)
            else:
                for i in range(4):
                    # check the right position color answers
                    if self.user_color_guesses[i] == self.random_color_guesses[i]:
                        self.right_position += 1
                    
                    # check the wrong position color answers
                    elif self.user_color_guesses[i] in self.random_color_guesses and self.user_color_guesses[i] != self.random_color_guesses[i]:
                        self.wrong_position += 1

                print(self.right_position)
                print(self.wrong_position)
                # self.wrong_position = self.wrong_position - self.right_position
                self.update_hint_label(self.hint_index,self.right_position,self.wrong_position)
                self.hint_index -= 1

                # disable the 4 buttons of current row 
                for i in range(self.enable_index - 4, self.enable_index):    
                    self.enabled_button_fg_color = self.user_color_guesses[i - (self.enable_index - 4)]
                    self.buttons_grid[i].configure(state="disabled", fg_color=self.enabled_button_fg_color)

                # enable the next row 4 buttons
                for j in range(self.index_i, self.index_i - 4, -1):
                    self.buttons_grid[j].configure(state="enabled", fg_color="#1F6AA5", cursor="hand2")



if __name__ == "__main__":
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    app = MasterMind(root)
    root.mainloop()
