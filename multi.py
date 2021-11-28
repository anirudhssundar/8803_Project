#!/usr/bin/env python3
import itertools
import multiprocessing
multiprocessing.set_start_method('fork')
#Generate values for each parameter
a = range(10)
b = range(10)

#Generate a list of tuples where each tuple is a combination of parameters.
#The list will contain all possible combinations of parameters.
paramlist = list(itertools.product(a,b))

#A function which will process a tuple of parameters
def func(params):
  a = params[0]
  b = params[1]
  return a*b

#Generate processes equal to the number of cores
pool = multiprocessing.Pool()

#Distribute the parameter sets evenly across the cores
res  = pool.map(func,paramlist)

print(res)
