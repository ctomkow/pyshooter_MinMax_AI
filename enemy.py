###
#
# Author: Craig Tomkow
# Date: April 16, 2011
#
#Function: This class holds all the information for an instance of an enemy object.
#
###

import copy
from pygame.locals import *
import bullet

class enemy():
    enemyStep = 0
    enemyWidth = 0
    enemyHeight = 0
    enemyState = 0
    enemyHealth = 0

    # Initialize an enemy object.
    def __init__(self, step, width, height, state, health):
        self.enemyStep = step
        self.enemyWidth = width
        self.enemyHeight = height
        self.enemyState = state
        self.enemyHealth = health

    # Erase the enemy from the screen
    def clearEnemy(self, background, screen):
        backgroundPart = (1, 1, 30, 30)
	screen.blit(background, (self.enemyWidth, self.enemyHeight), backgroundPart)

    # Draw the enemy to the screen
    def drawEnemy(self, enemyImage, screen):
	screen.blit(enemyImage, (self.enemyWidth, self.enemyHeight))

    # Fire the enemies gun (Not implemented...)
    def fireGun(self, bulletImage):
	return bullet.bullet(bulletImage, self.enemyWidth, self.enemyHeight)

    def isHit(self, bulletWidth, bulletHeight):
        if ( ((self.enemyWidth + 10) == bulletWidth) and ((self.enemyHeight + 10) == bulletHeight) ):
            return True

    # Check if enemy is dead
    def isDead(self):
        if self.enemyHealth <= 0:
            self.enemyState = False

    def updateHealth(self, change):
        self.enemyHealth = self.enemyHealth - change

    def getHealth(self):
        return self.enemyHealth

    # Update the enemy up
    def moveUp(self, height):
        self.enemyHeight = self.enemyHeight - height
        if self.enemyHeight <= 0:
            self.enemyHeight = 0  

    # Update the enemy to the right
    def moveRight(self, width):
        self.enemyWidth = self.enemyWidth + width
        if self.enemyWidth >= 450:
            self.enemyWidth = 450

    # Update the enemy down
    def moveDown(self, height):
        self.enemyHeight = self.enemyHeight + height
        if self.enemyHeight >= 450:
            self.enemyHeight = 450    
    
    # Update the enemy to the left
    def moveLeft(self, width):
        self.enemyWidth = self.enemyWidth - width
        if self.enemyWidth <= 0:
            self.enemyWidth = 0 
        
    # Return the x coordinate of the enemy
    def getWidth(self):
        return self.enemyWidth

    # Return the y coordinate of the enemy
    def getHeight(self):
        return self.enemyHeight

    # Return the state of the enemy ( exists or not)
    def getState(self):
        return self.enemyState

# Return a copy of the enemy Instance
def copyState(self):
    return copy.deepcopy(enemy)
