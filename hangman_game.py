import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
import sqlite3
import random

class Hangman():
    def __init__(self, master,username,update_callback):
        self.master = master
        self.username = username
        self.update_callback = update_callback
        self.master.title("HangMan Game")
        self.master.minsize(1300,750)

        # array with words to play
        self.words_to_pick = ["ghost", "snake", "socks", "person", "skateboard", "cowboy", "outside", "mountain", "snowflake", "flower", "chocolate", "espresso", "jacket", "swimsuit", "beach", "summary", "portal", "treasure", "whistle"]
        self.used_letters = []
        self.hangman_stages = [
            "  +---+\n  |   |\n      |\n      |\n      |\n      |\n=========",
            "  +---+\n  |   |\n  O   |\n      |\n      |\n      |\n=========",
            "  +---+\n  |   |\n  O   |\n  |   |\n      |\n      |\n=========",
            "  +---+\n  |   |\n  O   |\n /|   |\n      |\n      |\n=========",
            "  +---+\n  |   |\n  O   |\n /|\  |\n      |\n      |\n=========",
            "  +---+\n  |   |\n  O   |\n /|\  |\n /    |\n      |\n=========",
            "  +---+\n  |   |\n  O   |\n /|\  |\n / \  |\n      |\n=========",
            "  +---+\n  |   |\n  O   |\n /|\  |\n / \  |\n RIP  |\n========="
                            ]
        self.tries_left = 0
        self.win_points = 40
        self.loss_points = 20


        # CREATING TWO FRAMES
        # creating left frame
        self.left_frame = ctk.CTkFrame(master)
        self.left_frame.place(relx=0, rely=0, relwidth=0.5, relheight=1)

        # creating right frame
        self.right_frame = ctk.CTkFrame(master)
        self.right_frame.place(relx=0.5, rely=0, relwidth=0.5, relheight=1)

        # creating the left frame widgets
        self.left_frame_top_header = ctk.CTkLabel(self.left_frame, text="Welcome to the HangMan Game.", font=("Times New Roman", 35))
        self.left_frame_top_header.place(relx=0.5,rely=0.15,anchor="center")
        self.left_frame_start_game_button = ctk.CTkButton(self.left_frame, corner_radius=50, width=200, height=100, text="Start Game!!!", font=("Times New Roman", 20), command=self.create_left_game_frame)
        self.left_frame_start_game_button.place(relx=0.5,rely=0.3,anchor="center")

        # creating right hangman label
        self.tries_left_label_show = ctk.CTkLabel(self.right_frame, text=f"You have {8 - self.tries_left} tries left.", font=("Times New Roman", 20))
        self.tries_left_label_show.place(relx=0.3,rely=0.3,anchor="center")
        self.right_frame_hangman_label = ctk.CTkLabel(self.right_frame, text=self.hangman_stages[self.tries_left], font=("Times New Roman", 30))
        self.right_frame_hangman_label.place(relx=0.3, rely=0.5, anchor="center")

    def create_left_game_frame(self):
        self.left_frame_start_game_button.destroy()
        self.random_word = random.choice(self.words_to_pick)
        self.word_in_letters = list(self.random_word)
        self.correct_word = [" X "] * len(self.word_in_letters)
        self.word_to_print = "".join(self.correct_word)

        self.left_frame_len_word_label = ctk.CTkLabel(self.left_frame, text=f"The word has {len(self.word_in_letters)} letters.", font=("Times New Roman", 20))
        self.left_frame_len_word_label.place(relx=0.5,rely=0.25,anchor="center")
        print(self.word_in_letters)
        self.left_frame_hidden_word_label = ctk.CTkLabel(self.left_frame, text=f"{self.word_to_print}", font=("Times New Roman", 20))
        self.left_frame_hidden_word_label.place(relx=0.5, rely=0.32,anchor="center")
        self.left_frame_used_letter_label = ctk.CTkLabel(self.left_frame, text="Used letter: ", font=("Times New Roman", 20))
        self.left_frame_used_letter_label.place(relx=0.5,rely=0.4,anchor="center")

        # creating the keyboard to make letter choices 
        self.keyboard_frame = ctk.CTkFrame(self.left_frame)
        self.keyboard_frame.place(relx=0.5,rely=0.7,anchor="center")

        self.create_keyboard(self.username)

    def reset_game(self):
        # Destroy all existing game widgets
        for widget in self.master.winfo_children():
            widget.destroy()

        # Reset game variables
        self.tries_left = 0
        self.used_letters = []

        # Recreate the game UI
        self.__init__(self.master,self.username,self.update_callback)

    def create_keyboard(self, username):
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

        for i, letter in enumerate(alphabet):
            button = ctk.CTkButton(self.keyboard_frame, corner_radius=50, text=letter, width=40, height=40, command=lambda l=letter: self.handle_letter_press(l, username))
            button.grid(row=i // 9, column = i % 9, padx=5, pady=5)

    def handle_letter_press(self,letter,username):
        if letter.lower() in self.used_letters:
            return
        
        self.used_letters.append(letter.lower())

        self.left_frame_used_letter_label.configure(text=f"Used Letters: {', '.join(self.used_letters)}")

        if letter.lower() in self.word_in_letters:
            for idx, char in enumerate(self.word_in_letters):
                if char == letter.lower():
                    self.correct_word[idx] = char.upper()

            self.left_frame_hidden_word_label.configure(text=" ".join(self.correct_word))
        else:
            self.tries_left += 1

            # disable button after click
        for widget in self.keyboard_frame.winfo_children():
            if widget.cget("text") == letter:
                widget.configure("disabled")
                widget.configure(fg_color="gray")

        self.check_win_condition(username)

    def check_win_condition(self, username):
        connect = sqlite3.connect("game.db")
        cursor = connect.cursor()
        if "".join(self.correct_word).replace(" ", "") == self.random_word.upper():
            cursor.execute("UPDATE game SET points = points + ?, hangman = hangman + ? WHERE username = ?", (self.win_points,1,username))
            connect.commit()
            total_user_points = self.find_user_points(username)
            connect.close()
            self.master.winfo_toplevel().grab_release()
            self.msg = CTkMessagebox(title="You Win", message=f"Congratulations! You guessed the correct word correctly!\nYou win {self.win_points} points.\nTotal Points: {total_user_points} points.", icon="check", option_1="Exit Game", option_2="Play Again")
            if self.msg.get() == "Exit Game":
                self.update_callback(self.username)
                self.master.destroy()
            else:
                self.master.after(1000, self.reset_game)
        elif self.tries_left == 8:
            cursor.execute("UPDATE game SET points = points - ? WHERE username = ?", (self.loss_points, username))
            connect.commit()
            total_user_points = self.find_user_points(username)
            connect.close()
            self.master.winfo_toplevel().grab_release()
            self.msg = CTkMessagebox(title="Game Over", message=f"Game Over! The word was {self.random_word.upper()}.\nYou lost {self.loss_points} points.\nTotal Points: {total_user_points}", icon="cancel", option_1="Exit Game", option_2="Play Again")
            if self.msg.get() == "Exit Game":
                self.update_callback(self.username)
                self.master.destroy()
            else:
                self.master.after(1000, self.reset_game)
        else:
            self.tries_left_label_show.configure(text=f"You have {8 - self.tries_left} tries left.")
            self.right_frame_hangman_label.configure(text=self.hangman_stages[self.tries_left])

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
    app = Hangman(root)
    root.mainloop()
