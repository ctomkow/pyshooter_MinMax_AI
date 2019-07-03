#!/usr/bin/env python

###
#
# Author: Craig Tomkow
# Date: April 16, 2011
#
#Function: This is the main class of the program.  It contains the main game
#           loop.  As well it contains many helpful methods to enable the ai
#           to function.
#
###

import pygame
from pygame.locals import *

import screen
import person
import enemy
import sys
import copy
import time
import enemyAI


class shooter:
    # Initialize all the things needed for the program
    def __init__(self):
        # These have to stay at 30 so they move to each square properly
        self.personStep = 30
        self.enemyStep = 30
        self.bulletStep = 30

        # Starting positions
        self.personWidth = 210
        self.personHeight = 420
        self.enemyWidth = 210
        self.enemyHeight = 30

        # Some stats
        self.enemyHealth = 10
        self.bulletPower = 10
        self.personScore = 0

        # The speed, lower number is faster (has to do with modulous).
        # Min: 1 (Super fast), Max: 100 (Super slow), Default: 5 / 3
        self.aiSpeed = 5
        self.bulletSpeed = 3

        # The bullet fire rate.  This value is time in seconds (can be float)
        #  between each shot that can be taken.
        self.bulletFireRate = 0.3

        # The current time to calculate the fire rate time
        self.currentBulletFireRate = time.time()

        # (Frequency modulus/% xxxSpeed) to control the speed of bullets
        self.bulletFrequency = 1

        # (Frequency modulus/% xxxSpeed) to control the speed of ai
        self.aiFrequency = 1

        # The max depth that the computer looks down to determine his move
        # Default: 3  -Anything above 4 or 5 and the computer can't handle it.
        self.maxDepth = 1

        # The offset from the person/enemy is to where the bullet is.
        # For collision detection. Do not touch this.
        self.offsetWidth = 10
        self.offsetHeight = 10

        # Enemy List and object initialization
        self.enemyList = []

        # Initialization of bullet list of person
        self.personBulletList = []

        # Object   filename.classname
        self.menuScreenObj = screen.screen()
        self.gameScreenObj = screen.screen()
        self.personObj = person.person(self.personStep, self.personWidth, self.personHeight, True)

        # Start the menu
        self.menu()

    def menu(self):
        # Size of the menu screen
        menuWidth = 300
        menuHeight = 300

        # Initial setup of the menu display
        mainDisplay = self.menuScreenObj.setupScreen(menuWidth, menuHeight)
        self.menuScreenObj.setBackground("data/menu-background.jpg")

        # Initial setup of menu buttons
        titleImage = pygame.image.load("data/title.png").convert()
        instructionsImage = pygame.image.load("data/instructions.jpg").convert()
        survivalImage = pygame.image.load("data/survival.jpg").convert()

        # Display the images for the menu
        mainDisplay.blit(titleImage, (0, 0))
        mainDisplay.blit(instructionsImage, (50, 100))
        mainDisplay.blit(survivalImage, (50, 175))

        while(True):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouseLoc = pygame.mouse.get_pos()

                    # Go to the Instructions screen if clicked
                    if ( (mouseLoc[0] >= 50 and mouseLoc[0] <= 250)
                    and (mouseLoc[1] >= 100 and mouseLoc[1] <= 150) ):
                        self.instructions()

                    # Go to the game if survival image is clicked
                    if ( (mouseLoc[0] >= 50 and mouseLoc[0] <= 250)
                    and (mouseLoc[1] >= 175 and mouseLoc[1] <= 225) ):
                        self.main()
                else:
                  pass

            # Redraw the whole screen at the end of the loop
            self.gameScreenObj.redraw()

    def instructions(self):
        # Size of the instruction screen
        instructionWidth = 300
        instructionHeight = 300

        # Initial setup of the menu display
        self.menuScreenObj.setupScreen(instructionWidth, instructionHeight)
        self.menuScreenObj.setBackground("data/instruction-background.jpg")

        while(True):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.menu()
                else:
                  pass

            # Redraw the whole screen at the end of the loop
            self.gameScreenObj.redraw()

    def main(self):
        # Size of the screen
        width = 480
        height = 480

        # Used to limit the fps
        clock = pygame.time.Clock()

        # Initial setup of display
        mainDisplay = self.gameScreenObj.setupScreen(width, height)
        background = self.gameScreenObj.setBackground("data/background-new.jpg")

        # Initial setup of Character and bullet Images
        personImage = pygame.image.load("data/person.jpg").convert()
        enemyImage = pygame.image.load("data/enemy.jpg").convert()
        bulletImage = pygame.image.load("data/bullet.jpg").convert()

        # Set the font
        font = pygame.font.Font(None, 28)
        fontBig = pygame.font.Font(None, 36)

        # Adding the initial bad guy
        self.addEnemy(self.enemyStep, self.enemyWidth, self.enemyHeight, True, self.enemyHealth)
        
        ###################### Main game loop #############################
        # While the game is not over...
        while(True):
            
            # Make sure the game runs no faster than 30 fps
            clock.tick(30)
            
            # Control the level stages
            self.levelControl()
            
            # ----------------- If game is over then go to the menu ---------------

            if self.personLose(self):
                message = "You lose!  Your point total is: %d" % self.personScore
                text = fontBig.render(message, 1, (255,255,255))
                self.gameScreenObj.drawText(text, 50, 240)
                self.gameScreenObj.redraw()
                time.sleep(4)
                shooter()

            if self.enemyLose(self):
                pass
            
            if (self.personScore == 1700):
                message = "You beat all 6 levels!"
                message2 = "Your point total is: %d" % self.personScore
                text = fontBig.render(message, 1, (255,255,255))
                text2 = fontBig.render(message2, 1, (255, 255, 255))
                self.gameScreenObj.drawText(text, 50, 240)
                self.gameScreenObj.drawText(text2, 50, 275)
                self.gameScreenObj.redraw()
                time.sleep(4)
                shooter()

            # ---------- End checking game end state -----------------------------

            # -------------- Start Erasing of objects -------------------------

            # Erase the person
            self.personObj.clearPerson(background, mainDisplay)
            
            # Erase the enemy(s)
            if self.enemyList:
                for aEnemy in self.enemyList:
                    aEnemy.clearEnemy(background, mainDisplay)

            # Erase bullet of person first
            for i in range(0, len(self.personBulletList)):
                if self.personBulletList[i].getState():
                    self.personBulletList[i].clear(background, mainDisplay)

            # Erase the Points the user currently has
            message = "Points: %d" % self.personScore
            self.gameScreenObj.clearText(background, 350, 450)

            # ------------- End erasing of objects ----------------------

            # ---------------- Start to detect user keystrokes --------------------

            # Detect movement & exit keystrokes
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    shooter()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        shooter()
                    elif event.key == pygame.K_a:
                        self.personObj.moveLeft(self.personStep)
                    elif event.key == pygame.K_w:
                        self.personObj.moveUp(self.personStep)
                    elif event.key == pygame.K_d:
                        self.personObj.moveRight(self.personStep)
                    elif event.key == pygame.K_s:
                        self.personObj.moveDown(self.personStep)
                    elif event.key == pygame.K_SPACE:
                        if ( (time.time() - self.currentBulletFireRate) >= self.bulletFireRate):
                            self.personBulletList.append('bulletObj')
                            self.personBulletList[len(self.personBulletList) - 1] = self.personObj.fireGun(True)
                            self.currentBulletFireRate = time.time()
                    else:
                        pass
                else:
                    pass

            # ------------ End detection of user keystrokes ------------------

            # ------------ Update the bullet of person -----------------------
            # Has to do with limiting bullet speed
            if (self.personBulletList and ((self.bulletFrequency % self.bulletSpeed) == 0)):
                for i in range(0, len(self.personBulletList)):
                    if self.personBulletList[i].getState():
                        self.personBulletList[i].update(self.bulletStep)

            # ------------ End update of bullet of the person ----------------

            # ----------- Start enemy AI... (includes updating enemy) ------------
            # I have noticed that the enemy has a big flaw, he has slow reflexes when
            #   you are very close.  He has trouble dodging bullets that you fire
            #   at close range...which actually adds an element of realism

            # Has to do with limiting the speed of the ai
            if (self.enemyList and ( (self.aiFrequency % self.aiSpeed) == 0 ) ):

                enemyAIObj = enemyAI.enemyAI()

                # Need to copy the state of each class so I don't change the acutal values
                shooterCopy = copy.deepcopy(self)

                # Returns the best move as a single value (move)
                for aEnemy in self.enemyList:
                    aEnemyIndex = self.enemyList.index(aEnemy)
                    bestMove = enemyAIObj.miniMax(shooterCopy, self.maxDepth, aEnemy, aEnemyIndex)

                    # Make the move based upon the decision made by minimax
                    if bestMove == "up":
                        aEnemy.moveUp(self.enemyStep)
                    if bestMove == "right":
                        aEnemy.moveRight(self.enemyStep)
                    if bestMove == "down":
                        aEnemy.moveDown(self.enemyStep)
                    if bestMove == "left":
                        aEnemy.moveLeft(self.enemyStep)

            # ---------------- End enemy AI... ----------------------------------

            # ------------ Check if enemy is dead -----------------------------
            # This is done before the drawing of the objects because if an
            # enemy is dead then we don't want to draw him.

            # Check if enemy is hit or dead
            self.isEnemyHit()
            self.isEnemyDead()

            # Kill off the enemy
            if self.enemyList:
                for aEnemy in self.enemyList:
                    if not aEnemy.getState():
                        aEnemy.clearEnemy(background, mainDisplay)
                        self.enemyList.remove(aEnemy)

            # ------------------ End of check if enemy is dead -----------------

            # ------------ Start the Draw of Objects --------------------

            # Draw bullets of person / Has to do with limiting the bullet speed
            #if (self.personBulletList and ((self.bulletFrequency % self.bulletFireRate) == 0)):
            for i in range(0, len(self.personBulletList)):
                if self.personBulletList[i].getState():
                    self.personBulletList[i].draw(bulletImage, mainDisplay)

            # Remove the last bullet object from List if it is off the screen
            if self.personBulletList:
                if not self.personBulletList[(len(self.personBulletList) - 1)].getState():
                    self.personBulletList.remove(self.personBulletList[(len(self.personBulletList) - 1)])

            # Draw the person
            self.personObj.drawPerson(personImage, mainDisplay)
            # Draw the enemy
            if self.enemyList:
                for aEnemy in self.enemyList:
                    aEnemy.drawEnemy(enemyImage, mainDisplay)

            # Draw the Points the user currently has
            message = "Points: %d" % self.personScore
            text = font.render(message, 1, (255,255,255))
            self.gameScreenObj.drawText(text, 350, 450)

            # -------------- End update and draw of objects -------------------


            # To prevent the count from going way up and then causing delays in the modulus calculation
            # Increase bulletFrequency by 1
            self.bulletFrequency = self.bulletFrequency + 1
            if self.bulletFrequency > 100:
                self.bulletFrequency = 1

            self.aiFrequency = self.aiFrequency + 1
            if self.aiFrequency > 100:
                self.aiFrequency = 1

            # Redraw the whole screen at the end of the loop
            # This is to make sure all the blits show up.
            # Therefore we only need one screen redraw, because everything else is blitted.
            self.gameScreenObj.redraw()

        ##################### End Main game loop ###########################

    #####################################################################
    # PLEASE CLEANUP FROM HERE AND BELOW.....TIGHT COUPLING PLEASE!!!!! #
    #####################################################################

    # Add another enemy
    def addEnemy(self, enemyStep, enemyWidth, enemyHeight, state, enemyHealth):
        self.enemyList.append("enemyObj")
        self.enemyList[len(self.enemyList) - 1] = enemy.enemy(enemyStep, enemyWidth, enemyHeight, state, enemyHealth)

    # Determines the level and what happens at each.
    def levelControl(self):
        if self.personScore == 100 and not self.enemyList:
            time.sleep(2)
            self.aiSpeed = 4
            self.addEnemy(self.enemyStep, self.enemyWidth - 60, self.enemyHeight, True, self.enemyHealth)
        elif self.personScore == 200 and not self.enemyList:
            time.sleep(2)
            self.addEnemy(self.enemyStep, self.enemyWidth - 60, self.enemyHeight, True, self.enemyHealth + 10)
            self.addEnemy(self.enemyStep, self.enemyWidth + 60, self.enemyHeight, True, self.enemyHealth + 10)
        elif self.personScore == 400 and not self.enemyList:
            time.sleep(2)
            self.aiSpeed = 3
            self.bulletSpeed = 2
            self.addEnemy(self.enemyStep, self.enemyWidth - 60, self.enemyHeight, True, self.enemyHealth + 20)
            self.addEnemy(self.enemyStep, self.enemyWidth, self.enemyHeight, True, self.enemyHealth + 20)
            self.addEnemy(self.enemyStep, self.enemyWidth + 60, self.enemyHeight, True, self.enemyHealth + 20)
        elif self.personScore == 700 and not self.enemyList:
            time.sleep(2)
            self.aiSpeed = 3
            self.bulletFireRate = 0.2
            self.bulletSpeed = 2
            self.addEnemy(self.enemyStep, self.enemyWidth - 60, self.enemyHeight, True, self.enemyHealth + 30)
            self.addEnemy(self.enemyStep, self.enemyWidth - 30, self.enemyHeight, True, self.enemyHealth + 30)
            self.addEnemy(self.enemyStep, self.enemyWidth, self.enemyHeight, True, self.enemyHealth + 30)
            self.addEnemy(self.enemyStep, self.enemyWidth + 60, self.enemyHeight, True, self.enemyHealth + 30)
        elif self.personScore == 1100 and not self.enemyList:
            self.bulletSpeed = 1
            self.addEnemy(self.enemyStep, self.enemyWidth - 60, self.enemyHeight, True, self.enemyHealth + 40)
            self.addEnemy(self.enemyStep, self.enemyWidth - 30, self.enemyHeight, True, self.enemyHealth + 40)
            self.addEnemy(self.enemyStep, self.enemyWidth, self.enemyHeight, True, self.enemyHealth + 40)
            self.addEnemy(self.enemyStep, self.enemyWidth + 30, self.enemyHeight, True, self.enemyHealth + 40)
            self.addEnemy(self.enemyStep, self.enemyWidth + 60, self.enemyHeight, True, self.enemyHealth + 40)
            self.addEnemy(self.enemyStep, self.enemyWidth + 90, self.enemyHeight, True, self.enemyHealth + 40)
            

    # This checks to see if the person lost, if so then the game ends
    # It is a static method so it does not receive the self automatically,
    #   you have to provide the game instance
    @staticmethod
    def personLose(gameState):
        enemyList = gameState.enemyList

        # If enemy exists
        if enemyList:
            for aEnemy in enemyList:
                enemyWidth = aEnemy.getWidth()
                enemyHeight = aEnemy.getHeight()
                personWidth = gameState.personObj.getWidth()
                personHeight = gameState.personObj.getHeight()

                if (enemyWidth == personWidth):
                    if (enemyHeight == personHeight):
                        return True
        return False

    # This checks to see if the enemy lost, if so then the game ends
    # It is a static method so it does not receive the self automatically,
    #   you have to provide the game instance
    @staticmethod
    def enemyLose(gameState):
        # If enemyList is empty (all enemies are dead)
        #if not gameState.enemyList:
        #    print "YOU WIN!!! YAY  :)"
        #    print "You killed all the bad guys"
        #    return True
        return False

    # This checks to see if there is a win state, this is only for the utility
    #   funtion.
    # It is a static method so it does not receive the self automatically,
    #   you have to provide the game instance
    @staticmethod
    def checkIfWin(gameState, enemyList):
        # If enemy exists
        if enemyList:
            for i in range(len(gameState.enemyList)):
                enemyWidth = gameState.enemyList[i].getWidth()
                enemyHeight = gameState.enemyList[i].getHeight()
                personWidth = gameState.personObj.getWidth()
                personHeight = gameState.personObj.getHeight()
                if (enemyWidth == personWidth):
                    if (enemyHeight == personHeight):
                        return True
        return False


    # Check if enemy is Dead, if so, remove enemy from the list
    def isEnemyDead(self):
        for aEnemy in self.enemyList:
            aEnemy.isDead()
            if aEnemy.getState() == False:
                self.enemyList.remove(aEnemy)
                self.personScore = self.personScore + 100

    # Check if enemy got hit
    def isEnemyHit(self):
        if (self.personBulletList and self.enemyList):
            for aEnemy in self.enemyList:
                for i in range(0, len(self.personBulletList)):
                    if aEnemy.isHit(self.personBulletList[i].getWidth(), self.personBulletList[i].getHeight()):
                        aEnemy.updateHealth(self.bulletPower)
                    if not aEnemy.getState():
                        break;

    # This generates all the possible valid moves in a list.  Each move is a string.
    #   A valid move is one that does not put the enemy in harms way (e.g. running into a bullet)
    def generateMoves(self, aEnemy):
        moves = []
        moveBad = False

        # Check if up is a valid move.
        for i in range(0, len(self.personBulletList)):
            if ( ((aEnemy.getWidth() + self.offsetWidth) == self.personBulletList[i].getWidth()) and
                 ((aEnemy.getHeight() - self.enemyStep + self.offsetHeight) == self.personBulletList[i].getHeight()) ):
                moveBad = True

        if not moveBad:
            moves.append("up")
        moveBad = False

        # Check if right is a valid move.
        for j in range(0, len(self.personBulletList)):
            if ( ((aEnemy.getWidth() + self.enemyStep + self.offsetWidth) == self.personBulletList[j].getWidth()) and
                 ((aEnemy.getHeight() + self.offsetHeight) == self.personBulletList[j].getHeight()) ):
                moveBad = True

        if not moveBad:
            moves.append("right")
        moveBad = False

        # Check if down is a valid move.
        for k in range(0, len(self.personBulletList)):
            if ( ((aEnemy.getWidth() + self.offsetWidth) == self.personBulletList[k].getWidth()) and
                 ((aEnemy.getHeight() + self.enemyStep + self.offsetHeight) == self.personBulletList[k].getHeight()) ):
                moveBad = True

        if not moveBad:
            moves.append("down")
        moveBad = False

        # Check if left is a valid move.
        for l in range(0, len(self.personBulletList)):
            if ( ((aEnemy.getWidth() - self.enemyStep + self.offsetWidth) == self.personBulletList[l].getWidth()) and
                 ((aEnemy.getHeight() + self.offsetHeight) == self.personBulletList[l].getHeight()) ):
                moveBad = True

        if not moveBad:
            moves.append("left")
        moveBad = False

        return moves

    # This makes a move for the enemy determined by the given move
    def makeMove(self, move, gameState, aEnemyIndex):

        if move == "up":
            gameState.enemyList[aEnemyIndex].moveUp(self.enemyStep)
            return enemy.copyState(enemy)
        elif move == "right":
            gameState.enemyList[aEnemyIndex].moveRight(self.enemyStep)
            return enemy.copyState(enemy)
        elif move == "down":
            gameState.enemyList[aEnemyIndex].moveDown(self.enemyStep)
            return enemy.copyState(enemy)
        elif move == "left":
            gameState.enemyList[aEnemyIndex].moveLeft(self.enemyStep)
            return enemy.copyState(enemy)
        else:
            return enemy.copyState(enemy)
    
    def updateFutureBullets(self, gameState):
        if (gameState.personBulletList and ((gameState.bulletFrequency % gameState.bulletSpeed) == 0) ):
                for i in range(0, len(gameState.personBulletList)):
                    if gameState.personBulletList[i].getState():
                        gameState.personBulletList[i].update(gameState.bulletStep)

# Start the game
if __name__ == "__main__":
    shooter()
