import customtkinter as ctk
import sqlite3
from CTkMessagebox import *
import random
from r_p_s_game import *
from mastermind_game import *
from g_t_n_game import *
from hangman_game import *

# connect database
connect = sqlite3.connect("game.db")
cursor = connect.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS game (
        id INTEGER PRIMARY KEY AUTOINCREMENT,              
        username TEXT UNIQUE NOT NULL,
        mastermind INTEGER DEFAULT 0,
        g_t_n INTEGER DEFAULT 0,
        hangman INTEGER DEFAULT 0,
        r_p_s INTEGER DEFAULT 0,
        points INTEGER DEFAULT 100,
        FOREIGN KEY(username) REFERENCES users(username) ON DELETE CASCADE ON UPDATE CASCADE
    )
""")

connect.commit()

# print successful connection upon with database.
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='game';")
if cursor.fetchone():
    print("Database connection successful and 'game' table created.")
else:
    print("Failed to create 'game' table.")


def print_game_database():
    # Connect to the database
    connect = sqlite3.connect("game.db")
    cursor = connect.cursor()

    # Fetch all users, specifically selecting the columns you need
    cursor.execute("SELECT * FROM game")
    rows = cursor.fetchall()

    # Print results
    for row in rows:
        # Ensure the row has the correct number of columns (7 in this case)
        if len(row) == 7:
            user_id, username, mastermind, g_t_n, hangman, r_p_s, points = row
            print(f"ID: {user_id}, Username: {username}, Mastermind: {mastermind}, G_T_N: {g_t_n}, Hangman: {hangman}, R_P_S: {r_p_s}, Points: {points}")
        else:
            print(f"Skipping incomplete row: {row}")

    # Close connection
    connect.close()

class GameMenu(ctk.CTk):  

    def __init__(self, master,username, points):
        self.master = master
        self.username = username
        self.master.title("Game Menu")
        self.master.minsize(1600,800)     
        self.master.maxsize(1800,850)

        # instances 
        self.user_points = self.get_user_points_from_database(username)
        self.display_user_rank = self.find_user_rank(username)   

        # CREATING FRAMES 
        # frames left - middle - right 
        self.left_main_frame = ctk.CTkFrame(master)
        self.left_main_frame.place(relx=0.1, relwidth=0.25, rely=0.5, relheight=1, anchor="center")
        self.middle_main_frame = ctk.CTkFrame(master)
        self.middle_main_frame.place(relx=0.5, relwidth=0.55, rely=0.5, relheight=1, anchor="center")
        self.right_main_frame = ctk.CTkFrame(master)
        self.right_main_frame.place(relx=0.9, relwidth=0.25, rely=0.5, relheight=1, anchor="center")

        # left frame profile top section
        self.left_frame_profile_label = ctk.CTkLabel(self.left_main_frame, text=f"  Profile:\n {username}", font=("Times New Roman", 40))
        self.left_frame_profile_label.place(relx=0.4, rely=0.1, anchor="center")
        self.left_frame_profile_points_label = ctk.CTkLabel(self.left_main_frame, text=f"Points: {self.user_points[0]}", font=("Times New Roman", 20))
        self.left_frame_profile_points_label.place(relx=0.4, rely=0.18, anchor="center")
        self.left_frame_profile_ranking_label = ctk.CTkLabel(self.left_main_frame, text=f"Ranking: {self.display_user_rank}", font=("Times New Roman", 20))
        self.left_frame_profile_ranking_label.place(relx=0.4, rely=0.22, anchor="center")

        # left frame lucky roulette
        self.left_frame_lucky_roulette_head_label = ctk.CTkLabel(self.left_main_frame, text="LUCKY ROULETTE", font=("Times New Roman", 22))
        self.left_frame_lucky_roulette_head_label.place(relx=0.4, rely = 0.38, anchor="center")
        self.left_frame_lucky_roulette_chances_label = ctk.CTkLabel(self.left_main_frame, text="0 - 50pts = 70%\n50 - 70 pts = 50%\n70 - 100 pts = 35%\n100+ pts = 20%", font=("Times New Roman", 18))
        self.left_frame_lucky_roulette_chances_label.place(relx=0.4, rely=0.45, anchor="center")
        self.left_frame_lucky_roulette_points_entry = ctk.CTkEntry(self.left_main_frame, width=150, font=("Times New Roman", 18), placeholder_text="Points Bet...")
        self.left_frame_lucky_roulette_points_entry.place(relx=0.4, rely=0.53, anchor="center")
        self.left_frame_lucky_roulette_bet_button = ctk.CTkButton(self.left_main_frame, width=150, height=70, text="Play bet...", font=("Times New Roman", 18), corner_radius=50, command=lambda: self.roulette_play(username,self.user_points))
        self.left_frame_lucky_roulette_bet_button.place(relx=0.4, rely=0.62, anchor="center")

        # left frame buttons 
        self.left_frame_reset_challenges_button = ctk.CTkButton(self.left_main_frame, width=150, height=60, text="Pay 60 points.\nReset Games Challenges.", font=("Times New Roman", 16), cursor="hand2", corner_radius=50, command=lambda: self.reset_game_challenges(username))
        self.left_frame_reset_challenges_button.place(relx=0.4, rely=0.8, anchor="center")
        self.left_frame_exit_game_button = ctk.CTkButton(self.left_main_frame, width=150, height=60, text="Exit Game", font=("Times New Roman", 20), command=self.exit_game_button, corner_radius=50, cursor="hand2")
        self.left_frame_exit_game_button.place(relx=0.4, rely=0.9, anchor="center")

        # CREATING MIDDLE FRAME 
        # middle frame header
        self.middle_frame_head_label = ctk.CTkLabel(self.middle_main_frame, text="MINI GAMES TO PLAY", font=("Times New Roman", 55))
        self.middle_frame_head_label.place(relx = 0.47, rely=0.2, anchor="center")

        # 4 button for the actual games
        self.middle_main_frame_mastermind_button = ctk.CTkButton(self.middle_main_frame, width=180, height=130, text="MasterMind\n+50 , -25", font=("Times New Roman", 25), cursor="hand2", corner_radius=50, command=lambda: self.open_mastermind_window(username))
        self.middle_main_frame_mastermind_button.place(relx=0.25, rely=0.4, anchor="center")
        self.middle_main_frame_gtn_button = ctk.CTkButton(self.middle_main_frame, width=180, height=130, text="Guess\nThe Number\n+40 , -20", font=("Times New Roman", 25), cursor="hand2", corner_radius=50, command=lambda: self.open_gtn_window(username))
        self.middle_main_frame_gtn_button.place(relx=0.7, rely=0.4, anchor="center")
        self.middle_main_frame_hangman_button = ctk.CTkButton(self.middle_main_frame, width=180, height=130, text="HangMan\n+40 , -20", font=("Times New Roman", 25), cursor="hand2", corner_radius=50, command=lambda: self.open_hangman_window(username))
        self.middle_main_frame_hangman_button.place(relx=0.25, rely=0.7, anchor="center")
        self.middle_main_frame_mastermind_button = ctk.CTkButton(self.middle_main_frame, width=180, height=130, text="Rock\nPaper\nScissors\n+30 , -15", font=("Times New Roman", 25), corner_radius=50, cursor="hand2", command=lambda: self.open_rps_window(username))
        self.middle_main_frame_mastermind_button.place(relx=0.7, rely=0.7, anchor="center")

        # CREATING RIGHT FRAME
        # right frame daily challenges labels and 
        self.right_main_frame_top_label = ctk.CTkLabel(self.right_main_frame, text="Game Challenges", font=("Times New Roman", 35))
        self.right_main_frame_top_label.place(relx=0.4, rely=0.1, anchor="center")
        # first daily challenge
        self.right_first_challenge_label = ctk.CTkLabel(self.right_main_frame, text="* 5 wins in MasterMind = 60 Points", font=("Times New Roman", 20))
        self.right_first_challenge_label.place(relx=0.4, rely=0.2, anchor="center")
        self.right_first_progress_bar = ctk.CTkSlider(self.right_main_frame, width=250,from_=0, to=5, number_of_steps=5, state="disabled")
        self.right_first_progress_bar.set(0)
        self.right_first_progress_bar.place(relx=0.4, rely=0.23, anchor="center")
        # second daily challenge
        self.right_second_challenge_label = ctk.CTkLabel(self.right_main_frame, text="* 8 wins in Guess The Number = 35 Points", font=("Times New Roman", 20))
        self.right_second_challenge_label.place(relx=0.45, rely=0.3, anchor="center")
        self.right_second_progress_bar = ctk.CTkSlider(self.right_main_frame, width=250,from_=0, to=8, number_of_steps=8, state="disabled")
        self.right_second_progress_bar.set(0)
        self.right_second_progress_bar.place(relx=0.4, rely=0.33, anchor="center")
        # third daily challenge
        self.right_third_challenge_label = ctk.CTkLabel(self.right_main_frame, text="* 6 wins in HangMan = 30 Points", font=("Times New Roman", 20))
        self.right_third_challenge_label.place(relx=0.4, rely=0.4, anchor="center")
        self.right_third_progress_bar = ctk.CTkSlider(self.right_main_frame, width=250,from_=0, to=6, number_of_steps=6, state="disabled")
        self.right_third_progress_bar.set(0)
        self.right_third_progress_bar.place(relx=0.4, rely=0.43, anchor="center")
        # fourth daily challenge
        self.right_fourth_challenge_label = ctk.CTkLabel(self.right_main_frame, text="* 12 wins in R-P-S game = 25 points", font=("Times New Roman", 20))
        self.right_fourth_challenge_label.place(relx=0.4, rely=0.5, anchor="center")
        self.right_fourth_progress_bar = ctk.CTkSlider(self.right_main_frame, width=250,from_=0, to=12, number_of_steps=12, state="disabled")
        self.right_fourth_progress_bar.set(0)
        self.right_fourth_progress_bar.place(relx=0.4, rely=0.53, anchor="center")

        # Ranking system 
        # ranking system top label
        self.right_rank_top_label = ctk.CTkLabel(self.right_main_frame, text="Ranking Board", font=("Times New Roman", 40))
        self.right_rank_top_label.place(relx=0.4, rely=0.62, anchor="center")
        self.right_rank_show_rank_label = ctk.CTkLabel(self.right_main_frame, text="", font=("Times New Roman", 20))
        self.right_rank_show_rank_label.place(relx=0.4, rely=0.77, anchor="center")
        self.rank_board_print()
        self.update_daily_challenges(username)

    def rps_window(self, master,username,update_game_menu):
        rps_game_window = ctk.CTkToplevel(master)  # Create a new top-level window
        rps_game_window.transient(master)  # Make it a child of the main window
        rps_game_window.grab_set()  # Force focus on this window
        RPSGame(rps_game_window,username,update_game_menu)  # Initialize the account creation GUI

    def open_rps_window(self,username):
        self.rps_window(self.master,username,self.update_game_menu)

    def mastermind_window(self, master,username,update_game_menu):
        mastermind_game_window = ctk.CTkToplevel(master)  # Create a new top-level window
        mastermind_game_window.transient(master)  # Make it a child of the main window
        mastermind_game_window.grab_set()  # Force focus on this window
        MasterMind(mastermind_game_window,username,update_game_menu)  # Initialize the account creation GUI

    def open_mastermind_window(self,username):
        self.mastermind_window(self.master,username,self.update_game_menu)

    def hangman_window(self, master,username,update_game_menu):
        hangman_game_window = ctk.CTkToplevel(master)  # Create a new top-level window
        hangman_game_window.transient(master)  # Make it a child of the main window
        hangman_game_window.grab_set()  # Force focus on this window
        Hangman(hangman_game_window,username,update_game_menu)  # Initialize the account creation GUI

    def open_hangman_window(self,username):
        self.hangman_window(self.master,username,self.update_game_menu)

    def gtn_window(self, master,username,update_game_menu):
        gtn_game_window = ctk.CTkToplevel(master)  # Create a new top-level window
        gtn_game_window.transient(master)  # Make it a child of the main window
        gtn_game_window.grab_set()  # Force focus on this window
        GuessTheNumber(gtn_game_window,username,update_game_menu)  # Initialize the account creation GUI

    def open_gtn_window(self,username):
        self.gtn_window(self.master,username,self.update_game_menu)

    def rank_board_print(self):
        connect = sqlite3.connect("game.db")
        cursor = connect.cursor()

        # Fetch all users sorted by points (highest first)
        cursor.execute("SELECT username, points FROM game ORDER BY points DESC")
        rows = cursor.fetchall()
        connect.close()

        rank_str = ""  # String to display top 5
        user_rank = None  # Store user ranking

        for i in range(len(rows)):
            user, points = rows[i]  # Unpack the tuple into user and points
            rank_str += f"{i + 1}. {user} = {points} points\n"  # i + 1 to start from 1 instead of 0

        self.right_rank_show_rank_label.configure(text=f"{rank_str}")
    
    def find_user_rank(self, username):
        connect = sqlite3.connect("game.db")
        cursor = connect.cursor()

        # Fetch all users sorted by points (highest first)
        cursor.execute("SELECT username, points FROM game ORDER BY points DESC")
        rows = cursor.fetchall()
        connect.close()

        user_rank = None  # Store user ranking

        for i, (user, points) in enumerate(rows, start=1):

            if user == username:
                user_rank = i  # Get rank of logged-in user

        return user_rank
    
    def roulette_play(self, username, user_points):
        connect = sqlite3.connect("game.db")
        cursor = connect.cursor()

        if user_points: # get the int value of user points 
            points = user_points[0]

        bet = self.left_frame_lucky_roulette_points_entry.get().strip()
        if bet.isdigit():
            bet = int(bet)

        if not bet:
            CTkMessagebox(title="Error", message="Bet is required to play the game", icon="warning")
            return
        
        if bet <= 0:
            CTkMessagebox(title="Error", message="Bet must be greater(>) that 0", icon="warning")
            return
        
        if bet > points:
            CTkMessagebox(title="Error", message="You don't have enough points to place this bet", icon="warning")
            return
        
        if bet <= 50:# chance are 70-100 = +30
            rng_num = random.randint(1,100)
            if rng_num >= 30:
                winnings = bet * 2
                cursor.execute("UPDATE game SET points = points + ? WHERE username = ?", (winnings, username))
                CTkMessagebox(title="Bet Wins", message=f"You drew: {rng_num}\nCongratulations you won the roulette.\nYou won {winnings} points.", icon="check")
            else:
                cursor.execute("UPDATE game SET points = points - ? WHERE username = ?", (bet, username))
                CTkMessagebox(title="Bet Lost", message=f"You draw: {rng_num}\nToo bad. You lost the roulette.\nYou lost {bet} points.\nBETTER LUCK NEXT TIME!", icon="cancel")
            connect.commit()
        elif bet <= 70 and bet > 50: # chances are 50-100 = +50
            rng_num = random.randint(1,100)
            if rng_num >= 50:
                winnings = bet * 2
                cursor.execute("UPDATE game SET points = points + >? WHERE username = ?", (winnings, username))
                CTkMessagebox(title="Bet Wins", message=f"You drew: {rng_num}\nCongratulations you won the roulette.\nYou won {winnings} points.", icon="check")
            else:
                cursor.execute("UPDATE game SET points = points - ? WHERE username = ?", (bet, username))
                CTkMessagebox(title="Bet Lost", message=f"You drew: {rng_num}\nToo bad. You lost the roulette.\nYou lost {bet} points.\nBETTER LUCK NEXT TIME!", icon="cancel")
            connect.commit()
        elif bet <= 100 and bet > 70: # chances are 35-100 = +65
            rng_num = random.randint(1,100)
            if rng_num >= 65:
                winnings = bet * 2
                cursor.execute("UPDATE game SET points = points + ? WHERE username = ?", (winnings, username))
                CTkMessagebox(title="Bet Wins", message=f"You drew: {rng_num}\nCongratulations you won the roulette.\nYou won {winnings} points.", icon="check")
            else:
                cursor.execute("UPDATE game SET points = points - ? WHERE username = ?", (bet, username))
                CTkMessagebox(title="Bet Lost", message=f"You drew: {rng_num}\nToo bad. You lost the roulette.\nYou lost {bet} points.\nBETTER LUCK NEXT TIME!", icon="cancel")
            connect.commit()
        else: #chances are 25-100 = +75
            rng_num = random.randint(1,100)
            if rng_num >= 75:
                winnings = bet * 2
                cursor.execute("UPDATE game SET points = points + ? WHERE username = ?", (winnings, username))
                CTkMessagebox(title="Bet Wins", message=f"You drew: {rng_num}\nCongratulations you won the roulette.\nYou won {winnings} points.", icon="check")
            else:
                cursor.execute("UPDATE game SET points = points - ? WHERE username = ?", (bet, username))
                CTkMessagebox(title="Bet Lost", message=f"You drew: {rng_num}\nToo bad. You lost the roulette.\nYou lost {bet} points.\nBETTER LUCK NEXT TIME!", icon="cancel")
        connect.close()
        self.update_game_menu(username)
        
    def exit_game_button(self):
        self.msg = CTkMessagebox(title="Exit", message="Do you want to close the program?", icon="question", option_1="No", option_2="Yes")
        
        if self.msg.get() == "Yes":
            self.master.destroy()
        else:
            return
        
    def update_game_menu(self, username):
        # Update user points and rank from the database or wherever they are stored
        self.user_points = self.get_user_points_from_database(username)  
        self.display_user_rank = self.find_user_rank(username)

        self.left_frame_profile_points_label.configure(text=f"Points: {self.user_points[0]}")

        self.left_frame_profile_ranking_label.configure(text=f"Ranking: {self.display_user_rank}")

        self.left_frame_lucky_roulette_points_entry.delete(0, 'end')
        self.left_frame_lucky_roulette_points_entry.insert(0, "")

        self.rank_board_print()
        self.update_daily_challenges(username)

    def get_user_points_from_database(self, username):
        connect = sqlite3.connect("game.db")
        cursor = connect.cursor()
        cursor.execute("SELECT points FROM game WHERE username = ?", (username,))
        user_points = cursor.fetchone()
        connect.commit()
        connect.close()

        return user_points

    def update_daily_challenges(self, username):
        connect = sqlite3.connect("game.db")
        cursor = connect.cursor()

        cursor.execute("SELECT mastermind, g_t_n, hangman, r_p_s FROM game where username = ?", (username,))
        items = cursor.fetchone()

        if items:
            mastermind, g_t_n, hangman, rps = items
        
        max_mastermind = 5
        max_gtn = 8
        max_hangman = 6
        max_rps = 12


        self.right_first_progress_bar.set(min(mastermind,  max_mastermind))
        self.right_second_progress_bar.set(min(g_t_n, max_gtn))
        self.right_third_progress_bar.set(min(hangman, max_hangman))
        self.right_fourth_progress_bar.set(min(rps, max_rps))

    def reset_game_challenges(self,username):
        connect = sqlite3.connect("game.db")
        cursor = connect.cursor()
        cursor.execute("SELECT mastermind,g_t_n,hangman,r_p_s FROM game WHERE username = ?", (username,))
        rows = cursor.fetchone()
        connect.commit()
        mastermind_wins, gtn_wins, hangman_wins, rps_wins = rows

        if mastermind_wins >= 5 and gtn_wins >= 8 and hangman_wins >= 6 and rps_wins >= 12:
            cursor.execute("UPDATE game SET mastermind = ?, g_t_n = ?, hangman = ?, r_p_s = ?, points = points - ? WHERE username = ?", (0,0,0,0,60,username))
            connect.commit()
            connect.close()
            self.update_game_menu(username)
            CTkMessagebox(title="Reset Complete", message="Game challenges have been reset successfully!", icon="check")
        else:
            connect.close()
            CTkMessagebox(title="Error", message="You need to complete all game challenges first\nin order to reset them.", icon="warning")




        




if __name__ == "__main__":
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")

    print_game_database()
    root = ctk.CTk()
    app = GameMenu(root)
    root.mainloop()