#!/usr/bin/env python
# -*- coding: utf-8 -*-

## Created by Alejandro Encalado Masia and Albert Xaiver Lopez Barrantes

import numpy as np
import random
import pandas as pd
import sys

class Population:

    def __init__(self, n, max_population, prob_mutation, number_tournament,tournament_rand,llargada_one_point_crossover_maxima,crosover_rand,proportion_of_best):

        self.N = n
        self.MAX_POPULATION = max_population
        self.MUTATION_PROBABILITY = prob_mutation
        self.NUMBER_TOURNAMENT_MAX = number_tournament
        self.TOURNAMENT_RAND = tournament_rand
        self.LLARGADA_MAXIMA = llargada_one_point_crossover_maxima
        self.CROSSOVER_RAND = crosover_rand
        self.PROPORTION_OF_BEST = proportion_of_best

    def initialize(self):
        self.list_population = []
        i = 0
        for i in range(self.MAX_POPULATION):
            individual = Individual(self.N)
            individual.create()
            self.list_population.append((individual))
            self.AverageFitness()
            i += 1

    def viewPopulation(self):

        for element in self.list_population:

            print(element.genome)


    def CrossOver(self,individual1,individual2): #Funció per creuar dos individus

        if self.CROSSOVER_RAND:
            crosover_point = random.randint(1,self.LLARGADA_MAXIMA)
        else:
            crosover_point = self.LLARGADA_MAXIMA


        genome_individual1 = individual1.genome
        genome_individual2 = individual2.genome


        new_genome_individual1 = [None] * len(genome_individual1)
        new_genome_individual2 = [None] * len(genome_individual1)

        for index in range(len(genome_individual1)):

            if index >= crosover_point:

                new_genome_individual1[index] = genome_individual1[index]
                new_genome_individual2[index] = genome_individual2[index]

        new_index_ind_2 = 0
        new_index_ind_1 = 0

        for gene in genome_individual1:

            if new_index_ind_2 < crosover_point:

                if gene not in new_genome_individual2:

                    new_genome_individual2[new_index_ind_2] = gene
                    new_index_ind_2 += 1
            else:
                break

        for gene in genome_individual2:

            if new_index_ind_1 < crosover_point:

                if gene not in new_genome_individual1:

                    new_genome_individual1[new_index_ind_1] = gene
                    new_index_ind_1 += 1
            else:
                break




        if len(new_genome_individual1) != len(genome_individual1) or len(new_genome_individual2) != len(genome_individual1):

            print("Diferencies en la llargada del genoma")
            print(new_genome_individual1)
            print(new_genome_individual2)

            sys.exit()

        new_genome_individual1 = self.mutation(new_genome_individual1)
        new_genome_individual2 = self.mutation(new_genome_individual2)

        new_genome_individual1 = tuple(new_genome_individual1)
        new_genome_individual2 = tuple(new_genome_individual2)



        child_1, child_2  = Individual(self.N), Individual(self.N)

        child_1.assign(new_genome_individual1)
        child_2.assign(new_genome_individual2)

        return (child_1,child_2)


    def mutation(self, genome_individual): #Metode per mutar. Nomes muta com a molt dos gens (intercanviant la posició) per cada individu (genoma)

        new_genome_individual = list(genome_individual)

        rand_value = random.uniform(0,1)

        if rand_value < self.MUTATION_PROBABILITY:


            rnd_index_1 = random.randint(0,self.N - 1)
            rnd_index_2 = random.randint(0,self.N - 1)

            new_genome_individual[rnd_index_1] = genome_individual[rnd_index_2]
            new_genome_individual[rnd_index_2] = genome_individual[rnd_index_1]




        return new_genome_individual

    def TournamentSelection(self): #Metode per escollir el proxim pare

        best_fitness = None
        i = 0

        if self.TOURNAMENT_RAND:
            number_tournament = random.randint(1,self.NUMBER_TOURNAMENT_MAX)
        else:
            number_tournament = self.NUMBER_TOURNAMENT_MAX

        for i in range(number_tournament):

            individual = random.choice(self.list_population)

            if (best_fitness == None) or (individual.fitness < best_fitness):

                best_fitness = individual.fitness
                best_individual = individual

            i += 1


        return best_individual


    def NextGeneration(self): #Metode per generar la següent generació 


        parents = [None,None]
        list_child = []
        childs = []
        i = 0
        k = 0

        for i in range(len(self.list_population)/2):

            parents[0] = self.TournamentSelection()
            parents[1] = self.TournamentSelection()

            childs = self.CrossOver(parents[0],parents[1])

            for child in childs:

                list_child.append(child)

            i += 1

        self.list_population = []
        self.list_population = list_child
        self.AverageFitness()

    def AverageFitness(self): #Calcula la average fitness function

        list_fitness = []
        best_list_fitness = []
        proportion_of_best = int(self.MAX_POPULATION * self.PROPORTION_OF_BEST)

        for individual in self.list_population:

            list_fitness.append(individual.fitness)




        list_fitness.sort()
        best_list_fitness = list_fitness[0:proportion_of_best]
        self.fitnessavg = sum(best_list_fitness)/len(best_list_fitness)

    def BestIndidivualSoFar(self): #Aquesta funció la fem servir per trobar si existeix algun individu que la seva fitness function sigui 0

        for individual in self.list_population:

            if individual.fitness == 0:

                return individual


        return None



















class Individual: #Classe per generar el individu, crea un de nou on la posició de les reines no es repeteix per fila usant el metode .create().
                  # També permet assignar un genoma específic a un nou individu, aixo es fa servir alhora de generar els fills

    number_of_individual = 0

    def __init__(self,n):

        self.SIZE = n
        Individual.number_of_individual += 1
        self.id = Individual.number_of_individual


    def create(self):

        genome_constructor = []
        while len(genome_constructor) < self.SIZE :

            random_number = random.randint(0,self.SIZE-1)

            if random_number not in genome_constructor:

                genome_constructor.append(random_number)

        self.genome = tuple(genome_constructor)


        self.fitness = self.FitnessFunction()



    def FitnessFunction(self):

        individual = list(self.genome)
        fitness = 0

        while True:

            try:
                queen_pos = individual.pop(0)

            except IndexError:
                break



            for i,next_queen in enumerate(individual):

                if next_queen == queen_pos - i - 1:

                    fitness = fitness + 1

                if next_queen == queen_pos + i + 1:

                    fitness = fitness + 1

                if next_queen == queen_pos:

                    fitness = fitness + 1


        return fitness


    def assign(self,new_genome):

        self.genome = tuple(new_genome)
        self.fitness = self.FitnessFunction()





###############################################
        #cos del programa #
###############################################

poblacio_total = Population(
    n = 8,                                      #Dimensio del tablero (De moment ho fem per 8 que es el que ens demanen)
    max_population = 100,                       #Poblacio maxima
    prob_mutation = 0.03,                       #Probabilitat de que muti un gen
    number_tournament = 99,                     #Numero de comparacions que es fan per escollir un pare
    tournament_rand = False,                    #Per cada elecció de pare: si TRUE el numero de comparacions varia entre 0 i number_tournament, si FALSE, el numero de comparacions es number_tournament
    llargada_one_point_crossover_maxima = 7,    #Posició del genoma on es fara el crossover
    crosover_rand = True,                       #si True, per cada crossover el punt de tall sera un numero aleatori entre 0 i llargada_one_point_crossover_maxima. Si False, sera sempre llargada_one_point_crossover_maxima
    proportion_of_best = 0.2)                   #Proporció de la població ordenada de millor a pitjor fitness que volem utilitzar per calcular la avg fitness function (Aquest numero nomes serveix per veure en pantalla com evoluciona la fitness function dels millors a cada iteració )

poblacio_total.initialize()
i = 0

for i in range(40000):

    poblacio_total.NextGeneration()
    individual_solution = poblacio_total.BestIndidivualSoFar()
    print(i)
    if i%1 == 0:
        print(poblacio_total.fitnessavg)

    if individual_solution != None:

        print(individual_solution.genome)
        print("Solucio trobada!")
        break

    i += 1
