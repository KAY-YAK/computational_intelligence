import numpy as np
import math as m
import random
from operator import  add
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
def individual(length, min, max):
    return [ random.uniform(min,max) for x in range(length) ]

# Generate population
'''---------------------------------------------------------------------
@params
        count: the number of individuals in the population
        length: the number of values per individual
        min: the minimum possible value in an individual's list of values
        max: the maximum possible value in an individual's list of values
---------------------------------------------------------------------'''
def population(count, length, min, max):
        return [ individual(length, min, max) for x in range(count) ]

# Find average fitness for a population.
def grade(pop, func):
        sum = 0
        for indi in pop:
                sum = sum + func(indi)
        return sum/len(pop)

# version_1
def evolve_ver1(pop, func, sigma):
        I = np.identity(len(pop[0]))
        mean = np.zeros(len(pop[0]))
        for pos in range(len(pop)) :
                rand_var = np.random.multivariate_normal(mean, I)
                temp = list(map(add, pop[pos], [sigma*x for x in list(rand_var)]))
                fitness_individual = func(pop[pos])
                fitness_child = func(temp)
                if fitness_child < fitness_individual:
                        pop[pos] = temp
                        sigma = 1.5 * sigma
                elif fitness_child > fitness_individual:
                        sigma = 1.5**-.25 * sigma
                        
        return pop, sigma

# version_2
def evolve_ver2(pop, func, sigma):
        for pos in range(len(pop)):
                I = np.identity(len(pop[0]))
                mean = np.zeros(len(pop[0]))
                rand_var = np.random.multivariate_normal(mean, I)
                temp = list(map(add, pop[pos], [sigma * x for x in list(rand_var)]))
                fitness_individual = func(pop[pos])
                fitness_child = func(temp)
                if fitness_child < fitness_individual:
                        pop[pos] = temp
                        sigma = 1.5 * sigma
                elif fitness_child == fitness_individual:
                        pop[pos] = temp
                else:
                        sigma = 1.5 ** -.25 * sigma
        
        return pop, sigma






for x in [10,50]:
        sigma = 2
        time_ini = time.time()
        pop=[]
        pop = population(x*10, x, -5.12, 5.12)
        for y in range(2 * x):
                pop , sigma = evolve_ver1(pop, de_jong, sigma)
        
        elapsed_time = (time.time() - time_ini) * 1000

        print("DeJong :: Time Elapsed =", elapsed_time, "milliseconds")

        print("DIM =  ", x)
        score = 99999999
        pick = None
        for i in pop:
                if score > de_jong(i):
                        pick = i
        print(pick)

        sigma = 2
        time_ini = time.time()
        pop = []
        pop = population(x * 10, x, -5.12, 5.12)
        for y in range(2 * x):
                pop, sigma = evolve_ver1(pop, rastrigin, sigma)

        elapsed_time = (time.time() - time_ini) * 1000

        print("Rastrigin :: Time Elapsed =", elapsed_time, "milliseconds")

        print("DIM =  ", x)
        score = 99999999
        pick = None
        for i in pop:
                if score > rastrigin(i):
                        pick = i
        print(pick)

        sigma = 2
        time_ini = time.time()
        pop = []
        pop = population(x * 10, x, -500, 500)
        for y in range( 5):
                pop, sigma = evolve_ver1(pop, schwefel, sigma)

        elapsed_time = (time.time() - time_ini) * 1000

        print("Schwefel :: Time Elapsed =", elapsed_time, "milliseconds")

        print("DIM =  ", x)
        score = 99999999
        pick = None
        for i in pop:
                if score > schwefel(i):
                        pick = i
        print(pick)

        sigma = 2
        time_ini = time.time()
        pop = []
        pop = population(x * 10, x, 0, m.pi)
        for y in range(2 * x):
                pop, sigma = evolve_ver1(pop, michalewicz, sigma)

        elapsed_time = (time.time() - time_ini) * 1000

        print("Michalewicz :: Time Elapsed =", elapsed_time, "milliseconds")

        print("DIM =  ", x)
        score = 99999999
        pick = None
        for i in pop:
                if score > michalewicz(i):
                        pick = i
        print(pick)



#ver_2
for x in [10, 50]:
        sigma = 2
        time_ini = time.time()
        pop = []
        pop = population(x * 10, x, -5.12, 5.12)
        for y in range(2 * x):
                pop, sigma = evolve_ver2(pop, de_jong, sigma)
        
        elapsed_time = (time.time() - time_ini) * 1000
        
        print("DeJong :: Time Elapsed =", elapsed_time, "milliseconds")
        
        print("DIM =  ", x)
        score = 99999999
        pick = None
        for i in pop:
                if score > de_jong(i):
                        pick = i
        print(pick)
        
        sigma = 2
        time_ini = time.time()
        pop = []
        pop = population(x * 10, x, -5.12, 5.12)
        for y in range(2 * x):
                pop, sigma = evolve_ver2(pop, rastrigin, sigma)
        
        elapsed_time = (time.time() - time_ini) * 1000
        
        print("Rastrigin :: Time Elapsed =", elapsed_time, "milliseconds")
        
        print("DIM =  ", x)
        score = 99999999
        pick = None
        for i in pop:
                if score > rastrigin(i):
                        pick = i
        print(pick)
        
        sigma = 2
        time_ini = time.time()
        pop = []
        pop = population(x * 10, x, -500, 500)
        for y in range(5):
                pop, sigma = evolve_ver2(pop, schwefel, sigma)
        
        elapsed_time = (time.time() - time_ini) * 1000
        
        print("Schwefel :: Time Elapsed =", elapsed_time, "milliseconds")
        
        print("DIM =  ", x)
        score = 99999999
        pick = None
        for i in pop:
                if score > schwefel(i):
                        pick = i
        print(pick)
        
        sigma = 2
        time_ini = time.time()
        pop = []
        pop = population(x * 10, x, 0, m.pi)
        for y in range(2 * x):
                pop, sigma = evolve_ver2(pop, michalewicz, sigma)
        
        elapsed_time = (time.time() - time_ini) * 1000
        
        print("Michalewicz :: Time Elapsed =", elapsed_time, "milliseconds")
        
        print("DIM =  ", x)
        score = 99999999
        pick = None
        for i in pop:
                if score > michalewicz(i):
                        pick = i
        print(pick)
