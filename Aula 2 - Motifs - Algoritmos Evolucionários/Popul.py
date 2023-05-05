# -*- coding: utf-8 -*-

from Indiv import Indiv, IndivInt, IndivReal
from random import uniform
from random import random


class Popul:

    def __init__(self, popsize:int, indsize:int, indivs:list[int]=[])->None:
        """
        @brief Contrutor da class Popul
        @param popsize: tamanho da população
        @param indsize: tamanho dos indivíduos
        @param indivs : lista de indivíduos
        """
        self.popsize = popsize
        self.indsize = indsize
        if indivs:   #se tivermos indivíduos da lista, usamos estes
            self.indivs = indivs
        else:
            self.initRandomPop()  #se não, geramo-los de forma aleatória

    def getIndiv(self, index:int)->int:
        """
        @brief Escolhe um indívuo a uma posição
        @param index: posição do indivíduo
        """
        return self.indivs[index]

    def initRandomPop(self)->None:
        """
        @brief Geração de indivíduos de forma aleatória
        """
        self.indivs = []
        for _ in range(self.popsize):
            indiv_i = Indiv(self.indsize, [])  #gera os indivíduos de forma aleatória
            self.indivs.append(indiv_i)

    def getFitnesses(self, indivs=None)->list[float]:
        """
        @brief Função que guarda os valores de fitness/aptidão dos indivíduos
        @param indivs: lista de indivíduos, que leva como default None caso não existam indivíduos
        @returns lista de fitnesses
        """
        fitnesses = []
        if not indivs:
            indivs = self.indivs
        for ind in indivs:
            fitnesses.append(ind.getFitness())
        return fitnesses

    def bestSolution(self)->None:
        """
        @brief Melhor solução dos indivíduos
        @return valor máximo desses indivíduos
        """
        return max(self.indivs)

    def bestFitness(self)->list[float]:
        """
        @brief Melhor fitness dos indivíduos
        @returns lista de fitnesses
        """
        indv = self.bestSolution()
        return indv.getFitness()


    def selection(self, n, indivs=None)->None:
        """
        @brief Mecanismo de seleção para a reprodução
        @param n: número de novos descendentes
        @param indivs: lista dos indivíduos"""
        res = []
        fitnesses = list(self.linscaling(self.getFitnesses(indivs)))  #obtém os fitnesses dos indivíduos e faz a normalização
        print(fitnesses)
        for _ in range(n):
            sel = self.roulette(fitnesses)  #seleção através da roleta
            fitnesses[sel] = 0.0
            res.append(sel)
        return res

    def roulette(self, fit:list[float])->list[int]:
        """
        @brief Faz a seleção por roleta
        @param fit lista de fitnesses
        @returns lista de indices dos individuos escolhidos
        """
        tot = sum(fit)
        val = random()
        acum = 0.0
        ind = 0
        while acum < val:
            acum += (fit[ind]/tot)
            ind += 1
        return ind-1
    

    def linscaling(self, fitnesses:list[float])->list[float]:
        """
        @brief Normalização do valor de aptidão para uniforme [0,1]
        @param fitnesses: valores de fitness
        @returns Lista de valores de fitness normalizados
        """
        mx = max(fitnesses)
        mn = min(fitnesses)
        res = []
        for f in fitnesses:
            val = (f-mn)/(mx-mn) #normalização
            res.append(val)
        return res

    def recombination(self, parents:int, noffspring:int)->list[int]:
        """
        @brief Usa o cruzamento para criar novas soluções e aplica mutação a cada nova solução
        @param parents: indivíduos que vão sofrer cruzamento
        @param noffspring : novos descendentes
        @retuns lista de novos descendentes
        """
        offspring = []
        new_inds = 0
        while new_inds < noffspring:
            parent1 = self.indivs[parents[new_inds]]  #progenitor 1
            parent2 = self.indivs[parents[new_inds+1]] #progenitor 2
            offsp1, offsp2 = parent1.crossover(parent2)  #cruzzamento entre os progenitores
            offsp1.mutation() #mutação
            offsp2.mutation()
            offspring.append(offsp1)
            offspring.append(offsp2)
            new_inds += 2
        return offspring

    def reinsertion(self, offspring:int)->None:
        """
        @brief Mecanismo de reinserção -> seleção de indivíduos que vão constituir a população OU interação seguinte
        @param offpring: descendentes
        """
        tokeep = self.selection(self.popsize-len(offspring))  #seleção dos indivíduos
        ind_offsp = 0
        for i in range(self.popsize):
            if i not in tokeep:
                self.indivs[i] = offspring[ind_offsp]  #preencher o resto da população com novos indivíduos
                ind_offsp += 1


class PopulInt(Popul):

    def __init__(self, popsize:int, indsize:int, ub:float, indivs:list[int]=[]):
        """
        @brief Construtor da class PopulInt
        @param popsize: tamanho da população
        @param indsize: tamanho do indivíduo
        @param ub: upper bound
        @param indivs: lista de indivíduos
        """
        self.ub = ub
        Popul.__init__(self, popsize, indsize, indivs)

    def initRandomPop(self)->None:
        """
        @brief Geração de população de forma aleatória
        """
        self.indivs = []
        for _ in range(self.popsize):
            indiv_i = IndivInt(self.indsize, [], 0, self.ub)
            self.indivs.append(indiv_i)

#ALTERADO
class PopulReal(Popul):

    def __init__(self, popsize:int, indsize:int, lb:float=0.0, ub:float=1.0, indivs:list[int]=[])->None:
        """
        @brief Construtor da População Real
        @param popsize: tamanho da população
        @param indsize: tamanho do indivíduo
        @param lb: lower bound, que corresponde ao menor valor do alfabeto do gene
        @param ub: upper bound, que corresponde ao maior valor do alfabeto do gene
        @param indivs: lista dos indivíduos
            """
        self.lb = lb
        self.ub = ub
        Popul.__init__(self, popsize, indsize, indivs)

    def initRandomPop(self)->None:
        """
        @brief Criação de uma população aleatória
        """
        self.indivs = []
        for _ in range(self.popsize):
            indiv_r = IndivReal(self.indsize, [], self.lb, self.ub)
            self.indivs.append(indiv_r)
