import customtkinter as ctk
import random
from CTkMessagebox import CTkMessagebox
import sqlite3
import time

class GuessTheNumber():
    
    def __init__(self, master,username,update_callback):
        self.master = master
        self.username = username
        self.update_callback = update_callback
        self.master.title("Guess The Number Game")
        self.master.minsize(1000, 600)

        # Instance variables to track
        self.player_vs_computer_win_points = 0
        self.player_vs_computer_loss_points = 0
        self.computer_vs_player_win_points = 35
        self.computer_vs_player_loss_points = 20
        self.button_pressed = None
        self.player_button_pressed = None
        self.guesses = []
        self.computer_guesses_array = []
        self.player_tries = 6
        self.low = 1
        self.high = 100
        
        # CREATING FRAMES
        self.left_small_frame = ctk.CTkFrame(master)
        self.left_small_frame.place(relx=0.1, relwidth=0.25, rely=0.5, relheight=1, anchor="center")
        self.rest_big_frame = ctk.CTkFrame(master)
        self.rest_big_frame.place(relx=0.7, relwidth=1, rely=0.5, relheight=1, anchor="center")

        # Left frame buttons
        self.left_small_frame_player_button = ctk.CTkButton(self.left_small_frame, width=150, corner_radius=50, height=100, text="Player\nVS\nComputer\n+40 , -10", font=("Times New Roman", 20), command=lambda: self.player_vs_computer(username))
        self.left_small_frame_player_button.place(relx=0.5, rely=0.3, anchor="center")
        self.left_small_frame_computer_button = ctk.CTkButton(self.left_small_frame, width=150, corner_radius=50, height=100, text="Computer\nVS\nPlayer\n+35 , -20", font=("Times New Roman", 20), command=lambda: self.computer_vs_player(username))
        self.left_small_frame_computer_button.place(relx=0.5, rely=0.58, anchor="center")

        self.rest_big_frame_top_label = ctk.CTkLabel(self.rest_big_frame, text="Welcome To Guess The Number Game", font=("Times New Roman", 40))
        self.rest_big_frame_top_label.place(relx=0.4, rely=0.2, anchor="center")

    def disable_frame_button(self):
        self.left_small_frame_player_button.configure(state="disabled") 
        self.left_small_frame_computer_button.configure(state="disabled")

    def reset_frames(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def reset_game(self):
    # Reset game variables
        self.player_tries = 6
        self.low = 1
        self.high = 100
        self.warnings = 0
        self.guesses = []
        self.computer_guesses_array = []
        self.button_pressed = None
        self.player_button_pressed = None

        # Enable buttons again
        self.left_small_frame_player_button.configure(state="normal")
        self.left_small_frame_computer_button.configure(state="normal")

        # Reset frames
        self.reset_frames(self.rest_big_frame)

        # Restore the welcome label
        self.rest_big_frame_top_label = ctk.CTkLabel(
            self.rest_big_frame, text="Welcome To Guess The Number Game", font=("Times New Roman", 40)
        )
        self.rest_big_frame_top_label.place(relx=0.4, rely=0.2, anchor="center")

    def player_vs_computer(self, username):

        # disable play button and exit button
        self.disable_frame_button()

        # reset the frame before game starts
        self.reset_frames(self.rest_big_frame)

        # big frame top label welcome 
        self.rest_big_frame_top_label = ctk.CTkLabel(self.rest_big_frame, text="Welcome To Guess The Number Game", font=("Times New Roman", 40))
        self.rest_big_frame_top_label.place(relx=0.4, rely=0.2, anchor="center")

        # Guess explain label
        self.rest_big_frame_guess_explain_label = ctk.CTkLabel(self.rest_big_frame, text="Try to guess in how many tries the computer will find your number.", font=("Times New Roman", 25))
        self.rest_big_frame_guess_explain_label.place(relx=0.4, rely=0.30, anchor="center")

        # Label and entry for user to enter a number
        self.rest_big_frame_entry_label = ctk.CTkLabel(self.rest_big_frame, text="Enter a number from 1 to 100", font=("Times New Roman", 25))
        self.rest_big_frame_entry_label.place(relx=0.4, rely=0.38, anchor="center")
        self.rest_big_frame_player_entry = ctk.CTkEntry(self.rest_big_frame, width=150, font=("Times New Roman", 20), placeholder_text="Enter the number...")
        self.rest_big_frame_player_entry.place(relx=0.4, rely=0.46, anchor="center")

        # button for computer tries 
        self.rest_big_frame_left_guess_button = ctk.CTkButton(self.rest_big_frame, corner_radius=50, width=80, height=60, text="less than 4\n+40 , -20", font=("Times New Roman", 20), cursor="hand2", command=lambda: self.button_callback("left", username))
        self.rest_big_frame_left_guess_button.place(relx=0.25, rely=0.55, anchor="center")
        self.rest_big_frame_middle_guess_button = ctk.CTkButton(self.rest_big_frame, corner_radius=50, width=80, height=60, text="5 - 6\n+30 , -15", font=("Times New Roman", 20), cursor="hand2",command=lambda: self.button_callback("middle", username))
        self.rest_big_frame_middle_guess_button.place(relx=0.4, rely=0.55, anchor="center")
        self.rest_big_frame_right_guess_button = ctk.CTkButton(self.rest_big_frame, corner_radius=50, width=80, height=60, text="7 - 10\n+20, -10", font=("Times New Roman", 20), cursor="hand2",command=lambda: self.button_callback("right", username))
        self.rest_big_frame_right_guess_button.place(relx=0.55, rely=0.55, anchor="center")

        # Label to display computer's guess
        self.rest_big_frame_computer_guess_label = ctk.CTkLabel(self.rest_big_frame, text="-", font=("Times New Roman", 20))
        self.rest_big_frame_computer_guess_label.place(relx=0.4, rely=0.65, anchor="center")

    def player_button_guess(self, username):
        self.computer_vs_player_game_logic(username)

    def computer_vs_player(self, username):

        # disable left frame button and exit
        self.disable_frame_button()

        # reset the frame before game starts
        self.reset_frames(self.rest_big_frame)

        # big frame top label welcome 
        self.rest_big_frame_top_label = ctk.CTkLabel(self.rest_big_frame, text="Welcome To Guess The Number Game", font=("Times New Roman", 40))
        self.rest_big_frame_top_label.place(relx=0.4, rely=0.2, anchor="center")

        self.computer_guess = random.randint(self.low, self.high)
        self.computer_guess_hidden = ctk.CTkLabel(self.rest_big_frame, text=f"Computer has generated successfully a number: {self.computer_guess}", font=("Times New Roman", 20))
        self.computer_guess_hidden.place(relx=0.4, rely=0.3, anchor="center")
        self.player_guess_entry = ctk.CTkEntry(self.rest_big_frame, width=200, font=("Times New Roman", 20), placeholder_text="Enter a number to guess")
        self.player_guess_entry.place(relx=0.4, rely=0.37, anchor="center")
        self.computer_hint_label = ctk.CTkLabel(self.rest_big_frame, text="", font=("Times New Roman", 15))
        self.computer_hint_label.place(relx=0.4, rely=0.43, anchor="center")
        self.player_guess_button = ctk.CTkButton(self.rest_big_frame, width=200, corner_radius=50, text="Make A Guess", font=("Times New Roman", 15), cursor="hand2", command=lambda: self.player_button_guess(username))
        self.player_guess_button.place(relx=0.4, rely=0.5, anchor="center")
        self.player_tries_label = ctk.CTkLabel(self.rest_big_frame, text="Tries: 6", font=("Times New Roman", 20))
        self.player_tries_label.place(relx=0.4,rely=0.57,anchor="center")
        self.guesses_history_label = ctk.CTkLabel(self.rest_big_frame, text="", font=("Times New Roman", 20))
        self.guesses_history_label.place(relx=0.4, rely=0.7, anchor="center")

    def computer_vs_player_game_logic(self, username):

        connect = sqlite3.connect("game.db")
        cursor = connect.cursor()

        # get the numbered entered by the player
        player_guess = self.player_guess_entry.get().strip()
        if player_guess.isdigit():
            player_guess = int(player_guess)
            if player_guess > 0 and player_guess <= 100:
                if self.player_tries > 0:
                    self.player_tries_label.configure(text=f"Tries: {self.player_tries-1}")
                    if player_guess == self.computer_guess:
                        cursor.execute("UPDATE game SET points = points + ?, g_t_n = g_t_n + ? WHERE username = ?", (self.computer_vs_player_win_points,1,username))
                        connect.commit()
                        total_user_points = self.find_user_points(username)
                        connect.close()
                        self.master.winfo_toplevel().grab_release()
                        self.msg = CTkMessagebox(title="Congratulations!", message=f"Congratulations! You won {self.computer_vs_player_win_points}!\nYou are the best!\nTotal Points: {total_user_points}", icon="check", option_1="Exit Game", option_2="Play Again")
                        if self.msg.get() == "Exit Game":
                            self.update_callback(self.username)
                            self.master.destroy()
                        else:
                            self.master.after(1000, self.reset_game)    
                    elif player_guess > self.computer_guess:
                        self.computer_hint_label.configure(text="Your number is HIGHER")
                        self.hint = "HIGH"
                        self.guesses.append([player_guess, self.hint])
                        self.player_tries -= 1
                        history_text = "\n".join([f"Player Guessed: {guess}, Computer said: {hint}" for guess, hint in self.guesses])
                        self.guesses_history_label.configure(text=history_text)
                        if self.player_tries == 0:
                            cursor.execute("UPDATE game SET points = points - ? WHERE username = ?", (self.computer_vs_player_loss_points, username))
                            connect.commit()
                            total_user_points = self.find_user_points(username)
                            connect.close()
                            self.master.winfo_toplevel().grab_release()
                            self.msg = CTkMessagebox(title="Unlucky", message=f"Too bad you lost {self.computer_vs_player_loss_points} points.\nBetter luck next time.\nTotal Points: {total_user_points}", icon="warning", option_1="Exit Game", option_2="Play Again")
                            if self.msg.get() == "Exit Game":
                                self.update_callback(self.username)
                                self.master.destroy()
                            else:
                                self.master.after(1000, self.reset_game)
                    else:
                        self.computer_hint_label.configure(text="Your number is LOWER")
                        self.hint = "LOW"
                        self.guesses.append([player_guess, self.hint])
                        self.player_tries -= 1
                        history_text = "\n".join([f"Player Guessed: {guess}, Computer said: {hint}" for guess, hint in self.guesses])
                        self.guesses_history_label.configure(text=history_text)
                        if self.player_tries == 0:
                            cursor.execute("UPDATE game SET points = points - ? WHERE username = ?", (self.computer_vs_player_loss_points, username))
                            connect.commit()
                            total_user_points = self.find_user_points(username)
                            connect.close()
                            self.master.winfo_toplevel().grab_release()
                            self.msg = CTkMessagebox(title="Unlucky", message=f"Too bad you lost {self.computer_vs_player_loss_points} points.\nBetter luck next time.\nTotal Points: {total_user_points}", icon="warning", option_1="Exit Game", option_2="Play Again")
                            if self.msg.get() == "Exit Game":
                                self.update_callback(self.username)
                                self.master.destroy()
                            else:
                                self.master.after(1000, self.reset_game)
            else:
                self.master.winfo_toplevel().grab_release()
                CTkMessagebox(title="Warning Message!", message="Please enter a number\nbetween [1 and 100]", icon="warning")
        else:
            self.master.winfo_toplevel().grab_release()
            CTkMessagebox(title="Warning Message!", message="Please enter a number.\nDo not use letter or special characters.", icon="warning")

    def button_callback(self,button, username):
        self.button_pressed = button
        self.process_game(button, username)

    def process_game(self,button, username):
        connect = sqlite3.connect("game.db")
        cursor = connect.cursor()

        self.computer_guess = random.randint(1, 100)
        self.computer_guesses_array.append(self.computer_guess)

        # Convert user input to integer safely
        try:
            self.user_number = int(self.rest_big_frame_player_entry.get())
        except ValueError:
            self.master.winfo_toplevel().grab_release()
            msg = CTkMessagebox(title="Error", message="Invalid input. Please give a number between [1 - 100]", icon="warning", option_1="Exit Game", option_2="Ok") 
            if msg.get() == "Exit Game":
                self.update_callback(self.username)
                self.master.destroy()
            else:
                self.master.after(1000, self.reset_game())

        if button == "left":
            self.player_vs_computer_win_points = 40
            self.player_vs_computer_loss_points = 20
            self.computer_tries = 4

            while self.computer_tries > 0:
                # Update the label to show the current guesses
                self.rest_big_frame_computer_guess_label.configure(text=f"Computer guesses: {self.computer_guesses_array}")
                self.rest_big_frame_computer_guess_label.update_idletasks()  # Force GUI update

                if self.computer_guess == self.user_number:
                    cursor.execute("UPDATE game SET points = points + ?, g_t_n_ = g_t_n + ? WHERE username = ?", (self.player_vs_computer_win_points, 1, username))
                    connect.commit()
                    total_user_points = self.find_user_points(username)
                    connect.close()
                    self.master.winfo_toplevel().grab_release()
                    msg = CTkMessagebox("You Won", message=f"Congratulations. You won {self.player_vs_computer_win_points} points.\nTotal Points: {total_user_points}", icon="check", option_1="Exit Game", option_2="Play Again")
                    if msg.get() == "Exit Game":
                        self.update_callback(self.username)
                        self.master.destroy()
                    else:
                        self.master.after(1000, self.reset_game)
                else:
                    self.computer_tries -= 1
                    print(f"Computer guessed: {self.computer_guess} (Tries left: {self.computer_tries})")

                    if self.computer_tries > 0:  # Only generate a new guess if there are tries left
                        self.computer_guess = random.randint(1, 100)
                        self.computer_guesses_array.append(self.computer_guess)
                        time.sleep(1)
            
            cursor.execute("UPDATE game SET points = points - ? WHERE username = ?", (self.player_vs_computer_loss_points, username))
            connect.commit()
            total_user_points = self.find_user_points(username)
            connect.close()
            self.master.winfo_toplevel().grab_release()
            msg = CTkMessagebox(title="Game Over", message=f"Game Over. You lost {self.player_vs_computer_loss_points} points. Better luck next time.\nTotal Points: {total_user_points}", icon="cancel", option_1="Exit Game", option_2="Play Again")
            if msg.get() == "Exit Game":
                self.update_callback(self.username)
                self.master.destroy()
            else:
                self.master.after(1000, self.reset_game)
            
        elif button == "middle":
            self.player_vs_computer_win_points = 30
            self.player_vs_computer_loss_points = 15
            self.computer_tries = 6

            while self.computer_tries > 0:
                # Update the label to show the current guesses
                self.rest_big_frame_computer_guess_label.configure(text=f"Computer guesses: {self.computer_guesses_array}")
                self.rest_big_frame_computer_guess_label.update_idletasks()  # Force GUI update

                if self.computer_guess == self.user_number:
                    cursor.execute("UPDATE game SET points = points + ?, g_t_n_ = g_t_n + ? WHERE username = ?", (self.player_vs_computer_win_points, 1, username))
                    connect.commit()
                    total_user_points = self.find_user_points(username)
                    connect.close()
                    self.master.winfo_toplevel().grab_release()
                    msg = CTkMessagebox("You Won", message=f"Congratulations. You won {self.player_vs_computer_win_points} points.\nTotal Points: {total_user_points}", icon="check", option_1="Exit Game", option_2="Play Again")
                    if msg.get() == "Exit Game":
                        self.update_callback(self.username)
                        self.master.destroy()
                    else:
                        self.master.after(1000, self.reset_game)
                else:
                    self.computer_tries -= 1
                    print(f"Computer guessed: {self.computer_guess} (Tries left: {self.computer_tries})")

                    if self.computer_tries > 0:  # Only generate a new guess if there are tries left
                        self.computer_guess = random.randint(1, 100)
                        self.computer_guesses_array.append(self.computer_guess)
                        time.sleep(1)
            
            cursor.execute("UPDATE game SET points = points - ? WHERE username = ?", (self.player_vs_computer_loss_points, username))
            connect.commit()
            total_user_points = self.find_user_points(username)
            connect.close()
            self.master.winfo_toplevel().grab_release()
            msg = CTkMessagebox(title="Game Over", message=f"Game Over. You lost {self.player_vs_computer_loss_points} points. Better luck next time.\nTotal Points: {total_user_points}", icon="cancel", option_1="Exit Game", option_2="Play Again")
            if msg.get() == "Exit Game":
                self.update_callback(self.username)
                self.master.destroy()
            else:
                self.master.after(1000, self.reset_game)
        elif button == "right":
            self.computer_tries = 10

            while self.computer_tries > 0:
                # Update the label to show the current guesses
                self.rest_big_frame_computer_guess_label.configure(text=f"Computer guesses: {self.computer_guesses_array}")
                self.rest_big_frame_computer_guess_label.update_idletasks()  # Force GUI update

                if self.computer_guess == self.user_number:
                    cursor.execute("UPDATE game SET points = points + ?, g_t_n_ = g_t_n + ? WHERE username = ?", (self.player_vs_computer_win_points, 1, username))
                    connect.commit()
                    total_user_points = self.find_user_points(username)
                    connect.close()
                    self.master.winfo_toplevel().grab_release()
                    msg = CTkMessagebox("You Won", message=f"Congratulations. You won {self.player_vs_computer_win_points} points.\nTotal Points: {total_user_points}", icon="check", option_1="Exit Game", option_2="Play Again")
                    if msg.get() == "Exit Game":
                        self.update_callback(self.username)
                        self.master.destroy()
                    else:
                        self.master.after(1000, self.reset_game)
                else:
                    self.computer_tries -= 1
                    print(f"Computer guessed: {self.computer_guess} (Tries left: {self.computer_tries})")

                    if self.computer_tries > 0:  # Only generate a new guess if there are tries left
                        self.computer_guess = random.randint(1, 100)
                        self.computer_guesses_array.append(self.computer_guess)
                        time.sleep(1)
            
            cursor.execute("UPDATE game SET points = points - ? WHERE username = ?", (self.player_vs_computer_loss_points, username))
            connect.commit()
            total_user_points = self.find_user_points(username)
            connect.close()
            self.master.winfo_toplevel().grab_release()
            msg = CTkMessagebox(title="Game Over", message=f"Game Over. You lost {self.player_vs_computer_loss_points} points. Better luck next time.\nTotal Points: {total_user_points}", icon="cancel", option_1="Exit Game", option_2="Play Again")
            if msg.get() == "Exit Game":
                self.update_callback(self.username)
                self.master.destroy()
            else:
                self.master.after(1000, self.reset_game)
        else:
            print("Entry must have a number from [1 - 100]. Please try again.")
            
    def find_user_points(self, username):
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





if __name__ == "__main__":
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    app = GuessTheNumber(root)
    root.mainloop()
