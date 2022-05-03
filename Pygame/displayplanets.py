#Jack Blair and Daniel DeConti 
#Linear Algebra Final Project
#May 3rd, 2022

#----------------------DESCRIPTION----------------------#
#This program uses linear algebra to calculate the orbit
#of a celestial body given points of observation. The program
#then displays the orbit on a pygame window. The user is able 
#to move the points of observation around and see the orbit change
#in real time.
#----------------------END DESCRIPTION------------------#

import pygame as pg #For graphics
import numpy as np
import math as m

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


# rectangle = pg.rect.Rect(176, 134, 17, 17)
# rectangle_draging = False


def simScreen():
    global SCREEN_WIDTH, SCREEN_HEIGHT, FPS, rectangle_draging
    
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
                            
                            
                    
                    # if rectangle.collidepoint(event.pos):
                    #     rectangle_draging = True
                    #     mouse_x, mouse_y = event.pos
                    #     offset_x = rectangle.x - mouse_x
                    #     offset_y = rectangle.y - mouse_y

            elif event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:            
                    for i in range(len(POINTS)):
                        if POINTS[i][1]:
                            POINTS[i] = (POINTS[i][0], False)

            elif event.type == pg.MOUSEMOTION:
                for i in range(len(POINTS)):
                    if POINTS[i][1]:
                        mouse_x, mouse_y = event.pos
                        POINTS[i] = ((mouse_x + offset_x, mouse_y + offset_y), POINTS[i][1])
                        # POINTS[i][0] = (mouse_x, mouse_y)
                        # POINTS[i][0] += (offset_x, offset_y)
                    
                # if rectangle_draging:
                #     mouse_x, mouse_y = event.pos
                #     rectangle.x = mouse_x + offset_x
                #     rectangle.y = mouse_y + offset_y
                
                            
        #Draw on Screen
        screen.fill(BLACK) #Paint the whole screen black
        
        for i in range(len(POINTS)):
            pg.draw.circle(screen, RED, POINTS[i][0], POINT_RADIUS)
        
        # currentInterval += 1
        backgroundInputCheck(pg.event.get())
        clock.tick(FPS)
        pg.display.flip()
        

## 1 points - not enough

## 2 points - not enough

## 3 points (must be circle through)

## 




#display 5 planet points
#splines for each planet

#draw matrix in bottom left corner

#draw equation


pg.init()
pg.display.set_icon(CELESTIAL_OBJECT)
screen = pg.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pg.display.set_caption("Linear Algebra - OrbitTrack Display")
clock = pg.time.Clock()
simScreen()