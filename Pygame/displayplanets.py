#Jack Blair and Daniel DeConti 
#Linear Algebra Final Project
#May 3rd, 2022

#----------------------DESCRIPTION----------------------#
#This program uses linear algebra to calculate the orbit
#of a celestial body given points of observation. The program
#then displays the orbit on a pygame window. The user is able 
#to move the points of observation around and see the orbit change
#in real time.

#Resources: 
#    https://math.stackexchange.com/questions/163920/how-to-find-an-ellipse-given-five-points 
#    hhttps://numpy.org/doc/stable/reference/generated/numpy.linalg.det.html#numpy.linalg.det
#

#----------------------END DESCRIPTION------------------#



import pygame as pg #For graphics
import numpy as np
import math as m
import scipy.linalg as la
from sympy import solve_poly_system
from sympy.solvers.diophantine import diophantine

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
ORANGE = (202, 105, 46) 
BLUE = (50, 50, 200) 
GREEN = (50, 200, 50) 
PURPLE = (100, 32, 117)
RED = (225, 50, 50)
GRAY = (50, 50, 50)

CELESTIAL_OBJECT = pg.image.load('./Pygame/Earth.png')

SCREEN_WIDTH = 1440
SCREEN_HEIGHT = 800
FPS = 60 #Standard Smooth FPS

POINT_RADIUS = 10 #Pixels
POINTS = [
    #(xCoordinate, yCoordinate), currentlyBeingDragged
    ((10, 10), False), 
    ((30, 10), False),
    ((50, 20), False),
    ((20, 40), False),
    ((70, 20), False),
]


def quitSimulation(): #Quits Pygame and Python
    pg.quit()
    quit()
    

def backgroundInputCheck(eventList): #Constantly checks for quits and enters
    for event in eventList:
            if event.type == pg.QUIT:
                quitSimulation()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    quitSimulation()
                    
                ##write control code here
    return True

def pointAlreadyDragging():
    for point in POINTS:
        if point[1]:
            return True


def computeBezierPoints(vertices, numPoints=None):
    if numPoints is None:
        numPoints = 30
    # if numPoints &lt; 2 or len(vertices) != 4:
    #     return None

    result = []

    b0x = vertices[0][0]
    b0y = vertices[0][1]
    b1x = vertices[1][0]
    b1y = vertices[1][1]
    b2x = vertices[2][0]
    b2y = vertices[2][1]
    b3x = vertices[3][0]
    b3y = vertices[3][1]



    # Compute polynomial coefficients from Bezier points
    ax = -b0x + 3 * b1x + -3 * b2x + b3x
    ay = -b0y + 3 * b1y + -3 * b2y + b3y

    bx = 3 * b0x + -6 * b1x + 3 * b2x
    by = 3 * b0y + -6 * b1y + 3 * b2y

    cx = -3 * b0x + 3 * b1x
    cy = -3 * b0y + 3 * b1y

    dx = b0x
    dy = b0y

    # Set up the number of steps and step size
    numSteps = numPoints - 1 # arbitrary choice
    h = 1.0 / numSteps # compute our step size

    # Compute forward differences from Bezier points and "h"
    pointX = dx
    pointY = dy

    firstFDX = ax * (h * h * h) + bx * (h * h) + cx * h
    firstFDY = ay * (h * h * h) + by * (h * h) + cy * h


    secondFDX = 6 * ax * (h * h * h) + 2 * bx * (h * h)
    secondFDY = 6 * ay * (h * h * h) + 2 * by * (h * h)

    thirdFDX = 6 * ax * (h * h * h)
    thirdFDY = 6 * ay * (h * h * h)

    # Compute points at each step
    result.append((int(pointX), int(pointY)))

    for i in range(numSteps):
        pointX += firstFDX
        pointY += firstFDY

        firstFDX += secondFDX
        firstFDY += secondFDY

        secondFDX += thirdFDX
        secondFDY += thirdFDY

        result.append((int(pointX), int(pointY)))

    return result




def makeMatrix(points):
    #x^2, xy, y^2, x, y, 1
    matrix = np.zeros((5, 6))
    for i in range(len(points)):
        x = points[i][0]
        y = points[i][1]
        matrix[i][0] = x*x
        matrix[i][1] = x*y
        matrix[i][2] = y*y
        matrix[i][3] = x
        matrix[i][4] = y
        matrix[i][5] = 1
        
    return matrix

def printMatrix(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            print(int(matrix[i][j]), end = " ")
        print()
    

def simScreen():
    global SCREEN_WIDTH, SCREEN_HEIGHT, FPS, rectangle_draging
    refreshMath = False
    from sympy.abc import x, y
    
    while True:
    
        events = pg.event.get()
        backgroundInputCheck(events)
        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:     
                    for i in range(len(POINTS)):
                        if POINTS[i][0][0] - POINT_RADIUS <= event.pos[0] <= POINTS[i][0][0] + POINT_RADIUS and POINTS[i][0][1] - POINT_RADIUS <= event.pos[1] <= POINTS[i][0][1] + POINT_RADIUS and not pointAlreadyDragging():
                            POINTS[i] = (POINTS[i][0], True)
                            
                            mouse_x, mouse_y = event.pos
                            offset_x = POINTS[i][0][0] - mouse_x
                            offset_y = POINTS[i][0][1] - mouse_y
                            
                            refreshMath = True

            elif event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:            
                    for i in range(len(POINTS)):
                        if POINTS[i][1]:
                            POINTS[i] = (POINTS[i][0], False)
                            refreshMath = False

            elif event.type == pg.MOUSEMOTION:
                for i in range(len(POINTS)):
                    if POINTS[i][1]:
                        mouse_x, mouse_y = event.pos
                        POINTS[i] = ((mouse_x + offset_x, mouse_y + offset_y), POINTS[i][1])
                            
        #Draw on Screen
        screen.fill(BLACK) #Paint the whole screen black
        
        controlPoints = [(point[0][0], point[0][1]) for point in POINTS] + [(POINTS[0][0][0], POINTS[0][0][1])]
        pg.draw.lines(screen, GRAY, False, controlPoints)

        ### Draw bezier curve
        # b_points = computeBezierPoints(controlPoints, 100)
        # pg.draw.lines(screen, BLUE, False, b_points, 2)
        
        controlPoints = [(point[0][0], point[0][1]) for point in POINTS]
        if refreshMath:
            m = makeMatrix(controlPoints)
            printMatrix(m)
            dets = la.null_space(m)
            print(dets)
            
            #Round dets for better display
            dets = [int(det[0]*100000000) for det in dets]
            
            equation = str(dets[0]) + "*x*x + " + str(dets[1]) + "*x*y + " + str(dets[2]) + "*y*y + " + str(dets[3]) + "*x + " + str(dets[4]) + "*y + " + str(dets[5])
            print(equation)
                
            # ans = diophantine(dets[0]*x*x + dets[1]*x*y + dets[1]*y*y + dets[3]*x + dets[4]*y + dets[5])
            ans = diophantine(5*x*x + 2*x*y + 6*y*y + 2*x + 8*y + 1)
            # ans = solve_poly_system([dets[0]*x*x + dets[1]*x*y + dets[1]*y*y + dets[3]*x + dets[4]*y + dets[5], 0], x, y)
            print(ans)
            
            # x = Symbol('x')
            # y = Symbol('y')
            # ans = solve(equation, x, y)
            # print(ans)
        
        
        for i in range(len(POINTS)):
            pg.draw.circle(screen, RED, POINTS[i][0], POINT_RADIUS)
        
        # currentInterval += 1
        backgroundInputCheck(pg.event.get())
        clock.tick(FPS)
        pg.display.flip()
        


#splines for each planet

#draw matrix in bottom left corner

#draw equation


pg.init()
pg.display.set_icon(CELESTIAL_OBJECT)
screen = pg.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pg.display.set_caption("Linear Algebra - OrbitTrack Display")
clock = pg.time.Clock()
simScreen()