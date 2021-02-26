#! /usr/bin/env python

# imports of external packages to use in our code
import sys
import math
import numpy as np
import matplotlib.pyplot as plt

import math
import numpy as np
from random import random, uniform
from math import log

# import our Random class from python/Random.py file
sys.path.append(".")
from MySort import MySort

def random_triangular(self,low, high, mode):
        while True:
            proposal = uniform(low, high)
            if proposal < mode:
                acceptance_prob = (proposal - low) / (mode - low)
            else:
                acceptance_prob = (high - proposal) / (high - mode)
            if random() < acceptance_prob: break
        return proposal

# main function for our CookieAnalysis Python code
if __name__ == "__main__":
   
    haveInput = False

    for i in range(1,len(sys.argv)):
        if sys.argv[i] == '-h' or sys.argv[i] == '--help':
            continue

        InputFile = sys.argv[i]
        haveInput = True
    
    if '-h' in sys.argv or '--help' in sys.argv or not haveInput:
        print ("Usage: %s [options] [input file]" % sys.argv[0])
        print ("  options:")
        print ("   --help(-h)          print options")
        print
        sys.exit(1)
    
    Nmeas = 1
    times0 = []
    times1= []
    times_avg0 = []
    times_avg1=[]
    times_val0=[]
    times_val1=[]

    haveH0 = False
    haveH1 = False

    if '-prob0' in sys.argv:
        p = sys.argv.index('-prob0')
        ptemp = float(sys.argv[p+1])
        if ptemp >= 0 and ptemp <= 1:
            p0 = ptemp
    if '-prob1' in sys.argv:
        p = sys.argv.index('-prob1')
        ptemp = float(sys.argv[p+1])
        if ptemp >= 0 and ptemp <= 1:
            p1 = ptemp
    if '-input0' in sys.argv:
        p = sys.argv.index('-input0')
        InputFile0 = sys.argv[p+1]
        haveH0 = True
    if '-input1' in sys.argv:
        p = sys.argv.index('-input1')
        InputFile1 = sys.argv[p+1]
        haveH1 = True


    list_times0 = []
    list_times1 = []
    LogLikeRatio0=0
    LogLikeRatio1=0

    low0= 2
    low1 = 3

    need_rate = True
    
    with open(InputFile0) as ifile:
        for line in ifile:
            if need_rate:
                need_rate = False
                rate0 = float(line)
                continue
            
            lineVals = line.split()
            Nmeas = len(lineVals)
            t_avg = 0
            times_val = []
            for v in lineVals:
                t_avg += float(v)
                times0.append(float(v))
                times_val0.append(float(v))


            list_times0.append(times_val0)
            t_avg /= Nmeas
            times_avg0.append(t_avg)
            LogLikeRatio0 += log( random_triangular(times0, 9,5 ,6))

    if haveH1:
        with open(InputFile1) as ifile:
            for line in ifile:
                if need_rate:
                    need_rate = False
                    rate1 = float(line)
                    continue
            
                lineVals = line.split()
                Nmeas = len(lineVals)
                t_avg = 0
                times_val = []
                for v in lineVals:
                    t_avg += float(v)
                    times1.append(float(v))
                    times_val1.append(float(v))


                list_times1.append(times_val1)
                t_avg /= Nmeas
                times_avg1.append(t_avg)
                LogLikeRatio1 -= log( random_triangular(times1, 7,4,5) )
    
        
        



    Sorter = MySort()

    times0 = Sorter.DefaultSort(times0)
    times_avg0 = Sorter.DefaultSort(times_avg0)

    times1 = Sorter.DefaultSort(times1)
    times_avg1 = Sorter.DefaultSort(times_avg1)





    # try some other methods! see how long they take
    # times_avg = Sorter.BubbleSort(times_avg)
    # times_avg = Sorter.InsertionSort(times_avg)
    # times_avg = Sorter.QuickSort(times_avg)

    # ADD YOUR CODE TO PLOT times AND times_avg HERE

    #Calculate Quantiles:
    q1_0 = np.quantile(times0,0.0)


    q2_0 = np.quantile(times0,0.50)
    q3_0 = np.quantile(times0,0.75)

    q1_1 = np.quantile(times1,0.25)
    q2_1 = np.quantile(times1,0.50)
    q3_1 = np.quantile(times1,0.75)

    avg0_q1 = np.quantile(times_avg0,0.25)
    avg0_q2 = np.quantile(times_avg0,0.50)
    avg0_q3 = np.quantile(times_avg0,0.75)

    avg1_q1 = np.quantile(times_avg1,0.25)
    avg1_q2 = np.quantile(times_avg1,0.50)
    avg1_q3 = np.quantile(times_avg1,0.75)

    #make Npass figure
    plt.figure()
    plt.hist(times0,Nmeas+1,density=True,alpha=0.75)
    if haveH1:
        plt.hist(times1, Nmeas+1, density=True, facecolor='g', alpha=0.7)
        plt.legend()
    plt.xlabel('Time between missing cookies[days]')
    plt.ylabel('Probability')
    plt.title("rate of 2.00 cookies/day")
    plt.grid(True)
    plt.axvline(q1_0,label="",color="r")


    plt.legend()
    plt.show()



    plt.figure()
    plt.hist(times_avg0,Nmeas+1,density=False,alpha=0.5,color='r')
    if haveH1:
        plt.hist(times_avg1,Nmeas+1,density=False,alpha=0.5,color='r')
    plt.xlabel('Average time between missing cookies[days]')
    plt.ylabel('Probability')
    plt.title("10 measurments/experiment with rate of 2.00 cookies/day")
    plt.grid(True)
    
    plt.legend()
    plt.show()
