# -*- coding: utf-8 -*-
"""

"""

from MySeq import MySeq
from MyMotifs import MyMotifs


class MotifFinding:
    
    def __init__(self, size:int = 8, seqs:list = None)-> None:
        """
        Construtor com os atributos necessários para a class MotifFinding

        Args:
            size: vê o tamanho do motif, em caso de não ser definido recebe o valor 8
            seqs: lista com as sequências, recebe None se não forem dadas sequências e teremos uma lista vazia
        """
        self.motifSize = size
        if (seqs != None):
            self.seqs = seqs
            self.alphabet = seqs[0].alfabeto()
        else:
            self.seqs = []
                    
    def __len__ (self) -> int:
        """
        Indica o número de elementos/sequências presentes na lista self.seqs
        Returns:
            Devolve o número de elementos da lista
        """
        return len(self.seqs)
    
    def __getitem__(self, n) -> str:
        """
        Interface para a indexação []
        """
        return self.seqs[n]
    
    def seqSize (self, i: int) -> int:
        """
        Comprimento da sequência i que está presente na lista self.seqs
        """
        return len(self.seqs[i])
    
    def readFile(self, fic:str, t:str) -> None:
        """
        Função que lê ("r") um ficheiro, separa por espaços cada sequência (strip), e adiciona cada sequência à lista self.seqs
        Args:
            fic : ficheiro a ser lido
            t : tipo de sequência
        """
        for s in open(fic, "r"):
            self.seqs.append(MySeq(s.strip().upper(),t))
        self.alphabet = self.seqs[0].alfabeto()
        
        
    def createMotifFromIndexes(self, indexes:int) -> list:
        """
        Crição de uma matriz, a partir da definição da posição onde o motif começará a ser contado e onde termina, identificando o seu tipo (t). 
        Esta info é adicionada à lista pseqs, que é uma lista de motifs
        Args:
            indexes : indica a posição pela qual vamos começar a contar o motif
        """
        pseqs = []
        for i,ind in enumerate(indexes):
            pseqs.append( MySeq(self.seqs[i][ind:(ind+self.motifSize)], self.seqs[i].tipo) )
        return MyMotifs(pseqs)
        
        
    # SCORES
        
    def score(self, s:int) -> list:
        score = 0
        motif = self.createMotifFromIndexes(s)
        motif.doCounts()
        mat = motif.counts
        for j in range(len(mat[0])):   #colunas da matriz
            maxcol = mat[0][j]          #a cada ronda, define que aquela coluna é maxima e a primeira linha
            for  i in range(1, len(mat)):   
                if mat[i][j] > maxcol:   #se houver outra linha da coluna máxima que seja maior que a definida antes, admitimos nova maxcol
                    maxcol = mat[i][j]
            score += maxcol             #adiciona o valor de cada coluna ao score
        return score                    #lista das várias colunas com valores maiores das linhas = score
   
    def scoreMult(self, s):
        """
        Acho que é o mesmo de cima mas com PWM not sure
        """
        score = 1.0
        motif = self.createMotifFromIndexes(s)
        motif.createPWM()
        mat = motif.pwm
        for j in range(len(mat[0])):
            maxcol = mat[0][j]
            for  i in range(1, len(mat)):
                if mat[i][j] > maxcol: 
                    maxcol = mat[i][j]
            score *= maxcol
        return score     
       
    # EXHAUSTIVE SEARCH
       
    def nextSol (self, s):
        nextS = [0]*len(s)
        pos = len(s) - 1     
        while pos >=0 and s[pos] == self.seqSize(pos) - self.motifSize:
            pos -= 1
        if (pos < 0): 
            nextS = None
        else:
            for i in range(pos): 
                nextS[i] = s[i]
            nextS[pos] = s[pos]+1;
            for i in range(pos+1, len(s)):
                nextS[i] = 0
        return nextS
        
    def exhaustiveSearch(self):
        """
        Calcula o score de cada possível vetor de posições
        """
        melhorScore = -1
        res = []
        s = [0]* len(self.seqs)
        while (s!= None):
            sc = self.score(s)
            if (sc > melhorScore):
                melhorScore = sc
                res = s
            s = self.nextSol(s)
        return res
     
    # BRANCH AND BOUND     
     
    def nextVertex (self, s):
        res =  []
        if len(s) < len(self.seqs): # internal node -> down one level
            for i in range(len(s)): 
                res.append(s[i])
            res.append(0)
        else: # bypass
            pos = len(s)-1 
            while pos >=0 and s[pos] == self.seqSize(pos) - self.motifSize:
                pos -= 1
            if pos < 0: res = None # last solution
            else:
                for i in range(pos): res.append(s[i])
                res.append(s[pos]+1)
        return res
    
    
    def bypass (self, s):
        res =  []
        pos = len(s) -1
        while pos >=0 and s[pos] == self.seqSize(pos) - self.motifSize:
            pos -= 1
        if pos < 0: res = None 
        else:
            for i in range(pos): res.append(s[i])
            res.append(s[pos]+1)
        return res
        
    def branchAndBound (self):
        melhorScore = -1
        melhorMotif = None
        size = len(self.seqs)
        s = [0]*size
        while s != None:
            if len(s) < size:
                optimScore = self.score(s) + (size-len(s)) * self.motifSize
                if optimScore < melhorScore: s = self.bypass(s)
                else: s = self.nextVertex(s)
            else:
                sc = self.score(s)
                if sc > melhorScore:
                    melhorScore = sc
                    melhorMotif  = s
                s = self.nextVertex(s)
        return melhorMotif

    # Consensus (heuristic)
  
    def heuristicConsensus(self)->list[int]:
        """
        Considera apenas as duas primeiras sequências, escolhe as posições inicias que dão um melhor score, e isto dá o melhor score parcial.
        Depois itera para as restantes sequências e seleciona a posição que maximiza o score.
        """
        #Passo 1: Considerando apenas as duas primeiras sequências, escolher as posições iniciais s1 e s2 que dão um melhor score (melhor contribuição parcial para o score, i.e. considerando que existem apenas estas duas sequências).
        find = MotifFinding(self.motifSize, self.seqs[:2])
        es = find.exhaustiveSearch()

        #Passo 2: Para cada uma das sequências seguintes (i=3, …,t) , de forma iterativa, escolher a melhor posição inicial na sequência i, de forma a maximizar o score, considerando as posições anteriores fixas
        for p in range(2, len(self.seqs)):
            es.append(p)
            max_score = -1
            bestpos = 0
            for g in range (self.seqSize(p)-self.motifSize+1):
                es[p] = g   #vetor das posições
                score = self.score(es)
                if score > max_score:
                    max_score = score
                    bestpos = g
                es[p] = bestpos
        return es

    def heuristicStochastic (self):
        #...

        return None

    # Gibbs sampling 


        
    def gibbs (self, iterations:int) -> list[int]:
        """
        Implementa o algoritmo de Gibbs Sampling
        
        Args:
            Interations : número inteiro de iterações 

        Returns:
            best_score: float do melhor score até ao fim da ultima iteração
            s: lista das posições inicias dos motifs nas sequências

        Returns:

        """
        from random import randint
        
        seqPos = []
        for i in range(0, len(self.seqs)):
            randPos = (randint(0, self.seqSize(i)-self.motifSize-1))
            seqPos.append(randPos)
        best_score = self.scoreMult(seqPos) #calcula o score com base nas seqs da lista s

        x=0
        while x<iterations:
            x+=1

            randSeq = randint(0, (len(self.seqs)-1)) #Passo 2
           
            random = self.seqs[randSeq]
            seqNoRandom = self.seqs.pop(randSeq)  #remove-se a sequência escolhida aleatoriamente anteriormente
            aux_seq_list = seqPos.copy()  #lista auxiliar com todas as posições
            aux_seq_list.pop(randSeq)  #remover a posição da sequência escolhida aleatoriamente na lista s com as posições iniciais
            pwm = self.createMotifFromIndexes(aux_seq_list)#criação do perfil sem a sequência removida
            pwm.createPWM() 

            probPos= pwm.probAllPositions(random) #Obter a melhor posição
            self.seqs.insert(randSeq,seqNoRandom)#Inserir a sequencia aleatoria 
            pos = self.roulette(probPos)
            aux_seq_list.insert(randSeq,pos)
            new_score = self.scoreMult(aux_seq_list)
               
            if  new_score > best_score: #Verifica se houve melhoria  
                best_score = new_score
                best_s = list(seqPos)
        return best_score, best_s

    def roulette(self, f):
        from random import random
        tot = 0.0
        for x in f: tot += (0.01+x)
        val = random()* tot
        acum = 0.0
        ind = 0
        while acum < val:
            acum += (f[ind] + 0.01)
            ind += 1
        return ind-1

# tests

def test1():  
    sm = MotifFinding()
    sm.readFile("exemploMotifs.txt","dna")
    sol = [25,20,2,55,59]
    sa = sm.score(sol)
    print(sa)
    scm = sm.scoreMult(sol)
    print(scm)

def test2():
    print ("Test exhaustive:")
    seq1 = MySeq("ATAGAGCTGA","dna")
    seq2 = MySeq("ACGTAGATGA","dna")
    seq3 = MySeq("AAGATAGGGG","dna")
    mf = MotifFinding(3, [seq1,seq2,seq3])
    sol = mf.exhaustiveSearch()
    print ("Solution", sol)
    print ("Score: ", mf.score(sol))
    print("Consensus:", mf.createMotifFromIndexes(sol).consensus())

    print ("Branch and Bound:")
    sol2 = mf.branchAndBound()
    print ("Solution: " , sol2)
    print ("Score:" , mf.score(sol2))
    print("Consensus:", mf.createMotifFromIndexes(sol2).consensus())
    
    print ("Heuristic consensus: ")
    sol1 = mf.heuristicConsensus()
    print ("Solution: " , sol1)
    print ("Score:" , mf.score(sol1))

def test3():
    mf = MotifFinding()
    mf.readFile("exemploMotifs.txt","dna")
    print ("Branch and Bound:")
    sol = mf.branchAndBound()
    print ("Solution: " , sol)
    print ("Score:" , mf.score(sol))
    print("Consensus:", mf.createMotifFromIndexes(sol).consensus())

def test4():
    mf = MotifFinding()
    mf.readFile("exemploMotifs.txt","dna")
    print("Heuristic stochastic")
    sol = mf.heuristicStochastic()
    print ("Solution: " , sol)
    print ("Score:" , mf.score(sol))
    print ("Score mult:" , mf.scoreMult(sol))
    print("Consensus:", mf.createMotifFromIndexes(sol).consensus())
    
    sol2 = mf.gibbs(1000)
    print ("Score:" , mf.score(sol2))
    print ("Score mult:" , mf.scoreMult(sol2))

#test4()
