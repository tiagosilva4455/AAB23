from random import randint, random, shuffle, uniform


class Indiv:
    """
    @brief Class de Indivíduo
    """

    def __init__(self, size:int, genes:list=[], lb:int=0, ub:int=1)->None:
        """
        @brief Construtor da class Indiv
        @param size: tamanho do indivíduo
        @param genes: genoma
        @param lb: limite inferior do intevalo para representação do gene, assume 0 caso nenhum valor for indicado
        @param ub: limite superior do intevalo para representação do gene, assume 1 caso nenhum valor for indicado
        """
        self.lb = lb
        self.ub = ub
        self.genes = genes
        self.fitness = None
        if not self.genes:
            self.initRandom(size)

    # comparadores.
    # Permitem usar sorted, max, min

    def __eq__(self, solution):
        if isinstance(solution, self.__class__):
            return self.genes.sort() == solution.genes.sort()
        return False

    def __gt__(self, solution):
        if isinstance(solution, self.__class__):
            return self.fitness > solution.fitness
        return False

    def __ge__(self, solution):
        if isinstance(solution, self.__class__):
            return self.fitness >= solution.fitness
        return False

    def __lt__(self, solution):
        if isinstance(solution, self.__class__):
            return self.fitness < solution.fitness
        return False

    def __le__(self, solution):
        if isinstance(solution, self.__class__):
            return self.fitness <= solution.fitness
        return False

    def __str__(self):
        return f"{str(self.genes)} {self.getFitness()}"

    def __repr__(self):
        return self.__str__()

    def setFitness(self, fit):
        self.fitness = fit

    def getFitness(self):
        return self.fitness

    def getGenes(self):
        return self.genes

    def initRandom(self, size:int)->None:
        """
        @brief Inicialização de um indivíduo de forma aleatória (o genoma terá valores 0 ou 1)
        @param size tamanho do indivíduo
        """
        self.genes = []
        for _ in range(size):
            self.genes.append(randint(self.lb, self.ub))

    def mutation(self)->None:
        """
        @brief Mutações para representações binárias que altera um único gene, em que apenas uma poisção vai variar (se for 0 passa para 1, e se for 1 passa para 0)
        """
        s = len(self.genes)
        pos = randint(0, s-1)  #seleciona uma posição no vetor de forma aleatória
        if self.genes[pos] == 0:  #se o vetor é zero passa para um 
            self.genes[pos] = 1
        else:
            self.genes[pos] = 0  #se o vetor não for zero, passa a ser zero

    def crossover(self, indiv2:list[int])->list[int]:
        """
        @brief Cruzamento de um ponto
        @param indiv2: indivíduo com o qual o indiv vai fazer o cruzamento
        """
        return self.one_pt_crossover(indiv2)

    def one_pt_crossover(self, indiv2:list[int])->list[int]:
        """
        @brief Função operadora do cruzamento em um ponto
        @param indiv2: indivíduo com o qual o indiv vai fazer o cruzamento
        @returns Nova instância com base na representação do novo indivíduo
        """
        offsp1 = []
        offsp2 = []
        s = len(self.genes)
        pos = randint(0, s-1)  #seleciona uma posição de maneira aleatória
        for i in range(pos):
            offsp1.append(self.genes[i])  #a primeira parte da sequência mantém-se até pos-1
            offsp2.append(indiv2.genes[i])  
        for i in range(pos, s):
            offsp2.append(self.genes[i])  #ocorre a troca da pos até ao final da sequência do progenitor 2 com o progenitor 1
            offsp1.append(indiv2.genes[i])
        res1 = self.__class__(s, offsp1, self.lb, self.ub)
        res2 = self.__class__(s, offsp2, self.lb, self.ub)
        return res1, res2


class IndivInt (Indiv):
    """
    @brief Class IndivInt que estende a class Indiv, herdando todos os seus métodos
    """

    def __init__(self, size:int, genes:list=[], lb:int=0, ub:int=1)->None:
        """
        @brief Construtor da class Indiv
        @param size: tamanho do indivíduo
        @param genes: genoma
        @param lb: limite inferior do intevalo para representação do gene, assume 0 caso nenhum valor for indicado
        @param ub: limite superior do intevalo para representação do gene, assume 1 caso nenhum valor for indicado
        """
        self.lb = lb
        self.ub = ub
        self.genes = genes
        self.fitness = None
        if not self.genes:
            self.initRandom(size)

    def initRandom(self, size:int)->None:
        """
        @brief Inicialização de um indivíduo de forma aleatória aleatória
        @param size tamanho do individuo
        """
        self.genes = []
        for _ in range(size):
            self.genes.append(randint(0, self.ub))

    def mutation(self):
        """
        @brief Mutações para representações binárias que altera um único gene, em que apenas uma poisção vai variar.
        """
        s = len(self.genes)
        pos = randint(0, s-1)
        self.genes[pos] = randint(0, self.ub)

#ALTERADO
class IndivReal(Indiv):
    """
    @brief Class IndivReal que estende a class Indiv, herdando todos os seus métodos
    """

    def __init__(self, size:int, genes:list=[], lb:float=0.0, ub:float=1.0)->None:
        """
        @brief Construtor do indivíduo real
        @param size: tamanho do indivíduo
        @param genes: lista de genes no indivíduo
        @param lb: limite inferior do intevalo para representação do gene, assume 0.0 caso nenhum valor for indicado
        @param ub: limite superior do intevalo para representação do gene, assume 1.0 caso nenhum valor for indicado
        """
        self.lb = lb
        self.ub = ub
        Indiv.__init__(self, size, genes, lb, ub)

    def initRandom(self, size:int)->None:
        """
        @brief Inicialização de um indivíduo de forma aleatória aleatória
        @param size tamanho do indivíduo

        """
        self.genes = []
        for _ in range(size):
            self.genes.append(uniform(self.lb, self.ub))

    def mutation(self)->None:
        """
        @brief Acontecimento de uma mutação numa posição aleatória, seguindo uma distribuição uniforme num indivíduo
        """
        s = len(self.genes)
        pos = randint(0, s-1)
        self.genes[pos] = uniform(self.lb, self.ub)
#usamos uniform devido ao cruzamento uniform dos genes

