# -*- coding: utf-8 -*-


class Automata:
    
    def __init__(self, alphabet, pattern):
        self.numstates = len(pattern) + 1
        self.alphabet = alphabet
        self.pattern = pattern
        self.transitionTable = {}
        self.buildTransitionTable()        
    
    def buildTransitionTable(self):
        '''
        Cria a tabela das transições, em que as chaves são tuplos e os valores representam o next state
        '''
        for q in range(self.numstates):
            for a in self.alphabet:
                pref = self.pattern[0:q] + a 
                hit = overlap(pref,self.pattern)
                self.transitionTable[(q,a)] = hit
       
    def printAutomata(self):
        print ("States: " , self.numstates)
        print ("Alphabet: " , self.alphabet)
        print ("Transition table:")
        for k in self.transitionTable.keys():
            print (k[0], ",", k[1], " -> ", self.transitionTable[k])
         
    def nextState(self, current:int, symbol:str)->int:
        """
        Vai à tabela de transições e, de acordo com o símbolo atual, altera o seu estado
        Args:
            current: estado atual
            symbol: nucleótido a analisar
        Returns:
            valor inteiro representativo do estado
        """
        return self.transitionTable.get((current, symbol)) #current - estado atual; symbol - simbolo de sequencia 
    
    #Poe se 2 parenteses porque a nossa key é o tuplo estado corrente e o symbolo que queremos analisar
        
    def applySeq(self, seq:str)->list[int]:
        """
        Processa a sequência e devolve uma lista dos estados, iniciando no estado zero
        Args:
            seq: sequência a processar
        Returns:
            lista de inteiros com os estados da sequência
        """
        q = 0
        res = [q]
        for n in seq:
            q = self.nextState(q, n)
            res.append(q)
        return res
        
    def occurencesPattern(self, text:str)->list[int]: # posiçoes onde iniciam os p
        """
        Função que devolve a lista de indices das posições iniciais dos padrões
        Args:
            text: sequência a analisar
        Returns:
            lista de índices das posições iniciais de onde se encontra o padrão
        """
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





