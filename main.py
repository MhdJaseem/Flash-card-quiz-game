from tkinter import *
from tkinter import messagebox
import pandas
import random
import os

BACKGROUND_COLOR = "#B1DDC6"

try:
    data = pandas.read_csv("./data/Translated Words.csv")

except FileNotFoundError:
    data = pandas.read_csv("./data/Translated Words.csv")

except pandas.errors.EmptyDataError:
    data = pandas.read_csv("./data/french_words.csv")

data_dict = data.to_dict(orient="records")
current_card = random.choice(data_dict)

# ---------------------------------- NEW FLASH CARD --------------------------------


def new_card():
    global current_card
    try:
        current_card = random.choice(data_dict)
    except IndexError:
        ok = messagebox.showinfo(title="WELL DONE!", message="You successfully completed the Quiz...!")
        if ok:
            os.remove("./data/words_to_learn.csv")
            window.destroy()

    canvas.itemconfig(card_image, image=card_front_img)
    canvas.itemconfig(lang_text, text='French', fill='black')
    canvas.itemconfig(word_text, text=current_card['French'], fill='black')
    window.after(3000, flip_card)

# ------------------------------------ SAVE WORDS ----------------------------------


def known_word():

    data_dict.remove(current_card)
    words_to_learn = pandas.DataFrame(data_dict)
    words_to_learn.to_csv("./data/words_to_learn.csv", index=False)
    new_card()


def unknown_word():

    words_to_learn = pandas.DataFrame(data_dict)
    words_to_learn.to_csv("./data/words_to_learn.csv", index=False)
    new_card()
# ------------------------------------ FLIP CARD -----------------------------------


def flip_card():

    canvas.itemconfig(card_image, image=card_back_img)
    canvas.itemconfig(lang_text, text='English', fill='white')
    canvas.itemconfig(word_text, text=current_card['English'], fill='white')

# ------------------------------------ UI SETUP ------------------------------------


window = Tk()
window.title("Flash Card")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)


canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_img = PhotoImage(file="./images/card_front.png")
card_back_img = PhotoImage(file="./images/card_back.png")

card_image = canvas.create_image(400, 260, image=card_front_img)
canvas.grid(row=1, column=1, columnspan=2)

lang_text = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
word_text = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))

right_img = PhotoImage(file="./images/right.png")
right_button = Button(image=right_img, highlightthickness=0, bd=0, command=known_word)
right_button.grid(row=2, column=1)

wrong_img = PhotoImage(file="./images/wrong.png")
wrong_button = Button(image=wrong_img, highlightthickness=0, bd=0, command=unknown_word)
wrong_button.grid(row=2, column=2)

new_card()
window.after(3000, flip_card)

window.mainloop()
