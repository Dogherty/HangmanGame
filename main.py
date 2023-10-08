import tkinter as tk
from tkinter import ttk
from tkinter import *
from PIL import Image, ImageTk
import random

# Створення класу гри Шибениця
class HangmanGame:
    def __init__(self, root):
        # Ініціалізація основного вікна
        self.root = root
        self.root.title('Шибениця')
        self.root.geometry('400x600')
        self.main_font = ('Helvetica', 12)
        self.attempts_left = 0
        self.history = []

        # Ініціалізація інтерфейсу гри
        self.init_interface()

    def init_interface(self):
        # Відображення зображення шибениці
        self.image_label = ttk.Label(self.root)
        self.image_label.grid(row=1, columnspan=3)
        self.update_image("main")

        # Створення кнопки "Старт"
        self.start_button = ttk.Button(text='Старт', command=self.start_game)
        self.start_button.grid(row=5, columnspan=3)

    def update_image(self, image_name):
        # Оновлення зображення шибениці
        image = Image.open(f"images/{image_name}.png")
        image_tk = ImageTk.PhotoImage(image)

        self.image_label.configure(image=image_tk)
        self.image_label.image = image_tk

    def update_word_label(self):
        # Оновлення відображення загаданого слова
        self.word_label.config(text=" ".join(self.word_silent_list))

    def check_letter(self):
        # Перевірка літери гравця і видалення її з поля для вводу
        letter = self.letter_entry.get().lower()
        self.letter_entry.delete(0, tk.END)

        if len(letter) != 1 or not letter.isalpha():
            # Перевірка на коректність літери
            self.system_text.config(text='Будь-ласка, вкажіть лише 1 літеру')
            return

        if letter in self.target_word and letter not in self.word_silent_list and letter not in self.history:
            # Перевірка, чи є літера в загаданому слові
            self.history.append(letter)
            self.letter_history.insert(tk.END, letter + ", ")
            indexes = [i for i, c in enumerate(self.target_word) if c == letter]
            self.system_text.config(text=f'Літера {letter} є в слові!')
            for n in indexes:
                self.word_silent_list[n] = letter
            self.update_word_label()
            if "*" not in self.word_silent_list:
                self.system_text.config(text='Ура! Перемога!')
                self.letter_entry.config(state="disabled")
                self.button_letter.config(state="disabled")
                ttk.Button(text='Почати спочатку', command=self.restart_game).grid(row=7, column=1, pady=10)
                return
        elif letter in self.word_silent_list or letter in self.history:
            # Перевірка, чи вказував гравець цю літеру
            self.system_text.config(text='Ви вже вказували цю літеру!')
        else:
            # Зменшення кількості спроб
            self.attempts_left += 1
            self.update_image(str(self.attempts_left))
            if self.attempts_left >= 7:
                # Якщо спробі закінчились - завершуємо гру
                self.system_text.config(text=f'Гра закінчена.\nЗагадане слово було: {self.target_word}',
                                        anchor='center', justify='center')
                self.letter_entry.config(state="disabled")
                self.button_letter.config(state="disabled")
                ttk.Button(text='Почати спочатку', command=self.restart_game).grid(row=7, column=1, pady=10)
                return
            else:
                # Додаємо літеру в історію
                self.history.append(letter)
                self.letter_history.insert(tk.END, letter + ", ")
                self.system_text.config(text=f'Такої літери немає!\nЛишилось спроб: {7 - self.attempts_left}',
                                        anchor='center', justify='center')

    def start_game(self):
        # Початок гри
        self.start_button.destroy()
        f = open('words.txt', 'r', encoding='UTF-8')
        word_list = [i.strip() for i in f]
        self.target_word = random.choice(word_list).lower()
        word_silent = '*' * len(self.target_word)
        self.word_silent_list = list(word_silent)
        self.attempts_left = 0

        self.image_label.grid(row=1, columnspan=3)

        word_label_font = ('Helvetica', 21)
        word_label_text = ttk.Label(text='Загадане слово:', font=self.main_font)
        word_label_text.grid(row=2, column=0)

        self.word_label = ttk.Label(text=self.word_silent_list, font=word_label_font)
        self.word_label.grid(row=2, column=1)

        entry_label = ttk.Label(self.root, text="Введіть літеру:", font=self.main_font)
        entry_label.grid(row=4, column=0)

        self.letter_entry = ttk.Entry(self.root)
        self.letter_entry.grid(row=4, column=1)

        self.button_letter = ttk.Button(text='Відправити', command=self.check_letter)
        self.button_letter.grid(row=4, column=2)

        system_text_font = ('Helvetica', 14)
        self.system_text = ttk.Label(text='', font=system_text_font)
        self.system_text.grid(row=3, columnspan=3, pady=20)

        letter_history_label = ttk.Label(text='Використані літери:', font=self.main_font)
        letter_history_label.grid(row=6, column=0, pady=20)

        self.letter_history = ttk.Entry()
        self.letter_history.grid(row=6, column=1, pady=20)

    def restart_game(self):
        # Перезапуск гри
        self.attempts_left = 0
        self.history = []
        self.target_word = ""

        self.system_text.config(text='')

        self.letter_entry.delete(0, tk.END)
        self.letter_history.delete(0, tk.END)

        self.button_letter.config(state="normal")
        self.letter_entry.config(state="normal")

        self.update_image("main")
        self.word_label.config(text='')
        self.word_silent_list = []

        self.start_game()


if __name__ == "__main__":
    root = Tk()
    game = HangmanGame(root)
    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=1)
    root.columnconfigure(2, weight=1)
    root.mainloop()
