from EvolAlgorithm import EvolAlgorithm
from Popul import PopulInt, PopulReal
from MotifFinding import MotifFinding
from MyMotifs import MyMotifs


def createMatZeros(nl, nc):
    res = []
    for _ in range(0, nl):
        res.append([0]*nc)
    return res


def printMat(mat):
    for i in range(0, len(mat)):
        for j in range(len(mat[i])):
            print(f"{mat[i][j]:.3f}", end=' ')
        print()


class EAMotifsInt (EvolAlgorithm):
    def __init__(self, popsize, numits, noffspring, filename):
        self.motifs = MotifFinding()
        self.motifs.readFile(filename, "dna")
        indsize = len(self.motifs)
        EvolAlgorithm.__init__(self, popsize, numits, noffspring, indsize)

    def initPopul(self, indsize):
        maxvalue = self.motifs.seqSize(0) - self.motifs.motifSize
        self.popul = PopulInt(self.popsize, indsize,
                              maxvalue, [])

    def evaluate(self, indivs):
        for i in range(len(indivs)):
            ind = indivs[i]
            sol = ind.getGenes()
            fit = self.motifs.score(sol)
            ind.setFitness(fit)

#Alterado
class EAMotifsReal (EvolAlgorithm):
    """
    Classe que devolve o melhor valor de fitness de uma população real
    """
    def __init__(self, popsize:int, numits:int, noffspring:int, filename:str, indsize:int)->None:
        """
        Args:
            popsize: valor inteiro que indica o valor da população
            numits: número de iterações
            noffspring: número de descendentes
            filename: ficheiro que contém as sequências
            indsize: valor inteiro que indica o tamanho do indivíduo
        """
        self.motifs = MotifFinding()
        self.motifs.readFile(filename,"dna")
        indsize = self.motifs.motifSize * len(self.motifs.alphabet)
        EvolAlgorithm.__init__(self, popsize, noffspring, numits, indsize)

    def initPopul(self, indsize:int)->None:
        """
        Cria uma população real
        Args:
            indsize: valor inteiro que indica o tamanho do indivíduo
        """
        maxvalue = self.motifs.seqSize(0) - self.motifs.motifSize
        minvalue = 0
        self.popul=PopulReal(self.popsize, indsize, minvalue, maxvalue, [])
    
    def pwmReal(self, vector:list[int])-> list[float]:
        """
        Cria uma PWM de dimensão (tamanho do motif, número de símbolos do alfabeto do indivíduo)
        Args:
            vector: lista de genes do indivíduo
        Returns:
            lista correspondente à PWM
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
    
    def evaluate(self, indivs:list[int]):
        """
        Avalia qual é o melhor fitness da população
        Args:
            indivs: 
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
