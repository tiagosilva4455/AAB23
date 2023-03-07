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
    def __init__(self, popsize, numits, noffspring, filename, indsize):
        self.motifs = MotifFinding()
        self.motifs.readFile(filename,"dna")
        indsize = self.motifs.motifSize * len(self.motifs.alphabet)
        EvolAlgorithm.__init__(self, popsize, noffspring, numits, indsize)

    def initPopul(self, indsize):
        maxvalue = self.motifs.seqSize(0) - self.motifs.motifSize
        minvalue = 0
        self.popul=PopulReal(self.popsize, indsize, minvalue, maxvalue, [])
    
    def pwmReal(self, vector):
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
    
    def evaluate(self, indivs):
        for x in range(len(indivs)):
            ind = indivs[x]
            gen = ind.getGenes()
            pwm = self.pwmReal(gen)
            mymotifs = MyMotifs(pwm = pwm, alphabet=self.motifs.alphabet)
        
            pos=[]
            for seq in self.motifs.seqs:
                p = mymotifs.mostProbableSeq(seq)
                pos.append(p)
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
