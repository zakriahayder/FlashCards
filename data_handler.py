# data_handler.py

import pandas as pd

class DataHandler:
    def __init__(self, data_file='data/french_words.csv', to_learn_file='data/words_to_learn.csv'):
        """
        Initializes the DataHandler with file paths.
        
        :param data_file: Path to the original French words CSV.
        :param to_learn_file: Path to the CSV storing words to learn.
        """
        self.data_file = data_file
        self.to_learn_file = to_learn_file
        self.words_dict = self.load_words()

    def load_words(self):
        """
        Loads words from 'words_to_learn.csv' if it exists; otherwise, from 'french_words.csv'.
        
        :return: List of word dictionaries.
        """
        try:
            data = pd.read_csv(self.to_learn_file)
            print(f"Loaded {len(data)} words from {self.to_learn_file}.")
        except FileNotFoundError:
            data = pd.read_csv(self.data_file)
            print(f"Loaded {len(data)} words from {self.data_file}.")
        return data.to_dict(orient='records')

    def save_words(self, words_dict):
        """
        Saves the current list of words to 'words_to_learn.csv'.
        
        :param words_dict: List of word dictionaries to save.
        """
        data = pd.DataFrame(words_dict)
        data.to_csv(self.to_learn_file, index=False)
        print(f"Saved {len(words_dict)} words to {self.to_learn_file}.")
