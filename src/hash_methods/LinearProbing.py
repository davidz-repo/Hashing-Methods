""" ===========================================================================
CompSci 261P Data Structures Project 1

Tests for hash methods (linear, chained, cuckoo, chained with tabulation)

Author: Qixiang Zhang (David)
Student ID: 70644128
Email: qixianz@uci.edu
=========================================================================== """

from util.util import isPrime

class LinearProbing:
    num_rehash = 0
    population = 0
    alpha_max = 0.5
    cap = 1
    table = [[None, None]]

    def __init__(self, alpha_max=0.5):
        self.num_rehash = 0
        self.population = 0
        self.alpha_max = alpha_max
        self.cap = 107
        self.table = [[None, None] for i in range(107)]

    """ search operation """
    def search(self, key):
        N = self.cap
        loc = key % N
        while (self.table[loc] != [None, None]):
            if (self.table[loc][0] == key):
                return True, loc, self.table[loc][1]
            else:
                loc = (loc+1) % N
        return False, loc, None
    
    """ insert (put) operation """
    def insert(self, key, value):
        self.population += 1
        if (self.current_alpha() >= self.alpha_max):
            self.__rehash_up()
        found, loc, v = self.search(key)
        if (found):
            raise Exception("Same key already exists in the hash: {}\n"\
                    .format(key))
        else:
            self.table[loc][0], self.table[loc][1]= key, value
            #print("inserted - ({}, {})\n".format(key, value))

    """ delete operation """ 
    def delete(self, key):
        found, loc, v = self.search(key)
        if (found):
            self.table[loc] = [None, None]
            self.__shiftback(loc)
            self.population -= 1
        else:
            raise Exception('{} not found'.format(key))


    def __reInsert(self, key, value):
        found, loc, v = self.search(key)
        self.table[loc][0], self.table[loc][1]= key, value
    def __shiftback(self, loc):
        N = self.cap
        if loc == N-1:
            loc = 0
        else: 
            loc += 1
        while ( self.table[loc] != [None, None] ):
            [key, value] = self.table[loc]
            real_loc = key % N
            if (real_loc != loc):
                self.table[loc] = [None, None]
                self.__reInsert(key,value)
            loc = (loc+1) % N

    """ rehash operation """
    def __next_prime(self, int_):
        while(not isPrime(int_)):
            int_ += 1
        return int_

    def __rehash(self, new_cap):
        old_cap = self.cap
        # construct new table
        new_table = [[None, None] for i in range(new_cap)]
        # copy the old key value pairs to the new table
        for i in range(0, old_cap):
            if (self.table[i] != [None, None]):
                [key,value] = self.table[i]
                loc = key % new_cap
                while (new_table[loc]!= [None, None]):
                    loc = (loc + 1) % new_cap
                new_table[loc] = [key, value]
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

    """ get the number of collisions """
    def get_collision(self):
        size = self.cap
        res = 0
        for i in range(size):
            key = self.table[i][0]
            if key != None:
                if key % self.cap != i:
                    res += 1
        return res
    
    """ helpers """
    def current_alpha(self):
        return self.population / self.cap
