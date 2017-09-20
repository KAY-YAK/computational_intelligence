import random
import  math as m
import  numpy as np
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

def saturate(vector, bounds):
        for x in range(len(vector)):
                vector[x] = min(max(vector[x], bounds[0]),bounds[1])
        return vector

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

#  Genetic operations
def evolve(pop,func, bounds, retain=0.5, random_select=0.2, mutate=0.01):
        retain_length = int(len(pop) * retain)
        parents =[]
        
        # Tournament selection
        for x in range(retain_length):
                pos_1 = random.randint(0, len(pop) - 1)
                pos_2 = random.randint(0, len(pop) - 1)
                if (pos_1 == pos_2):
                        while (pos_1 == pos_2):
                                pos_2 = random.randint(0, len(pop) - 1)
                                
                # same parents not allowed
                if(pop[pos_1] in parents or pop[pos_2] in parents):
                        continue
                
                # add the winner to parents list [one with low f() is the winner]
                if (func(pop[pos_1]) > func(pop[pos_2])):
                        parents.append(pop[pos_2])
                else:
                        parents.append(pop[pos_1])
        
        # randomly add other individuals to promote genetic diversity
        for x in pop:
                if x in parents:
                        continue
                if random_select > random.random():
                        parents.append(x)
        
        # parents could end up with 1 individual
        if len(parents) == 1:
                while(True):
                        other_parent = pop[random.randint(0, len(pop) - 1)]
                        if(other_parent not in parents):
                                parents.append(other_parent)
                                break
        

        # Box crossover
        parents_length = len(parents)
        pop_length = len(pop)
        desired_length = pop_length - parents_length
        children =[]
        while (len(children) < desired_length):
                # select random parents
                male = random.randint(0, len(parents) - 1)
                female = random.randint(0, len(parents) - 1)
                # male and female shouldnt be same
                if(male == female):
                        while (male == female):
                                male = random.randint(0, len(parents) - 1)
                # crossover
                temp = []
                for x in range(len(parents[male])):
                        temp.append(min(parents[male][x],parents[female][x]) + random.uniform(0, 1)*abs(parents[male][x] - parents[female][x]))
                
                temp = saturate(temp, bounds)
                
                children.append(temp)
                
                
        # add children to parents
        parents.extend(children)
        
        
        # mutate [GAUSSIAN]
        for indi in parents:
                if mutate > random.random():
                        for pos in range(len(indi)):
                                indi[pos] = indi[pos] + np.random.normal(1,.25)
        
                                
        return parents
        
                        
                        
func = [de_jong, rastrigin, schwefel, michalewicz ]
bounds =[[-5.12,5.12], [-5.12,5.12], [-500, 500], [0,m.pi]]


for index in range(4):
        time_ini = time.time()
        print("Function = ", func[index].__name__)
        for x in [10, 50]:
                p = population(x * 10, x, bounds[index][0], bounds[index][1])
                fitness = grade(p, func[index])
                store = p
                for r in range(1000):
                        p = evolve(p, func[index], bounds[index])
                        if fitness > grade(p, func[index]):
                                store = p
                                fitness = grade(p, func[index])
                
                score = 99999999
                pick = 0
                for i in store:
                        if score > func[index](i):
                                pick = i
                                score = func[index](i)

                elapsed_time = (time.time() - time_ini) * 1000
                
                print("Time Elapsed =", elapsed_time, "milliseconds")
                
                
                print("DIM =  ",x)
                
                print("Pick = ", pick)
        print("-----------------------------------------------------------------------------------------------------")
        
        
