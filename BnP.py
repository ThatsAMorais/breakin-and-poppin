#####	   File : BnP.py
####	 Author : Alex Morais
### Description	: The script that runs the game and instantiates the
###		    game engine object.
##

import os, sys, socket
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from engine.GameEngine import *


if __name__ == '__main__':

    engine = GameEngine()

    while True:
	glutMainLoop()
	

