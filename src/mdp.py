### code for representing/solving an MDP

import random
import numpy
import time
from problem_utils import *

class State :

    def __init__(self) :
        self.utility = 0.0
        self.reward = 0.0
        ### an action maps to a list of probability/state pairs
        self.transitions = {}
        self.actions = []
        self.policy = None
        self.coords = 0
        self.isGoal = False
        self.isWall = False
        self.id = 0

    def computeEU(self, action) :
        return sum([trans[0] * trans[1].utility \
            for trans in self.transitions[action]])

    def selectBestAction(self) :
        best = max([(self.computeEU(a), a) for a in self.actions])
        return best #used to be return best[1]



class Map :
    def __init__(self) :
        self.states = {}
        self.stop_crit = 0.01
        self.gamma = 0.8
        self.n_rows = 0
        self.n_cols = 0
    
    class PrintType :
        ACTIONS = 0
        VALUES = 1

    ### you write this method
    def valueIteration(self) :
       #Arrays and loops for testing effects of gamma and stop_crit on the algorithm
        gammaArray = [0.1, 0.5, 0.8, 0.9, 0.99, 0.999, 1]
        stopCritArray = [0.001, 0.01, 0.05, 0.1, 0.8]
        #for x in gammaArray :
        #    self.gamma = x
        #for x in stopCritArray :
        #    self.stop_crit = x
        ### 1. initialize utilities to 0
        start = time.time()
        for i in range(self.n_cols) :
            for j in range(self.n_rows) :
                if self.states[(i,j)].isGoal == False :
                    self.states[(i,j)].utility = 0


        largestChange = 1
        iterations = 0
        ### 2. repeat value iteration loop until largest change is smaller than
        ###    stop criterion
        while largestChange > self.stop_crit :
            iterations = iterations + 1
            largestChange = 0
            for i in range(self.n_cols) : #Loop over all states
                for j in range(self.n_rows) :
                    if self.states[(i,j)].isGoal == False : #That arent goals
                        oldUtility = self.states[(i,j)].utility #Save utilities
                        best = State.selectBestAction(self.states[(i,j)])
                        self.states[(i,j)].utility = self.states[(i,j)].reward + self.gamma * best[0] #Calculate utilities
                        if self.states[(i,j)].utility - oldUtility > largestChange : #check whether this change is larger than the biggest until now
                            largestChange = self.states[(i,j)].utility - oldUtility
        end = time.time()
        self.printValues()
        print('iterations:', iterations, 'time : ', end - start)
    #
        

    ### you write this method
    def policyIteration(self) :

         ### 1. initialize random policy
        directions = ['left', 'right','up','down']
        #Array and loop for testing effect of gamma
        gammaArray = [0.1, 0.5, 0.8, 0.9, 0.99]
        #for x in gammaArray :
        #    self.gamma = x
        start = time.time()
        for i in range(self.n_cols) :
            for j in range(self.n_rows) :
                self.states[(i,j)].policy = directions[random.randint(0,3)]
        ### 2 repeat policy iteration loop until policy is stable
        noChange = False
        iterations = 0
        while not noChange : #While the policy hasnt changed
            iterations = iterations + 1
            noChange = True # End the loop if no change has been detected at (1)
            self.calculateUtilitiesLinear()
            for i in range(self.n_cols) : #Loop over all states
                for j in range(self.n_rows) :
                    if self.states[(i,j)].isGoal == False : #That arent goals
                        oldPolicy = self.states[(i,j)].policy #Save the old policy
                        best = State.selectBestAction(self.states[(i,j)]) #Select best policy due to surrounding utilities
                        self.states[(i,j)].policy = best[1]
                        if self.states[(i,j)].policy != oldPolicy : # (1) If policy changed keep on looping
                            noChange = False
        end = time.time()
        self.printActions()
        print('iterations:', iterations, 'time : ', end - start)
    #
    
    def calculateUtilitiesLinear(self) :
        n_states = len(self.states)
        coeffs = numpy.zeros((n_states, n_states))
        ordinate = numpy.zeros((n_states, 1))
        for s in self.states.values() :
            row = s.id
            ordinate[row, 0] = s.reward
            coeffs[row,row] += 1.0
            if not s.isGoal :
                probs = s.transitions[s.policy]
                for p in probs :
                    col = p[1].id
                    coeffs[row,col] += -self.gamma * p[0]
        solution, _, _, _ = numpy.linalg.lstsq(coeffs, ordinate)
        for s in self.states.values() :
            if not s.isGoal :
                s.utility = solution[s.id, 0]
    
    def printActions(self) :
        self.printMaze(self.PrintType.ACTIONS)

    def printValues(self) :
        self.printMaze(self.PrintType.VALUES)
    
    def printMaze(self, print_type) :
        to_print = ":"
        for c in range(self.n_cols) :
            to_print = to_print + "--------:"
        to_print = to_print + '\n'
        for r in range(self.n_rows) :
            to_print = to_print + "|"
            for c in range(self.n_cols) :
                if self.states[(c,r)].isWall :
                    to_print = to_print + "        "
                else:
                    to_print = to_print + ' '
                    if self.states[(c,r)].isGoal :
                        to_print = to_print + \
                        "  {0: d}  ".format(int(self.states[(c,r)].utility))
                    else :
                        if print_type == self.PrintType.VALUES :
                            to_print = to_print + \
                                "{0: .3f}".format(self.states[(c,r)].utility)
                        elif print_type == self.PrintType.ACTIONS :
                            a = self.states[(c,r)].policy #policy used to be selectBestAction()
                            to_print = to_print + "  "
                            if a == 'left' :
                                to_print = to_print + "<<"
                            elif a == 'right' :
                                to_print = to_print + ">>"
                            elif a == 'up' :
                                to_print = to_print + "/\\"
                            elif a == 'down' :
                                to_print = to_print + "\\/"
                            to_print = to_print + "  "
                    to_print = to_print + ' '
                to_print = to_print + "|"
            to_print = to_print + '\n'
            to_print = to_print + ":"
            for c in range(self.n_cols) :
                to_print = to_print + "--------:"
            to_print = to_print + '\n'
        print to_print

def makeRNProblem() :
    """
    Creates the maze defined in Russell & Norvig. Utilizes functions defined
    in the problem_utils module.
    """


    walls = [(1,1)]
    actions = ['left', 'right','up','down']
    cols = 4
    rows = 3

    def filterState(oldState, newState) :
        if (newState[0] < 0 or newState[1] < 0 or newState[0] > cols - 1  or 
            newState[1] > rows - 1 or newState in walls) :
            return oldState
        else :
            return newState

    m = Map()
    m.n_cols = cols;
    m.n_rows = rows;
    for i in range(m.n_cols) :
        for j in range(m.n_rows) :
            m.states[(i,j)] = State()
            m.states[(i,j)].coords = (i,j)
            m.states[(i,j)].isGoal = False
            m.states[(i,j)].actions = actions
            m.states[(i,j)].id = j * m.n_cols + i
            m.states[(i,j)].reward = -0.04
                    
    m.states[(3,0)].isGoal = True
    m.states[(3,1)].isGoal = True

    m.states[(3,0)].utility = 1.0
    m.states[(3,1)].utility = -1.0

    m.states[(3,0)].reward = 1.0
    m.states[(3,1)].reward = -1.0

    for t in walls :
        m.states[t].isGoal = True
        m.states[t].isWall = True
        m.states[t].reward = 0.0
        m.states[t].utility = 0.0

    for s in m.states.items() :
        for a in actions :
            s[1].transitions[a] = [\
            (0.8, m.states[filterState(s[0], getSuccessor(s[0],a))]),  
            (0.1, m.states[filterState(s[0],getSuccessor(s[0], left(a)))]),
            (0.1, m.states[filterState(s[0], getSuccessor(s[0], right(a)))])]
    return m

def make2DProblem() :
    """
    Creates the larger maze described in the exercise. Utilizes functions 
    defined in the problem_utils module.
    """

    walls = [(1,1), (4,1), (5,1), (6,1),(7,1),(1,2), (7,2), (1,3), (5,3),
             (7,3), (1,4), (5,4), (7,4), (1,5), (5,5), (7,5), (1,6), (5,6), 
             (7,6), (1,7), (5,7), (7,7), (1,8), (3,8), (4,8), (5,8), 
             (7,8), (1,9)]
    actions = ['left', 'right','up','down']

    def filterState(oldState, newState) :
        if (newState[0] < 0 or newState[1] < 0 or newState[0] > 9 or 
            newState[1] > 9 or newState in walls) :
            return oldState
        else :
            return newState

    m = Map()
    m.n_cols = 10;
    m.n_rows = 10;
    for i in range(m.n_cols) :
        for j in range(m.n_rows) :
            m.states[(i,j)] = State()
            m.states[(i,j)].coords = (i,j)
            m.states[(i,j)].isGoal = False
            m.states[(i,j)].actions = actions
            m.states[(i,j)].id = j * 10 + i
            m.states[(i,j)].reward = -0.04
                    
    m.states[(0,9)].isGoal = True
    m.states[(9,9)].isGoal = True
    m.states[(9,0)].isGoal = True

    m.states[(0,9)].utility = 1.0
    m.states[(9,9)].utility = -1.0
    m.states[(9,0)].utility = 1.0

    m.states[(0,9)].reward = 1.0
    m.states[(9,9)].reward = -1.0
    m.states[(9,0)].reward = 1.0

    for t in walls :
        m.states[t].isGoal = True
        m.states[t].isWall = True
        m.states[t].utility = 0.0
        m.states[t].reward = 0.0


    for s in m.states.items() :
        for a in actions :
            s[1].transitions[a] = [\
            (0.7, m.states[filterState(s[0], getSuccessor(s[0],a))]),  
            (0.1, m.states[filterState(s[0], getSuccessor(s[0], opposite(a)))]), 
            (0.1, m.states[filterState(s[0],getSuccessor(s[0], left(a)))]),
            (0.1, m.states[filterState(s[0], getSuccessor(s[0], right(a)))])]

    return m
        
            
            
