#Group Members
#Ahmad Amjad Mughal and Hamad Nasir
#Lab-02 Artificial Intelligence
#Project-01 Improving of Pacman Game's Search Agents by giving them Searching Algorithms



 
# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    #we get startState to start from
    start = problem.getStartState()
    #Defining the exploredList which is initialy empty
    exploredList = []
    #destination state to where we stop our algorithm
    destination = problem.getStartState()
    #We append our current startState into ExploredList
    exploredList.append(start)
    #Getting the stack data structure from utilities.py
    frontierList = util.Stack()
    #List of actions from StartState
    stateTuple = (start, [])
    #Pushing the states into frontierList
    frontierList.push(stateTuple)
    #Loop that runs for Checking whether our FrontierList is empty or we reached Goal State
    while not problem.isGoalState(destination) and not frontierList.isEmpty():
        nextstate, actions = frontierList.pop()
        exploredList.append(nextstate)
        successor = problem.getSuccessors(nextstate)
        #Traversing through all successors
        for i in successor:
            nextState = i[0]
            #If successor is already in exploredList then ignore that state otherwise assign current state to that successor
            if not nextState in exploredList:
                destination = i[0]
                direction = i[1]
                frontierList.push((nextState, actions + [direction]))
                #we return actions made from state Start to Destination + directions of each successor state
    return actions + [direction]
    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    "*** YOUR CODE HERE ***"
    #We get start state from where to begin
    start = problem.getStartState()
    #We define ExploredList which is initialy empty
    exploredList = []
    #we add startState to our exploredList as it is already visited
    exploredList.append(start)
    #We get the data structure Queue from utilities.py
    frontierList = util.Queue()
    #List of possible actions from startState
    stateTuple = (start, [])
    #We push the possible states into frontierList
    frontierList.push(stateTuple)
    #While all the states are not poped or list is not empty
    while not frontierList.isEmpty():
        state, action = frontierList.pop()
        #Checking whether we reached our goal state or not
        if problem.isGoalState(state):
            return action
            #we traverse through other successors and check that whether that nextState is already in exploredList or not
        successor = problem.getSuccessors(state)
        for i in successor:
            nextState = i[0]
            #if not then we assign our current state to  nextState which is then append to ExploredList
            if not nextState in exploredList:
                direction = i[1]
                exploredList.append(nextState)
                #we push the nextState + actions moved to nextState + direction in terms of [N,S,W,E]
                frontierList.push((nextState, action + [direction]))
    return action
    util.raiseNotDefined()

def uniformCostSearch(problem):
    "Search the node of least total cost first. "
    "*** YOUR CODE HERE ***"
    #We get the startState from getStartState function from where to begin
    start = problem.getStartState()
    ExploredList = []
    #We use PriorityQueue in UniformCost and we import this from utilities.py
    frontierList = util.PriorityQueue()
    #We push startState + listOfActions + cost of that State
    frontierList.push((start, []) ,0)
    #While loop runs when frontierList is not empty and we pop the state that has least cost
    while not frontierList.isEmpty():
        state, actions = frontierList.pop()
        #if we reached our goalState then simply return actions
        if problem.isGoalState(state):
            return actions
            #If state is not already explored
        if state not in ExploredList:
            successors = problem.getSuccessors(state)
            #We traverse through each successor
            for i in successors:
                nextState = i[0]
                if nextState not in ExploredList:
                    #We move in that direction
                    directions = i[1]
                    #We calculate the cost to that path
                    newCost = actions + [directions]
                    #We push nextState to move into + action used to move + direction to where we move + cost of that path in frontierList
                    frontierList.push((nextState, actions + [directions]), problem.getCostOfActions(newCost))
                    #That state is exploed
        ExploredList.append(state)
    return actions
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
