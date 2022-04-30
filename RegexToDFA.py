from os import popen
import time

class AutomataLanguage:

    def __init__(self, language = set(['0', '1'])):  #method that defines the automata language start state and final state and the transition dictionary with the language and all the states.
        self.startState = None
        self.finalStates = []
        self.states = set()
        self.transitions = dict()
        self.language = language

    def epsilon():
        return ":e:"

    def setStartState(self, state):                                         #method which takes a state as a parameter and then makes it a start state by adding it to the startState attribute 
        self.startState = state                                                 #and adding this state to the set of states
        self.states.add(state)

    def setFinalStates(self, state):                                        #method that checks first for the specified type them adds this state to the set oif final states
        if isinstance(state, int):
            state = [state]
        for i in state:
            if i not in self.finalStates:
                self.finalStates.append(i)

    def transitionStates(self, source, target, inputChar):       #method that checks first for the input type then adds the source state and the target state to the set of states
        if isinstance(inputChar, str):
            inputChar = set([inputChar])
        self.states.add(source)
        self.states.add(target)

        if source in self.transitions:                                              #then it checks if the source state is in the transitions
            if target in self.transitions[source]:                             #then it checks also if the target state is in the transitions of the source
                self.transitions[source][target] = self.transitions[source][target].union(inputChar)           #if both states are in the transitions and the target is in the transitions of source
                                                                                                                                                                      # then it links them with the input
            else:
                self.transitions[source][target] = inputChar          #if only the source state is in the transitions and the target is not in the source transitions then it adds the source to
                                                                                                    #the target with the input linking them
        else:
            self.transitions[source] = {target : inputChar}          #else if the source itself is not in the transitions then we add from the begining the source and the target with the input

    def addTransition(self, transitions):                                   #method that takes the transition function as a whole and then adds them all in the transitions dictionary
        for source, targets in transitions.items():
            for state in targets:
                self.transitionStates(source, state, targets[state])

    def getStateTransitions(self, state, key):                          #method that searches for specific transition as it searches first for the source in the transitions then for the target
        if isinstance(state, int):                                                  #and see the key that they are linked together and it adds it to transStates set if it is found and returns the whole set
            state = [state]
        transStates = set()
        for s in state:
            if s in self.transitions:
                for t in self.transitions[s]:
                    if key in self.transitions[s][t]:
                        transStates.add(t)
        return transStates

    def getEpsilonClosure(self, find):                                  #method that searches for the eClosure for certain state then makes a set of the eClosureStates and returns it at the end
        eClosureStates = set()
        states = set([find])
        while len(states)!= 0:
            state = states.pop()
            eClosureStates.add(state)
            if state in self.transitions:
                for t in self.transitions[state]:
                    if AutomataLanguage.epsilon() in self.transitions[state][t] and t not in eClosureStates:
                        states.add(t)
        return eClosureStates

    def displayInCLI(self):                         #method to display in the terminal all the states and the start state and all the final states with the transition for each state.
        print ("All the states:", self.states)
        print ("Start state:", self.startState)
        print ("Final states:", self.finalStates)
        print ("Transitions:")
        for source, targets in self.transitions.items():
            for state in targets:
                for char in targets[state]:
                    print ("  ",source, "->", state, "on '"+char+"'",)


    def numberState(self, startNumber):     #method that takes the states and number them incrementally from the start number
        changeName = {}
        for i in list(self.states):
            changeName[i] = startNumber
            startNumber += 1
        update = AutomataLanguage(self.language)
        update.setStartState(changeName[self.startState])
        update.setFinalStates(changeName[self.finalStates[0]])
        for source, targets in self.transitions.items():
            for state in targets:
                update.transitionStates(changeName[source], changeName[state], targets[state])
        return [update, startNumber]


    def getDotFile(self):                                      #method for creating the states graph
        DotFile = "digraph DFA {\nrankdir=LR\n"
        if len(self.states) != 0:
            DotFile += "root=s1\nstart [shape=point]\nstart->s%d\n" % self.startState
            for state in self.states:
                if state in self.finalStates:
                    DotFile += "s%d [shape=doublecircle]\n" % state
                else:
                    DotFile += "s%d [shape=circle]\n" % state
            for source, targets in self.transitions.items():
                for state in targets:
                    for char in targets[state]:
                        DotFile += 's%d->s%d [label="%s"]\n' % (source, state, char)
        DotFile += "}"
        return DotFile

#class that defines the NFA structure from the normal structure, the concatenate, the OR and the repeatition
class createNFA:

    @staticmethod
    def normalStructure(inputChar):                                 #the normal structure when it recieves a character it creates 2 states with the first one as the start and the second one
        firstState = 1                                                             #as final and make transition between the two states with the given char
        secondState = 2
        normal = AutomataLanguage()
        normal.setStartState(firstState)
        normal.setFinalStates(secondState)
        normal.transitionStates(1, 2, inputChar)
        return normal

    @staticmethod
    def orStructure(firstInput, secondInput):                        #the or strructure which takes two inputs and or them together by creating two new states one that is the start state
        [firstInput, firstFinal] = firstInput.numberState(2)      # and other that is the final state and then takes the start state and connect it with the start states of the two inputs
        [secondInput, secondFinal] = secondInput.numberState(firstFinal)    #with epsilons and also take the fin al states of the two inputs and connect them with the final state 
        firstState = 1                                                                  #with epsilons and then adds this transitions of the two inputs in the transitions dictionary
        secondState = secondFinal
        orOperation = AutomataLanguage()
        orOperation.setStartState(firstState)
        orOperation.setFinalStates(secondState)
        orOperation.transitionStates(orOperation.startState, firstInput.startState, AutomataLanguage.epsilon())
        orOperation.transitionStates(orOperation.startState, secondInput.startState, AutomataLanguage.epsilon())
        orOperation.transitionStates(firstInput.finalStates[0], orOperation.finalStates[0], AutomataLanguage.epsilon())
        orOperation.transitionStates(secondInput.finalStates[0], orOperation.finalStates[0], AutomataLanguage.epsilon())
        orOperation.addTransition(firstInput.transitions)
        orOperation.addTransition(secondInput.transitions)
        return orOperation

    @staticmethod
    def concatStructure(firstInput, secondInput):           #the concatination structure which takes two inputs and concatemate them, sets the starts state as the first state in the 
        [firstInput, firstFinal] = firstInput.numberState(1) #first input then makes a final state as the last state in the second input and then it takes these and connect them with epsilon
        [secondInput, secondFinal] = secondInput.numberState(firstFinal)    #and add this in the transition dictionary to be used later in printing
        firstState = 1
        secondState = secondFinal-1
        concat = AutomataLanguage()
        concat.setStartState(firstState)
        concat.setFinalStates(secondState)
        concat.transitionStates(firstInput.finalStates[0], secondInput.startState, AutomataLanguage.epsilon())
        concat.addTransition(firstInput.transitions)
        concat.addTransition(secondInput.transitions)
        return concat

    @staticmethod
    def starStructure(firstInput):                                          #the star structure is the repition structure and it takes only one input and then it repeats it. It creates two new states
        [firstInput, firstFinal] = firstInput.numberState(2)    #one at the begining as start state and one at the end as final state. The start state is connected with the starts state 
        firstState = 1                                                                  #of the input and the start state is also connected with epsilon with the finals state. The final state of the input is 
        secondState = firstFinal                                             #connected to the final state with epsioln and the final state of the input is then connected with the start state of the input
        star = AutomataLanguage()                                       #to create the loop. After all this, the first input transitions are added to the transitions dictionary.
        star.setStartState(firstState)
        star.setFinalStates(secondState)
        star.transitionStates(star.startState, firstInput.startState, AutomataLanguage.epsilon())
        star.transitionStates(star.startState, star.finalStates[0], AutomataLanguage.epsilon())
        star.transitionStates(firstInput.finalStates[0], star.finalStates[0], AutomataLanguage.epsilon())
        star.transitionStates(star.finalStates[0], star.startState, AutomataLanguage.epsilon())
        star.addTransition(firstInput.transitions)
        return star

    def plusStructure(firstinput):                                          #the plus structure is the repition structure and it takes only one input and then it repeats it. It creates two new states
        [firstInput, firstFinal] = firstInput.numberState(2)    #one at the begining as start state and one at the end as final state. The start state is connected with the starts state 
        firstState = 1                                                                  #of the input. The final state of the input is connected to the final state with epsioln and the final
        secondState = firstFinal                                              # state is then connected with the start state to create the loop. After all this, the first input transitions 
        plusOperation = AutomataLanguageLanguage()     #are added to the transitions dictionary.
        plusOperation.setStartState(firstState)
        plusOperation.setfinalStates(secondState)
        plusOperation.transitionStates(plusOperation.startState, firstInput.startState,AutomataLanguageLanguage.epsilon())
        plusOperation.transitionStates(firstInput.finalStates[0], plusOperation.finalStates[0], AutomataLanguageLanguage.epsilon())
        plusOperation.transitionStates(plusOperation.finalStates[0], plusOperation.startState, AutomataLanguageLanguage.epsilon())
        plusOperation.transitionStates(firstInput.transitions)
        return plusOperation