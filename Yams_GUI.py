# -*- coding: utf-8 -*-
"""
Jeu de yams - projet de NSI
Auteur : G. Costa, K. Ndjock, M. Flouret
Entrée: Si l'utilisateur veut relancer le dé ou non.
Sortie: Valeurs dices dé, ainsi que le nombres de relances qu'il lui reste

Programme principal : Gabriel
Relance : Keyrane
UI : Mathieu
"""
# Import de randint et tkinter
from random import randint
import tkinter as tk
from functools import partial
from PIL import Image, ImageTk

def lancer_de(max:int=6, nb_des:int=5):
	"""
	Renvoie une liste de dés aléatoires.
	max: Valeur maximale d'un dé. Défaut : 6
	nb_des : Nombre de dés à lancer. Défaut : 5
	"""
	return [randint(1, max) for k in range(nb_des)]

dices = [0] * 5
dices_to_rethrow = [i for i in range(len(dices))]

def clicked_button(button_number):
	"""
	Si un bouton est cliqué, on lui change sa couleur et on ajoute son index
	à la liste dices dés à relancer.
	"""
	global dices_to_rethrow
	global rethrows_amount

	if nombre_relances > 0:
		if button_number not in des_a_relancer:
			buttons[button_number].config(bg="#18db4c", fg="white", borderwidth=2)
			des_a_relancer.append(button_number)
		else:
			buttons[button_number].config(bg="#f0f0f0", fg="black", borderwidth=0)
			des_a_relancer.remove(button_number)


def afficher_des(window, row:int=None):
	"""
	Affiche de manière stylisée les dés disponibles
	window : La fenêtre tkinter
	row : La ligne pour le placement dices dés. Sera par
	défaut attribuée automatiquement.
	"""
	global dices

	# Assignation automatique de la ligne minimum via la taille de la grille
	if row is None:
		row = window.grid_size()[1] + 1
		globals()["buttons_row"] = row

	# Initialisation d'une liste de boutons, en variable globale
	globals()["buttons"] = []
	global buttons

	# Affichage dices dés, pour chaque dé dans la liste de dés
	for i in range(len(des)):
		de = des[i]
		buttons.append(
			tk.Button(
				window,
				text=str(de),
				font=("Impact", 20),
				borderwidth=0,
				command=partial(clicked_button, i),
				state = "disabled"
			)
		)
		buttons[len(buttons) - 1].grid(row=row, column=i)


def relancer():
	"""
	Réinitialise entièrement le jeu
	"""
	global buttons
	global dices_to_rethrow
	global dices
	global rethrows_amount
	global window
	global rethrow_button
	global stop_frame

	if nombre_relances == og_rethrows:
		# Affichage du frame
		stop_frame.grid(
			row=bouton_relance.grid_info()["row"],
			column=3,
			columnspan=2
		)

		# Possibilité de cliquer les dés
		for index in des_a_relancer:
			des[index] = randint(1, 6)
			buttons[index].config(text=str(des[index]), state="normal")

	if nombre_relances > 0 and nombre_relances != og_rethrows:
		for index in des_a_relancer:
			# Reset du style
			buttons[index].config(bg="#f0f0f0", fg="black", borderwidth=0)

			# Changement de la valeur
			des[index] = randint(1, 6)
			buttons[index].config(text=str(des[index]))

	des_a_relancer = []
	nombre_relances -= 1

	# If you cannot rethrow anymore
	if nombre_relances == 0:
		arret()

def calculer_scores():
	"""
	Calcule les scores à la fin du temps.
	"""
	global dices
	global score_label
	global score_text

	# Crée un tuple de tuples avec le nombre, et le
	# nombre de fois où il est apparu.
	# Format : ((1, 1), (2, 3), (3, 0), (4, 1), (5, 0), (6, 0))
	numbers = list()
	for i in range(1, 7):
		numbers.append((i, des.count(i)))
	numbers = tuple(numbers)

	# Crée une clé pour la fonction sorted, pour trier à partir du deuxième élément
	def sort_second(elem):
		return elem[1]

	numbers = sorted(numbers, key=sort_second, reverse=True)

	# Initialisation du score
	score = 0
	score_message = ""

	# On checke les résultats
	if numbers[0][1] == 5:  # Yam's
		score = 50
		score_message = "Yam's !"
	elif numbers[0][1] == 4:  # Carré
		score = 40
		score_message = f"Carré de {numbers[0][0]}"
	elif numbers[0][1] == 3 and numbers[1][1] == 2:  # Full
		score = 25
		score_message = f"Full en {numbers[0][0]} et {numbers[1][0]}"
	elif numbers[0][1] == 3:  # Brelan
		score = numbers[0][0] * 3
		score_message = f"Brelan de {numbers[0][0]}"
	else:
		for number in numbers:
			score += number[0] * number[1]

	# Affichage du score
	score_text.set(f"Votre score est de {score} !" +\
	     (f"\n({score_message})" if score_message != "" else ""))

def arret():
	"""
	Arrête le jeu.
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

	frame_rejouer.grid(row = rethrow_button.grid_info()["row"], column = 0, columnspan = 2)

	# Calcul dices scores
	calculer_scores()

def rejouer():
	"""
	Permet de rejouer.
	Réinitialise tous les éléments du jeu.
	"""
	global dices
	global dices_to_rethrow
	global buttons
	global buttons_row
	global rethrow_button
	global rethrows_amount
	global og_rethrows
	global score_text

	des = [0] * 5
	des_a_relancer = [i for i in range(len(des))]

	frame_replay.grid_forget()

	afficher_des(window, buttons_row)

	nombre_relances = og_relances

	bouton_relance.config(state="normal")

	score_text.set("")


window = tk.Tk()
window.geometry("400x260")
window.minsize(400, 260)
window.maxsize(400, 260)
window.title("Jeu de Yams")
window.iconbitmap("dice.ico")

# Création du titre
title = tk.Label(window, text="Jeu de Yams", font=("Goudy Stout", 24))
title.grid(row=0, column=0, columnspan=5)

# Affichage du logo
logo_img = Image.open("dice.ico")
logo_img = logo_img.resize((32, 32))
logo_image = ImageTk.PhotoImage(logo_img)
tk.Label(window, image=logo_image).grid(row=1, column=1, columnspan=3)

buttons_row = 1
# Affichage dices dés
afficher_des(window)

# Bouton de relance
rethrow_button = tk.Button(
	window,
	text="LANCER !",
	command=relancer,
	font=("Berlin Sans FB Demi", 23)
)
rethrow_button.grid(row=window.grid_size()[1], column=1, columnspan=3)

# Création du frame d'arrêt
stop_frame = tk.Frame(window)

# Chargement de l'image pour l'arrêt et création du bouton
stop_img = Image.open("stop.png")
stop_img = stop_img.resize((32, 32))
stop_image = ImageTk.PhotoImage(stop_img)
bouton_arret = tk.Button(
	stop_frame,
	command=arret,
	image=stop_image,
	borderwidth=0
).pack()

stop_label = tk.Label(
	stop_frame,
	text="Stop"
).pack()

# Frame pour rejouer
frame_replay = tk.Frame(window)

# Chargement de l'image pour rejouer et création du bouton
rejouer_img = Image.open("replay.png")
rejouer_img = rejouer_img.resize((32, 32))
rejouer_image = ImageTk.PhotoImage(rejouer_img)
bouton_rejouer = tk.Button(
	frame_replay,
	command=rejouer,
	image=rejouer_image,
	borderwidth=0
).pack()

rejouer_label = tk.Label(
	frame_replay,
	text="Rejouer"
).pack()

# Définition dices variables nécessaires
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
