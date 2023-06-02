from tkinter import *
import random
import pickle

GAME_WIDTH = 700
GAME_HEIGHT = 600
SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"
SPEED = {
    "Easy": 100,
    "Medium": 75,
    "Hard": 50
}

class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []
        self.direction = "down"

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)


class Food:
    def __init__(self):
        x = random.randint(0, (GAME_WIDTH / SPACE_SIZE)-1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE

        self.coordinates = [x, y]

        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")


def next_turn(snake, food):
    x, y = snake.coordinates[0]

    if snake.direction == "up":
        y -= SPACE_SIZE
    elif snake.direction == "down":
        y += SPACE_SIZE
    elif snake.direction == "left":
        x -= SPACE_SIZE
    elif snake.direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))

    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)

    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1
        label.config(text="Score:{}  High Score:{}  Level:{}".format(score, high_score, level))
        canvas.delete("food")
        food = Food()
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collisions(snake):
        game_over()
    else:
        window.after(get_speed(), next_turn, snake, food)


def change_direction(event, snake):
    key = event.keysym.lower()
    
    if key == "up":
        if snake.direction != "down":
            snake.direction = "up"
    elif key == "down":
        if snake.direction != "up":
            snake.direction = "down"
    elif key == "left":
        if snake.direction != "right":
            snake.direction = "left"
    elif key == "right":
        if snake.direction != "left":
            snake.direction = "right"


def check_collisions(snake):
    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH:
        return True
    elif y < 0 or y >= GAME_HEIGHT:
        return True

    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    return False


def game_over():
    global score, high_score
    canvas.delete(ALL)
    canvas.create_text(
        canvas.winfo_width() / 2, canvas.winfo_height() / 2,
        font=('consolas', 70), text="GAME OVER", fill="red", tag="gameover"
    )
    start_button.config(state=NORMAL)

    if score > high_score:
        high_score = score
        save_high_score(high_score)

    label.config(text="Score:{}  High Score:{}  Level:{}".format(score, high_score, level))


def start_game():
    global snake, food, score, level, high_score
    score = 0
    level = level_var.get()
    label.config(text="Score:{}  High Score:{}  Level:{}".format(score, high_score, level))
    canvas.delete(ALL)
    start_button.config(state=DISABLED)
    snake = Snake()
    food = Food()
    next_turn(snake, food)


def load_high_score():
    try:
        with open("high_score.pickle", "rb") as file:
            high_score = pickle.load(file)
        return high_score
    except (OSError, IOError, pickle.UnpicklingError):
        return 0


def save_high_score(high_score):
    with open("high_score.pickle", "wb") as file:
        pickle.dump(high_score, file)


def get_speed():
    return SPEED[level]


window = Tk()
window.title("Snake Game")
window.resizable(False, False)

score = 0
level = "Easy"
high_score = load_high_score()

label = Label(window, text="Score:{}  High Score:{}  Level:{}".format(score, high_score, level), font=('consolas', 40))
label.pack()

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

start_button = Button(window, text="Start", font=('consolas', 20), command=start_game)
start_button.pack()

level_var = StringVar()
level_var.set(level)
level_menu = OptionMenu(window, level_var, *SPEED.keys())
level_menu.config(font=('consolas', 15))
level_menu.pack()

window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width/2) - (window_width/2))
y = int((screen_height/2) - (window_height/2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

window.bind('<Key>', lambda event: change_direction(event, snake))

snake = None
food = None

window.mainloop()