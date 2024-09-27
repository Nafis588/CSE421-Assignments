from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import random


SCREEN_WIDTH=800
SCREEN_HEIGHT=600
CATCHER_WIDTH=150
CATCHER_HEIGHT=30
FALL_SPEED=2
NUM_DIAMONDS=10
RETRY_BUTTON_LOCATION=(10,SCREEN_HEIGHT-30)
PAUSE_BUTTON_LOCATION=(SCREEN_WIDTH/2,SCREEN_HEIGHT-30)
EXIT_BUTTON_LOCATION=(SCREEN_WIDTH-10,SCREEN_HEIGHT-30)

# Colors
white=(1.0,1.0,1.0)
red=(1.0,0.0,0.0)
teal=(0.0,1.0,1.0)
amber=(1.0,0.5,0.0)
green=(0.0,1.0,0.0)
blue=(0.0,0.0,1.0)
purple=(1.0,0.0,1.0)
yellow=(1.0,1.0,0.0)
colors=[white,red,teal,amber,green,blue,purple,yellow]

# Initial values
game_over=False
paused=False
exit_game=False
catcher_x=SCREEN_WIDTH/2
catcher_y=20
diamond_x=random.randint(0,SCREEN_WIDTH)
diamond_y=SCREEN_HEIGHT-10
diamonds=[]
falling_diamond=None
current_fall_speed=FALL_SPEED
score=0

catcher_color=white
retry_color=teal
pause_color=amber
exit_color=red


def retryButton(x,y,color=retry_color):
    draw_line(x,y,x+20,y-20,color)
    draw_line(x,y,x+20,y+20,color)
    draw_line(x,y,x+50,y,color)


def pauseButton(x,y,color=pause_color):
    draw_line(x+10,y+20,x+10,y-20,color)
    draw_line(x-10,y+20,x-10,y-20,color)


def playButton(x,y,color=pause_color):
    draw_line(x-10,y+20,x+10,y,color)
    draw_line(x-10,y-20,x+10,y,color)


def exitButton(x,y,color=exit_color):
    draw_line(x-10,y+10,x+10,y-10,color)
    draw_line(x-10,y-10,x+10,y+10,color)


def draw_diamond(x,y,color):
    width=7.5
    height=15

    draw_line(x,y,x-width,y+height,color)
    draw_line(x,y,x+width,y+height,color)
    draw_line(x,y+(2*height),x-width,y+height,color)
    draw_line(x,y+(2*height),x+width,y+height,color)


def draw_catcher():
    x1,x2=catcher_x-CATCHER_WIDTH/2,catcher_x+CATCHER_WIDTH/2
    x3,x4=x1+20,x2-20
    y1,y2=catcher_y,catcher_y-20
    draw_line(x1,y1,x2,y1,catcher_color)
    draw_line(x3,y2,x4,y2,catcher_color)
    draw_line(x2,y1,x4,y2,catcher_color)
    draw_line(x1,y1,x3,y2,catcher_color)


def animate(v):
    global catcher_x,catcher_y,falling_diamond,score,game_over,catcher_color,current_fall_speed,paused

    if not paused and not game_over:
        if not falling_diamond:
            if diamonds:
                falling_diamond=diamonds.pop(0)
        if falling_diamond:
            diamond_x,diamond_y,diamond_color=falling_diamond
            diamond_y -=current_fall_speed
            falling_diamond=(diamond_x,diamond_y,diamond_color)

            if collision(diamond_y,diamond_x,catcher_x):
                handle_collision()

            elif diamond_y<0:
                game_over=True
                falling_diamond=None
                catcher_color=red
                current_fall_speed=FALL_SPEED
                print(f'Game Over!!! Score: {score}')

    if exit_game:
        glutLeaveMainLoop()

    glutPostRedisplay()
    glutTimerFunc(10,animate,0)


def draw_line(x1, y1, x2, y2, color):
    glColor(color)
    glBegin(GL_POINTS)

    dx = x2 - x1
    dy = y2 - y1
    sx = 1 if dx > 0 else -1
    sy = 1 if dy > 0 else -1

    dx = abs(dx)
    dy = abs(dy)

    if dx > dy:
        d = dy - (dx // 2)
        while x1 != x2:
            glVertex2f(x1, y1)
            if d >= 0:
                y1 += sy
                d -= dx
            x1 += sx
            d += dy
            if abs(x1 - x2) <= 1 and abs(y1 - y2) <= 1:
                break
        glVertex2f(x1, y1)
    else:  # Slope > 1
        d = dx - (dy // 2)
        while y1 != y2:
            glVertex2f(x1, y1)
            if d >= 0:
                x1 += sx
                d -= dy
            y1 += sy
            d += dx
            if abs(x1 - x2) <= 1 and abs(y1 - y2) <= 1:
                break
        glVertex2f(x1, y1)

    glEnd()




def display():
    glClear(GL_COLOR_BUFFER_BIT)
    draw_catcher()

    if falling_diamond:
        x,y,color=falling_diamond
        draw_diamond(x,y,color)
    retryButton(RETRY_BUTTON_LOCATION[0],RETRY_BUTTON_LOCATION[1])
    exitButton(EXIT_BUTTON_LOCATION[0],EXIT_BUTTON_LOCATION[1])
    if paused:
        playButton(PAUSE_BUTTON_LOCATION[0],PAUSE_BUTTON_LOCATION[1])
    else:
        pauseButton(PAUSE_BUTTON_LOCATION[0],PAUSE_BUTTON_LOCATION[1])

    glutSwapBuffers()


def handle_mouse(button,state,x,y):
    global paused,exit_game,game_over
    if button==GLUT_LEFT_BUTTON and state==GLUT_DOWN:
        if RETRY_BUTTON_LOCATION[0] <= x <= RETRY_BUTTON_LOCATION[0] + 50 and SCREEN_HEIGHT - y >= RETRY_BUTTON_LOCATION[1] - 20 and SCREEN_HEIGHT - y <= RETRY_BUTTON_LOCATION[1] + 20:
            retry_game()
            print("Game Restarted")
        if EXIT_BUTTON_LOCATION[0] - 20 <= x <= EXIT_BUTTON_LOCATION[0] + 20 and SCREEN_HEIGHT - y >= EXIT_BUTTON_LOCATION[1] - 20 and SCREEN_HEIGHT - y <= EXIT_BUTTON_LOCATION[1] + 20:
            exit_game=True
            print("Exit Game")
        if not game_over:
            if PAUSE_BUTTON_LOCATION[0] - 20 <= x <= PAUSE_BUTTON_LOCATION[0] + 20 and SCREEN_HEIGHT - y >= PAUSE_BUTTON_LOCATION[1] - 20 and SCREEN_HEIGHT - y <= PAUSE_BUTTON_LOCATION[1] + 20:
                paused=not paused
                if paused:
                    print("Game Paused")
                else:
                    print("Game Resumed")
        else:
            print("You cannot press resume or play button when game is over")





def handle_keypress(key,x,y):
    global catcher_x
    if key == b"a" or key == b"A" or key == GLUT_KEY_LEFT:
        catcher_x -=15
    if key == b"d" or key == b"D" or key == GLUT_KEY_RIGHT:
        catcher_x +=15

    if catcher_x < 0:
        catcher_x=0

    if catcher_x > SCREEN_WIDTH:
        catcher_x=SCREEN_WIDTH


def collision(diamond_y,diamond_x,catcher_x):
    return diamond_y <= catcher_y and catcher_x - CATCHER_WIDTH / 2 <= diamond_x <= catcher_x + CATCHER_WIDTH / 2


def handle_collision():
    global score,falling_diamond,current_fall_speed

    score += 1
    current_fall_speed +=0.3
    falling_diamond=None
    print(f'Score: {score}')


def retry_game():
    global diamonds,falling_diamond,game_over,catcher_color,current_fall_speed,paused,score

    diamonds = [(random.randint(0,SCREEN_WIDTH),SCREEN_HEIGHT,random.choice(colors)) for i in range(NUM_DIAMONDS)]
    falling_diamond=None
    game_over=False
    catcher_color=white
    current_fall_speed=FALL_SPEED
    paused=False
    score=0


def init():
    glClearColor(0.0,0.0,0.0,1.0)
    gluOrtho2D(0,SCREEN_WIDTH,0,SCREEN_HEIGHT)
    retry_game()


glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(SCREEN_WIDTH, SCREEN_HEIGHT)
glutCreateWindow(b"Catch the Falling Diamonds")
glutDisplayFunc(display)
glutTimerFunc(10, animate, 0)
glutKeyboardFunc(handle_keypress)
glutSpecialFunc(handle_keypress)
glutMouseFunc(handle_mouse)
init()
glutMainLoop()
