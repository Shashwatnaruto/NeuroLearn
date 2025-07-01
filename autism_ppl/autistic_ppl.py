import serial
import time
import os
import subprocess
import threading
import pygame
import random
import time
from flask import Flask, render_template, request
app = Flask(__name__)

class Snake:
    def _init_(self):
        self.body = [(100, 100), (90, 100), (80, 100)]
        self.direction = "RIGHT"
        self.color = (0, 0, 255)

    def move(self):
        head_x, head_y = self.body[0]
        if self.direction == "UP":
            head_y -= 10
        elif self.direction == "DOWN":
            head_y += 10
        elif self.direction == "LEFT":
            head_x -= 10
        elif self.direction == "RIGHT":
            head_x += 10

        head_x %= 800
        head_y %= 600

        new_head = (head_x, head_y)
        self.body = [new_head] + self.body[:-1]

    def grow(self):
        self.body.append(self.body[-1])

    def draw(self, screen):
        for block in self.body:
            pygame.draw.rect(screen, self.color, pygame.Rect(block[0], block[1], 10, 10))

class Apple:
    def _init_(self):
        self.size = 10
        self.color = (255, 0, 0)
        self.position = self.spawn()

    def spawn(self):
        x = random.randint(0, 79) * self.size
        y = random.randint(0, 59) * self.size
        return (x, y)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, pygame.Rect(self.position[0], self.position[1], self.size, self.size))

def run_snake(duration=300):
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("NeuroLearn Snake Game")
    clock = pygame.time.Clock()

    snake = Snake()
    apple = Apple()

    running = True
    start_time = time.time()

    while running:
        screen.fill((0, 255, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake.direction != "DOWN":
                    snake.direction = "UP"
                elif event.key == pygame.K_DOWN and snake.direction != "UP":
                    snake.direction = "DOWN"
                elif event.key == pygame.K_LEFT and snake.direction != "RIGHT":
                    snake.direction = "LEFT"
                elif event.key == pygame.K_RIGHT and snake.direction != "LEFT":
                    snake.direction = "RIGHT"

        snake.move()

        if snake.body[0] == apple.position:
            snake.grow()
            apple = Apple()

        apple.draw(screen)
        snake.draw(screen)

        pygame.display.update()
        clock.tick(10)

        if time.time() - start_time >= duration:
            print(f"[INFO] Snake game ended after {duration} seconds.")
            running = False

    pygame.quit()

class EEGController:
    def _init_(self, port='COM10', baudrate=9600, timeout=1):
        try:
            self.arduino = serial.Serial(port, baudrate, timeout=timeout)
            print(f"[CONNECTED] Arduino on {port}")
        except Exception as e:
            self.arduino = None
            print(f"[ERROR] Arduino not found: {e}")

        self.running_game = False

    def read_serial(self):
        while True:
            if self.arduino and self.arduino.in_waiting:
                try:
                    line=self.arduino.readline().decode().strip().lower()
                    print(f"[DATA] Brain state: {line}")
                    self.handle_state(line)
                except Exception as e:
                    print(f"[ERROR] Serial read: {e}")
            time.sleep(1)
        if line== "bored":
            threading.Thread(target=lambda: run_snake(300), daemon=True).start()
        elif line== "tired":
            threading.Thread(target=lambda: run_snake(600), daemon=True).start()
        elif line=="overstimulated":
            print("[EXIT] Overstimulated detected. Shutting down.")
    os._exit(1)
    def handle_state(self, state):
        if state == "bored":
            if not self.running_game:
                self.running_game = True
                print("[ACTION] Launching snake game for 5 min (bored)")
                threading.Thread(target=self.play_game, args=(5,), daemon=True).start()

        elif state == "tired":
            if not self.running_game:
                self.running_game = True
                print("[ACTION] Launching snake game for 10 min (tired)")
                threading.Thread(target=self.play_game, args=(10,), daemon=True).start()

        elif state == "overstimulated":
            print("[EXIT] User overstimulated. Exiting app.")
            os._exit(0)

    def play_game(self, duration_minutes):
        # Run a snake game (replace this path with your own game script or exe)
        # You can use subprocess to run a script or open any game.
        try:
            subprocess.Popen(["python", "snake_game.py"])  # run your snake game file
            time.sleep(duration_minutes * 60)
            print(f"[CLOSE] {duration_minutes} min elapsed, close the game manually if needed.")
            # Optionally: kill game here if you want automatic closure
        except Exception as e:
            print(f"[ERROR] Failed to run game: {e}")
        finally:
            self.running_game = False
            import pygame
@app.route("/motion", methods=["GET", "POST"])
def motion():
    global current_q_index
    result = None
    explanation = None
    question = question[current_q_index]

    if request.method == "POST":
        try:
            user_ans = float(request.form["answer"])
            correct = question["ans"]
            explanation = question["explanation"]
            if abs(user_ans - correct) < 0.01:
                result = " Correct!"
                current_q_index = (current_q_index + 1) % len(question)  # Move to next
            else:
                result = " Incorrect. Try again!"
        except:
            result = " Please enter a number."

    return render_template("motion.html", question=question["q"], result=result, explanation=explanation)

@app.route("/learn")
def learn():
    return render_template("learn.html")

# --- RUN ----------
if _name_ == '_main_':
    os.environ['FLASK_ENV'] = 'development'
    app.run(debug=True,port=5000)