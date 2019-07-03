###
#
# Author: Craig Tomkow
# Date: April 16, 2011
#
#Function: This class holds all the relevant information for an instance of
#           a bullet object.
#
###

import copy
import pygame
from pygame.locals import *
pygame.init()

class bullet():
    # Initialize a bullet object
    def __init__(self, Width, Height, state):
	self.posWidth = Width
	self.posHeight = Height
        self.bulletState = state

    # Update the bullet postition
    def update(self, speed):
	self.posHeight = self.posHeight - speed
	if (self.posHeight < 0):
	    self.bulletState = False

    # Erase the bullet from the screen
    def clear(self, background, screen):
        backgroundPart = (10, 10, 10, 10)
	screen.blit(background, (self.posWidth, self.posHeight), backgroundPart)

    # Draw the bullet to the screen
    def draw(self, bulletImage, screen):
	screen.blit(bulletImage, (self.posWidth, self.posHeight))

    # Return the bullets x coordinate
    def getWidth(self):
        return self.posWidth

    # Return the bullets y coordinate
    def getHeight(self):
        return self.posHeight

    # Returns the bullet state (exists or not)
    def getState(self):
        return self.bulletState

    # Copy's the state of the bullet
    def copyState(self):
        return copy.deepcopy(self)