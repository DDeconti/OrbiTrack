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
CELESTIAL_OBJECT = pg.transform.scale(CELESTIAL_OBJECT, (76, 76))

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

DRAW_WEB = True
DRAW_ORBIT = True
DRAW_FILL = False
DRAW_MATRIX = True
DRAW_EQUATION = True
DRAW_PLANET = True


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
    t = 0
    
    #First time math
    controlPoints = [(point[0][0], point[0][1]) for point in POINTS]
    matrix = makeMatrix(controlPoints)
    null_space_coeffiecients = la.null_space(matrix)
    
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


        if refreshMath or firstLoop:
            firstLoop = False
            
            try:
                controlPoints = [(point[0][0], point[0][1]) for point in POINTS]
                matrix = makeMatrix(controlPoints)
                # printMatrix(matrix)
                null_space_coeffiecients = la.null_space(matrix)
                # print(null_space_coeffiecients)
                A, B, C, D, E, F = null_space_coeffiecients
                
                threshold = 0.0000005
                if abs(A) < threshold or abs(B) < threshold or abs(C) < threshold or abs(D) < threshold or abs(E) < threshold or abs(F) < threshold:
                    # print("No Solution")
                    continue
        
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
                
                this_a = np.arctan(1/right)/2
                rot_angle = 90 - (this_a * 180 / math.pi)
                
            except:
                print("Error")
        
        
        if DRAW_ORBIT:
            if A == C:
                #perfect circle 
                drawRotatedEllipse(screen, GRAY, (center_x - semi_major, center_y - semi_major, 2 * semi_major, 2 * semi_major), 0, (center_x, center_y))
            elif A == 0 or C == 0 and (A != 0 or C != 0):
                #parabola
                pass
            elif A / abs(A) == C / abs(C):
                #ellipse
                
                drawRotatedEllipse(screen, BLUE, (0, 0, 2 * semi_minor, 2 * semi_major), rot_angle%360, (center_x, center_y))
            else: 
                #hyperbola
                pass
            
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


        if DRAW_PLANET:
            #planet location math
            #in terms of parametric equations with variable t
            
            #𝑥′=𝑥cos𝛼−𝑦sin𝛼 and 𝑦′=𝑥sin𝛼+𝑦cos𝛼.
            center_x_before_rotation = (semi_major * math.cos(t))
            center_y_before_rotation = (semi_minor * math.sin(t))
            
            planet_center_x = center_x + (center_x_before_rotation * math.cos(this_a)) - (center_y_before_rotation * math.sin(this_a))
            planet_center_y = center_y + (center_x_before_rotation * math.sin(this_a)) + (center_y_before_rotation * math.cos(this_a))
            
            screen.blit(CELESTIAL_OBJECT, (planet_center_x - CELESTIAL_OBJECT.get_width()/2, planet_center_y - CELESTIAL_OBJECT.get_height()/2))
        
            
        
        t += 0.01
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