#Ahmad Amjad Mughal & Hamad Nasir
#121672 & 120312
#Lab-05 Game Intelligent Stretegies Implementation
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
        #We basicaly return move with a top score when we perform some action or move to next state we get some score
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
        """
        "*** YOUR CODE HERE ***"
        #get legal moves
    	Moves=gameState.getLegalActions(0)
    	#result gamestate for all legal actions
    	nextStates=[gameState.generateSuccessor(0,action) for action in Moves]
    	#get scores from minimizer for all states in nextstate
    	scores=[self.minimizer(0,nextState,1) for nextState in nextStates]
        #storing the max score
        topScore = max(scores)
        #returns a list of legal actions
    	bestOptions = [index for index in range(len(scores)) if scores[index]==topScore]
        #randomly select an action from the list
        chosenIndex = random.choice(bestOptions)
        #return the choosen action
    	return Moves[chosenIndex]

    def maximizer(self,currentDepth,gameState):
        #if current depth is  final depth then return it and evaluate it
    	if(self.depth==currentDepth or gameState.isLose() or gameState.isWin()):
    		return self.evaluationFunction(gameState)
        #getting the legal actions
    	legalMoves=gameState.getLegalActions(0)
        #for each action generate successor legal actions
        resultStates=[gameState.generateSuccessor(0,action) for action in legalMoves]
    	scores=[self.minimizer(currentDepth,state,1) for state in resultStates]
        #return the max of the scores
        return max(scores)

    def minimizer(self,currentDepth,gameState,ghostIndex):
        #if we reaches the final stage of game or this game gives us some result then simply return evaluation function of terminal state
        if(self.depth==currentDepth or gameState.isLose() or gameState.isWin()):
    		return self.evaluationFunction(gameState)
    	#getting the legal actions
    	legalMoves=gameState.getLegalActions(ghostIndex)
        #for each action generate successor legal actions
    	resultStates=[gameState.generateSuccessor(ghostIndex, action) for action in legalMoves]

    	if (ghostIndex>=gameState.getNumAgents()-1):
    		scores=[self.maximizer(currentDepth+1,state) for state in resultStates]
    	else:
    		scores=[self.minimizer(currentDepth,state,ghostIndex+1) for state in resultStates]
       #return the minimum of the scores
        return min(scores)

class AlphaBetaAgent(MultiAgentSearchAgent):
    #We actually return a list of best actions which makes our MultiAgentSearchAgent intelligent enough to go for best move that leads to completion
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """
    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def min_val(state, depth, agent, alpha, beta):

            if agent == state.getNumAgents():
                #returns the max value at min level
                return max_val(state, depth + 1, 0, alpha, beta)

            val = None
            #loop through the legal actions
            for action in state.getLegalActions(agent):
                #generate the successors for tha legal actiom
                successor = min_val(state.generateSuccessor(agent, action), depth, agent + 1, alpha, beta)
                #If successor is already has a min value assign it to current state otherwise get the min value from all its successors using min function
                val = successor if val is None else min(val, successor)
                #Assigned a state value but don't update alpha as value is not greater than alpha
                if alpha is not None and val < alpha:
                    return val
                #Assign the beta some value if beta has -infinity or not assigned some value otherwise update a beta's value
                beta = val if beta is None else min(beta, val)
            #If state hasn't assigned some value then give it value passes from leaf node's heuristic
            if val is None:
                return self.evaluationFunction(state)

            return val

        def max_val(state, depth, agent, alpha, beta):
            assert agent == 0

            if depth > self.depth:
                return self.evaluationFunction(state)

            val = None
            #Loop iterates for each successor and generates a min value and assigned to that successor then give a Max value from list of Successors to current state
            for action in state.getLegalActions(agent):
                successor = min_val(state.generateSuccessor(agent, action), depth, agent + 1, alpha, beta)
                val = max(val, successor)
                #beta is not updated as old beta value is already Minimal than the current state value
                if beta is not None and val > beta:
                    return val
                #We check for alpha's value that gets updated only if value > alpha
                alpha = max(alpha, val)
            #if none value is assigned then we calculate heuristic or evaluation function of that state
            if val is None:
                return self.evaluationFunction(state)

            return val
        #We consider that action as best action if Alpha value is Max for that state from where to perform action.
        val, alpha, beta, best = None, None, None, None
        for action in gameState.getLegalActions(0):
            val = max(val, min_val(gameState.generateSuccessor(0, action), 1, 1, alpha, beta))
            #If alpha is infinity then assign current value to alpha otherwise update alpha's value if value > alpha and this action is best
            if alpha is None:
                alpha, best = val, action
            else:
                alpha, best = max(val, alpha), action if val > alpha else best

        return best

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
        #getting all the legal actions
        legalMoves=gameState.getLegalActions(0)
        #for every legal move generate successors
    	resultStates=[gameState.generateSuccessor(0,move) for move in legalMoves]
    	scores=[self.expecti(0,state,1) for state in resultStates]
        #getting the max score
        bestScore=max(scores)
        #select best indeces for the score is the highest
    	bestIndices=[index for index in range(len(scores)) if scores[index]==bestScore]
        #randomly select from the best indeces list
        chosenIndex=random.choice(bestIndices)
        #return a list of legal moves
        return legalMoves[chosenIndex]

    def expecti (self,currentDepth,gameState,ghostIndex):
        #if current depth is  final depth then return it and evaluate it
    	if(self.depth==currentDepth or gameState.isLose() or gameState.isWin()):
    		return self.evaluationFunction(gameState)
            #getting the legal actions
    	legalMoves=gameState.getLegalActions(ghostIndex)
        #for each lega move generate successors
    	resultStates=[gameState.generateSuccessor(ghostIndex,move) for move in legalMoves]

    	if(ghostIndex==gameState.getNumAgents()-1):
    		scores=[self.maximizer(currentDepth+1,state) for state in resultStates]
    	elif(ghostIndex<gameState.getNumAgents()-1):
    		scores=[self.expecti(currentDepth,state,ghostIndex+1) for state in resultStates]
    	#returning the averge
    	return sum(scores)/len(scores)

    def maximizer(self,currentDepth,gameState):
        #if current depth is  final depth then return it and evaluate it
    	if(self.depth==currentDepth or gameState.isLose() or gameState.isWin()):
    		return self.evaluationFunction(gameState)
            #getting the legal actions
    	legalMoves=gameState.getLegalActions(0)
        #for each legal move get successors
    	resultStates=[gameState.generateSuccessor(0,move) for move in legalMoves]
    	scores=[self.expecti(currentDepth,state,1) for state in resultStates]
        #return the max of the scores
        return max(scores)

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
