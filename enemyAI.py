###
#
# Author: Craig Tomkow
# Date: April 16, 2011
#
#Function: This class has the minimax algorithm and the associated utility function.
#
###

import random
import copy
import math
import shooter
from pygame.locals import *

class enemyAI():    
    # Constructor to initialize an instance of the minimax algorithm for one iteration
    #   of the main loop
    def enemyAI(self):
        pass

    # This is the utility function to determine the value of a move.  It does not work
    #   perfectly and needs some work still.
    def utilityFunction(self, gameState, aEnemyIndex):

        # Check if the proposed move in the gameState is game over for the person
        if (gameState.checkIfWin(gameState, gameState.enemyList)):
            return 10000

        utility = 0

        ### Since only the valid moves by generateMoves method (i.e. only moves that won't get him killed)
        ###   are supplied then this will work.

        # If difference of enemy & person width is at different intervals, gets different utility
        if ( math.fabs( gameState.enemyList[aEnemyIndex].getWidth() - gameState.personObj.getWidth() ) in range(0, 1) ):
            utility = utility + 987
        elif ( math.fabs( gameState.enemyList[aEnemyIndex].getWidth() - gameState.personObj.getWidth() ) in range(1, 30) ):
            utility = utility + 610
        elif ( math.fabs( gameState.enemyList[aEnemyIndex].getWidth() - gameState.personObj.getWidth() ) in range(30, 60) ):
            utility = utility + 377
        elif ( math.fabs( gameState.enemyList[aEnemyIndex].getWidth() - gameState.personObj.getWidth() ) in range(60, 90) ):
            utility = utility + 233
        elif ( math.fabs( gameState.enemyList[aEnemyIndex].getWidth() - gameState.personObj.getWidth() ) in range(90, 120) ):
            utility = utility + 144
        elif ( math.fabs( gameState.enemyList[aEnemyIndex].getWidth() - gameState.personObj.getWidth() ) in range(120, 150) ):
            utility = utility + 89
        elif ( math.fabs( gameState.enemyList[aEnemyIndex].getWidth() - gameState.personObj.getWidth() ) in range(150, 180) ):
            utility = utility + 55
        elif ( math.fabs( gameState.enemyList[aEnemyIndex].getWidth() - gameState.personObj.getWidth() ) in range(180, 210) ):
            utility = utility + 34
        elif ( math.fabs( gameState.enemyList[aEnemyIndex].getWidth() - gameState.personObj.getWidth() ) in range(210, 240) ):
            utility = utility + 21
        elif ( math.fabs( gameState.enemyList[aEnemyIndex].getWidth() - gameState.personObj.getWidth() ) in range(240, 270) ):
            utility = utility + 13
        elif ( math.fabs( gameState.enemyList[aEnemyIndex].getWidth() - gameState.personObj.getWidth() ) in range(270, 300) ):
            utility = utility + 8
        elif ( math.fabs( gameState.enemyList[aEnemyIndex].getWidth() - gameState.personObj.getWidth() ) in range(300, 330) ):
            utility = utility + 5
        elif ( math.fabs( gameState.enemyList[aEnemyIndex].getWidth() - gameState.personObj.getWidth() ) in range(330, 360) ):
            utility = utility + 3
        elif ( math.fabs( gameState.enemyList[aEnemyIndex].getWidth() - gameState.personObj.getWidth() ) in range(360, 390) ):
            utility = utility + 2
        elif ( math.fabs( gameState.enemyList[aEnemyIndex].getWidth() - gameState.personObj.getWidth() ) in range(390, 420) ):
            utility = utility + 1
        elif ( math.fabs( gameState.enemyList[aEnemyIndex].getWidth() - gameState.personObj.getWidth() ) in range(420, 451) ):
            utility = utility + 1
            
        # Now the height...

        # If difference of enemy & person height is at different intervals, gets different utility
        if ( math.fabs( gameState.enemyList[aEnemyIndex].getHeight() - gameState.personObj.getHeight() ) in range(0, 1) ):
            utility = utility + 987
        elif ( math.fabs( gameState.enemyList[aEnemyIndex].getHeight() - gameState.personObj.getHeight() ) in range(1, 30) ):
            utility = utility + 610
        elif ( math.fabs( gameState.enemyList[aEnemyIndex].getHeight() - gameState.personObj.getHeight() ) in range(30, 60) ):
            utility = utility + 377
        elif ( math.fabs( gameState.enemyList[aEnemyIndex].getHeight() - gameState.personObj.getHeight() ) in range(60, 90) ):
            utility = utility + 233
        elif ( math.fabs( gameState.enemyList[aEnemyIndex].getHeight() - gameState.personObj.getHeight() ) in range(90, 120) ):
            utility = utility + 144
        elif ( math.fabs( gameState.enemyList[aEnemyIndex].getHeight() - gameState.personObj.getHeight() ) in range(120, 150) ):
            utility = utility + 89
        elif ( math.fabs( gameState.enemyList[aEnemyIndex].getHeight() - gameState.personObj.getHeight() ) in range(150, 180) ):
            utility = utility + 55
        elif ( math.fabs( gameState.enemyList[aEnemyIndex].getHeight() - gameState.personObj.getHeight() ) in range(180, 210) ):
            utility = utility + 34
        elif ( math.fabs( gameState.enemyList[aEnemyIndex].getHeight() - gameState.personObj.getHeight() ) in range(210, 240) ):
            utility = utility + 21
        elif ( math.fabs( gameState.enemyList[aEnemyIndex].getHeight() - gameState.personObj.getHeight() ) in range(240, 270) ):
            utility = utility + 13
        elif ( math.fabs( gameState.enemyList[aEnemyIndex].getHeight() - gameState.personObj.getHeight() ) in range(270, 300) ):
            utility = utility + 8
        elif ( math.fabs( gameState.enemyList[aEnemyIndex].getHeight() - gameState.personObj.getHeight() ) in range(300, 330) ):
            utility = utility + 5
        elif ( math.fabs( gameState.enemyList[aEnemyIndex].getHeight() - gameState.personObj.getHeight() ) in range(330, 360) ):
            utility = utility + 3
        elif ( math.fabs( gameState.enemyList[aEnemyIndex].getHeight() - gameState.personObj.getHeight() ) in range(360, 390) ):
            utility = utility + 2
        elif ( math.fabs( gameState.enemyList[aEnemyIndex].getHeight() - gameState.personObj.getHeight() ) in range(390, 420) ):
            utility = utility + 1
        elif ( math.fabs( gameState.enemyList[aEnemyIndex].getHeight() - gameState.personObj.getHeight() ) in range(420, 451) ):
            utility = utility + 1

        return utility

    # This is the recursive loop for the minimax algorithm
    def minimaxValue(self, gameCopy, maxDepth, aEnemy, aEnemyIndex):

        # If end of the recursive descent or if enemy wins then call utilityFunction
        if (maxDepth == 0) or (gameCopy.checkIfWin(gameCopy, gameCopy.enemyList)):
            return self.utilityFunction(gameCopy, aEnemyIndex)

        bestMove = None

        # This tries each move that is legal
        for move in gameCopy.generateMoves(aEnemy):
            gameInstance = copy.copy(gameCopy)

            # Make a move in the future and update the future bullets
            gameInstance.makeMove(move, gameCopy, aEnemyIndex)
            gameInstance.updateFutureBullets(gameCopy)
            gameInstance.aiFrequency = gameInstance.aiFrequency + 1

            # The recursive call
            value = self.minimaxValue(gameInstance, maxDepth - 1, aEnemy, aEnemyIndex)

            # Stores the move with highest utility
            if value > bestMove:
                bestMove = value
        return bestMove

    # This starts off the minimax algorithm and returns the final result
    def miniMax(self, gameCopy, maxDepth, aEnemy, aEnemyIndex):
        # A default move of down is given...it is always overwritten anyway
        bestMove = None
        bestActions = [("down")]

        # This tries each move that is legal
        for move in gameCopy.generateMoves(aEnemy):
            gameInstance = copy.deepcopy(gameCopy)

            # Make a move in the future and update the future bullets
            gameInstance.makeMove(move, gameCopy, aEnemyIndex)
            gameInstance.updateFutureBullets(gameCopy)
            gameInstance.aiFrequency = gameInstance.aiFrequency + 1

            # The recursive call providing a copy of the game instance to
            #   be able to look into the future...
            value = -1 * self.minimaxValue(gameInstance, maxDepth, aEnemy, aEnemyIndex)


            # Update with the best move so far
            if bestMove is None or value > bestMove[0]:
                bestMove = (value, move)
                bestActions[0] = bestMove[1]
            elif value == bestMove[0]:
                bestActions.append(move)

        # Deal with running into a wall/corner that the enemy is beside.
        if (gameCopy.enemyList[aEnemyIndex].getHeight() == 450) and ("down" in bestActions):
            bestActions.remove("down")
        if (gameCopy.enemyList[aEnemyIndex].getHeight() == 0) and ("up" in bestActions):
            bestActions.remove("up")
        if (gameCopy.enemyList[aEnemyIndex].getWidth() == 450) and ("right" in bestActions):
            bestActions.remove("right")
        if (gameCopy.enemyList[aEnemyIndex].getWidth() == 0) and ("left" in bestActions):
            bestActions.remove("left")
        if not bestActions:
            aRandomMove = ("up", "right", "down", "left")
            bestActions.append(random.choice(aRandomMove))

        # If there are more than one move that is valid, then choose one randomly
        return random.choice(bestActions)