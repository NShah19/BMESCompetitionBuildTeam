#!/usr/bin/env python

from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
from pygame.locals import *
import serial
import numpy as np

ser = serial.Serial('/dev/tty.usbmodem1421', 115200, timeout=1)

ax = ay = az = 0.0
yaw_mode = False

def deg_rad(x):
    return x*(np.pi)/180

def draw_axes():
    glColor3f(1.0,0.0,0.0) # red x
    glBegin(GL_LINES)
    # x aix
 
    glVertex3f(-4.0, 0.0, 0.0);
    glVertex3f(4.0, 0.0, 0.0);
 
    # arrow
    glVertex3f(4.0, 0.0, 0.0);
    glVertex3f(3.0, 1.0, 0.0);
 
    glVertex3f(4.0, 0.0, 0.0);
    glVertex3f(3.0, -1.0, 0.0);
    glEnd();
    glFlush();
 
 
 
    # y 
    glColor3f(0.0,1.0,0.0); # green y
    glBegin(GL_LINES);
    glVertex3f(0.0, -4.0, 0.0);
    glVertex3f(0.0, 4.0, 0.0);
 
    # arrow
    glVertex3f(0.0, 4.0, 0.0);
    glVertex3f(1.0, 3.0, 0.0);
 
    glVertex3f(0.0, 4.0, 0.0);
    glVertex3f(-1.0, 3.0, 0.0);
    glEnd();
    glFlush();
 
    # z 
    glColor3f(0.0,0.0,1.0); # blue z
    glBegin(GL_LINES);
    glVertex3f(0.0, 0.0 ,-4.0 );
    glVertex3f(0.0, 0.0 ,4.0 );
 
    # arrow
    glVertex3f(0.0, 0.0 ,4.0 );
    glVertex3f(0.0, 1.0 ,3.0 );
 
    glVertex3f(0.0, 0.0,4.0 );
    glVertex3f(0.0, -1.0 ,3.0 );
    glEnd();
    glFlush();
    
    
def resize(tuple):
    height = tuple[1]
    width = tuple[0]
    if height==0:
        height=1
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 1.0*width/height, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def init():
    glShadeModel(GL_SMOOTH) #sets the coloring mode to be interpolated over surface
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClearDepth(1.0)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)

def drawText(position, textString):     
    font = pygame.font.SysFont ("Courier", 18, True)
    textSurface = font.render(textString, True, (255,255,255,255), (0,0,0,255))     
    textData = pygame.image.tostring(textSurface, "RGBA", True)     
    glRasterPos3d(*position)     
    glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)

def draw(calibs):
    x1,y1,z1,x2,y2,z2 = np.array([ax,ay,az,bx,by,bz]) - np.array(calibs)
    global rquad
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);	
    draw_axes()
    glLoadIdentity()
    glTranslatef(0,0.0,-7.0)

    osd_text = "pitch: " + str("{0:.2f}".format(y1)) + ", yaw: " + str("{0:.2f}".format(x1))
    osd_line = osd_text + ", roll: " + str("{0:.2f}".format(z1+180))

    drawText((-2,-2, 2), osd_line) #draws the line to show pitch roll and yaw of primary piece
    
    glRotatef(y1  , 1.0, 0.0, 0.0)  # Yaw,   rotate around x-axis
    glRotatef(x1  , 0.0, 1.0, 0.0)    # Pitch, rotate around y-axis
    glRotatef(z1  , 0.0, 0.0, 1.0)    # Roll,  rotate around z-axis

    glBegin(GL_QUADS)	
    glColor3f(1,.6,.6) #salmon side 1A
    glVertex3f( 0.2, 0.2,-0.4)
    glVertex3f(-0.2, 0.2,-0.4)		
    glVertex3f(-0.2, 0.2, 0.4)		
    glVertex3f( 0.2, 0.2, 0.4)		

    glColor3f(.6,1,0.6)	#teal side 2A
    glVertex3f( 0.2,-0.2, 0.4)
    glVertex3f(-0.2,-0.2, 0.4)		
    glVertex3f(-0.2,-0.2,-0.4)		
    glVertex3f( 0.2,-0.2,-0.4)		

    glColor3f(.6,0.6,1.0) #purple side	endcap 1
    glVertex3f( 0.2, 0.2, 0.4) #these points are what we are going to connect our point to.
    glVertex3f(-0.2, 0.2, 0.4)		
    glVertex3f(-0.2,-0.2, 0.4)		
    glVertex3f( 0.2,-0.2, 0.4)		

    glColor3f(1.0,1.0,0.6)	#light blue endcap 2
    glVertex3f( 0.2,-0.2,-0.4)
    glVertex3f(-0.2,-0.2,-0.4)
    glVertex3f(-0.2, 0.2,-0.4)		
    glVertex3f( 0.2, 0.2,-0.4)		

    glColor3f(0.6,1.0,1.0)	#yellow 3A
    glVertex3f(-0.2, 0.2, 0.4)
    glVertex3f(-0.2, 0.2,-0.4)		
    glVertex3f(-0.2,-0.2,-0.4)		
    glVertex3f(-0.2,-0.2, 0.4)		

    glColor3f(1.0,0.6,1.0)	#pink side 4A
    glVertex3f( 0.2, 0.2,-0.4)
    glVertex3f( 0.2, 0.2, 0.4)
    glVertex3f( 0.2,-0.2, 0.4)		
    glVertex3f( 0.2,-0.2,-0.4)
    
    '''
    #SECOND BONE
    glColor3f(1,1,1) #white side endcap3
    glVertex3f( 0.2, 0.2, 1.8)
    glVertex3f(-0.2, 0.2, 1.8)		
    glVertex3f(-0.2,-0.2, 1.8)		
    glVertex3f( 0.2,-0.2, 1.8)	

    glColor3f(1,1,1) #white side endcap 4
    glVertex3f( 0.2, 0.2, 0.5)
    glVertex3f(-0.2, 0.2, 0.5)		
    glVertex3f(-0.2,-0.2, 0.5)		
    glVertex3f( 0.2,-0.2, 0.5)	

    glColor3f(.8,.8,.8) #grey side 1B
    glVertex3f( 0.2, 0.2, 0.5)
    glVertex3f(-0.2, 0.2, 0.5) 	
    glVertex3f(-0.2, 0.2, 1.8)
    glVertex3f( 0.2, 0.2, 1.8)	 

    glColor3f(.1,.8,.8) #grey side 4B
    glVertex3f( 0.2, 0.2, 0.5)
    glVertex3f( 0.2,-0.2, 0.5)		
    glVertex3f( 0.2,-0.2, 1.8) 
    glVertex3f( 0.2, 0.2, 1.8) 

    glColor3f(.1,.8,.8) #grey side 3B
    glVertex3f(-0.2, 0.2, 0.5)
    glVertex3f(-0.2,-0.2, 0.5)		
    glVertex3f(-0.2,-0.2, 1.8) 
    glVertex3f(-0.2, 0.2, 1.8) 
    
    glColor3f(.1,.8,.8) #grey side 2B
    glVertex3f( 0.2,-0.2, 0.5)
    glVertex3f(-0.2,-0.2, 0.5)		
    glVertex3f(-0.2,-0.2, 1.8) 
    glVertex3f( 0.2,-0.2, 1.8) 
    '''
    glEnd()
    x3 = deg_rad(x1-x2); y3 = deg_rad(y1-y2); z3 = deg_rad(z1-z2)
    #print([ax-bx,ay-by,az-bz])
    
    np.set_printoptions(precision=2)
    #if np.abs(y3*180/np.pi) > 5
    #print((x3,y3,z3))
    
    start_point = np.array([0.0,0.0,0.5])
    '''
    z_mat = np.matrix([[ np.cos(x3),-np.sin(x3), 0.0],
                       [ np.sin(x3), np.cos(x3), 0.0],
                       [ 0.0       , 0.0       , 1.0]])
                      
    y_mat = np.matrix([[ np.cos(z3), 0.0, np.sin(z3)],
                       [ 0.0       , 1.0,         0.0],
                       [-np.sin(z3), 0.0, np.cos(z3)]])
                      
    x_mat = np.matrix([[ 1.0,        0.0,        0.0],
                       [ 0.0, np.cos(y3),-np.sin(y3)],
                       [ 0.0, np.sin(y3), np.cos(y3)]])
    col_vect = np.matrix([[0.7],[0.0],[0.0]])
    
    
    #x and y deviation determined by x and y angles we are going to have the calf by .8 long
    vrtx_calf = np.array(z_mat @ y_mat @ x_mat @ col_vect).flatten() + start_point
    '''
    x_coord = .7*np.sin(x3)#*np.cos(y3)
    y_coord = .7*np.sin(y3)
    z_coord = .7*np.cos(x3)*np.cos(y3)
    vrtx_calf = [x_coord,y_coord,z_coord] + start_point

    y3_deg = (180 / np.pi) * y3

    if y3_deg > 10 or y3_deg < -10:
        glBegin(GL_TRIANGLES)
    
        glColor3f(1,0,0)
        glVertex3f( 0.2, 0.2, 0.5)
        glVertex3f( 0.2,-0.2, 0.5)      
        glVertex3f(vrtx_calf[0],vrtx_calf[1], vrtx_calf[2])
        
        glColor3f(1,0,0)
        glVertex3f( 0.2, 0.2, 0.5)
        glVertex3f(-0.2, 0.2, 0.5)      
        glVertex3f(vrtx_calf[0],vrtx_calf[1], vrtx_calf[2])
        
        glColor3f(1,0,0)
        glVertex3f(-0.2, 0.2, 0.5)
        glVertex3f(-0.2,-0.2, 0.5)      
        glVertex3f(vrtx_calf[0],vrtx_calf[1], vrtx_calf[2])
        
        glColor3f(1,0,0)
        glVertex3f( 0.2,-0.2, 0.5)
        glVertex3f(-0.2,-0.2, 0.5)      
        glVertex3f(vrtx_calf[0],vrtx_calf[1], vrtx_calf[2])
        glEnd()

        if y3_deg > 0:
            deviation = y3_deg - 10
        else:
            deviation = y3_deg + 10

        drawText((-1,-1, 1), "Deviation of " + str("{0:.2f}".format(deviation)) + " degrees detected!")

        return
    
    
    else:
        glBegin(GL_TRIANGLES)
        
        glColor3f(1,1,1)
        glVertex3f( 0.2, 0.2, 0.5)
        glVertex3f( 0.2,-0.2, 0.5)		
        glVertex3f(vrtx_calf[0],vrtx_calf[1], vrtx_calf[2])
        
        glColor3f(.4,.4,.4)
        glVertex3f( 0.2, 0.2, 0.5)
        glVertex3f(-0.2, 0.2, 0.5)		
        glVertex3f(vrtx_calf[0],vrtx_calf[1], vrtx_calf[2])
        
        glColor3f(.6,.6, .6)
        glVertex3f(-0.2, 0.2, 0.5)
        glVertex3f(-0.2,-0.2, 0.5)		
        glVertex3f(vrtx_calf[0],vrtx_calf[1], vrtx_calf[2])
        
        glColor3f(.8,.8,.8)
        glVertex3f( 0.2,-0.2, 0.5)
        glVertex3f(-0.2,-0.2, 0.5)		
        glVertex3f(vrtx_calf[0],vrtx_calf[1], vrtx_calf[2])
        glEnd()
    
def normalize_vector(vector):
    length = np.sqrt(vector[0]**2+vector[1]**2+vector[2]**2)
    return (vector[0]/length, vector[1]/length, vector[2]/length)

def read_data():
    global ax, ay, az, bx, by, bz
    ax = ay = az = bx = by = bz = 0.0
    line_done = False

    # request data by sending a dot
    ser.write(".".encode('utf-8'))
    #while not line_done:
    line = ser.readline().decode("utf-8")
    angles = line.split(", ")
    if len(angles) == 6:    
        ax = float(angles[0])
        ay = float(angles[1])
        az = float(angles[2])
        bx = float(angles[3])
        by = float(angles[4])
        bz = float(angles[5])
        line_done = True
    if az < 0:
        az += 360
    if bz < 0:
        bz += 360
    print('Primary sensor XYZ: {}, '.format(ax) + '{}, '.format(ay) + str(az) + 
         ' Secondary sensor XYZ: {}, '.format(bx) + '{}, '.format(by) + str(bz))
         
def calibrate():
    currang = [ 0, 0, 0, 0, 0, 0]
    forang  = [-1,-1,-1,-1,-1,-1]
    ticks = 0
    while sum([currang[i]-forang[i] for i in range(len(forang))]) != 0:
        read_data()
        if ticks % 120:
            forang  = [ax,ay,az,bx,by,bz]
        else:
            currang = [ax,ay,az,bx,by,bz]
        ticks+=1    
    print(currang)
    return currang
    
def main():

    video_flags = OPENGL|DOUBLEBUF
    calibs = calibrate()
    pygame.init()
    screen = pygame.display.set_mode((640,480), video_flags)
    pygame.display.set_caption("Press Esc to quit")
    resize((640,480)) #resizes the dimensions of the ouput screen
    init() #initializes the environment
    frames = 0 #starts the frame counter
    ticks = pygame.time.get_ticks()     #get the amount of ticks the program has run for
    while 1: #run forever unitl quit command is entered
        event = pygame.event.poll()
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            break
        read_data() #this function reads the data incoming serial port
        draw(calibs)#creates the data in order to be output to the screen
        pygame.display.flip() #updates the screen
        frames+=1 #increment the frame counter
        frames = frames%1000 #reset the frame counter every 1000 frames
        #print ("fps:  %d" % ((frames*1000)/(pygame.time.get_ticks()-ticks))) #this prints out the frames
    ser.close() #closes the serial pot after opening it.


if __name__ == '__main__': main()

