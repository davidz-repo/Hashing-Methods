""" ===========================================================================
CompSci 261P Data Structures Project 1

Tests for hash methods (linear, chained, cuckoo, chained with tabulation)

Author: Qixiang Zhang (David)
Student ID: 70644128
Email: qixianz@uci.edu
=========================================================================== """

from util.util import isPrime
from math import floor

class Cuckoo:
    num_rehash = 0
    population = 0
    alpha_max = 0.5
    cap = 2
    table = [[[None,None]], [[None, None]]]

    def __init__(self, alpha_max=0.5):
        self.num_rehash = 0
        self.population = 0
        self.alpha_max = alpha_max
        self.cap = 106
        self.table = [ [[None, None] for i in range(53)],
                    [[None, None] for i in range(53)] ]

    """ search operation """
    def search(self, key):
        # return boolean found, table i, location at table i, and value
        # search both tables
        size = len(self.table[0])
        loc0 = self.__getloc0( key,size )
        loc1 = self.__getloc1( key,size )
        if (self.table[0][loc0][0] == key):
            return True, 0, loc0, self.table[0][loc0][1]
        elif (self.table[1][loc1][0] == key):
            return True, 1, loc1, self.table[1][loc1][1]
        #  # debug
        #  print("Key {} not found".format(key))
        if (self.table[0][loc0][0] == None):
            return False, 0, loc0, None
        elif (self.table[1][loc1][0] == None):
            return False, 1, loc1, None
        return False, "X", loc0, loc1
    
    """ insert (put) operation """
    def insert(self, key, value):
        self.population += 1

        if (self.current_alpha() >= self.alpha_max):
            self.__rehash_up()

        found, t, loc, v = self.search(key)

        if (found):
            # if none of the location is empty, __cuckoo_insert it
            raise Exception('same kv pair exists!! table[{}][{}]'.format(t, loc))
        else:
            # if one of the location is empty, insert it
            if (t != "X"):
                self.table[t][loc] = [key, value]
                #  # debug
                #  print("inserted - ({}, {})\n".format(key, value))
            else:
                flag, self.table = self.__cuckoo_insert( key, value, self.table )
                while ( not flag):
                    self.__rehash_up()
                    flag, self.table = self.__cuckoo_insert( key, value, self.table )

    """ delete operation """ 
    def delete(self, key):
        found, t, loc, v = self.search(key)
        if (found):
            self.table[t][loc] = [None, None]
            self.population -= 1
        # else - the key is not found
        else:
            raise Exception('{} not found'.format(key))

    """ get the number of collisions """
    def get_collision(self):
        size = len(self.table[0])
        population0 = 0
        population1 = 0
        for _ in range ( size ):
            if self.table[0][_] != [None, None]:
                population0 += 1
        population1 = self.population - population0
        return population0 if population0 < population1 else population1

    """ cuckoo insert operation """
    def __cuckoo_insert( self, k0, v0, table ):
        size = len(table[0])
        new_table=[ [[None, None] for i in range(size)],
                    [[None, None] for i in range(size)] ]
        for t in range(2):
            for i in range(size):
                new_table[t][i] = table[t][i]

        next_table = 0
        next_loc = self.__getloc0( k0,size )

        out_k, out_v = k0, v0
        in_k, in_v = k0, v0

        while( True ):
            if (new_table[next_table][next_loc] == [None, None]):
                new_table[next_table][next_loc] = [out_k, out_v]
                return True, new_table
            else:
                if (new_table[next_table][next_loc] == [k0, v0]):
                    return False, table
                elif (new_table[next_table][next_loc] != [k0, v0]):
                    out_k = new_table[next_table][next_loc][0]
                    out_v = new_table[next_table][next_loc][1]
                    new_table[next_table][next_loc] = [in_k, in_v]
                    in_k, in_v = out_k, out_v
                    next_table = 1 - next_table
                    if (next_table == 0):
                        next_loc = self.__getloc0( out_k, size )
                    else:
                        next_loc = self.__getloc1( out_k, size )

    """ rehash operation """
    def __rehash(self, new_cap):
        old_t_size = len(self.table[0])
        new_t_size = floor( new_cap/2 )
        # construct new table
        new_table=[ [[None, None] for i in range(new_t_size)],
                    [[None, None] for i in range(new_t_size)] ]
        # copy the old key value pairs to the new table
        for t in range(0, 2):
            for i in range(old_t_size):
                if (self.table[t][i][0] != None):
                    key, value = self.table[t][i][0], self.table[t][i][1]
                    loc0 = self.__getloc0( key,new_t_size )
                    loc1 = self.__getloc1( key,new_t_size )
                    if (new_table[0][loc0] == [None, None]):
                        new_table[0][loc0] = [key, value]
                    elif (new_table[1][loc1] == [None, None]):
                        new_table[1][loc1] = [key, value]
                    else: 
                        flag, new_table = self.__cuckoo_insert( key, value, new_table )
                        if (not flag):
                            return False
        # change the reference of the table and cap
        self.table = new_table
        self.cap = new_cap
        return True
    
    def __next_prime(self, int_):
        while(not isPrime(int_)):
            int_ += 1
        return int_

    def __sizeup(self, cap):
        # if the current alpha reached the threshold, double the capacity
        return self.__next_prime( cap/2*2 )

    def __rehash_up(self):
        self.num_rehash += 1
        new_cap = floor(self.__sizeup(self.cap)*2)
        flag = self.__rehash(new_cap)
        while (not flag):
            self.num_rehash += 1
            new_cap = floor(self.__sizeup(new_cap)*2)
            flag = self.__rehash(new_cap)

    
    """ helpers functions """
    def current_alpha(self):
        return self.population / self.cap

    def __getloc0(self, key, size):
        # assuming both tables are same size
        return key % size
    def __getloc1(self, key, size):
        return floor(key*101/size) % size


