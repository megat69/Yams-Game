# -*- coding: utf-8 -*-
"""
Yam's Game - Computer Science courses project
Auteur : Majorspic, Ranekey, TheAssassin71
"""
# Imports of the required libraries
from random import randint
import tkinter as tk
from functools import partial
from PIL import Image, ImageTk

def lancer_de(max:int=6, dices_amount:int=5):
	"""
	Retruns a random list of dices.
	max: Max value of a dice. Default : 6
	dices_amount: Amount of dices to throw. Default : 5
	"""
	return [randint(1, max) for k in range(dices_amount)]

dices = [0] * 5
dices_to_rethrow = [i for i in range(len(dices))]

def clicked_button(button_number):
	"""
	When a button is clicked, we change its color and add its index
	to the list of dices to rethrow.
	"""
	global dices_to_rethrow
	global rethrows_amount

	if rethrows_amount > 0:
		if button_number not in dices_to_rethrow:
			buttons[button_number].config(bg="#18db4c", fg="white", borderwidth=2)
			dices_to_rethrow.append(button_number)
		else:
			buttons[button_number].config(bg="#f0f0f0", fg="black", borderwidth=0)
			dices_to_rethrow.remove(button_number)


def dispaly_dices(window, row:int=None):
	"""
	Displays the dices.
	window : The tkinter rot window
	row : The line to place dices on. Will by default
	be automatically selected.
	"""
	global dices

	# Automatic assignment of the minimum row using the grid size
	if row is None:
		row = window.grid_size()[1] + 1
		globals()["buttons_row"] = row

	# Initialising of a buttons list, as a global var
	globals()["buttons"] = []
	global buttons

	# Displaying of the dices, for each dice in the dice list
	for i in range(len(dices)):
		dice = dices[i]
		buttons.append(
			tk.Button(
				window,
				text=str(dice),
				font=("Impact", 20),
				borderwidth=0,
				command=partial(clicked_button, i),
				state = "disabled"
			)
		)
		buttons[len(buttons) - 1].grid(row=row, column=i)


def rethrow():
	"""
	Resets entirely the game.
	"""
	global buttons
	global dices_to_rethrow
	global dices
	global rethrows_amount
	global window
	global rethrow_button
	global stop_frame

	if rethrows_amount == og_rethrows:
		# Frame displaying
		stop_frame.grid(
			row=rethrow_button.grid_info()["row"],
			column=3,
			columnspan=2
		)

		# Ability to click the dices
		for index in dices_to_rethrow:
			dices[index] = randint(1, 6)
			buttons[index].config(text=str(dices[index]), state="normal")

	if rethrows_amount > 0 and rethrows_amount != og_rethrows:
		for index in dices_to_rethrow:
			# Reset of the style
			buttons[index].config(bg="#f0f0f0", fg="black", borderwidth=0)

			# Change of the value
			dices[index] = randint(1, 6)
			buttons[index].config(text=str(dices[index]))

	dices_to_rethrow = []
	rethrows_amount -= 1

	# If you cannot rethrow anymore
	if rethrows_amount == 0:
		arret()

def calculer_scores():
	"""
	Calculates the scores at the end of the game.
	"""
	global dices
	global score_label
	global score_text

	# Creates a tuple of tuple containing the number, and
	# the amount of times it appeared.
	# Format : ((1, 1), (2, 3), (3, 0), (4, 1), (5, 0), (6, 0))
	numbers = list()
	for i in range(1, 7):
		numbers.append((i, dices.count(i)))
	numbers = tuple(numbers)

	# Creates a key for the sorted() function, to sort by the second element
	def sort_second(elem):
		return elem[1]

	numbers = sorted(numbers, key=sort_second, reverse=True)

	# Initialising of the score
	score = 0
	score_message = ""

	# Checking the results
	if numbers[0][1] == 5:  # Yam's
		score = 50
		score_message = "Yam's !"
	elif numbers[0][1] == 4:  # Square
		score = 40
		score_message = f"Square of {numbers[0][0]}"
	elif numbers[0][1] == 3 and numbers[1][1] == 2:  # Full
		score = 25
		score_message = f"Full of {numbers[0][0]} by {numbers[1][0]}"
	elif numbers[0][1] == 3:  # Brelan
		score = numbers[0][0] * 3
		score_message = f"Brelan of {numbers[0][0]}"
	else:
		for number in numbers:
			score += number[0] * number[1]

	# Affichage du score
	score_text.set(f"Your score is {score} !" +\
	     (f"\n({score_message})" if score_message != "" else ""))

def arret():
	"""
	Stops the game.
	"""
	global stop_frame
	global frame_replay

	rethrow_button.config(
		command=None,
		state="disabled"
	)
	for i in range(len(buttons)):
		buttons[i].config(state="disabled")

	stop_frame.grid_forget()

	frame_replay.grid(row = rethrow_button.grid_info()["row"], column = 0, columnspan = 2)

	# Calculates the score
	calculer_scores()

def rejouer():
	"""
	Allows to play again.
	Resets all the game elements.
	"""
	global dices
	global dices_to_rethrow
	global buttons
	global buttons_row
	global rethrow_button
	global rethrows_amount
	global og_rethrows
	global score_text

	dices = [0] * 5
	dices_to_rethrow = [i for i in range(len(dices))]

	frame_replay.grid_forget()

	dispaly_dices(window, buttons_row)

	rethrows_amount = og_rethrows

	rethrow_button.config(state="normal")

	score_text.set("")


window = tk.Tk()
window.geometry("400x260")
window.minsize(400, 260)
window.maxsize(400, 260)
window.title("Yam's Game")
window.iconbitmap("dice.ico")

# Title creation
title = tk.Label(window, text="Yam's Game", font=("Goudy Stout", 24))
title.grid(row=0, column=0, columnspan=5)

# Logo displaying
logo_img = Image.open("dice.ico")
logo_img = logo_img.resize((32, 32))
logo_image = ImageTk.PhotoImage(logo_img)
tk.Label(window, image=logo_image).grid(row=1, column=1, columnspan=3)

buttons_row = 1
# Dices displaying
dispaly_dices(window)

# Rethrow button
rethrow_button = tk.Button(
	window,
	text="THROW !",
	command=rethrow,
	font=("Berlin Sans FB Demi", 23)
)
rethrow_button.grid(row=window.grid_size()[1], column=1, columnspan=3)

# Stop frame creation
stop_frame = tk.Frame(window)

# Loading of the stop image and button creation
stop_img = Image.open("stop.png")
stop_img = stop_img.resize((32, 32))
stop_image = ImageTk.PhotoImage(stop_img)
stop_button = tk.Button(
	stop_frame,
	command=arret,
	image=stop_image,
	borderwidth=0
).pack()

stop_label = tk.Label(
	stop_frame,
	text="Stop"
).pack()

# Frame to play again
frame_replay = tk.Frame(window)

# Loading of the replay image and button creation
replay_img = Image.open("replay.png")
replay_img = replay_img.resize((32, 32))
replay_image = ImageTk.PhotoImage(replay_img)
replay_button = tk.Button(
	frame_replay,
	command=rejouer,
	image=replay_image,
	borderwidth=0
).pack()

replay_label = tk.Label(
	frame_replay,
	text="Play again"
).pack()

# Init of the necessary variables
rethrows_amount = 3
og_rethrows = rethrows_amount
max_size = window.grid_size()[1]
score_text = tk.StringVar()
score_label = tk.Label(
	window,
	textvariable=score_text,
	fg="red",
	font=("Arial Rounded MT Bold", 16)
).grid(
	row = window.grid_size()[1],
	column = 0,
	columnspan = window.grid_size()[0]
)

window.mainloop()
