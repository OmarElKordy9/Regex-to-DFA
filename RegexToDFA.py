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

    def normalStructure(inputChar):                                 #the normal structure when it recieves a character it creates 2 states with the first one as the start and the second one
        firstState = 1                                                             #as final and make transition between the two states with the given char
        secondState = 2
        normal = AutomataLanguage()
        normal.setStartState(firstState)
        normal.setFinalStates(secondState)
        normal.transitionStates(1, 2, inputChar)
        return normal

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

    def plusStructure(firstInput):                                          #the plus structure is the repition structure and it takes only one input and then it repeats it. It creates two new states
        [firstInput, firstFinal] = firstInput.numberState(2)    #one at the begining as start state and one at the end as final state. The start state is connected with the starts state 
        firstState = 1                                                                  #of the input. The final state of the input is connected to the final state with epsioln and the final
        secondState = firstFinal                                              # state is then connected with the start state to create the loop. After all this, the first input transitions 
        plus = AutomataLanguage()     #are added to the transitions dictionary.
        plus.setStartState(firstState)
        plus.setFinalStates(secondState)
        plus.transitionStates(plus.startState, firstInput.startState,AutomataLanguage.epsilon())
        plus.transitionStates(firstInput.finalStates[0], plus.finalStates[0], AutomataLanguage.epsilon())
        plus.transitionStates(plus.finalStates[0], plus.startState, AutomataLanguage.epsilon())
        plus.addTransition(firstInput.transitions)
        return plus


#class for converting the regex to NFA
class RegexToNFA:

    def __init__(self, regex):                                          #method to define what is the star and what is the or operator and all the things that might be written in the regex
        self.star = '*'                                                         #The alphabet is also defined to accept any lowercase letter, any uppercase letter and any number.
        self.plus = '+'
        self.oring = '|'
        self.concat = '.'
        self.openedBracket = '('
        self.closedBracket = ')'
        self.operators = [self.oring, self.concat]
        self.regex = regex
        self.alphabet = [chr(i) for i in range(65,91)]
        self.alphabet.extend([chr(i) for i in range(97,123)])
        self.alphabet.extend([chr(i) for i in range(48,58)])
        self.scanBuildNFA()

    def scanBuildNFA(self):                                              #method that scan the regex and responsible for the logics of creating the NFA by storing the operators and the opened
        language = set()                                                      #brackets in the opStack and also checks the brackets if they are balaned or not. The automataStack is responsible
        self.opStack = []                                                      #for creating the automata step by step and putting them in the stack until an operation comes and collects them together
        self.checkStack = []                                                #then the new automata is added to the automataStack at the end.
        self.automataStack = []
        previous = "::e::"        #previous is defined to check the previous character of the character we are scanning. It is defined as :e: as for the first character it should by epsilon


        for char in self.regex:     #looping on th characters in the regex

            #CASE 1: character is alphabet ----- we check if the previous character is not dot and it is an alphabet or closed bracket or star to handle the case that the user
            #may write AB which means A.B, he may write (A)B which means (A).B, he may alsow write A*B which means A*.B
            if char in self.alphabet:
                language.add(char)
                if previous != self.concat and (previous in self.alphabet or previous in [self.closedBracket,self.star]):
                    self.addToOpStack(self.concat)              #handling the concatination cases and sending the concat to another function to work on it
                self.automataStack.append(createNFA.normalStructure(char))      #if it is character we build the NFA of that character and add it to the automataStack

            #Case 2: character is opened bracket ----- we check the concatination cases as explained before. 
            elif char  ==  self.openedBracket:
                if previous != self.concat and (previous in self.alphabet or previous in [self.closedBracket,self.star]):
                    self.addToOpStack(self.concat)      #sending the concat character to another function to work on it.
                self.opStack.append(char)                  #adding the opened bracket to the opStack to be accessed in another function
                self.checkStack.append(char)            #adding the opened bracket also to the checkStack to check for the balance of the brackets later.

            #Case 3: character is star  ----- we check for the exceptions that may happen that causes errors.
            #Exceptions as .* or |* or (* or **
            elif char == self.star:
                if previous in self.operators or previous  == self.openedBracket or previous == self.star:
                    raise BaseException("Error processing '%s' after '%s'" % (char, previous))
                self.workOnOperator(char)           #sending the star to another function to work on it.

             #Case 4: character is plus  ----- we check for the exceptions that may happen that causes errors.
            #Exceptions as .+ or |+ or (+ or ++
            elif char == self.plus:
                if previous in self.operators or previous  == self.openedBracket or previous == self.plus:
                    raise BaseException("Error processing '%s' after '%s'" % (char, previous))
                self.workOnOperator(char)           #sending the plus to another function to work on it.

            #Case 5: character is concat or OR  ----- we check for the exceptions that may happen that causes errors.
            #Exceptions as .. or .| or || or (. or (|
            elif char in self.operators:
                if previous in self.operators or previous  == self.openedBracket:
                    raise BaseException("Error processing '%s' after '%s'" % (char, previous))
                else:
                    self.addToOpStack(char)         #sending the operaor to other function to work on it.

            #Case 6: character is closed barcket we check for the exceptions that may happen that causes errors.
            #Exceptions as .) or |) or stack is empty and doesn't have any operators inside
            elif char  ==  self.closedBracket:
                if previous in self.operators:
                    raise BaseException("Error processing '%s' after '%s'" % (char, previous))
                while(1):
                    if len(self.opStack) == 0:
                        raise BaseException("Error processing '%s'. Empty opStack" % char)
                    o = self.opStack.pop()
                    if o == self.openedBracket:
                        break
                    elif o in self.operators:
                        self.workOnOperator(o)
                if len(self.checkStack) == 0:
                     raise BaseException("Error processing, brackets are incorrect")
                else:
                    self.checkStack.pop()

            #Case 7: character is anything that we did not define should raise an exception that causes an error.
            else:
                raise BaseException("Symbol '%s' is not allowed" % char)
            previous = char    #incrementing the previous at the end of each loop of scan to the next character

        while len(self.opStack) != 0:           #work on the operators inside the stack until it is empty
            op = self.opStack.pop()
            self.workOnOperator(op)

        if len(self.checkStack) != 0:           #check for the balance of the brackets and if they are unbalanced then an exception is raised.
            raise BaseException("Error processing, brackets are incorrect")
        
        self.nfa = self.automataStack.pop()             #retrieving the last automata created
        self.nfa.language = language                        #retrieving the language used in building the automata


    def addToOpStack(self, char):               #checking for the coming operator to be able to process it correctly.
        while(1):                       #looping on the opStack until it is empty
            if len(self.opStack) == 0:
                break
            top = self.opStack[len(self.opStack)-1]          #retrieving the top of the stack and checking if it is an opened bracket then it will be appended to the opStack
            if top == self.openedBracket:                           #and if it is a character or concat then it will be sent to another function to work on it and popping it from the opStack
                break
            if top == char or top == self.concat:
                op = self.opStack.pop()
                self.workOnOperator(op)
            else:
                break
        self.opStack.append(char)


    def workOnOperator(self, operator):             #method for working on the operators that comes to it to determine what to do with it.
        if len(self.automataStack) == 0:                 #if the automataStack is empty then there is nothing to concat or nothing to OR then an exception will be raised.
            raise BaseException("Error processing operator '%s'. opStack is empty" % operator)

        #CASE 1: if the operator star then it only needs one input from the automataStack so it pops from the automataStack and send it to createNFA with the star structure.
        if operator == self.star:
            firstInput = self.automataStack.pop()
            self.automataStack.append(createNFA.starStructure(firstInput))

        #CASE 2: if the operator plus then it only needs one input from the automataStack so it pops from the automataStack and send it to createNFA with the star structure.
        elif operator == self.plus:
            firstInput = self.automataStack.pop()
            self.automataStack.append(createNFA.plusStructure(firstInput))

        #CASE 3: if the operator is concat or OR then it needs two inputs to work on. So it pops the first two inputs and save them and send each one fo them to the suitable structure.
        elif operator in self.operators:
            if len(self.automataStack) < 2:         #if the automataStack has less than two inouts and we need two inputs then an exception will be raised.
                raise BaseException("Error processing operator '%s'. Inadequate operands" % operator)
            firstInput = self.automataStack.pop()
            secondInput = self.automataStack.pop()
            if operator == self.oring:
                self.automataStack.append(createNFA.orStructure(secondInput, firstInput))
            elif operator == self.concat:
                self.automataStack.append(createNFA.concatStructure(secondInput, firstInput))

    def getNFA(self):
        return self.nfa
    
    def displayNFA(self):
        self.nfa.display()

#Class for building the DFA from the NFA that is created previously
class DFAfromNFA:

    def __init__(self, nfa):
        self.buildDFA(nfa)

    def getDFA(self):
        return self.dfa

    def displayDFA(self):
        self.dfa.displayInCLI()

    def buildDFA(self, nfa):                            #Method that builds the dfa from the nfa and displays it and this will be the final step.
        eClosureStates = dict()
        eclose = dict()
        count = 1
        state1 = nfa.getEpsilonClosure(nfa.startState)          # combine the initial state with any other state with the transition epsilon
        eclose[nfa.startState] = state1                                    # dict of nfa states + eclosure
        dfa = AutomataLanguage(nfa.language)
        dfa.setStartState(count)
        states = [[state1, count]]                                              # one element dict of dfa states + eclosure
        eClosureStates[count] = state1                                    # all elements dict of dfa states + eclosure
        count +=  1
        while len(states) != 0:                         #loop on the states until they are all done
            [state, fromindex] = states.pop()   #get the first state with its index and pop it from the states to not be repeated again
            for char in dfa.language:               #for each state we have, we loop on the characters and the alphabets that we have until we finish them.
                transStates = nfa.getStateTransitions(state, char)      #get the transition of the state that we have and save its target states in transStates.
                for s in list(transStates)[:]:        #loop on the transStates
                    if s not in eclose:
                        eclose[s] = nfa.getEpsilonClosure(s)            # combine two states when any state is connected with epsilon with another state.
                    transStates = transStates.union(eclose[s])
                if len(transStates) != 0:               #link the states with next state with its index if it is not present in any created state from before.
                    if transStates not in eClosureStates.values():
                        states.append([transStates, count])
                        eClosureStates[count] = transStates
                        toindex = count
                        count +=  1
                    else:                                   #if a state is present in any created state before then we should connect to the created state and not create a new one
                        toindex = [k for k, v in eClosureStates.items() if v  ==  transStates][0]       # search in the allstates to connect the current state to the already existing state
                    dfa.transitionStates(fromindex, toindex, char)
        for value, state in eClosureStates.items():                     #loop on the states at the end and any state that is final in the NFA, make it final in the DFA
            if nfa.finalStates[0] in state:
                dfa.setFinalStates(value)
        self.dfa = dfa


def drawGraph(AutomataLanguage, file = ""):
    f = popen(r"dot -Tpng -o graph%s.png" % file, 'w')     #popen function or method opens a pipe from this command the pipe allows the command to send
                                                                                                                                 #its ouput to another command this is done to generate the png file from this command line
    try:
        f.write(AutomataLanguage.getDotFile())
    except:
        raise BaseException("Error creating graph")
    finally:
        f.close()

