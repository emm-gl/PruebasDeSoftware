# 1. Compute statistics

"""
Req1. The program shall be invoked from a command line. The program shall receive a
file as parameter. The file will contain a list of items (presumable numbers).

Req 2. The program shall compute all descriptive statistics from a file containing numbers. The results shall be print on a 
screen and on a file named StatisticsResults.txt. All computation MUST be calculated using the basic algorithms,
not functions or libraries.The descriptive statistics are mean, median, mode, standard deviation, and variance.

Req 3. The program shall include themechanism to handle invalid data in the file. Errors should be displayed in the console
and the execution must continue.

Req 4. The name of the program shall be computeStatistics.py

Req 5. The minimum format to invoke the program shall be as follows: python computeStatistics.py fileWithData.txt

Req 6. The program shall manage files having from hundreds of items to thousands of items.

Req 7. The program should include at the end of the execution the time elapsed for the execution and calculus of the data. This
number shall be included in the results file and on the screen. 

Req 8. Be compliant with PEP8.
"""

import sys
import numpy as np
import math
import tkinter as tk
import time


# Get the argumtent (file)
fileName = sys.argv[1]

def computeStat(file: str):
    tstart = time.time()

    try:
        data = []
        with open(file, 'r') as doc:                        #Get the data of the file:
            for line in doc:
                try:
                    number = float(line.strip())
                    data.append(number)
                except ValueError:
                    print(f"Invalid data in {file}. Skipping line: {line.strip()}")

        n = len(data)

        #Mean:
        msum = 0
        for i in data:
            msum = msum + i
        mean = round(msum / n, 4)

        #Median:
        sorted_numbers = sorted(data)
        if(n % 2 == 0): 
            median = (sorted_numbers[n // 2 - 1] + sorted_numbers[n // 2]) / 2            #Even observations insde the list
        else:
            median = sorted_numbers[int((n/2) + 1)]                                        #Odd observations insde the list

        #Mode
        freq = {}
        for value in data:
            freq[value] = freq.get(value, 0) + 1
        mode = next(iter([clave for clave, valor in freq.items() if valor == max(freq.values())]), None)

        #Variance:
        vsum = 0
        for num in data:
            vsum = vsum + (num - mean) ** 2
        var = round(vsum / (n - 1),4)

        #Standard Deviation:
        sdev = round(math.sqrt(var), 4)

        span = round((time.time() - tstart) * 1000, 4)       #Time in miliseconds

        return n, mean, median, mode, var, sdev, span

    except Exception as e:
        print(f"Unexpected error: {e}")
    return []


count, mean, median, mode, variance, sdev, span = computeStat(fileName)


print(count)
print(mean)
print(median)
print(mode)
print(variance)
print(sdev)
span: str
print(f'Execution time {span} miliseconds ')