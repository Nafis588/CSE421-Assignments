#------------------Importing necessary function
from OpenGL.GL import*
from OpenGL.GLUT import*
from OpenGL.GLU import*
import random
import time
import math

#-------------------Screen Setup & Variable declearation
SCREEN_H=800
SCREEN_W=1000
rainDropCount=100
rainPoints=[(random.randint(0,SCREEN_W),random.randint(SCREEN_H,SCREEN_H+200),random.randint(10,20))]
rainVertical='DOWN'
rainSkew=0
rainSpeedHz=5
rainSpeed=[10,rainSpeedHz]
timeInterval=1
lastRainTime=time.time()
lastTimeDay=time.time()
day=True
color=1

#Night to day
def change_time():
    global day
    day=not day

#adjust daylight
def set_day():
    global day,color,lastTimeDay
    change=False
    if day==True:
        if color<1 and time.time() > lastTimeDay+0.01:
            lastTimeDay=time.time()
            color+=0.01
            change= True
    else:
        if color>0 and time.time()>lastTimeDay+0.01:
            lastTimeDay=time.time()
            color-=0.01
            change=True
    if color<0:
        color=0
        change= True

    if change:
        glClearColor(color,color,color,color)
        glutPostRedisplay()

#Shitkey to night
def keyboardListener(key,x,y):
    if key==b'n' and day:
        print('time changed to night')
        change_time()
    if key==b'd' and not day:
        print('time changed to day')
        change_time()


#Wind Factor
def specialKeyListener(key, x,y):
    global rainVertical,rainSkew,day

    if key==GLUT_KEY_LEFT and rainSkew >-50:
        rainSkew -=0.1
        print('Wind from Right to Left')
    if key==GLUT_KEY_RIGHT and rainSkew <50:
        rainSkew +=0.1
        print('Wind from Left to Right')

    glutPostRedisplay()

#House
def drawHouse(start_x,start_y,base,height,roof_height,roof_base, scale=15):
    global color
    glColor3f(0.1,0.5,0.0)
    draw_triangle(start_x,start_y,base=roof_base,height=roof_height,hollow=True,scale=scale,color=color)
    glColor3f(0.1, 0.5, 0.0)

    #main box
    x1,y1=int(start_x-(roof_base/2))+int((roof_base-base)/2),start_y-roof_height
    x2,y2=x1,y1-height
    x3,y3=x2+base,y2
    x4,y4=x3,y1
    draw_box(x1, y1, x2, y2, x3, y3, x4, y4, 5)

    #door & window

    door_height=int(height/2)
    door_width=int(base/5)
    door_x1=int(x1+(base/4)-(door_width/2))
    draw_box(door_x1, y2, door_x1, y2 + door_height, door_x1 + door_width, y2 + door_height, door_x1 + door_width, y2)
    draw_points(door_x1 + door_width - 20, y2 + int(door_height / 2))
    window_height = int(base / 6)
    window_width = int(base / 6)
    window_x1 = int(x3 - (base / 4) - (window_width / 2))
    window_y1 = y2 + door_height + 10
    draw_box(window_x1, window_y1, window_x1, window_y1 + window_height, window_x1 + window_width,window_y1 + window_height, window_x1 + window_width, window_y1)
    draw_line(window_x1 + window_width / 2, window_y1, window_x1 + window_width / 2, window_y1 + window_height, 2)


#adding rain
def addRainPoint():
    global rainDropCount,rainPoints,timeInterval,lastRainTime
    now=time.time()
    if now>lastRainTime+timeInterval and len(rainPoints)<rainDropCount:
        print(len(rainPoints))
        lastRainTime=now
        rainPoints.append((random.randint(0,SCREEN_W),random.randint(SCREEN_H,SCREEN_H+200),random.randint(10,20)))


# check points in triangle
def point_in_triangle(px,py,x1,y1,x2,y2,x3,y3):
    denominator=((y2-y3)*(x1-x3)+(x3-x2)*(y1-y3))
    a=((y2-y3)*(px-x3)+(x3-x2)*(py-y3))/denominator
    b=((y3-y1)*(px-x3)+(x1-x3)*(py-y3))/denominator
    c=1-a-b
    return 0<=a<=1 and 0<=b<=1 and 0<=c<= 1

# check points in rectangle
def point_in_rectangle(px,py,x1,y1,x2,y2,x3,y3,x4,y4):
    min_x=min(x1,x2,x3,x4)
    max_x=max(x1,x2,x3,x4)
    min_y=min(y1,y2,y3,y4)
    max_y=max(y1,y2,y3,y4)
    return min_x<= px <=max_x and min_y<= py <=max_y

def drawRain(x, y, h):
    global rainSkew,SCREEN_W,SCREEN_H
    house_base_x1=(SCREEN_W/2)-250
    house_base_y1=350
    house_base_x2=house_base_x1
    house_base_y2=house_base_y1-200
    house_base_x3=house_base_x1+400
    house_base_y3=house_base_y2
    house_base_x4=house_base_x3
    house_base_y4=house_base_y1

    roof_base_x1=SCREEN_W/2
    roof_base_y1=500
    roof_base_x2=house_base_x1
    roof_base_y2=house_base_y1
    roof_base_x3=house_base_x3
    roof_base_y3=house_base_y1

    if (point_in_rectangle(x, y, house_base_x1, house_base_y1, house_base_x2, house_base_y2, house_base_x3, house_base_y3, house_base_x4, house_base_y4) or
        point_in_triangle(x, y, roof_base_x1, roof_base_y1, roof_base_x2, roof_base_y2, roof_base_x3, roof_base_y3)):
        return

    if rainSkew == 0:
        draw_line(x, y, x, y + h, 1)
    else:
        x2 = int(math.atan(rainSkew) * h)
        draw_line(x, y, x - x2, y + h, 1)



def rain(speed):  # Line 98
    global rainVertical, rainSkew, timeInterval, rainPoints, lastRainTime
    if rainVertical == 'UP':
        speed[0] = -speed[0]
    now = time.time()
    if now > lastRainTime + 0.01 and timeInterval > 0.3:
        timeInterval -= 1
    for i, (x, y, h) in enumerate(rainPoints):
        new_y = y - speed[0]
        if rainSkew != 0:
            new_x = x + speed[1] * (rainSkew / abs(rainSkew))
        else:
            new_x = x
        if rainVertical == 'DOWN' and new_y < 0:
            new_y = SCREEN_H
        elif rainVertical == 'UP' and new_y > SCREEN_H:
            new_y = 0
        if new_x < 0:
            new_x = SCREEN_W
        elif new_x > SCREEN_W:
            new_x = 0

        rainPoints[i] = (new_x, new_y, h)
    glutPostRedisplay()


def draw_points(x, y):
    glPointSize(5)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()

def draw_line(x1, y1, x2, y2, w=5):
    glLineWidth(w)
    glBegin(GL_LINES)
    glVertex2f(x1, y1)
    glVertex2f(x2, y2)
    glEnd()

def draw_box(x1, y1, x2, y2, x3, y3, x4, y4, w=5):
    glLineWidth(w)
    glBegin(GL_LINES)
    glVertex2f(x1, y1)
    glVertex2f(x2, y2)
    glVertex2f(x2, y2)
    glVertex2f(x3, y3)
    glVertex2f(x3, y3)
    glVertex2f(x4, y4)
    glVertex2f(x4, y4)
    glVertex2f(x1, y1)
    glEnd()



def draw_triangle(starting_x, starting_y, base, height, hollow=False, scale=5, color=1.0):
    x1, y1 = starting_x, starting_y
    x2, y2 = int(x1 - (base / 2)), y1 - height
    x3, y3 = int(x1 + (base / 2)), y1 - height

    # Draw the outer triangle
    glBegin(GL_TRIANGLES)
    glVertex2f(x1, y1)  # top vertex
    glVertex2f(x2, y2)  # bottom left vertex
    glVertex2f(x3, y3)  # bottom right vertex
    glEnd()

    if hollow:
        # Draw a smaller, inner triangle to create a hollow effect
        center_y = y1 - int(height / 2)
        scale = 1.2
        base = int(base * (1 / scale))
        height = int(height * (1 / scale))
        y1 = center_y + int(height / 2)
        x2, y2 = int(x1 - (base / 2)), y1 - height
        x3, y3 = int(x1 + (base / 2)), y1 - height

        glColor3f(color, color, color)
        glBegin(GL_TRIANGLES)
        glVertex2f(x1, y1)  # top vertex
        glVertex2f(x2, y2)  # bottom left vertex
        glVertex2f(x3, y3)  # bottom right vertex
        glEnd()

        glColor3f(0.0, 0.0, 0.0)  # Reset color to black for subsequent drawing




def iterate():
    glViewport(0, 0, SCREEN_W, SCREEN_H)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 1000, 0.0, 700, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def showScreen():
    global x, rainSkew, rainDropCount, day
    addRainPoint()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    iterate()
    glColor3f(0.0, 0.0, 0.0)
    glMatrixMode(GL_MODELVIEW)

    glColor3f(0.0, 0.0, 1.0)
    for x, y, h in rainPoints:
        drawRain(x, y, h)
    set_day()
    drawHouse(start_x=SCREEN_W / 2, start_y=500, base=400, height=200, roof_base=500, roof_height=150, scale=10)

    glutSwapBuffers()

def init():
    glClearColor(1, 1, 1, 1)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(504, 1, 1, 1000.0)



def main():
    glutInit()
    glutInitWindowSize(1000, 800)
    glutInitWindowPosition(0, 0)
    glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
    wind = glutCreateWindow(b"Bristy pore?")
    init()
    glutDisplayFunc(showScreen)
    glutSpecialFunc(specialKeyListener)
    glutKeyboardFunc(keyboardListener)
    glutIdleFunc(lambda: rain(rainSpeed))
    glutMainLoop()

if __name__ == '__main__':
    main()

