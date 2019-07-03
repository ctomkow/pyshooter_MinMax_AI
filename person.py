###
#
# Author: Craig Tomkow
# Date: April 16, 2011
#
#Function: This class contains everything relevant to the person Object
#
###

import copy
from pygame.locals import *
import bullet

class person():
    # Initialize the person Object
    def __init__(self, step, width, height, state):
	self.personStep = step
        self.personWidth = width
        self.personHeight = height
        self.personState = state

    # Erase the enemy from the screen
    def clearPerson(self, background, screen):
        backgroundPart = (1, 1, 30, 30)
	screen.blit(background, (self.personWidth, self.personHeight), backgroundPart)
	
    # Draw the person to the screen
    def drawPerson(self, personImage, screen):
	screen.blit(personImage, (self.personWidth, self.personHeight))
	
    # Fire the persons gun
    def fireGun(self, state):
	return bullet.bullet(self.personWidth + 10, self.personHeight + 10, state)

    # Check if the person is dead or not
    def isDead(self, bulletWidth, bulletHeight):
        if ( ((self.personWidth + 10) == bulletWidth) and ((self.personHeight + 10) == bulletHeight) ):
            self.personState = true;

    # Update the person position up
    def moveUp(self, height):
        self.personHeight = self.personHeight - height
        if self.personHeight <= 0:
            self.personHeight = 0

    # Update the person position to the right
    def moveRight(self, width):
        self.personWidth = self.personWidth + width
        if self.personWidth >= 450:
            self.personWidth = 450

    # Update the person position down
    def moveDown(self, height):
        self.personHeight = self.personHeight + height
        if self.personHeight >= 450:
            self.personHeight = 450

    # Update the person postition to the left
    def moveLeft(self, width):
        self.personWidth = self.personWidth - width
        if self.personWidth <= 0:
            self.personWidth = 0

    # Return the x coordinate of the person
    def getWidth(self):
        return self.personWidth

    # Return the y coordinate of the person
    def getHeight(self):
        return self.personHeight

    # Return the state of the person (exists or not)
    def getState(self):
        return self.personState

    # Returns a copy of the person instance
    def copyState(self):
        return copy.deepcopy(self)
