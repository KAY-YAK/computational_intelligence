import numpy as np
import math as m
import random
from operator import *
import copy
import time


# dejong function [-5.12,5.12].
def de_jong(vector):
        sum = 0
        for dim in vector:
                sum = sum + dim ** 2
        
        return sum


# rastrigin  function [-5.12,5.12].
def rastrigin(vector):
        sum = 10 * len(vector)
        for dim in vector:
                sum = sum + dim ** 2 - 10 * m.cos(2 * m.pi * dim)
        
        return sum


# schwefel fucntion [-500, 500]
def schwefel(vector):
        sum = 0
        for dim in vector:
                sum = sum + dim * m.sin(m.sqrt(abs(dim)))
        
        sum = 418.9829 * len(vector) - sum
        return sum


# michalewicz function  [0, pi]
def michalewicz(vector):
        sum = 0
        count = 0
        for dim in vector:
                count = count + 1
                sum = m.sin(dim) * m.sin((count * dim ** 2) / m.pi) ** 20
        
        return -sum


# Create an Individual
def individual(dim, min, max):
        return [random.uniform(min, max) for x in range(dim)]


# Generate population
'''---------------------------------------------------------------------
@params
        count: the number of individuals in the population
        dim: the number of values per individual
        min: the minimum possible value in an individual's list of values
        max: the maximum possible value in an individual's list of values
---------------------------------------------------------------------'''


def population(count, dim, min, max):
        return [individual(dim, min, max) for x in range(count)]


# vec_2 is mutated  individual and vec_1 is the jth individual
def crossover_exponential(vec_1, vec_2, crossover_rate):
        # copy vec_2
        offspring = copy.deepcopy(vec_2)
        length = len(vec_1)
        rand_index = np.random.randint(0, length - 1)
        
        if (rand_index == length - 1):
                index = 0
        else:
                index = rand_index + 1
        
        count = 0
        while (np.random.uniform(0, 1) <= crossover_rate or index != rand_index):
                count = count + 1
                offspring[index] = vec_1[index]
                index = index + 1
                if index > length - 1:
                        index = 0
        
        return offspring

def crossover_binomial(vec_1, vec_2, crossover_rate):
        length = len(vec_1)
        offspring = [0] *length
        index = random.randint(0, length - 1)
        for pos in range(length):
                if(np.random.uniform(0,1) <= crossover_rate or pos == index):
                        offspring[pos] = vec_1[pos]
                else:
                        offspring[pos] = vec_2[pos]
        
        return offspring
                

'''
 [Liu and Lampinen, 2005]
 F 2 [0:5; 1];
I CR 2 [0:8; 1]
I population size = 10 * D
 '''


def diff_evolve_rand_1( count, dim, low, high, budget, func, factor,crossover_rate, crossover_func, tou_1=.1, tou_2=.1 ):
        count_gen = 1
        # Generate population
        pop = population(count, dim, low, high)
        
        fitness = []
        for individual in pop:
                fitness.append(func(individual))
        
        # fittest individual
        best = min(fitness)
        pos = fitness.index(best)
        best = copy.deepcopy(pop[pos])
        budget_no = 0
        while (budget_no < budget):
                length = len(pop)
                pop_nextgen = []
                for index in range(length):
                        # select 3 random individual
                        rand_lst = []
                        while (True):
                                rand = random.randint(0, length - 1)
                                if (len(rand_lst) == 3):
                                        break
                                if (rand not in rand_lst):
                                        rand_lst.append(rand)
                                        # print(rand_lst)
                        
                        rand_1, rand_2, rand_3 = rand_lst

                        # change factor
                        if (np.random.uniform(0, 1) < tou_1):
                                factor = factor + np.random.uniform(0, 1)

                        # change crossover_rate
                        if (np.random.uniform(0, 1) < tou_2):
                                crossover_rate = np.random.uniform(0, 1)

                        # mutate
                        temp = list(map(sub, pop[rand_2], pop[rand_3]))
                        for x in range(len(temp)):
                                temp[x] = temp[x] * factor
                        mutation = list(map(add, pop[rand_1], temp))

                        # crossover
                        offspring = crossover_func(pop[index], mutation, crossover_rate)

                        # next gen pop
                        
                        
                        if (func(offspring) <= func(pop[index])):
                                pop_nextgen.append(offspring)
                        else:
                                pop_nextgen.append(pop[index])

                # incr budget_no
                budget_no = budget_no + 2
                count_gen = count_gen + 1
                # Now replace old population
                pop = []
                pop = copy.deepcopy(pop_nextgen)

                # empty fitness
                fitness = []
                for individual in pop:
                        fitness.append(func(individual))
                        budget_no = budget_no + 1
                # fittest individual
                best = min(fitness)
                pos = fitness.index(best)
                best = copy.deepcopy(pop[pos])
        
        return best





time_ini = time.time()
print(diff_evolve_rand_1(100,10,-5.12,5.12,50000,de_jong,.65,.9,crossover_exponential))
elapsed_time = (time.time() - time_ini) * 1000
print(elapsed_time)

time_ini = time.time()
print(diff_evolve_rand_1(100,10,-5.12,5.12,50000,de_jong,.78,.8,crossover_binomial))
elapsed_time = (time.time() - time_ini) * 1000
print(elapsed_time)

#Do same for  all the other functions 