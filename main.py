import time
import turtle
import sqlite3
import random
import math

# se connecter à la base de données (ou la créer si elle n'existe pas)
conn = sqlite3.connect('pong.db')

# créer la table 'players' si elle n'existe pas déjà
conn.execute('''CREATE TABLE IF NOT EXISTS players
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 name TEXT NOT NULL,
                 score INTEGER NOT NULL);''')

# ajouter un nouveau joueur dans la table
def add_player(name, score):
    conn.execute("INSERT INTO players (name, score) VALUES (?, ?)", (name, score))
    conn.commit()

# récupérer la liste des joueurs classés par score décroissant
def get_players():
    cursor = conn.execute("SELECT name, score FROM players ORDER BY score DESC")
    return cursor.fetchall()

# fermer la connexion à la base de données
def close_db():
    conn.close()

# initialiser l'écran
screen = turtle.Screen()
screen.title("Pong Game")
screen.bgcolor("black")
screen.setup(width=600, height=400)

# demander les noms des joueurs
player_a_name = turtle.textinput("Player A Name", "Enter name for Player A:")
player_b_name = turtle.textinput("Player B Name", "Enter name for Player B:")

# ajouter les raquettes
racket_a = turtle.Turtle()
racket_a.speed(0)
racket_a.shape("square")
racket_a.color("white")
racket_a.shapesize(stretch_wid=5, stretch_len=1)
racket_a.penup()
racket_a.goto(-250, 0)

racket_b = turtle.Turtle()
racket_b.speed(0)
racket_b.shape("square")
racket_b.color("white")
racket_b.shapesize(stretch_wid=5, stretch_len=1)
racket_b.penup()
racket_b.goto(250, 0)

# ajouter la balle
ball = turtle.Turtle()
ball.speed(40)
ball.shape("circle")
ball.color("white")
ball.penup()
ball.goto(0, 0)
ball.dx = 4
ball.dy = -4

# ajouter les scores
score_a = 0
score_b = 0

score = turtle.Turtle()
score.speed(0)
score.color("white")
score.penup()
score.hideturtle()
score.goto(0, 160)
score.write(f"{player_a_name}: {score_a}  {player_b_name}: {score_b}", align="center", font=("Courier", 16, "normal"))


# Générer un angle aléatoire entre 30 et 150 degrés ball.dx = 4 * math.cos(angle) # Calculer la nouvelle vitesse horizontale ball.dy = 4 * math.sin(angle) # Calculer la nouvelle vitesse verticale
def set_random_ball_direction(ball): angle = random.uniform(math.radians(30), math.radians(150))
set_random_ball_direction(ball)
if ball.xcor() > 290:
    ball.goto(0, 0)
    set_random_ball_direction(ball)
    score_a += 1
    score.clear()

if ball.xcor() < -290:
    ball.goto(0, 0)
    set_random_ball_direction(ball)
    score_b += 1
    score.clear()


def check_collision_with_racket(racket, ball):
    if racket.distance(ball) < 50:
        ball.dx *= -1.5 # Augmenter la vitesse horizontale de la balle de 15%
        ball.dy *= 1.5 # Augmenter la vitesse verticale de la balle de 15%

def racket_a_up():
    y = racket_a.ycor()
    y += 20
    if y > 190:  # Vérifier si la raquette touche le bord de l'écran
        y = 190
    racket_a.sety(y)

def racket_a_down():
    y = racket_a.ycor()
    y -= 20
    if y < -190:  # Vérifier si la raquette touche le bord de l'écran
        y = -190
    racket_a.sety(y)

def racket_b_up():
    y = racket_b.ycor()
    y += 20
    if y > 190:  # Vérifier si la raquette touche le bord de l'écran
        y = 190
    racket_b.sety(y)

def racket_b_down():
    y = racket_b.ycor()
    y -= 20
    if y < -190:  # Vérifier si la raquette touche le bord de l'écran
        y = -190
    racket_b.sety(y)

# associer les touches du clavier aux mouvements des raquettes
screen.listen()
screen.onkeypress(racket_a_up, "w")
screen.onkeypress(racket_a_down, "s")
screen.onkeypress(racket_b_up, "Up")
screen.onkeypress(racket_b_down, "Down")

# boucle principale du jeu
while True:
    screen.update()

    # déplacer la balle
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

    # vérifier les collisions avec les bords de l'écran
    if ball.ycor() > 190:
        ball.sety(190)
        ball.dy *= -1

    if ball.ycor() < -190:
        ball.sety(-190)
        ball.dy *= -1

    if ball.xcor() > 290:
        ball.goto(0, 0)
        ball.dx *= -1
        score_a += 1
        score.clear()
        ball.dx = 4
        ball.dy = -4
        ball.goto(0, 0)

    if ball.xcor() < -290:
        ball.goto(0, 0)
        ball.dx *= -1
        score_b += 1
        score.clear()
        ball.dx = 4
        ball.dy = -4
        ball.goto(0, 0)

    score.write(f"{player_a_name}: {score_a}  {player_b_name}: {score_b}", align="center", font=("Courier", 16, "normal"))

# vérifier les collisions avec les raquettes
    if 240 < ball.xcor() < 250 and racket_b.ycor() + 50 > ball.ycor() > racket_b.ycor() - 50:
        ball.setx(240)
        check_collision_with_racket(racket_b, ball)

    if -240 > ball.xcor() > -250 and racket_a.ycor() + 50 > ball.ycor() > racket_a.ycor() - 50:
        ball.setx(-240)
        check_collision_with_racket(racket_a, ball)

    # vérifier si un joueur a gagné
    if score_a >= 5:
        score.clear()
        score.goto(0, 0)
        score.write(f"{player_a_name} wins!", align="center", font=("Courier", 16, "normal"))
        time.sleep(3)
        break
    elif score_b >= 5:
        score.clear()
        score.goto(0, 0)
        score.write(f"{player_b_name} wins!", align="center", font=("Courier", 16, "normal"))
        time.sleep(3)
        break

# après l'affichage du message "Player A wins!" ou "Player B wins!" dans la boucle principale du jeu

# enregistrer le joueur gagnant dans la base de données
    if score_a >= 5:
        add_player(player_a_name, score_a)
        score.clear()
        score.goto(0, 0)
        score.write(f"{player_a_name} wins!", align="center", font=("Courier", 16, "normal"))
        break
    elif score_b >= 5:
        add_player(player_b_name, score_b)
        score.clear()
        score.goto(0, 0)
        score.write(f"{player_b_name} wins!", align="center", font=("Courier", 16, "normal"))
        break

# afficher les 10 meilleurs joueurs dans la console
for i, (name, score) in enumerate(get_players()[:10], start=1):
    print(f"{i}. {name}: {score} points")

