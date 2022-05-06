# Regular expressions to DFA

## Overview 
A  program to build DFA of a given regular expression entered by user.

## Language
Python

## Instructions
* You can run the program by entering th regular expression on your terminal for example: Python DisplayWithCLI.py "(0+1) * 01 * 0"

* The generated DFA will be displayed as a png in the same folder

## Structure
The code is divided into 4 classes which are 
* AutomataLanguage: It is mainly implemented to define the start state, final states. And to create the transitions, display the output, also visualize the final DFA.
* createNFA: implemented to define the operations that can connect the states as the concatenation, OR and the 2 types of Repetition ( * ),( + ).
* RegexToNFA: to convert the regular expression to NFA, scan input and handles errors, and display the built NFA.
* DFAfromNFA: for building the DFA from the NFA that is created previously.
