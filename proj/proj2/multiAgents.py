# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"
        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        
        "*** YOUR CODE HERE ***"
        score = successorGameState.getScore()
        # Avoid ghosts: heavily penalize positions close to ghosts unless they are scared
        for ghostState in newGhostStates:
            ghostPos = ghostState.getPosition()
            distanceToGhost = manhattanDistance(newPos, ghostPos)
            if ghostState.scaredTimer > 0:
                # Encourage chasing scared ghosts
                score += max(10 - distanceToGhost, 0)
            else:
                # Penalize being close to active ghosts
                if distanceToGhost < 2:
                    score -= 100

        # Prioritize eating food: incentivize positions closer to food
        foodList = newFood.asList()
        if foodList:
            closestFoodDistance = min([manhattanDistance(newPos, food) for food in foodList])
            score += 10 / closestFoodDistance

        # Avoid stopping unless necessary
        if action == Directions.STOP:
            score -= 10

        return score
        #return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState: GameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        bestScore, bestAction = self.minimax(gameState, 0, 0, 0)
        return bestAction

    def minimax(self, gameState, depth, agentIndex, movedTimes):
        #check if the state is win/lose or reach maxDepth
        #print("agentIndex:", agentIndex)
        #print("depth:", depth)
        #print("movedTimes: ", movedTimes)
        if depth == self.depth and movedTimes % gameState.getNumAgents() == 0:
            return self.evaluationFunction(gameState), None
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState), None
        
    
        if agentIndex:
            return self.minValue(gameState, depth, agentIndex, movedTimes)
        else:
            return self.maxValue(gameState, depth, agentIndex, movedTimes)
        

    def maxValue(self, gameState, depth, agentIndex, movedTimes):
        maxScore = float('-inf')
        maxAction = None
        
        movedTimes += 1
        nextAgent = (agentIndex + 1) % gameState.getNumAgents()
        nextDepth = depth 
        if movedTimes % gameState.getNumAgents() == 0:
            nextDepth += 1

        for action in gameState.getLegalActions(agentIndex):
            successor = gameState.generateSuccessor(agentIndex, action)
            
            score, _ = self.minimax(successor, nextDepth, nextAgent, movedTimes)
            if score > maxScore:
                maxScore = score
                maxAction = action
        return maxScore, maxAction        
        

    def minValue(self, gameState, depth, agentIndex, movedTimes):
        minScore = float('inf')
        minAction = None

        movedTimes += 1
        nextAgent = (agentIndex + 1) % gameState.getNumAgents()
        nextDepth = depth 
        if movedTimes % gameState.getNumAgents() == 0:
            nextDepth += 1

        for action in gameState.getLegalActions(agentIndex):
            successor = gameState.generateSuccessor(agentIndex, action)
            
            score, _ = self.minimax(successor, nextDepth, nextAgent, movedTimes)
            if score < minScore:
                minScore = score
                minAction = action
        return minScore, minAction 
    

            

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        alpha = float('-inf') 
        beta = float('inf') 
        bestScore, bestAction = self.minimax(gameState, 0, 0, 0, alpha, beta)
        return bestAction

    def minimax(self, gameState, depth, agentIndex, movedTimes, alpha, beta):
        #check if the state is win/lose or reach maxDepth
        #print("Using minimax function...")
        #print("alpha: ", alpha)
        #print("beta: ", beta)
        
        if depth == self.depth and movedTimes % gameState.getNumAgents() == 0:
            eval = self.evaluationFunction(gameState)
            #print("evaluated to: ", eval)
            return eval, None
        if gameState.isWin() or gameState.isLose():
            eval = self.evaluationFunction(gameState)
            #print("evaluated to: ", eval)
            return eval, None
        
    
        if agentIndex:
            return self.minValue(gameState, depth, agentIndex, movedTimes, alpha, beta)
        else:
            return self.maxValue(gameState, depth, agentIndex, movedTimes, alpha, beta)
        

    def maxValue(self, gameState, depth, agentIndex, movedTimes, alpha, beta):
        #print("Using maxValue function...")
        #print("alpha: ", alpha)
        #print("beta: ", beta)
        maxScore = float('-inf')
        maxAction = None
        
        movedTimes += 1
        nextAgent = (agentIndex + 1) % gameState.getNumAgents()
        nextDepth = depth 
        if movedTimes % gameState.getNumAgents() == 0:
            nextDepth += 1

        for action in gameState.getLegalActions(agentIndex):
            successor = gameState.generateSuccessor(agentIndex, action)
            
            score, _ = self.minimax(successor, nextDepth, nextAgent, movedTimes, alpha, beta)
            if score > maxScore:
                maxScore = score
                maxAction = action
            if maxScore > beta:
                #print("Break because of beta pruning...")
                break
            alpha = max(alpha, maxScore)
        return maxScore, maxAction        
        

    def minValue(self, gameState, depth, agentIndex, movedTimes, alpha, beta):
        #print("Using minValue function...")
        #print("alpha: ", alpha)
        #print("beta: ", beta)
        minScore = float('inf')
        minAction = None

        movedTimes += 1
        nextAgent = (agentIndex + 1) % gameState.getNumAgents()
        nextDepth = depth 
        if movedTimes % gameState.getNumAgents() == 0:
            nextDepth += 1



        for action in gameState.getLegalActions(agentIndex):
            successor = gameState.generateSuccessor(agentIndex, action)
            
            score, _ = self.minimax(successor, nextDepth, nextAgent, movedTimes, alpha, beta)
            if score < minScore:
                minScore = score
                minAction = action
            if minScore < alpha:
                #print("Break because of alpha pruning...")
                break
            beta = min(beta, minScore)
        return minScore, minAction 

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        bestScore, bestAction = self.expectimax(gameState, 0, 0, 0)
        return bestAction

    def expectimax(self, gameState, depth, agentIndex, movedTimes):
        #check if the state is win/lose or reach maxDepth
        if depth == self.depth and movedTimes % gameState.getNumAgents() == 0:
            return self.evaluationFunction(gameState), None
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState), None
        
    
        if agentIndex:
            return self.expectiValue(gameState, depth, agentIndex, movedTimes)
        else:
            return self.maxValue(gameState, depth, agentIndex, movedTimes)
        

    def maxValue(self, gameState, depth, agentIndex, movedTimes):
        maxScore = float('-inf')
        maxAction = None
        
        movedTimes += 1
        nextAgent = (agentIndex + 1) % gameState.getNumAgents()
        nextDepth = depth 
        if movedTimes % gameState.getNumAgents() == 0:
            nextDepth += 1

        for action in gameState.getLegalActions(agentIndex):
            successor = gameState.generateSuccessor(agentIndex, action)
            
            score, _ = self.expectimax(successor, nextDepth, nextAgent, movedTimes)
            if score > maxScore:
                maxScore = score
                maxAction = action
        return maxScore, maxAction        
        

    def expectiValue(self, gameState, depth, agentIndex, movedTimes):
        expectiScore = 0
        expectiAction = None
        actionNum = 0

        movedTimes += 1
        nextAgent = (agentIndex + 1) % gameState.getNumAgents()
        nextDepth = depth 
        if movedTimes % gameState.getNumAgents() == 0:
            nextDepth += 1

        for action in gameState.getLegalActions(agentIndex):
            successor = gameState.generateSuccessor(agentIndex, action)
            score, _ = self.expectimax(successor, nextDepth, nextAgent, movedTimes)
            expectiScore += score
            actionNum += 1
        
        expectiScore /= actionNum
                
        return expectiScore, expectiAction 

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    pos = currentGameState.getPacmanPosition()
    ghostStates = currentGameState.getGhostStates()
    food = currentGameState.getFood()
    score = currentGameState.getScore()

    # Avoid ghosts: heavily penalize positions close to ghosts unless they are scared
    for ghostState in ghostStates:
        ghostPos = ghostState.getPosition()
        distanceToGhost = manhattanDistance(pos, ghostPos)
        if ghostState.scaredTimer > 0:
            # Encourage chasing scared ghosts
            score += max(10 - distanceToGhost, 0)
        else:
            # Penalize being close to active ghosts
            if distanceToGhost < 2:
                score -= 100
    
    # Prioritize eating food: incentivize positions closer to food
    foodList = food.asList()
    if foodList:
        closestFoodDistance = min([manhattanDistance(pos, food) for food in foodList])
        score += 10 / closestFoodDistance

    return score


    

# Abbreviation
better = betterEvaluationFunction
