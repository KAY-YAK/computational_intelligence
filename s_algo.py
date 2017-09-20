import math as m
import random as rand
import copy
import time

# dejong function [-5.12,5.12].
def de_jong(vector):
        sum = 0
        for dim in vector:
                sum = sum + dim**2
        
        return sum

# rastrigin  function [-5.12,5.12].
def rastrigin(vector):
        sum = 10 * len(vector)
        for dim in vector:
                sum = sum + dim**2 - 10*m.cos(2*m.pi*dim)
        
        return sum

# schwefel fucntion [-500, 500]
def  schwefel(vector):
        sum = 0
        for dim in vector:
                sum = sum + dim*m.sin(m.sqrt(abs(dim)))
        
        sum = 418.9829*len(vector) - sum
        return  sum

# michalewicz function  [0, pi]
def michalewicz(vector):
        sum = 0
        count = 0
        for dim in vector:
                count = count + 1
                sum = m.sin(dim) * m.sin((count * dim**2)/m.pi)**20
        
        return -sum



def fix(value):
        value = m.floor(value)  if value >= 0 else m.ceil(value)
        return value


# toroidal correction
'''----------------------------------------------------------------------------
@params :
        vector  :    is a vector of values(basically a list of values)
        bounds :    is a 2 dim list containing lower bound (bounds[0]) and upper bound (bounds[1])

------------------------------------------------------------------------------'''

def toroidal_correction(vector, bounds):
        for x in range(len(vector)):
                temp  = (vector[x] - bounds[0]) / (bounds[1] - bounds[0])
                if temp > 1:
                        temp  = temp - fix(temp)
                elif temp < 0:
                        temp = temp - abs(temp - fix(temp))
                
                vector[x] = bounds[0] + temp*(bounds[1] - bounds[0])
        return vector
                
        

def saturate(vector, bounds):
        for x in range(len(vector)):
                vector[x] = min(max(vector[x], bounds[0]),bounds[1])
        return vector

# s algorithm
'''----------------------------------------------------------------------------
 @params :
        no_iter   :       budget
        dim         :       dimension of func
        bounds   :      2 dimensional list containing lower bound (bounds[0]) and upper bound (bounds[1])
        func        :       name of function to be optimized
        
 ----------------------------------------------------------------------------'''
def s_algo(no_iter, dim, bounds,func):
        random_guess = []
        for x in range(dim):
                random_guess.append( rand.uniform(bounds[0], bounds[1]))
        
        best_guess = toroidal_correction(random_guess, bounds)
        evaluate = func(best_guess)
        
        
        delta = .4*(bounds[1]-bounds[0])
        
        temp = copy.deepcopy(best_guess)
        
        # no_iter is th no of calls to the function
        iter_no = 0
        while(iter_no <= no_iter):
                temp = saturate(temp, bounds)
                best_eval = evaluate
                
                for y in range(len(best_guess)):
                        temp[y] = best_guess[y] - delta
                        evaluate = func(temp)
                        iter_no = iter_no + 1
                        
                        
                        if evaluate <= best_eval:
                                best_guess[y] = copy.deepcopy(temp[y])
                                best_eval = evaluate
                        else:
                                temp[y] = best_guess[y]  + (delta *.5)
                                evaluate = func(temp)
                                iter_no = iter_no + 1
                                if evaluate <= best_eval:
                                        best_guess[y] = copy.deepcopy(temp[y])
                                        best_eval = evaluate
                                else:
                                        temp[y] = best_guess[y]
                                        evaluate = best_eval
                
                                        
                if evaluate  == best_eval:
                        delta = delta*.5
                        

        best_guess = saturate(best_guess,bounds)
        return best_guess
        


dimension = [10,30,50,75,100]
for x in dimension:
        func1 = func2 = func3 = func4 = 0
        for y in range(30):
                time1 = time.time()
                s_algo(200, x, [-5.12,5.12], de_jong)
                elapsed_time = (time.time() - time1)*1000
                func1 = elapsed_time + func1

                time1 = time.time()
                s_algo(200, x, [-5.12,5.12], rastrigin)
                elapsed_time = (time.time() - time1) * 1000
                func2 = elapsed_time + func2

                time1 = time.time()
                s_algo(200, x, [-500, 500], schwefel)
                elapsed_time = (time.time() - time1) * 1000
                func3 = elapsed_time + func3

                time1 = time.time()
                s_algo(200, x, [0, m.pi], michalewicz)
                elapsed_time = (time.time() - time1) * 1000
                func4 = elapsed_time + func4
        
        print("Func>> DEJONG :: DIM>>", x ,":: Time>>",func1/30, "milliseconds")
        print("Func>> RASTRIGIN :: DIM>>", x, ":: Time>>", func2 / 30,"milliseconds")
        print("Func>> SCHWEFEL :: DIM>>", x, ":: Time>>", func3 / 30,"milliseconds")
        print("Func>> MICHALEWICZ :: DIM>>", x, ":: Time>>", func4 / 30,"milliseconds")
        print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        