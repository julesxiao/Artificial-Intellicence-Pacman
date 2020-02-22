# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
  """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
  """


  def getAction(self, gameState):
    """
    You do not need to change this method, but you're welcome to.

    getAction chooses among the best options according to the evaluation function.

    Just like in the previous project, getAction takes a GameState and returns
    some Directions.X for some X in the set {North, South, West, East, Stop}
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

  def evaluationFunction(self, currentGameState, action):
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
    def disToNearestFood(position, foodGrid) :
        disToNearestFood = 0
        for i in range(foodGrid.width):
            for j in range(foodGrid.height):
                if foodGrid[i][j] == True:
                    tempDist = manhattanDistance(position, (i,j))
                    if (disToNearestFood == 0) or (tempDist < disToNearestFood):
                        disToNearestFood = tempDist
        return disToNearestFood
    
    if newFood.count() > 0 :
        successorGameState.data.score += 1.0/disToNearestFood(newPos,newFood) * 10
    else :
        return 1000
      
    if manhattanDistance(newPos, newGhostStates[0].getPosition()) == 1:
        successorGameState.data.score = -1000
    
    return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
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

  def getAction(self, gameState):
    """
      Returns the minimax action from the current gameState using self.depth
      and self.evaluationFunction.

      Here are some method calls that might be useful when implementing minimax.

      gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

      Directions.STOP:
        The stop direction, which is always legal

      gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

      gameState.getNumAgents():
        Returns the total number of agents in the game
    """
    "*** YOUR CODE HERE ***"
    #util.raiseNotDefined()
    agentIndex = -1
    currentDepth = -1
    def value(state, agentIndex, currentDepth):
      agentIndex = (agentIndex+1)%gameState.getNumAgents()
      if agentIndex == 0:
        currentDepth += 1
      if currentDepth is self.depth or state.isWin() or state.isLose():
        return self.evaluationFunction(state)
      else:
        if agentIndex == 0:
          return maxValue(state, agentIndex, currentDepth)
        else:
          return minValue(state, agentIndex, currentDepth)
          
    def maxValue(state, agentIndex, currentDepth):
      v = (Directions.STOP , -float("inf")) # initialize negative infinity
      agentAction = state.getLegalActions(agentIndex)
      for action in agentAction:
        succesorState = state.generateSuccessor(agentIndex, action)
        tempv = value(succesorState,agentIndex, currentDepth)
        if type(tempv) is tuple:
          tempv = tempv[1]
        vScore = max (v[1], tempv)
        if not vScore == v[1]:
          v = (action, vScore)
      return v
      
    def minValue(state, agentIndex, currentDepth):
      v = (Directions.STOP , float("inf")) #initialize infinity
      agentAction = state.getLegalActions(agentIndex)
      for action in agentAction:
        succesorState = state.generateSuccessor(agentIndex, action)
        tempv = value(succesorState,agentIndex, currentDepth)
        if type(tempv) is tuple:
          tempv = tempv[1]
        vScore = min (v[1], tempv)
        if not vScore == v[1]:
          v = (action, vScore)        
      return v
    
    return value(gameState, agentIndex, currentDepth)[0]

class AlphaBetaAgent(MultiAgentSearchAgent):
  """
    Your minimax agent with alpha-beta pruning (question 3)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action using self.depth and self.evaluationFunction
    """
    "*** YOUR CODE HERE ***"
    #util.raiseNotDefined()
    agentIndex = -1
    currentDepth = -1
    alpha = -float("inf")
    beta = float("inf")
    def value(state, agentIndex, currentDepth, alpha, beta):
      agentIndex = (agentIndex+1)%gameState.getNumAgents()
      if agentIndex == 0:
        currentDepth += 1
      if currentDepth is self.depth or state.isWin() or state.isLose():
        return self.evaluationFunction(state)
      else:
        if agentIndex == 0:
          return maxValue(state, agentIndex, currentDepth, alpha, beta)
        else:
          return minValue(state, agentIndex, currentDepth, alpha, beta)
          
    def maxValue(state, agentIndex, currentDepth, alpha, beta):
      v = (Directions.STOP , -float("inf")) # initialize negative infinity
      agentAction = state.getLegalActions(agentIndex)
      for action in agentAction:
        succesorState = state.generateSuccessor(agentIndex, action)
        tempv = value(succesorState,agentIndex, currentDepth, alpha, beta)
        if type(tempv) is tuple:
          tempv = tempv[1]
        vScore = max (v[1], tempv)
        if not vScore == v[1]:
          v = (action, vScore)
        if v[1] >= beta:
          return v
        alpha = max (alpha, v[1])
      return v
      
    def minValue(state, agentIndex, currentDepth, alpha, beta):
      v = (Directions.STOP , float("inf")) #initialize infinity
      agentAction = state.getLegalActions(agentIndex)
      for action in agentAction:
        succesorState = state.generateSuccessor(agentIndex, action)
        tempv = value(succesorState,agentIndex, currentDepth, alpha, beta)
        if type(tempv) is tuple:
          tempv = tempv[1]
        vScore = min(v[1], tempv)
        if not vScore == v[1]:
          v = (action, vScore)
        if v[1] <= alpha:
          return v
        beta = min(beta, v[1])
      return v
    
    return value(gameState, agentIndex, currentDepth, alpha, beta)[0]

class ExpectimaxAgent(MultiAgentSearchAgent):
  """
    Your expectimax agent (question 4)
  """

  def getAction(self, gameState):
    """
      Returns the expectimax action using self.depth and self.evaluationFunction

      All ghosts should be modeled as choosing uniformly at random from their
      legal moves.
    """
    "*** YOUR CODE HERE ***"
    agentIndex = -1
    currentDepth = -1
    def value(state, agentIndex, currentDepth):
      agentIndex = (agentIndex+1)%gameState.getNumAgents()
      if agentIndex == 0:
        currentDepth += 1
      if currentDepth == self.depth or state.isWin() or state.isLose():
        return self.evaluationFunction(state)
      
      else:
        if agentIndex == 0:
          return maxValue(state, agentIndex, currentDepth)
        else:
          return expValue(state, agentIndex, currentDepth)
          
    def maxValue(state, agentIndex, currentDepth):
      v = (Directions.STOP , -float("inf")) # initialize negative infinity
      agentAction = state.getLegalActions(agentIndex)
      for action in agentAction:
        succesorState = state.generateSuccessor(agentIndex, action)
        tempv = value(succesorState,agentIndex, currentDepth)
        if type(tempv) is tuple:
          tempv = tempv[1]
        vScore = max (v[1], tempv)
        if not vScore == v[1]:
          v = (action, vScore)
      return v
      
    def expValue(state, agentIndex, currentDepth):
      v = (Directions.STOP , 0) #initialize infinity
      agentAction = state.getLegalActions(agentIndex)
      probability = 1.0/len(agentAction)
      vScore = v[1] 
      for action in agentAction:
        succesorState = state.generateSuccessor(agentIndex, action)
        tempv = value(succesorState,agentIndex, currentDepth)
        if type(tempv) is tuple:
          tempv = tempv[1]
        vScore = probability*tempv
        v = (action, vScore)
      return v
    
    return value(gameState, agentIndex, currentDepth)[0]
    util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
  """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    Important values for features about the state:
        win state return 10000
        lose state return -10000
        distance of pacman to nearest food
        distance of pacman to nearest ghost
        distance of pacman to nearest scaredghost
        number of food on board
        number of capsules on board
  """
  "*** YOUR CODE HERE ***"
  pacmanPos = currentGameState.getPacmanPosition()
  ghostStates = currentGameState.getGhostStates()
  foodList = currentGameState.getFood().asList()
  foodNum = len(foodList)
  capsulesNum = len(currentGameState.getCapsules())
  score = currentGameState.getScore()
  
  if currentGameState.isWin():
    return 10000
    
  if currentGameState.isLose():
    return -10000
  
  #get the distance between pacman and the nearest food
  distanceToFood = 0
  for food in foodList:
    tempDist = manhattanDistance(pacmanPos, food)
    if (distanceToFood == 0) or (tempDist < distanceToFood):
      distanceToFood = tempDist
  score += 1*(1.0/distanceToFood)

  #get the distance between pacman and the nearest ghost and the nearest scared ghost
  distanceToGhost = float("inf")
  distanceToScaredGhost = float("inf")
  tempDistGhost = []
  tempDistScaredGhost = []
  for ghostState in ghostStates:
    if ghostState.scaredTimer == 0:
      tempDistGhost.append(manhattanDistance(pacmanPos, ghostState.getPosition()))
    else:
      tempDistScaredGhost.append(manhattanDistance(pacmanPos, ghostState.getPosition()))
  if len(tempDistGhost) > 0:
    distanceToGhost = min(tempDistGhost)
  if len(tempDistScaredGhost) > 0 :
    distanceToScaredGhost = min(tempDistScaredGhost)
  score += -3*(1.0/distanceToGhost) + 1*(1.0/distanceToScaredGhost)
  
  #motivate pacman to eat all the food and capsules on board asap
  if not capsulesNum is 0:
    score += 20*(1.0/capsulesNum)
  if not foodNum is 0:
    score += 2*(1.0/foodNum)
    
  return score
# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
  """
    Your agent for the mini-contest
  """

  def getAction(self, gameState):
    """
      Returns an action.  You can use any method you want and search to any depth you want.
      Just remember that the mini-contest is timed, so you have to trade off speed and computation.

      Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
      just make a beeline straight towards Pacman (or away from him if they're scared!)
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

