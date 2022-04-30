from RegexToDFA import *
import sys

def main():
    inp = "(01*1)*1"
    if len(sys.argv)>1:
        inp = sys.argv[1]
    print ("Regular Expression: ", inp)
    nfaObj = RegexToNFA(inp)
    nfa = nfaObj.getNFA()
    dfaObj = DFAfromNFA(nfa)
    dfa = dfaObj.getDFA()
    print ("\nDFA: ")
    dfaObj.displayDFA()

    drawGraph(dfa, "dfa")

    print ("\nGraphs have been created in the code directory")


if __name__  ==  '__main__':
    t = time.time()
    try:
        main()
    except BaseException as e:
        print ("\nFailure:", e)
    print ("\nExecution time: ", time.time() - t, "seconds")
