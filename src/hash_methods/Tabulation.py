""" ===========================================================================
CompSci 261P Data Structures Project 1

Tests for hash methods (linear, chained, cuckoo, chained with tabulation)

Author: Qixiang Zhang (David)
Student ID: 70644128
Email: qixianz@uci.edu
=========================================================================== """

from util.util import isPrime
import random; random.seed(261)
from math import floor

class Tabulation:
    num_rehash = 0
    population = 0
    alpha_max = 0.5
    cap = 1
    table = [[[None, None]]]
    t1 = []
    t2 = []
    t3 = []
    t4 = []

    def __init__(self, alpha_max=0.5):
        self.num_rehash = 0
        self.population = 0
        self.alpha_max = alpha_max
        self.cap = 107
        self.table = [[[None, None]] for i in range(107)]
        self.t1 = []
        self.t2 = []
        self.t3 = []
        self.t4 = []
        self.__build_hashmap()

    def __build_hashmap(self):
        self.t1 = [floor(random.random()*0xffffffff) for _ in range(256)]
        self.t2 = [floor(random.random()*0xffffffff) for _ in range(256)]
        self.t3 = [floor(random.random()*0xffffffff) for _ in range(256)]
        self.t4 = [floor(random.random()*0xffffffff) for _ in range(256)]

    def __getloc(self, key, cap):
        h1 = self.t1[ (key)     & 0xff  ]
        h2 = self.t2[ (key>>8)  & 0xff  ]
        h3 = self.t3[ (key>>16) & 0xff  ]
        h4 = self.t4[ (key>>24) & 0xff  ]
        h = h1 ^ h2 ^ h3 ^ h4
        return h % cap
        
    """ search operation """
    def search(self, key):
        loc = self.__getloc(key, self.cap)
        for i in range(len(self.table[loc])):
            if self.table[loc][i][0] == key:
                return True, loc, self.table[loc][i][1], i
        #  # for debug
        #  print("key not found - ", key)
        return False, loc, None, 0
    
    """ insert (put) operation """

    def insert(self, key, value):
        self.population += 1
        if (self.current_alpha() >= self.alpha_max):
            self.__rehash_up()
        found, loc, v, i = self.search(key)
        if (not found):
            if self.table[loc][i] == [None, None]:
                self.table[loc][i] = [key,value]
            else:
                self.table[loc].append([key,value])
            # # for debug
            # print("inserted - ({}, {})\n".format(key, value))
        else:
            raise Exception("kv pair already exists at {loc}".format(loc))

    """ delete operation """ 
    def delete(self, key):
        found, loc, v, i= self.search(key)
        if (found):
            del self.table[loc][i]
            self.population -= 1
        # if the key is not found
        else:
            raise Exception('{} not found'.format(key))

    """ get the number of collisions """
    def get_collision(self):
        size = self.cap
        res = 0
        for i in range(size):
            chain_size = len(self.table[i])
            if chain_size > 1:
                res += (chain_size - 1)
        return res

    """ rehash operation """
    def __next_prime(self, int_):
        while(not isPrime(int_)):
            int_ += 1
        return int_

    def __rehash(self, new_cap):
        old_cap = self.cap
        # construct new table
        new_table = [[[None, None]] for i in range(new_cap)]
        # copy the old key value pairs to the new table
        for i in range(0, old_cap):
            if (self.table[i][0] != [None, None]):
                for pair in self.table[i]:
                    key, value = pair[0], pair[1]
                    loc = self.__getloc(key, new_cap)
                    if (new_table[loc][0] == [None, None]):
                        new_table[loc][0] = [key,value]
                    else:
                        new_table[loc].append([key,value])
        # change the reference of the table and cap
        self.table = new_table
        self.cap = new_cap
    
    def __sizeup(self):
        # if the current alpha reached the threshold, double the table cap
        return self.__next_prime(self.cap*2)
    def __rehash_up(self):
        self.num_rehash += 1
        new_cap = self.__sizeup()
        self.__rehash(new_cap)
    
    """ helpers """
    def current_alpha(self):
        return self.population / self.cap
    
