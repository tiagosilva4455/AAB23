# -*- coding: utf-8 -*-
"""
@author: miguelrocha
"""

def createMatZeros (nl:int, nc:int)->list[list[int]]:
    """
    @brief Função que cria uma matriz de zeros com o número de linhas e colunas especificado 
    @param nl (int): Número de linhas da matriz
    @param nc (int): Número de colunas da matriz.  
    @return List[int]: Matriz de zeros com o número de linhas e colunas especificado
    """
    res = [ ] 
    for i in range(0, nl):
        res.append([0]*nc)
    return res

def printMat(mat:list[list[int]])->None:
    """
    @brief Printa a matriz 
    @param mat (List[List[int]]): Matriz a ser printada
    @return None
    """
    for i in range(0, len(mat)): print(mat[i])

class MyMotifs:

    def __init__(self, seqs:list[str])->None:
        """
        @brief Construtor da class MyMotifs
        @param seqs: Lista de sequências 
        """
        self.size = len(seqs[0])
        self.seqs = seqs # objetos classe MySeq
        self.alphabet = seqs[0].alfabeto()
        self.doCounts()
        self.createPWM()
        
    def __len__ (self)->int:
        """
        @brief Função que retorna o tamanho do conjunto de sequências dadas
        @return Tamanho das sequências
        """
        return self.size        
        
    def doCounts(self)->None:
        """
        @brief Calcula a contagem de cada base por posição e guarda a matriz de contagem em 'self.counts'
        """
        self.counts = createMatZeros(len(self.alphabet), self.size)
        for s in self.seqs:
            for i in range(self.size):
                lin = self.alphabet.index(s[i])
                self.counts[lin][i] += 1
                
    def createPWM(self)->None:
        """
        @brief Calcula e armazena a matriz PWM (Position Weight Matrix) do conjunto de sequências. Esta matriz é calculada a partir da matriz de contagem armazenada em 'self.counts'.
        """
        if self.counts == None: self.doCounts()
        self.pwm = createMatZeros(len(self.alphabet), self.size)
        for i in range(len(self.alphabet)):
            for j in range(self.size):
                self.pwm[i][j] = float(self.counts[i][j]) / len(self.seqs)
                
    def consensus(self)->str:
        """
        @brief Retorna a sequência de consenso para o conjunto de sequências
        @return Sequência de consenso
        """
        res = ""
        for j in range(self.size):
            maxcol = self.counts[0][j]
            maxcoli = 0
            for i in range(1, len(self.alphabet) ):
                if self.counts[i][j] > maxcol: 
                    maxcol = self.counts[i][j]
                    maxcoli = i
            res += self.alphabet[maxcoli]        
        return res

    def maskedConsensus(self)->str:
        """
        @brief Retorna a sequência de consenso para o conjunto de sequências de DNA, onde as posições com contagem abaixo de 50% da contagem total das sequências são substituídas por '-'.
        @return str: Sequência de consenso com posições abaixo do limiar substituídas por '-'
        """
        res = ""
        for j in range(self.size):
            maxcol = self.counts[0][j]
            maxcoli = 0
            for i in range(1, len(self.alphabet) ):
                if self.counts[i][j] > maxcol: 
                    maxcol = self.counts[i][j]
                    maxcoli = i
            if maxcol > len(self.seqs) / 2:
                res += self.alphabet[maxcoli]        
            else:
                res += "-"
        return res

    def probabSeq (self, seq:str)->float:
        """
        @brief Calcula a probabilidade de uma sequência ser gerada pela matriz PWM
        @param seq: Sequência de DNA a ser avaliada
        @return Probabilidade da sequência ser gerada pela matriz PWM
        """
        res = 1.0
        for i in range(self.size):
            lin = self.alphabet.index(seq[i])
            res *= self.pwm[lin][i]
        return res
    
    def probAllPositions(self, seq:str)->list[float]:
        """
        @brief Calcula a probabilidade do motivo aparecer em cada posição possível da sequência especificada
        @param seq: sequência de DNA na qual procurar o motif
        @return: lista de probabilidade do motif aparecer em cada posição possível
        """
        res = []
        for k in range(len(seq)-self.size+1):
            res.append(self.probabSeq(seq))
        return res

    def mostProbableSeq(self, seq:str)->int:
        """
        Encontra a posição mais provável para o motf na sequência especificada
        @param seq: sequência de DNA na qual procurar o motif
        @return: index da posição mais provável para o motif
        """
        maximo = -1.0
        maxind = -1
        for k in range(len(seq)-self.size):
            p = self.probabSeq(seq[k:k+ self.size])
            if(p > maximo):
                maximo = p
                maxind = k
        return maxind

def test():
    # test
    from MySeq import MySeq
    seq1 = MySeq("AAAGTT")
    seq2 = MySeq("CACGTG")
    seq3 = MySeq("TTGGGT")
    seq4 = MySeq("GACCGT")
    seq5 = MySeq("AACCAT")
    seq6 = MySeq("AACCCT")
    seq7 = MySeq("AAACCT")
    seq8 = MySeq("GAACCT")
    lseqs = [seq1, seq2, seq3, seq4, seq5, seq6, seq7, seq8]
    motifs = MyMotifs(lseqs)
    printMat (motifs.counts)
    printMat (motifs.pwm)
    print(motifs.alphabet)
    
    print(motifs.probabSeq("AAACCT"))
    print(motifs.probabSeq("ATACAG"))
    print(motifs.mostProbableSeq("CTATAAACCTTACATC"))
    
    print(motifs.consensus())
    print(motifs.maskedConsensus())

if __name__ == '__main__':
    test()
