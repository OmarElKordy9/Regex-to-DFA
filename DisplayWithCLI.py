from RegexToDFA import *
import sys

def main():
    inp = "(01*1)*1"                        #if the user didn't enter any input then this should be a dummy input to use
    if len(sys.argv)>1:                     #if the user entered an input then this input will be saved and sent to the functions
        inp = sys.argv[1]
    print ("Regular Expression: ", inp)     #first we print to the user regex that he entered
    nfaObj = RegexToNFA(inp)                #then we send this input to create the NFA
    nfa = nfaObj.getNFA()                       #after that we get the created NFA and store it in variable nfa
    dfaObj = DFAfromNFA(nfa)               #the variable nfa is then sent to the function DFAfromNFA to create the DFA
    dfa = dfaObj.getDFA()                       #after this we get the created DFA and store it in the variable dfa

    print ("\nDFA: ")
    dfaObj.displayDFA()

    drawGraph(dfa, "dfa")

    print ("\nGraph is created in a png in the file explorer in the left of the window")

if __name__  ==  '__main__':
    executuionTime = time.time()
    try:
        main()
    except BaseException as e:
        print ("\nFailure:", e)
    print ("\nExecution time: ", time.time() - executuionTime, "seconds")                #show the execution time of the program
