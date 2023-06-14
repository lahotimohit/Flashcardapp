import tkinter
import pandas
import random
BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}

try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(canvas_title, text= "French", fill="black")
    canvas.itemconfig(french_word, text=current_card["French"], fill="black")
    canvas.itemconfig(card_background, image=card_front_img)
    flip_timer = window.after(3000, change_config)


def change_config():
    canvas.itemconfig(canvas_title, text="English", fill="white")
    canvas.itemconfig(french_word, text=current_card["English"], fill="white")
    canvas.itemconfig(card_background, image=card_back_img)


def is_known():
    to_learn.remove(current_card)
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn", index=False)
    next_card()


window = tkinter.Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
flip_timer = window.after(3000, func=change_config)

canvas = tkinter.Canvas(width=800, height=526)
card_front_img = tkinter.PhotoImage(file="images/card_front.png")
card_back_img = tkinter.PhotoImage(file="images/card_back.png")

card_background = canvas.create_image(400, 263, image=card_front_img)
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)

canvas_title = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
french_word = canvas.create_text(400, 263, text="", font=("Arial", 60, "bold"))
canvas.grid(row=0, column=0, columnspan=2)

right_img = tkinter.PhotoImage(file="images/right.png")
right_btn = tkinter.Button(image=right_img, highlightthickness=0, command=is_known)
right_btn.grid(row=1, column=1)

wrong_img = tkinter.PhotoImage(file="images/wrong.png")
wrong_btn = tkinter.Button(image=wrong_img, highlightthickness=0, command=next_card)
wrong_btn.grid(column=0, row=1)

next_card()

window.mainloop()
