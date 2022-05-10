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
#    https://numpy.org/doc/stable/reference/generated/numpy.linalg.det.html#numpy.linalg.det
#    https://en.wikipedia.org/wiki/Matrix_representation_of_conic_sections#Central_conics

#----------------------END DESCRIPTION------------------#


from cmath import pi
from pickle import TRUE
import pygame as pg #For graphics
import pygame.freetype  # Import the freetype module.
import numpy as np
import math
import scipy.linalg as la

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
    ((785, 232), False), 
    ((368, 131), False),
    ((198, 324), False),
    ((508, 581), False),
    ((1075, 630), False),
]

# POINTS = [
#     #(xCoordinate, yCoordinate), currentlyBeingDragged
#     ((-100, 100), False), 
#     ((0, 100), False),
#     ((100, 0), False),
#     ((0, -100), False),
#     ((-100, 0), False),
# ]

DRAW_WEB = True
DRAW_BEIZER = False
DRAW_ELLIPSE = True
DRAW_FILL = False
DRAW_MATRIX = True
DRAW_EQUATION = True


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
    

def drawRotatedEllipse(surface, color, rect, angle, center, width=0):
    target_rect = pygame.Rect(rect)
    shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
    pygame.draw.ellipse(shape_surf, color, (0, 0, *target_rect.size), width=1)
    rotated_surf = pygame.transform.rotate(shape_surf, angle)
    surface.blit(rotated_surf, rotated_surf.get_rect(center = center))


def simScreen():
    global SCREEN_WIDTH, SCREEN_HEIGHT, FPS, rectangle_draging
    refreshMath = False
    
    #First time math
    controlPoints = [(point[0][0], point[0][1]) for point in POINTS]
    matrix = makeMatrix(controlPoints)
    null_space_coeffiecients = la.null_space(matrix)
    
    a = 0
    b = 0
    rot_angle = 0
    h = 0
    k = 0

    firstLoop = True
    
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
        
        if DRAW_WEB:
            controlPoints = [(point[0][0], point[0][1]) for point in POINTS] + [(POINTS[0][0][0], POINTS[0][0][1])]
            pg.draw.lines(screen, GRAY, False, controlPoints)

        if DRAW_BEIZER:
            b_points = computeBezierPoints(controlPoints, 100)
            pg.draw.lines(screen, BLUE, False, b_points, 2)
        
        
        if refreshMath or firstLoop:
            firstLoop = False
            controlPoints = [(point[0][0], point[0][1]) for point in POINTS]
            matrix = makeMatrix(controlPoints)
            printMatrix(matrix)
            null_space_coeffiecients = la.null_space(matrix)
            print(null_space_coeffiecients)
            A, B, C, D, E, F = null_space_coeffiecients
        
            #Daniel
            #code the equations
            try:
                determinant = (B**2) - 4 * A * C
                center_x = (((2 * C * D) - (B * E)) / determinant)[0]
                center_y = (((2 * A * E) - (B * D)) / determinant)[0]
                
                
                comp_1 = (2 * ((A * E**2) + (C * D**2) - (B * D * E) + determinant * F))[0]
                comp_2 = ((A + C) + math.sqrt((A - C)**2 + B**2))[0]
                comp_3 = ((A + C) - math.sqrt((A - C)**2 + B**2))[0]
                dims = [(-math.sqrt(comp_1 * comp_2) / determinant)[0], (-math.sqrt(comp_1 * comp_3) / determinant)[0]]
                semi_major = max(dims)
                semi_minor = min(dims)
                
                
                #cot(2𝛼)=(𝐴−𝐶/𝐵)
                right = (A-C) / B
                #cot(2a)=(𝐴−𝐶/𝐵)
                
                
                this_a = np.arctan(1/right)/2
                print(this_a)
                rot_angle = 90 - (this_a * 180 / math.pi)
                
                # if B != 0:
                #     rot_angle = math.atan((C[0] - A[0] - math.sqrt((A[0] - C[0])**2 + B[0]**2) / B[0]))
                #     rot_angle = rot_angle * 180 / math.pi
                # elif A > C:
                #     rot_angle = 90
                # else:
                #     rot_angle = 0
                    
                    
            except:
                print("Error")
            
        
        if DRAW_ELLIPSE:
            drawRotatedEllipse(screen, BLUE, (0, 0, 2 * semi_minor, 2 * semi_major), rot_angle, (center_x, center_y))
            
            #also draw the center
            # pg.draw.circle(screen, RED, (int(center_x), int(center_y)), 5)
        
            
        if DRAW_FILL:
            coeffiecients = [int(det*100000000) for det in null_space_coeffiecients]
            for num_x in range(0, SCREEN_WIDTH, 10):
                for num_y in range(0, SCREEN_HEIGHT, 10):
                    if coeffiecients[0]*num_x*num_x + coeffiecients[1]*num_x*num_y + coeffiecients[2]*num_y*num_y + coeffiecients[3]*num_x + coeffiecients[4]*num_y + coeffiecients[5] < 100:
                        pg.draw.circle(screen, RED, (num_x, num_y), 1)
            
        if DRAW_MATRIX:
            y = SCREEN_HEIGHT - 150
            for item in matrix:
                x = 40
                for num in item:
                    SIM_FONT.render_to(screen, (x, y), str(int(num)), WHITE)
                    x += 80
                y += 30
                
        if DRAW_EQUATION:
            DISP_A, DISP_B, DISP_C, DISP_D, DISP_E, DISP_F = null_space_coeffiecients
            
            #format the decimals of A, B, C, D, E, F to be to 3 decimal places
            ammount_round = 5
            DISP_A = round(DISP_A[0], ammount_round)
            DISP_B = round(DISP_B[0], ammount_round)
            DISP_C = round(DISP_C[0], ammount_round)
            DISP_D = round(DISP_D[0], ammount_round)
            DISP_E = round(DISP_E[0], ammount_round)
            DISP_F = round(DISP_F[0], ammount_round)
            
            equation = str(DISP_A) + "*x*x + " + str(DISP_B) + "*x*y + " + str(DISP_C) + "*y*y + " + str(DISP_D) + "*x + " + str(DISP_E) + "*y + " + str(DISP_F)
            SIM_FONT.render_to(screen, (40, 15), equation, WHITE)
        
        
        for i in range(len(POINTS)):
            if POINTS[i][1]: #currently being dragged
                pg.draw.circle(screen, PURPLE, POINTS[i][0], POINT_RADIUS)
            else:
                pg.draw.circle(screen, RED, POINTS[i][0], POINT_RADIUS)
                
                

                        
        
        # currentInterval += 1
        backgroundInputCheck(pg.event.get())
        clock.tick(FPS)
        pg.display.flip()
        

pg.init()
pg.display.set_icon(CELESTIAL_OBJECT)
screen = pg.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pg.display.set_caption("Linear Algebra - OrbitTrack Display")
clock = pg.time.Clock()

SIM_FONT = pygame.freetype.Font("./Pygame/Avenir Next.ttc", 16)

simScreen()