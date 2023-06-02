from tkinter import *
import random
import pickle

GAME_WIDTH = 700
GAME_HEIGHT = 600
SPEED = 100
SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"
LEVELS = [1, 2, 3, 4, 5]
SPEED_DECREMENT = 10

class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

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

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))

    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)

    snake.squares.insert(0, square)  # Add the new square to the snake's squares list

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


def change_direction(new_direction):
    global direction

    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction
    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction
    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction
    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction


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
    global snake, food, score, direction, high_score, level
    score = 0
    direction = 'down'
    level = int(level_var.get())  # Get the selected level from the dropdown menu
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
    return SPEED - (level - 1) * SPEED_DECREMENT


window = Tk()
window.title("Snake game")
window.resizable(False, False)

score = 0
direction = 'down'
high_score = load_high_score()
level = 1

label = Label(window, text="Score:{}  High Score:{}  Level:{}".format(score, high_score, level), font=('consolas', 40))
label.pack()

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

level_label = Label(window, text="Level:", font=('consolas', 20))
level_label.pack()

level_var = StringVar(window)
level_var.set(LEVELS[0])  # Set the default level
level_dropdown = OptionMenu(window, level_var, *LEVELS)
level_dropdown.pack()

start_button = Button(window, text="Start", font=('consolas', 20), command=start_game)
start_button.pack()
start_button.focus_set()

window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width/2) - (window_width/2))
y = int((screen_height/2) - (window_height/2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))

snake = None
food = None

window.mainloop()