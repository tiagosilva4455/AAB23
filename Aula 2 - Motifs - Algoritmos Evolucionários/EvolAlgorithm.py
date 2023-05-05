from Popul import Popul


class EvolAlgorithm:

    def __init__(self, popsize:int, numits:int, noffspring:int, indsize:int)->None:
        """
        @brief Construtor da class EvolAlgorithm
        @param popsize: indica o tamanho da população
        @param numits: indica o número de iterações
        @param noffspring: indica o númerode novos descendentes
        @param indsize: indica o tamanho dos indivíduos
        @returns None
        """
        self.popsize = popsize
        self.numits = numits
        self.noffspring = noffspring
        self.indsize = indsize

    def initPopul(self, indsize:int)>None:
        """
        @brief Gera uma nova população
        @param indsize: indica o tamanho do indivíduo
        """
        self.popul = Popul(self.popsize, indsize)

    def evaluate(self, indivs:int)->None:
        """
        @brief Função de avaliação
        @param indivs: número de indivíduos
        """
        for i in range(len(indivs)):  #estamos a definiri a função de avaliação para cada indiv
            ind = indivs[i]
            fit = 0.0
            for x in ind.getGenes():  #para cada indivíduo, vai buscar a sua representação (vetor de 0 ou 1)
                if x == 1:
                    fit += 1.0
            ind.setFitness(fit)  #atribui o valor dessa fitness ao indivíduo
        return None

    def iteration(self)->None:
        """
        @brief Função que realiza a iteração
        """
        parents = self.popul.selection(self.noffspring)  #seleção da população inicial 
        offspring = self.popul.recombination(parents, self.noffspring)   #nova geração
        self.evaluate(offspring) #avaliação da nova geração
        self.popul.reinsertion(offspring)    #resinserção, onde há a selação dos indivíduos que vão constituir a população OU iteração seguinte
        #continua até atingir o critério de paragem -> solução final: melhor indivíduo da população final

    def run(self)->None:
        """
        @brief Função que mostra a que iteração é encontrada a melhor solução
        """
        self.initPopul(self.indsize)  #cria a população inicial
        self.evaluate(self.popul.indivs)  #avalia essa população
        self.bestsol = self.popul.bestSolution()  #encontra a primeira solução
        for i in range(self.numits+1):  
            self.iteration()
            bs = self.popul.bestSolution()
            if bs > self.bestsol:   #o ciclo for avalia as soluções e se a nova solução for melhor que a anterior, esta é atualizada
                self.bestsol = bs
            print("Iteration:", i, " ", "Best: ", self.bestsol)

    def printBestSolution(self)->None:
        """
        @brief Função que imprime a melhor solução
        """
        print("Best solution: ", self.bestsol.getGenes())
        print("Best fitness:", self.bestsol.getFitness())


def test():
    ea = EvolAlgorithm(100, 20, 50, 10)
    ea.run()


if __name__ == "__main__":
    test()
