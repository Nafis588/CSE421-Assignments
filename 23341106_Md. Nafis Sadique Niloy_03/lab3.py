from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.GLUT.fonts import GLUT_BITMAP_HELVETICA_18
import random
from math import sin, cos, sqrt
import time
import threading


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700
SHOOTER_RADIUS = 30
BALL_RADIUS = 20
PROJECTILE_RADIUS = 10
FALL_SPEED = 2
NUM_BALLS = 10
PROJECTILE_SPEED = 10

RETRY_BUTTON_LOCATION = (10, SCREEN_HEIGHT - 30)
PAUSE_BUTTON_LOCATION = (SCREEN_WIDTH / 2, SCREEN_HEIGHT - 30)
EXIT_BUTTON_LOCATION = (SCREEN_WIDTH - 10, SCREEN_HEIGHT - 30)

white = (1.0, 1.0, 1.0)
red = (1.0, 0.0, 0.0)
teal = (0.0, 1.0, 1.0)
amber = (1.0, 0.5, 0.0)
green = (0.0, 1.0, 0.0)
blue = (0.0, 0.0, 1.0)
purple = (1.0, 0.0, 1.0)
yellow = (1.0, 1.0, 0.0)
colors = [white, red, teal, amber, green, blue, purple, yellow]


shooter_x = SCREEN_WIDTH // 2
shooter_y = 50
balls = []
projectiles = []  
score = 0
missed_circles = 0
missed_shots = 0 
game_over = False
paused = False
exit_game = False

retry_color = teal
pause_color = amber
exit_color = red


def retryButton(x, y, color=retry_color):
    draw_line(x, y, x + 20, y - 20, color)
    draw_line(x, y, x + 20, y + 20, color)
    draw_line(x, y, x + 50, y, color)


def pauseButton(x, y, color=pause_color):
    draw_line(x + 10, y + 20, x + 10, y - 20, color)
    draw_line(x - 10, y + 20, x - 10, y - 20, color)


def playButton(x, y, color=pause_color):
    draw_line(x - 10, y + 20, x + 10, y, color)
    draw_line(x - 10, y - 20, x + 10, y, color)


def exitButton(x, y, color=exit_color):
    draw_line(x - 10, y + 10, x + 10, y - 10, color)
    draw_line(x - 10, y - 10, x + 10, y + 10, color)


def plot_circle_points(x_center, y_center, x, y, color):
    glColor(color)
    glBegin(GL_POINTS)
    glVertex2f(x_center + x, y_center + y)
    glVertex2f(x_center - x, y_center + y)
    glVertex2f(x_center + x, y_center - y)
    glVertex2f(x_center - x, y_center - y)
    glVertex2f(x_center + y, y_center + x)
    glVertex2f(x_center - y, y_center + x)
    glVertex2f(x_center + y, y_center - x)
    glVertex2f(x_center - y, y_center - x)
    glEnd()


def midpoint_circle(x_center, y_center, radius, color):
    x = 0
    y = radius
    d = 1 - radius
    plot_circle_points(x_center, y_center, x, y, color)
    
    while x < y:
        if d < 0:
            d = d + 2 * x + 3
        else:
            d = d + 2 * (x - y) + 5
            y -= 1
        x += 1
        plot_circle_points(x_center, y_center, x, y, color)


def draw_circle(x, y, radius, color):
    midpoint_circle(x, y, radius, color)


def init_balls():
    global balls
    balls = []

def spawn_ball():
    global balls
    ball = {
        'x': random.randint(0, SCREEN_WIDTH),
        'y': SCREEN_HEIGHT,  
        'speed': 1,  
        'color': (random.random(), random.random(), random.random())
    }
    balls.append(ball)

def ball_spawner():
    while not game_over:
        spawn_ball()
        time.sleep(random.uniform(0.5, 2)) 

def draw_balls():
    global balls
    for ball in balls:
        draw_circle(ball['x'], ball['y'], BALL_RADIUS, ball['color'])


def draw_shooter():
    draw_circle(shooter_x, shooter_y, SHOOTER_RADIUS, white)


def draw_projectiles():
    global projectiles
    for projectile in projectiles:
        draw_circle(projectile['x'], projectile['y'], PROJECTILE_RADIUS, red)


def handle_mouse(button, state, x, y):
    global paused, exit_game, game_over
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        if RETRY_BUTTON_LOCATION[0] <= x <= RETRY_BUTTON_LOCATION[0] + 50 and SCREEN_HEIGHT - y >= RETRY_BUTTON_LOCATION[1] - 20 and SCREEN_HEIGHT - y <= RETRY_BUTTON_LOCATION[1] + 20:
            retry_game()
            print("Game Restarted")
        if EXIT_BUTTON_LOCATION[0] - 20 <= x <= EXIT_BUTTON_LOCATION[0] + 20 and SCREEN_HEIGHT - y >= EXIT_BUTTON_LOCATION[1] - 20 and SCREEN_HEIGHT - y <= EXIT_BUTTON_LOCATION[1] + 20:
            exit_game = True
            print("Exit Game")
        if not game_over:
            if PAUSE_BUTTON_LOCATION[0] - 20 <= x <= PAUSE_BUTTON_LOCATION[0] + 20 and SCREEN_HEIGHT - y >= PAUSE_BUTTON_LOCATION[1] - 20 and SCREEN_HEIGHT - y <= PAUSE_BUTTON_LOCATION[1] + 20:
                paused = not paused
                if paused:
                    print("Game Paused")
                else:
                    print("Game Resumed")
        else:
            print("You cannot press resume or play button when game is over")


def handle_keyboard(key, x, y):
    global shooter_x, projectiles, game_over

    if game_over:
        return  

    if key == b'a' or key == b'A':
        shooter_x -= 15
    if key == b'd' or key == b'D':
        shooter_x += 15

    if shooter_x < SHOOTER_RADIUS:
        shooter_x = SHOOTER_RADIUS

    if shooter_x > SCREEN_WIDTH - SHOOTER_RADIUS:
        shooter_x = SCREEN_WIDTH - SHOOTER_RADIUS

    
    if key == b' ':
        projectile = {'x': shooter_x, 'y': shooter_y + SHOOTER_RADIUS}
        projectiles.append(projectile)


def collision(ball_x, ball_y, object_x, object_y, object_radius):
    distance = sqrt((ball_x - object_x) ** 2 + (ball_y - object_y) ** 2)
    return distance <= (BALL_RADIUS + object_radius)


def handle_collision(ball, projectile):
    global score
    score += 1
    print(f'Score: {score}')
    balls.remove(ball)
    
    if projectile is not None:
        if projectile in projectiles:
            projectiles.remove(projectile)


def retry_game():
    global balls, projectiles, score, missed_circles, missed_shots, game_over, paused
    init_balls()
    projectiles = []
    score = 0
    missed_circles = 0
    missed_shots = 0  
    game_over = False
    paused = False
    threading.Thread(target=ball_spawner, daemon=True).start()  

def animate(v):
    global balls, projectiles, missed_circles, missed_shots, game_over, paused

    if not paused and not game_over:
        for ball in balls:
            ball['y'] -= ball['speed']

            if collision(ball['x'], ball['y'], shooter_x, shooter_y, SHOOTER_RADIUS):
                game_over = True
                print(f"Game Over! A circle touched the shooter. Final Score: {score}")
                break

            elif ball['y'] < 0:
                missed_circles += 1
                balls.remove(ball)
                if missed_circles == 1:
                    print(f"Missed 1 circle. Score: {score}")
                elif missed_circles == 2:
                    print(f"Missed 2 circles. Score: {score}")
                elif missed_circles >= 3:
                    game_over = True
                    print(f"Game Over! Missed {missed_circles} circles. Final Score: {score}")
                    break  

        for projectile in projectiles:
            projectile['y'] += PROJECTILE_SPEED
            if projectile['y'] > SCREEN_HEIGHT:
                projectiles.remove(projectile)
                missed_shots += 1 
                if missed_shots == 1:
                    print(f"Missed 1 shot. Score: {score}")
                elif missed_shots == 2:
                    print(f"Missed 2 shot. Score: {score}")
                if missed_shots >= 3:
                    game_over = True
                    print(f"Game Over! You missed {missed_shots} shots. Final Score: {score}")
                    break

            for ball in balls:
                if collision(ball['x'], ball['y'], projectile['x'], projectile['y'], PROJECTILE_RADIUS):
                    handle_collision(ball, projectile)
                    break  

    if exit_game:
        glutLeaveMainLoop() 

    glutPostRedisplay()
    glutTimerFunc(10, animate, 0)


def draw_line(x1, y1, x2, y2, color):
    glColor(color)
    glBegin(GL_LINES)
    glVertex2f(x1, y1)
    glVertex2f(x2, y2)
    glEnd()


def display():
    glClear(GL_COLOR_BUFFER_BIT)
    draw_shooter()
    draw_balls()
    draw_projectiles()

    retryButton(RETRY_BUTTON_LOCATION[0], RETRY_BUTTON_LOCATION[1])
    exitButton(EXIT_BUTTON_LOCATION[0], EXIT_BUTTON_LOCATION[1])
    if paused:
        playButton(PAUSE_BUTTON_LOCATION[0], PAUSE_BUTTON_LOCATION[1])
    else:
        pauseButton(PAUSE_BUTTON_LOCATION[0], PAUSE_BUTTON_LOCATION[1])

    glutSwapBuffers()


def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    gluOrtho2D(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT)
    retry_game()


# OpenGL setup
glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(SCREEN_WIDTH, SCREEN_HEIGHT)
glutCreateWindow(b"Shoot The Circles!")
glutDisplayFunc(display)
glutTimerFunc(10, animate, 0)
glutKeyboardFunc(handle_keyboard)
glutMouseFunc(handle_mouse)
init()
glutMainLoop()