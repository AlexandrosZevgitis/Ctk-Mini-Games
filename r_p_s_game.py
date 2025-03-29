import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
import sqlite3
import random
import time

class RPSGame():

    def __init__(self, master,username,update_callback):
        self.master = master
        self.username = username
        self.update_callback = update_callback
        self.master.title("Rock - Paper - Scissor Game")
        self.master.minsize(800,600)
        self.master.maxsize(800,600)

        self.win_points = 30
        self.loss_points = 15
        self.button_pressed = None
        self.computer_choices = ["rock", "paper", "scissor"]

        # top head label
        self_game_top_head_label = ctk.CTkLabel(master, text="Welcome to\nROCK - PAPER - SCISSOR game.", font=("Times New Roman", 30))
        self_game_top_head_label.place(relx=0.5,rely=0.12,anchor="center")

        # 3 top computer buttons for choices 
        self.computer_rock_button = ctk.CTkButton(master, text="ROCK", width=130, corner_radius=50, height=50, font=("Times New Roman", 20), state="disabled")
        self.computer_rock_button.place(relx=0.3,rely=0.25,anchor="center")
        self.computer_paper_button = ctk.CTkButton(master, text="PAPER", width=130, corner_radius=50, height=50, font=("Times New Roman", 20), state="disabled")
        self.computer_paper_button.place(relx=0.5,rely=0.25,anchor="center")
        self.computer_scissor_button = ctk.CTkButton(master, text="SCISSOR", width=130, corner_radius=50, height=50, font=("Times New Roman", 20), state="disabled")
        self.computer_scissor_button.place(relx=0.7,rely=0.25,anchor="center")

        # example button for computer choice
        self.computer_choice_button = ctk.CTkButton(master, width=130, height=50, corner_radius=50, text="Computer\nChoice", font=("Times New Roman", 20), state="disabled")
        self.computer_choice_button.place(relx=0.5,rely=0.4,anchor="center")

        # middle label showing VS 
        self.middle_vs_label = ctk.CTkLabel(master,text="VS", font=("Times New Roman", 25))
        self.middle_vs_label.place(relx=0.5,rely=0.55,anchor="center")

        # example button for user choice
        self.user_choice_button = ctk.CTkButton(master, width=130, height=50, text="User\nChoice", corner_radius=50, font=("Times New Roman", 20), state="disabled")
        self.user_choice_button.place(relx=0.5,rely=0.7,anchor="center")

        # 3 bot user button for choices 
        self.user_rock_button = ctk.CTkButton(master, text="ROCK", width=130, height=50, corner_radius=50, font=("Times New Roman", 20), command=lambda: self.button_pressed_callback("rock",username))
        self.user_rock_button.place(relx=0.3,rely=0.85,anchor="center")
        self.user_paper_button = ctk.CTkButton(master, text="PAPER", width=130, height=50, corner_radius=50, font=("Times New Roman", 20), command=lambda: self.button_pressed_callback("paper",username))
        self.user_paper_button.place(relx=0.5,rely=0.85,anchor="center")
        self.user_scissor_button = ctk.CTkButton(master, text="SCISSOR", width=130, height=50, corner_radius=50, font=("Times New Roman", 20), command=lambda: self.button_pressed_callback("scissor",username))
        self.user_scissor_button.place(relx=0.7,rely=0.85,anchor="center")

    def reset_game(self):
        # Destroy all widgets (or hide them)
        self.computer_choice_button.destroy()
        self.user_choice_button.destroy()
        self.user_rock_button.destroy()
        self.user_paper_button.destroy()
        self.user_scissor_button.destroy()
        self.computer_rock_button.destroy()
        self.computer_paper_button.destroy()
        self.computer_scissor_button.destroy()
        self.middle_vs_label.destroy()

        # Reset game variables
        self.button_pressed = None

        # Recreate the game UI
        self.__init__(self.master,self.username,self.update_callback)

    def button_pressed_callback(self,button,username):
        self.button_pressed = button
        self.process_game(username)

    def find_user_points(self,username):
        # connect to the database to handle the points 
        connect = sqlite3.connect("game.db")
        cursor = connect.cursor()
        total_user_points = cursor.execute("SELECT points from game WHERE username = ?", (username,))
        result = total_user_points.fetchone()
        

        if result:
            total_user_points = result[0]
        else:
            total_user_points = 0
        connect.commit()
        connect.close()

        return total_user_points


    def process_game(self, username):
        # connect to the database to handle the points 
        connect = sqlite3.connect("game.db")
        cursor = connect.cursor()

        self.random_computer = random.randint(0,2)
        self.computer_choice = self.computer_choices[self.random_computer]

        
        if self.button_pressed == "rock":
            self.user_rock_button.destroy()
            self.user_choice_button.configure(text="ROCK")
            if self.computer_choice == "rock":
                self.computer_rock_button.destroy()
                self.computer_choice_button.configure(text="ROCK")
                time.sleep(1)
                total_user_points = self.find_user_points(username)
                connect.commit()
                connect.close()
                self.master.winfo_toplevel().grab_release()
                self.msg = CTkMessagebox(title="Info", message=f"Game was a TIE\nPlay again to win.\nTotal Points: {total_user_points}", icon="question", option_1="Exit Game", option_2="Play Again")
                if self.msg.get() == "Exit Game":
                    self.update_callback(self.username)
                    self.master.destroy()
                else:
                    self.master.after(1000, self.reset_game)
            elif self.computer_choice == "scissor":
                self.computer_scissor_button.destroy()
                self.computer_choice_button.configure(text="SCISSOR")
                time.sleep(1)
                cursor.execute("UPDATE game SET points = points + ?, r_p_s = r_p_s + ? WHERE username = ?", (self.win_points, 1, username))
                connect.commit()
                total_user_points = self.find_user_points(username)
                connect.close()
                self.master.winfo_toplevel().grab_release()
                self.msg = CTkMessagebox(title="Congratulations", message=f"Congratulations.\nYou won {self.win_points} points.\nTotal Points: {total_user_points}", icon="check", option_1="Exit Game", option_2="Play Again")
                if self.msg.get() == "Exit Game":
                    self.update_callback(self.username)
                    self.master.destroy()
                else:
                    self.master.after(1000, self.reset_game)
            else:
                self.computer_paper_button.destroy()
                self.computer_choice_button.configure(text="PAPER")
                time.sleep(1)
                cursor.execute("UPDATE game SET points = points - ? WHERE username = ?", (self.loss_points, username))
                connect.commit()
                total_user_points = self.find_user_points(username)
                connect.close()
                self.master.winfo_toplevel().grab_release()
                self.msg = CTkMessagebox(title="Game Over", message=f"Too bad.\nYou lost {self.loss_points} points.\nBetter luck next time.\nTotal Points: {total_user_points}", icon="cancel", option_1="Exit Game", option_2="Play Again")
                if self.msg.get() == "Exit Game":
                    self.update_callback(self.username)
                    self.master.destroy()
                else:
                    self.master.after(1000, self.reset_game)

        if self.button_pressed == "paper":
            self.user_paper_button.destroy()
            self.user_choice_button.configure(text="PAPER")
            if self.computer_choice == "paper":
                self.computer_paper_button.destroy()
                self.computer_choice_button.configure(text="PAPER")
                time.sleep(1)
                total_user_points = self.find_user_points(username)
                connect.commit()
                connect.close()
                self.master.winfo_toplevel().grab_release()
                self.msg = CTkMessagebox(title="Info", message=f"Game was a TIE\nPlay again to win.\nTotal Points: {total_user_points}", icon="question", option_1="Exit Game", option_2="Play Again")
                if self.msg.get() == "Exit Game":
                    self.update_callback(self.username)
                    self.master.destroy()
                else:
                    self.master.after(1000, self.reset_game)
            elif self.computer_choice == "rock":
                self.computer_rock_button.destroy()
                self.computer_choice_button.configure(text="ROCK")
                time.sleep(1)
                cursor.execute("UPDATE game SET points = points + ?, r_p_s = r_p_s + ? WHERE username = ?", (self.win_points, 1, username))
                connect.commit()
                total_user_points = self.find_user_points(username)
                connect.close()
                self.master.winfo_toplevel().grab_release()
                self.msg = CTkMessagebox(title="Congratulations", message=f"Congratulations.\nYou won {self.win_points} points.\nTotal Points: {total_user_points}", icon="check", option_1="Exit Game", option_2="Play Again")
                if self.msg.get() == "Exit Game":
                    self.update_callback(self.username)
                    self.master.destroy()
                else:
                    self.master.after(1000, self.reset_game)
            else:
                self.computer_scissor_button.destroy()
                self.computer_choice_button.configure(text="SCISSOR")
                time.sleep(1)
                cursor.execute("UPDATE game SET points = points - ? WHERE username = ?", (self.loss_points, username))
                connect.commit()
                total_user_points = self.find_user_points(username)
                connect.close()
                self.master.winfo_toplevel().grab_release()
                self.msg = CTkMessagebox(title="Game Over", message=f"Too bad.\nYou lost {self.loss_points} points..\nBetter luck next time.\nTotal Points: {total_user_points}", icon="cancel", option_1="Exit Game", option_2="Play Again")
                if self.msg.get() == "Exit Game":
                    self.update_callback(self.username)
                    self.master.destroy()
                else:
                    self.master.after(1000, self.reset_game)

        if self.button_pressed == "scissor":
            self.user_scissor_button.destroy()
            self.user_choice_button.configure(text="SCISSOR")
            if self.computer_choice == "scissor":
                self.computer_scissor_button.destroy()
                self.computer_choice_button.configure(text="SCISSOR")
                time.sleep(1)
                total_user_points = self.find_user_points(username)
                connect.commit()
                connect.close()
                self.master.winfo_toplevel().grab_release()
                self.msg = CTkMessagebox(title="Info", message=f"Game was a TIE\nPlay again to win.\nTotal Points: {total_user_points}", icon="question", option_1="Exit Game", option_2="Play Again")
                if self.msg.get() == "Exit Game":
                    self.update_callback(self.username)
                    self.master.destroy()
                else:
                    self.master.after(1000, self.reset_game)
            elif self.computer_choice == "paper":
                self.computer_paper_button.destroy()
                self.computer_choice_button.configure(text="PAPER")
                time.sleep(1)
                cursor.execute("UPDATE game SET points = points + ?, r_p_s = r_p_s + ? WHERE username = ?", (self.win_points, 1, username))
                connect.commit()
                total_user_points = self.find_user_points(username)
                connect.close()
                self.master.winfo_toplevel().grab_release()
                self.msg = CTkMessagebox(title="Congratulations", message=f"Congratulations.\nYou won {self.win_points} points.\nTotal Points: {total_user_points}", icon="check", option_1="Exit Game", option_2="Play Again")
                if self.msg.get() == "Exit Game":
                    self.update_callback(self.username)
                    self.master.destroy()
                else:
                    self.master.after(1000, self.reset_game)
            else:
                self.computer_rock_button.destroy()
                self.computer_choice_button.configure(text="ROCK")
                time.sleep(1)
                cursor.execute("UPDATE game SET points = points - ? WHERE username = ?", (self.loss_points, username))
                connect.commit()
                total_user_points = self.find_user_points(username)
                connect.close()
                self.master.winfo_toplevel().grab_release()
                self.msg = CTkMessagebox(title="Game Over", message=f"Too bad.\nYou lost {self.loss_points} points..\nBetter luck next time.\nTotal Points: {total_user_points}", icon="cancel", option_1="Exit Game", option_2="Play Again")
                if self.msg.get() == "Exit Game":
                    self.update_callback(self.username)
                    self.master.destroy()
                else:
                    self.master.after(1000, self.reset_game)

    

if __name__ == "__main__":
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    app = RPSGame(root)
    root.mainloop()
