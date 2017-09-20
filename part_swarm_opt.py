import numpy as np
import math as m
import random
from operator import  *
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
    return [ random.uniform(min,max) for x in range(dim) ]

# Generate population
'''---------------------------------------------------------------------
@params
        count: the number of individuals in the population
        dim: the number of values per individual
        min: the minimum possible value in an individual's list of values
        max: the maximum possible value in an individual's list of values
---------------------------------------------------------------------'''
def population(count, dim, min, max):
        return [ individual(dim, min, max) for x in range(count) ]


def particle_swarm_optimization(count, dim, min , max, budget, func, const_1, const_2, const_3):
        # Generate particles
        pop = population(count, dim, min, max)
        v_max = max - min
        v_min = -v_max
        swarm =[]
        global_best = None
        # Add velocity and local_best to each particle
        for individual in pop:
                velocity = []
                for x in range(dim):
                        velocity.append(random.uniform(v_min/3, v_max/3))
                local_best = individual
                swarm.append([individual, velocity, local_best])
                
                if global_best == None:
                        global_best = copy.deepcopy(local_best)
                        continue
                
                # Capture global_best
                if func(local_best) < func(global_best):
                        global_best = copy.deepcopy(local_best)
        
        print(swarm)
        # swarm activities
        budget_no = 0
        iter_no = 1
        while(budget_no < budget):
                # Divide by square root of iteration to get step size [There are many other methods]
                theta_1 = const_1/ m.sqrt(iter_no)
                iter_no = iter_no + 1
                for particle in swarm:
                        # update velocity
                        theta_2 = random.uniform(0, const_2)
                        theta_3 = random.uniform(0, const_3)
                        list_1 = [theta_1 * x for x in particle[1] ]
                        list_2 = [theta_2 * y for y in list(map(sub, particle[2], particle[0]))]
                        list_3 = [theta_3 * z for z in  list(map(sub, global_best, particle[0]))]
                        velocity = []
                        for pos in range(len(list_1)):
                                velocity.append(list_1[pos] + list_2[pos] + list_3[pos])
                        # calcuate new local_point
                        temp = list(map(add , particle[0], velocity))
                        
                        # calulate fitness
                        temp_fitness = func(temp)
                        local_best_fitness = func(particle[2])
                        global_best_fitness = func(global_best)
                        
                        # fitness called 3 times
                        budget_no = budget_no + 3
                        
                        # if  temp_fitness is better than or equal to local_best_fitness update local_best
                        if temp_fitness <= local_best_fitness:
                                particle[0] = copy.deepcopy(temp)
                                # if temp_fitness is better than or equal to gobal_best_fitness update global_best
                                if temp_fitness <= global_best_fitness:
                                        global_best = copy.deepcopy(temp)
        
        
        return global_best



def comprehensive_learning_particle_swarm_optimization(count, dim, min , max, budget, func, const_1, const_2):
        # Generate particles
        pop = population(count, dim, min, max)
        v_max = max - min
        v_min = -v_max
        swarm = []
        global_best = None
        
        # Add velocity and local_best to each particle
        local_best_list = []
        for individual in pop:
                velocity = []
                for x in range(dim):
                        velocity.append(random.uniform(v_min / 3, v_max / 3))
                local_best = individual
                swarm.append([individual, velocity, local_best])
                local_best_list.append(local_best)

                if global_best == None:
                        global_best = copy.deepcopy(local_best)
                        continue
        
                        # Capture global_best
                if func(local_best) < func(global_best):
                        global_best = copy.deepcopy(local_best)

        budget_no = 0
        iter_no = 1
        while(budget_no < budget):
                # Divide by square root of iteration to get step size [There are many other methods]
                theta_1 = const_1 / m.sqrt(iter_no)
                iter_no = iter_no + 1
                
                for pos in range(len(swarm)):
                        
                        # calculate probability
                        pow_1 = 10 * pos / (len(swarm) - 1)
                        probability = 0.05 + (0.45 *(m.exp(pow_1) -1)) / (m.exp(10) - 1)
                        
                        # select random local best
                        random_local_best = None
                        
                        if random.uniform(0,1) > probability:
                                random_local_best = swarm[pos][2]
                        else:
                                random_1 = random.choice(swarm)[2]
                                random_2 = random.choice(swarm)[2]
                                fitness_rand_1 = func(random_1)
                                fitness_rand_2 = func(random_2)
                                if fitness_rand_1 <=  fitness_rand_2:
                                        random_local_best = random_1
                                else:
                                        random_local_best =  random_2

                        # update velocity
                        velocity = []
                        list_1 = [theta_1 * x for x in swarm[pos][1]]
                        random_matrix = np.multiply(np.random.rand(dim,dim),const_2 )
                        #print(swarm[pos][0])
                        diff = list(map(sub, random_local_best, swarm[pos][0]))
                        matrix_dot_diff = np.ndarray.tolist(np.dot(random_matrix, np.asarray(diff)))
                        velocity = list(map(add, list_1, matrix_dot_diff))
                        
                        
                        # Same as particle_swarm_optimization
                        # calcuate new local_point
                        temp = list(map(add, swarm[pos][0], velocity))

                        # calulate fitness
                        temp_fitness = func(temp)
                        local_best_fitness = func(swarm[pos][2])
                        global_best_fitness = func(global_best)

                        # fitness called 3 times
                        budget_no = budget_no + 3

                        # if  temp_fitness is better than or equal to local_best_fitness update local_best
                        if temp_fitness <= local_best_fitness:
                                swarm[pos][0] = copy.deepcopy(temp)
                                # if temp_fitness is better than or equal to gobal_best_fitness update global_best
                                if temp_fitness <= global_best_fitness:
                                        global_best = copy.deepcopy(temp)
                                        
        return global_best
                        
                        
time_ini = time.time()
print(comprehensive_learning_particle_swarm_optimization(150, 10,-5.12,5.12,5000 * 50,de_jong,.9,.63))
elapsed_time = (time.time() - time_ini) * 1000
print(elapsed_time)

time_ini = time.time()
print(comprehensive_learning_particle_swarm_optimization(150, 10,-5.12,5.12,5000 * 50,rastrigin,.9,.63))
elapsed_time = (time.time() - time_ini) * 1000
print(elapsed_time)

time_ini = time.time()
print(comprehensive_learning_particle_swarm_optimization(150, 10,-500,500,5000 * 50,schwefel,.9,.63))
elapsed_time = (time.time() - time_ini) * 1000
print(elapsed_time)

time_ini = time.time()
print(comprehensive_learning_particle_swarm_optimization(150, 10,0,m.pi,5000 * 50,de_jong,.9,.63))
elapsed_time = (time.time() - time_ini) * 1000
print(elapsed_time)

# DO SAME FOR 50 D and repeat same for  particle_swarm_optimization