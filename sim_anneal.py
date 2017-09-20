import random  as rand
import math as m
import time
import copy

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



def neighbor(vector, bounds):
        vec_ret =[]
        for x in range(len(vector)):
                vec_ret.append( vector[x] + rand.uniform(bounds[0], bounds[1]))
        return vec_ret

def acceptance_probability(old_cost, new_cost, T):
        return m.exp((old_cost - new_cost) / T)

        

def random_vector(dim,bounds):
        random_guess = []
        for x in range(dim):
                random_guess.append(rand.uniform(bounds[0], bounds[1]))
        return random_guess

def saturate(vector, bounds):
        for x in range(len(vector)):
                vector[x] = min(max(vector[x], bounds[0]),bounds[1])
        return vector

def anneal(vector, bounds, cost_func, no_iter):
        old_cost = cost_func(vector)
        T = 100
        T_min = 0.00001
        alpha = 0.99
        i = 0
        while T > T_min:
                if(i >= no_iter):
                        print("Budget reached or exceeded")
                        print("No of iter = ", i)
                        break
                # Take a new move randomly and  correct bounds
                new_vector = neighbor(vector, bounds)
                new_vector = saturate(new_vector, bounds)
                # Evaluate func in the new situation.
                new_cost = cost_func(new_vector)
                i += 1
                # Evaluate the gain or loss in the new situation.
                # If new_cost is less then UPDATE.
                # Else calculate acceptance probability and if its greater than random number between 0 and 1.
                if new_cost < old_cost:
                        vector = new_vector
                        old_cost = new_cost
                else:
                        ap = acceptance_probability(old_cost, new_cost, T)
                        random_val = rand.uniform(0, 1)
                        if ap > random_val:
                                vector = new_vector
                                old_cost = new_cost
        #comment out
                
                T = T*alpha
        return vector



dimension = [10, 30, 50,75, 100]
for x in dimension:
        func1 = func2 = func3 = func4 = 0
        
        for y in range(30):
                time1 = time.time()
                vector = random_vector(x, [-5.12, 5.12])
                anneal(vector, [-5.12, 5.12], de_jong, 5000*x)
                elapsed_time = (time.time() - time1) * 1000
                func1 = elapsed_time + func1
                
                time1 = time.time()
                vector = random_vector(x, [-5.12, 5.12])
                anneal(vector, [-5.12, 5.12], rastrigin, 5000*x)
                elapsed_time = (time.time() - time1) * 1000
                func2 = elapsed_time + func2
                
                time1 = time.time()
                vector = random_vector(x, [-500, 500])
                anneal(vector, [-500, 500], schwefel, 5000*x)
                elapsed_time = (time.time() - time1) * 1000
                func3 = elapsed_time + func3
                
                time1 = time.time()
                vector = random_vector(x, [0, m.pi])
                anneal(vector, [0, m.pi], michalewicz, 5000*x)
                elapsed_time = (time.time() - time1) * 1000
                func4 = elapsed_time + func4
        
        print("Func>> DEJONG :: DIM>>", x, ":: Time>>", func1 / 30,"milliseconds")
        print("Func>> RASTRIGIN :: DIM>>", x, ":: Time>>", func2 / 30,"milliseconds")
        print("Func>> SCHWEFEL :: DIM>>", x, ":: Time>>", func3 / 30,"milliseconds")
        print("Func>> MICHALEWICZ :: DIM>>", x, ":: Time>>", func4 / 30,"milliseconds")
        print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
