###
#
# Author: Craig Tomkow
# Date: April 16, 2011
#
#Function: This class deals with the screen object
#
###

import pygame
import os
from pygame.locals import *

class screen():
    # Initialize the screen
    def __init__(self):
        os.environ['SDL_VIDEO_CENTERED'] = '1'
	pass

    # Setup the screen, width and height
    def setupScreen(self, width, height):
	self.display = pygame.display.set_mode((width, height))
	return self.display

    # Set the color of the background
    def setColor(self, red, green, blue):
	self.display.fill((red, green, blue))

    # Set a background picture
    def setBackground(self, background):
	self.image = pygame.image.load(background).convert()
	self.display.blit(self.image, (0, 0))
        return self.image

    def drawText(self, text, width, height):
        self.display.blit (text, (width, height))

    def clearText(self, background, width, height):
        backgroundPart = (350, 450, 129, 29)
        self.display.blit (background, (width, height), backgroundPart)

    # Redraw the screen (update it basically)
    def redraw(self):
	pygame.display.flip()
