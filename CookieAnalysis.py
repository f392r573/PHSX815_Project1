#! /usr/bin/env python

# imports of external packages to use in our code
import sys
import math
import numpy as np
import matplotlib.pyplot as plt

# import our Random class from python/Random.py file
sys.path.append(".")
from MySort import MySort

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
    times = []
    times_avg = []

    list_times = []

    need_rate = True
    
    with open(InputFile) as ifile:
        for line in ifile:
            if need_rate:
                need_rate = False
                rate = float(line)
                continue
            
            lineVals = line.split()
            Nmeas = len(lineVals)
            t_avg = 0
            times_val = []
            for v in lineVals:
                t_avg += float(v)
                times.append(float(v))
                times_val.append(float(v))


            list_times.append(times_val)
            t_avg /= Nmeas
            times_avg.append(t_avg)

    Sorter = MySort()

    times = Sorter.DefaultSort(times)
    times_avg = Sorter.DefaultSort(times_avg)
    # try some other methods! see how long they take
    # times_avg = Sorter.BubbleSort(times_avg)
    # times_avg = Sorter.InsertionSort(times_avg)
    # times_avg = Sorter.QuickSort(times_avg)

    # ADD YOUR CODE TO PLOT times AND times_avg HERE

    #Calculate Quantiles:
    q1 = np.quantile(times,0.25)
    q2 = np.quantile(times,0.50)
    q3 = np.quantile(times,0.75)

    avg_q1 = np.quantile(times_avg,0.25)
    avg_q2 = np.quantile(times_avg,0.50)
    avg_q3 = np.quantile(times_avg,0.75)

    #make Npass figure
    plt.figure()
    plt.hist(times,Nmeas+150,density=False,alpha=0.75)
    plt.xlabel('Time between missing cookies[days]')
    plt.ylabel('Probability')
    plt.title("rate of 2.00 cookies/day")
    plt.grid(True)
    plt.axvline(q1,label="25th Quantile",color="r")
    plt.axvline(q2,label="50th Quantile",color="g")
    plt.axvline(q3,label="75th Quantile",color="b")
    plt.legend()
    plt.show()



    plt.figure()
    plt.hist(times_avg,Nmeas+150,density=False,alpha=0.5,color='r')
    plt.xlabel('Average time between missing cookies[days]')
    plt.ylabel('Probability')
    plt.title("10 measurments/experiment with rate of 2.00 cookies/day")
    plt.grid(True)
    plt.axvline(avg_q1,label="25th Quantile",color="b")
    plt.axvline(avg_q2,label="50th Quantile",color="g")
    plt.axvline(avg_q3,label="75th Quantile",color="r")
    plt.legend()
    plt.show()
