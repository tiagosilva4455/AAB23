from EvolAlgorithm import EvolAlgorithm
from Popul import PopulInt, PopulReal
from MotifFinding import MotifFinding
from MyMotifs import MyMotifs


def createMatZeros(nl:int, nc:int)->list[int]:
    """
    @brief Cria uma matriz de zeros
    @param nl: número de linhas
    @param nc: número de colunas
    @returns lista de zeros, que corresponde à matriz
    """
    res = []
    for _ in range(0, nl):
        res.append([0]*nc)
    return res


def printMat(mat:list)->None:
    """
    @brief Função que imprime a matriz
    @param mat: matriz
    """
    for i in range(0, len(mat)):
        for j in range(len(mat[i])):
            print(f"{mat[i][j]:.3f}", end=' ')
        print()


class EAMotifsInt (EvolAlgorithm):
    """
    @brief Classe que devolve o melhor valor de fitness de uma população, herdando os métodos da class EvolAlgorithm
    """
    def __init__(self, popsize:int, numits:int, noffspring:int, filename:str)->None:
        """
        @brief Construtor da class EAMotifsInt
        @param popsize: indica o tamanho da população
        @param numits: indica o número de iterações
        @param noffspring: indica o númerode novos descendentes
        @param filename: indica o nome do ficheiro que vamos ler
        @return None
        """
        self.motifs = MotifFinding()
        self.motifs.readFile(filename, "dna")
        indsize = len(self.motifs)
        EvolAlgorithm.__init__(self, popsize, numits, noffspring, indsize)

    def initPopul(self, indsize:int)->None:
        """
        @brief Gera uma nova população
        @param indsize: indica o tamanho do indivíduo
        """
        maxvalue = self.motifs.seqSize(0) - self.motifs.motifSize
        self.popul = PopulInt(self.popsize, indsize,
                              maxvalue, [])

    def evaluate(self, indivs:list[int])->None:
        """
        @brief Função de avaliação, em que usamos o score, do melhor fitness da população
        @param indivs: indivíduos
        """
        for i in range(len(indivs)):
            ind = indivs[i]  #cada vetor de posições
            sol = ind.getGenes()
            fit = self.motifs.score(sol)  #avalia o score que será o fit para cada vetor de posições iniciais
            ind.setFitness(fit)

#ALTERADO
class EAMotifsReal (EvolAlgorithm):
    """
    @brief Classe que devolve o melhor valor de fitness de uma população real
    """
    def __init__(self, popsize:int, numits:int, noffspring:int, filename:str, indsize:int)->None:
        """
        @brief Contrutor da class EAMotifsReal
        @param popsize: valor inteiro que indica o valor da população
        @param numits: indica o número de iterações
        @param noffspring: indica o número de descendentes
        @param filename: ficheiro que vamos ler que contém as sequências
        @param indsize: valor inteiro que indica o tamanho do indivíduo
        """
        self.motifs = MotifFinding()
        self.motifs.readFile(filename,"dna")
        indsize = self.motifs.motifSize * len(self.motifs.alphabet)
        EvolAlgorithm.__init__(self, popsize, noffspring, numits, indsize)

    def initPopul(self, indsize:int)->None:
        """
        @brief Função que cria uma população real
        @params indsize: valor inteiro que indica o tamanho do indivíduo
        """
        maxvalue = self.motifs.seqSize(0) - self.motifs.motifSize
        minvalue = 0
        self.popul=PopulReal(self.popsize, indsize, minvalue, maxvalue, [])
    
    def pwmReal(self, vector:list[int])-> list[float]:
        """
        @brief Cria uma PWM de dimensão (tamanho do motif, número de símbolos do alfabeto do indivíduo)
        @params vector: lista de genes do indivíduo
        @returns lista correspondente à PWM
        """
        tamMotif = self.motifs.motifSize
        tamAlphabet = len(self.motifs.alphabet)

        mat_zero = createMatZeros(tamAlphabet, tamMotif)

        for x in range(0, len(vector), tamAlphabet):
            columnIndex = int(x/tamAlphabet)
            column = vector[x:x+tamAlphabet]
            delSum = sum(column)

            for y in range(tamAlphabet):
                mat_zero[y][columnIndex] =column[y]/delSum

        pwm = mat_zero

        return pwm
    
    def evaluate(self, indivs:list[int])->None:
        """
        @brief Função que avalia qual é o melhor fitness da população
        @params indivs: lista de indivíduos 
        """
        for x in range(len(indivs)):
            ind = indivs[x]
            gen = ind.getGenes()
            pwm = self.pwmReal(gen)
            mymotifs = MyMotifs(pwm = pwm, alphabet=self.motifs.alphabet)

            pos = [mymotifs.mostProbableSeq(seq) for seq in self.motifs.seqs]
            #pos=[]
            #for seq in self.motifs.seqs:
            #    p = mymotifs.mostProbableSeq(seq)
            #   pos.append(p)
            fit = self.motifs.score(pos)
            ind.setFitness(fit)


def test1():
    ea = EAMotifsInt(100, 1000, 50, "exemploMotifs.txt")
    ea.run()
    ea.printBestSolution()


def test2():
    ea = EAMotifsReal(100, 2000, 50, "exemploMotifs.txt", 2)
    ea.run()
    ea.printBestSolution()


#test1()
test2()
