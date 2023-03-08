# -*- coding: utf-8 -*-


class Automata:
    
    def __init__(self, alphabet, pattern):
        self.numstates = len(pattern) + 1
        self.alphabet = alphabet
        self.transitionTable = {}
        self.buildTransitionTable(pattern)        
    
    def buildTransitionTable(self, pattern):
        for q in range(self.numstates):
            for a in self.alphabet:
                pref = pattern[0:q] + a 
                hit = overlap(pref,pattern)
                self.transitionTable[(q,a)] = hit
       
    def printAutomata(self):
        print ("States: " , self.numstates)
        print ("Alphabet: " , self.alphabet)
        print ("Transition table:")
        for k in self.transitionTable.keys():
            print (k[0], ",", k[1], " -> ", self.transitionTable[k])
         
    def nextState(self, current, symbol):
        return self.transitionTable.get((current, symbol)) #current - estado atual; symbol - simbolo de sequencia 
    
    #Poe se 2 parenteses porque a nossa key é o tuplo estado corrente e o symbolo que queremos analisar
        
    def applySeq(self, seq):
        q = 0
        res = [q]
        for n in seq:
            q = self.nextState(q, n)
            res.append(q)
        return res
        
    def occurencesPattern(self, text): # posiçoes onde iniciam os p
        q = 0 
        res = []
        for n in range(len(text)):
            q = self.nextState(q, text[n])
            if q == self.numstates-1: 
                res.append(n-self.numstates+2)
        return res

def overlap(s1, s2):
    maxov = min(len(s1), len(s2))
    for i in range(maxov,0,-1):
        if s1[-i:] == s2[:i]: return i
    return 0
               
def test():
    auto = Automata("AC", "ACA")
    auto.printAutomata()
    print (auto.applySeq("CACAACAA"))
    print (auto.occurencesPattern("CACAACAA"))

test()

#States:  4
#Alphabet:  AC
#Transition table:
#0 , A  ->  1
#0 , C  ->  0
#1 , A  ->  1
#1 , C  ->  2
#2 , A  ->  3
#2 , C  ->  0
#3 , A  ->  1
#3 , C  ->  2
#[0, 0, 1, 2, 3, 1, 2, 3, 1]
#[1, 4]



