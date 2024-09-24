# main.py

from tkinter import Tk
from flashcard_app import FlashCardApp

def main():
    """
    Initializes and runs the FlashCardApp.
    """
    window = Tk()
    app = FlashCardApp(window)
    window.mainloop()

if __name__ == "__main__":
    main()
