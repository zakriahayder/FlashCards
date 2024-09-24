# flashcard_app.py

from tkinter import *
from data_handler import DataHandler
import random

BACKGROUND_COLOR = "#B1DDC6"

class FlashCardApp:
    def __init__(self, master):
        """
        Initializes the FlashCardApp with the main window and sets up the GUI.
        
        :param master: The root Tkinter window.
        """
        self.master = master
        self.master.title("Flashy")
        self.master.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

        # Initialize data handler
        self.data_handler = DataHandler()
        self.words_dict = self.data_handler.words_dict.copy()

        # Initialize score and unknown words list
        self.score = 0
        self.unknown_words = []
        self.current_word = {}
        self.flip_timer = None

        # Load images
        self.card_front_img = PhotoImage(file="images/card_front.png")
        self.card_back_img = PhotoImage(file="images/card_back.png")
        self.right_img = PhotoImage(file="images/right.png")
        self.wrong_img = PhotoImage(file="images/wrong.png")

        # Setup canvas
        self.canvas = Canvas(height=526, width=800, highlightthickness=0, bg=BACKGROUND_COLOR)
        self.card_background = self.canvas.create_image(400, 263, image=self.card_front_img)
        self.canvas.grid(row=0, column=0, columnspan=2)

        self.language_label = self.canvas.create_text(400, 150, text="French", font=("Arial", 40, "italic"))
        self.word_text = self.canvas.create_text(400, 263, text="", font=("Arial", 60, "bold"))
        
        # Score label
        self.score_label = Label(self.master, text=f"Score: {self.score}", bg=BACKGROUND_COLOR, font=("Arial", 24))
        self.score_label.grid(row=2, column=0, columnspan=2)

        # Buttons
        self.wrong_button = Button(image=self.wrong_img, highlightthickness=0, command=self.is_unknown)
        self.wrong_button.grid(row=1, column=0)

        self.right_button = Button(image=self.right_img, highlightthickness=0, command=self.is_known)
        self.right_button.grid(row=1, column=1)

        self.next_card()

    def next_card(self):
        """
        Selects the next card to display. If no words are left, ends the game.
        """
        if self.flip_timer:
            self.master.after_cancel(self.flip_timer)

        if self.words_dict:
            self.current_word = random.choice(self.words_dict)
            self.canvas.itemconfig(self.card_background, image=self.card_front_img)
            self.canvas.itemconfig(self.language_label, text="French", fill="black")
            self.canvas.itemconfig(self.word_text, text=self.current_word['French'], fill="black")
            self.flip_timer = self.master.after(3000, self.flip_card)
            print(f"Next card: {self.current_word['French']} - {self.current_word['English']}")
        else:
            self.end_game()

    def flip_card(self):
        """
        Flips the card to show the English translation.
        """
        self.canvas.itemconfig(self.card_background, image=self.card_back_img)
        self.canvas.itemconfig(self.language_label, text="English", fill="white")
        self.canvas.itemconfig(self.word_text, text=self.current_word['English'], fill="white")
        print(f"Flipped card to show English: {self.current_word['English']}")

    def is_known(self):
        """
        Marks the current word as known, updates the score, and proceeds to the next card.
        """
        self.words_dict.remove(self.current_word)
        self.score += 1
        self.update_score_label()
        self.data_handler.save_words(self.words_dict)
        print(f"Known word: {self.current_word['French']} | Score: {self.score}")
        self.next_card()

    def is_unknown(self):
        """
        Marks the current word as unknown and proceeds to the next card.
        """
        self.unknown_words.append(self.current_word)
        print(f"Unknown word: {self.current_word['French']}")
        self.next_card()

    def update_score_label(self):
        """
        Updates the score display.
        """
        self.score_label.config(text=f"Score: {self.score}")

    def end_game(self):
        """
        Displays the game over screen with the final score.
        """
        self.canvas.itemconfig(self.card_background, image=self.card_front_img)
        self.canvas.itemconfig(self.language_label, text="Game Over!", fill="red")
        self.canvas.itemconfig(self.word_text, text=f"Final Score: {self.score}", fill="red")
        self.wrong_button.config(state='disabled')
        self.right_button.config(state='disabled')
        print(f"Game Over! Final Score: {self.score}")
