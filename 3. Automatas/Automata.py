# -*- coding: utf-8 -*-


class Automata:
    
    def __init__(self, alphabet:list[str], pattern:str)->None:
        """
        @brief Construtor da class Automata
        @param alphabet: alfabeto
        @param pattern: padrão da sequência
        """
        self.numstates = len(pattern) + 1
        self.alphabet = alphabet
        self.pattern = pattern
        self.transitionTable = {}
        self.buildTransitionTable()        
    
    def buildTransitionTable(self)->None:
        '''
        @brief Cria a tabela das transições, em que as chaves são tuplos e os valores representam o next state
        '''
        def overlap(s1:str, s2:str)->None:
            """
            @brief Função usada para verificar se duas sequências têm um prefixo comum
            @param s1: sequência 1
            @param s2: sequência 2
            """
            maxov = min(len(s1), len(s2))  #comprimento das duas sequências de entrada
            for i in range(maxov, 0, -1):
                if s1[-i:] == s2[:i]: return i  #compara os últimos "i" caracteres de s1 com os primeiros "i" caracteres de s2, Se eles forem iguais, a função retorna o valor de "i", que é o comprimento do maior prefixo comum entre as duas sequências
            return 0 #se nenhum prefixo comum for encontrado, a função retorna 0

        for q in range(self.numstates): #por cada caractere no padrão
            for a in self.alphabet:   #por cada simbolo do alfabeto
                pref = self.pattern[0:q] + a #padrão que corresponde a esse estado e símbolo de entrada
                hit = overlap(pref,self.pattern) #encontrar o comprimento do maior prefixo comum entre essa string "pref" e o padrão completo que o autómato procura
                self.transitionTable[(q,a)] = hit #valor retornado pela função overlap é armazenado na tabela de transição na posição correspondente ao estado e símbolo de entrada
       
    def printAutomata(self)->None:
        """
        @brief Função que imprime o estado, o alfabeto e a tabela de transição
        """
        print ("States: " , self.numstates)
        print ("Alphabet: " , self.alphabet)
        print ("Transition table:")
        for k in self.transitionTable.keys():
            print (k[0], ",", k[1], " -> ", self.transitionTable[k])
         
    def nextState(self, current:int, symbol:str)->int:
        """
        @brief Vai à tabela de transições e, de acordo com o símbolo atual, altera o seu estado
        @param current: estado atual
        @param symbol: nucleótido a analisar
        @returns valor inteiro representativo do estado
        """
        return self.transitionTable.get((current, symbol)) #current - estado atual; symbol - simbolo de sequencia 
    #Poe se 2 parenteses porque a nossa key é o tuplo estado corrente e o symbolo que queremos analisar
        
    def applySeq(self, seq:str)->list[int]:
        """
        @brief Processa a sequência e devolve uma lista dos estados, iniciando no estado zero
        @param seq: sequência a processar
        @returns  devolve uma lista de inteiros que representa os estados visitados pelo autómato durante o processamento
        """
        q = 0
        res = [q]
        for n in seq:
            q = self.nextState(q, n) #o próximo estado é armazenado na variável q
            res.append(q) #adiciona-se à lista res que contém todos os estados visitados até o momento
        return res
        
    def occurencesPattern(self, text:str)->list[int]: # posiçoes onde iniciam os p
        """
        @brief Função que devolve a lista de indices das posições iniciais dos padrões
        @param text: sequência a analisar
        @returns lista de índices das posições iniciais de onde se encontra o padrão
        """
        q = 0 
        res = []
        for n in range(len(text)):
            q = self.nextState(q, text[n]) #obtem o próximo estado do autómato, dado o estado atual e o símbolo do alfabeto de entrada
            if q == self.numstates-1: #se o próximo estado for o estado final do autómato, significa que o padrão foi encontrado na posição atual da sequência
                res.append(n-self.numstates+2) #adiciona a posição inicial do padrão (calculada como n-self.numstates+2) à lista res que contém todas as posições iniciais onde o padrão é encontrado
        return res


def test():
    auto = Automata("AC", "ACA")
    auto.printAutomata()
    print (auto.applySeq("CACAACAA"))
    print (auto.occurencesPattern("CACAACAA"))

#test()

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





