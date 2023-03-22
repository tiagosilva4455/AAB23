# -*- coding: utf-8 -*-

from Indiv import Indiv, IndivInt, IndivReal
from random import random


class Popul:

    def __init__(self, popsize, indsize, indivs=[]):
        self.popsize = popsize
        self.indsize = indsize
        if indivs:
            self.indivs = indivs
        else:
            self.initRandomPop()

    def getIndiv(self, index):
        return self.indivs[index]

    def initRandomPop(self):
        self.indivs = []
        for _ in range(self.popsize):
            indiv_i = Indiv(self.indsize, [])
            self.indivs.append(indiv_i)

    def getFitnesses(self, indivs=None):
        fitnesses = []
        if not indivs:
            indivs = self.indivs
        for ind in indivs:
            fitnesses.append(ind.getFitness())
        return fitnesses

    def bestSolution(self):
        return max(self.indivs)

    def bestFitness(self):
        indv = self.bestSolution()
        return indv.getFitness()


    def selection(self, n, indivs=None):
        res = []
        fitnesses = list(self.linscaling(self.getFitnesses(indivs)))
        print(fitnesses)
        for _ in range(n):
            sel = self.roulette(fitnesses)
            fitnesses[sel] = 0.0
            res.append(sel)
        return res

    def roulette(self, f):
        tot = sum(f)
        val = random()
        print(f)
        print(val)
        acum = 0.0
        ind = 0
        print(tot)
        print()
        while acum <= val:
            acum += (f[ind] / tot)
            ind += 1
        return ind-1

    def linscaling(self, fitnesses):
        mx = max(fitnesses)
        mn = min(fitnesses)
        res = []
        for f in fitnesses:
            val = (f-mn)/(mx-mn)
            res.append(val)
        return res

    def recombination(self, parents, noffspring):
        offspring = []
        new_inds = 0
        while new_inds < noffspring:
            parent1 = self.indivs[parents[new_inds]]
            parent2 = self.indivs[parents[new_inds+1]]
            offsp1, offsp2 = parent1.crossover(parent2)
            offsp1.mutation()
            offsp2.mutation()
            offspring.append(offsp1)
            offspring.append(offsp2)
            new_inds += 2
        return offspring

    def reinsertion(self, offspring):
        tokeep = self.selection(self.popsize-len(offspring))
        ind_offsp = 0
        for i in range(self.popsize):
            if i not in tokeep:
                self.indivs[i] = offspring[ind_offsp]
                ind_offsp += 1


class PopulInt(Popul):

    def __init__(self, popsize, indsize, ub, indivs=[]):
        self.ub = ub
        Popul.__init__(self, popsize, indsize, indivs)

    def initRandomPop(self):
        self.indivs = []
        for _ in range(self.popsize):
            indiv_i = IndivInt(self.indsize, [], 0, self.ub)
            self.indivs.append(indiv_i)

#ALTERADO
class PopulReal(Popul):

    def __init__(self, popsize:int, indsize:int, lb:float=0.0, ub:float=1.0, indivs:list[int]=[])->None:
        """
        Construtor da População Real
        Args:
            popsize: tamanho da população
            indisize: tamanho do indivíduo
            lb: lower bound, que corresponde ao menor valor do alfabeto do gene
            ub: upper bound, que corresponde ao maior valor do alfabeto do gene
            indivs: lista dos indivíduos
            """
        self.lb = lb
        self.ub = ub
        Popul.__init__(self, popsize, indsize, indivs)

    def initRandomPop(self)->None:
        """
        Criação de uma população aleatória
        """
        self.indivs = []
        for _ in range(self.popsize):
            indiv_r = IndivReal(self.indsize, [], self.lb, self.ub)
            self.indivs.append(indiv_r)
