#!/bin/python3

import math
import os
import random
import re
import sys
from fractions import Fraction


def findPoint(px, py, qx, qy):
    dx = math.fabs(px - qx)
    dy = math.fabs(py - qy)

    if px <= qx:
        rx = qx + dx
    else:
        rx = qx - dx

    if py <= qy:
        ry = qy + dy
    else:
        ry = qy - dy

    return(f"{int(rx)} {int(ry)}")

def summingSeries(n):



    t1 = 1

    tn = (n**2) - (n - 1)**2

    sn = (n*(t1 + tn)) // 2

    answer = sn % (10**9 + 7)

    return answer 

def sherlockPermutations(n, m):
    # from m choose 1 * (m + n -1)!
    
    permutations = math.comb(m, 1) * math.factorial(m + n - 1)

    answer = permutations % (10**9 + 7)

    return answer 
        
def mehtaShopping(a, days):
    #a is an array of coin values, index is coin type
    #L is lower price and R is upper price in range
    #days in a list[list] where days[i][0] is L for each day i and days[i][1] is R
    
    #need a dp programme that finds for each permutation of "items bought" throughout the days what is max number
    #create an item value array that stores all item prices found from each price range in days
    #go through each item value array element in a loop, trial each coin and then move through item array
    #dp will store the indicie of each coin used
    #use dp array to return array of coins_used
    #print integer amount of coins on counter that = max(coins, coins for this item start)

    dp = {}
    n = len(a)

    items = [price for price in range(days[0], days[1]+1)]
    max_items = 0

    return False
                   
def studentsInClass(i):
    day = i
    students = 0

    for j in range(1, day):
        #find the students cycle:
        if ((day//j) % 2) == 0:
            students += 1

    #handle student 1
    if day % 2 == 1:
        students += 1   

    return students

def mehtaLazy(n):
    # floor the square root of n to find the max number that gives a perfect square < n
    # even perfect squares are only created by even numbers.
    # to find the perfect divisors, loop to sqrt(n) and add two to the counter for each n % k == 0 as you get the small half
    
    k = math.floor(math.sqrt(n))
    perfectDivisorCount = 0
    evenPerfectSquareCount = 0
    
    for i in range(1, k + 1):
        if n % i == 0:
            # i itself is always a proper divisor of n (i <= sqrt(n) < n for n > 1)
            perfectDivisorCount += 1
            r = math.isqrt(i)
            if (r * r == i) and i % 2 == 0:
                evenPerfectSquareCount += 1

            pair = n // i
            # skip the paired "large half" divisor when:
            #  - i == 1, since pair would equal n itself, and N is excluded from "proper divisors"
            #  - pair == i, to avoid double-counting the middle divisor of a perfect square
            if i != 1 and pair != i:
                perfectDivisorCount += 1
                q = math.isqrt(pair)
                if (q * q == pair) and pair % 2 == 0:
                    evenPerfectSquareCount += 1


    if perfectDivisorCount == 0 or evenPerfectSquareCount == 0:
        return 0
    else:
        return Fraction(evenPerfectSquareCount, perfectDivisorCount)

def isPrime(n):
    # int() converts n to a whole number (e.g. 5.0 -> 5).
    # math.isqrt() and range() below both refuse floats, so this guards against that.
    n = int(n)

    if n < 2:
        return False
    if n in (2,3):
        return True
    if n % 2 == 0:
        return False
    for i in range(3, math.isqrt(n) + 1, 2):
        if n % i == 0:
            return False

    return True

def sum_divisors_of_n(n):
    # int() converts n to a whole number so range(1, n) below accepts it.
    # (This was the line that crashed with "'float' object cannot be interpreted as an integer".)
    n = int(n)

    sum_previous_terms = 0

    result = 0

    for i in range(1, n+1):
        if n % i == 0:
            sum_x_divisors = 0
            for j in range(1, i+1):
                if i % j == 0:
                    sum_x_divisors += j
            result += sum_x_divisors
            
    return result        
    
def divisorExplorationII(m, a):
    # Make sure both inputs are whole numbers, since m is used in range() below.
    m = int(m)
    a = int(a)

    n = 1
    prime_count = 1
    value_i = 1

    while prime_count <= m:
            if isPrime(value_i):
                # math.pow() ALWAYS returns a float (e.g. math.pow(2, 3) -> 8.0),
                # so wrap it in int() to turn the result back into a whole number
                # before multiplying. That keeps n an int the whole way through.
                n = n*(int(math.pow(value_i, (a + prime_count))))
                prime_count += 1
            value_i += 1

    answer = sum_divisors_of_n(n) % (10**9 + 7)

    return answer    


# This block only runs when you run this file directly (e.g. `python HackerRank.py`),
# NOT when another file imports it. That's what the __name__ == '__main__' check does.
if __name__ == '__main__':
    # HackerRank sets an environment variable called OUTPUT_PATH; your PC doesn't.
    # Checking for it lets this same block work in BOTH places, so you can paste
    # the whole file into HackerRank without editing anything.
    if 'OUTPUT_PATH' in os.environ:
        # --- HackerRank mode: read queries from input, write answers to a file ---
        fptr = open(os.environ['OUTPUT_PATH'], 'w')

        # First line is a single number: how many queries follow
        q = int(input().strip())

        for q_itr in range(q):
            # Each query line holds TWO numbers, e.g. "2 0".
            # .split() breaks it at the space into a list of strings: ["2", "0"]
            first_multiple_input = input().strip().split()

            # Convert each piece from a string to an int separately
            m = int(first_multiple_input[0])
            a = int(first_multiple_input[1])

            result = divisorExplorationII(m, a)

            # fptr.write() only accepts strings, so convert the number with str()
            fptr.write(str(result) + '\n')

        fptr.close()
    else:
        # --- Local mode: run Sample Input 0 without typing anything in ---
        # Each tuple is one query line: (m, a)
        test_cases = [
            (2, 0),
            (3, 0),
            (2, 4),
        ]

        # Loop over each (m, a) pair, unpacking the tuple into two variables
        for m, a in test_cases:
            print(divisorExplorationII(m, a))