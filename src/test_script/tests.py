""" ===========================================================================
CompSci 261P Data Structures Project 1

Tests for hash methods (linear, chained, cuckoo, chained with tabulation)

Author: Qixiang Zhang (David)
Student ID: 70644128
Email: qixianz@uci.edu
=========================================================================== """

# libraries - begin

# import time.clock() to record time lapse for operations
from time import clock as clk

# import readInputs to read/generate sorted or randomized (key,value) pair inputs
from util.util import readInputs

# import hash methods
from hash_methods import LinearProbing as Lp
from hash_methods import Chaining as Cn
from hash_methods import Cuckoo as Cc
from hash_methods import Tabulation as Tb

# libries - end

# debug - begin
from ipdb import set_trace as XX
# debug - end

"""----------------------------------------------------------------------------
                            Factor 1 - Load Factor:
----------------------------------------------------------------------------"""

"""
T1. How does the preset load factor affect the time complexity for batch 
    operations?

Assumptions for batch operations:
    - Preset load factors { 0.05, 0.10, ..., 0.90, 0.95, 1.00 }
    - number of insertions, search, deletions: 700
    - search and delete non-existing keys not allowed - will throw exception
    - randomize seed (numpy): 33, 9723, 11937
"""
def t1(objname, testname, resetflag):

    # input parameters
    seeds = [33, 9723, 11937];
    input_0 = readInputs(700, shuffle=True, s=seeds[0]);
    input_1 = readInputs(700, shuffle=True, s=seeds[1]);
    input_2 = readInputs(700, shuffle=True, s=seeds[2]);
    inputs = [input_0, input_1, input_2];
    load_factors = [x/100 for x in range(5, 101, 5)]

    # test output
    filename = str(testname) + '_' + str(objname) + '.csv'
    columns = 'Method,Test,'
    columns += 'Seed,Alpha,Current_Alpha,Insert,Search,Delete\n'

    with open(filename, 'w') as f:

        f.write(columns)
        si = 0
        for input_list in inputs:
            s = seeds[si]

            for alpha in load_factors:
                analysis = []

                if resetflag == "lp":
                    obj = Lp.LinearProbing(alpha)
                elif resetflag == "cn":
                    obj = Cn.Chaining(alpha)
                elif resetflag == "cc":
                    obj = Cc.Cuckoo(alpha)
                elif resetflag == "tb":
                    obj = Tb.Tabulation(alpha)

                # clk insertion
                c0 = clk()
                for key, value in input_list:
                    obj.insert(key, value)
                c_insertion = clk() - c0
                calpha = obj.current_alpha()

                # clk search
                c0 = clk()
                for key, value in input_list:
                    obj.search(key)
                c_search = clk() - c0

                # clk deletion
                c0 = clk()
                for key, value in input_list:
                    obj.delete(key)
                c_deletion = clk() - c0

                analysis.append([objname, testname, s, alpha, \
                                 calpha, c_insertion, c_search, c_deletion])
                del obj

                for _ in analysis:
                    o = str(_[0])
                    t = str(_[1])
                    s = str(_[2])
                    a = str(_[3])
                    c = str(_[4])
                    x = str(_[5])
                    y = str(_[6])
                    z = str(_[7])
                    f.write(o+','+t+','+s+','+a+','+c+','+x+','+y+','+z+'\n')
            si += 1
            
"""
T2. How does the load factor affect the number of collisions?
T3. How does the load factor affect the number of re-hash?
T4. How does the load factor affect the time complexity for single operations?

Assumptions for single operations:
    - max load factor: 1.0
    - number of insertions, search, deletions: 1435
    - search and delete non-existing keys not allowed - will throw exception
    - randomize seed (numpy): 33, 9723, 11937
"""
def t2t3t4(objname, testname, resetflag):
    # input parameters
    seeds = [33, 9723, 11937];
    t_input_0 = readInputs(1435, shuffle=True, s=seeds[0]);
    t_input_1 = readInputs(1435, shuffle=True, s=seeds[1]);
    t_input_2 = readInputs(1435, shuffle=True, s=seeds[2]);
    t_inputs = [t_input_0, t_input_1, t_input_2];

    # test output
    filename = str(testname) + '_' + str(objname) + '.csv'
    columns = 'Test,Method,Operation,Seed,Population,Time,Load Factor,'
    columns += 'Collision,Num-Rehash\n'

    with open(filename, 'w') as f:

        f.write(columns)

        si = 0
        
        for input_list in t_inputs:
            s = seeds[si]
            alpha = 1

            if resetflag == "lp":
                obj = Lp.LinearProbing(alpha)
            elif resetflag == "cn":
                obj = Cn.Chaining(alpha)
            elif resetflag == "cc":
                obj = Cc.Cuckoo(alpha)
            elif resetflag == "tb":
                obj = Tb.Tabulation(alpha)

            for key, value in input_list:
                # clk insertion
                c0 = clk()
                obj.insert(key, value)
                c_i = clk() - c0
                c_s1 = clk()
                obj.search(key)
                c_s = clk() - c_s1
                pp = obj.population
                lf = obj.current_alpha()
                col = obj.get_collision()
                reh = obj.num_rehash
                f.write(str(testname)+','+str(objname)+',Insert,'+str(s)+',');
                f.write(str(pp)+','+str(c_i)+','+str(lf)
                        +','+str(col)+','+str(reh)+'\n')

                f.write(str(testname)+','+str(objname)+',Search,'+str(s)+',');
                f.write(str(pp)+','+str(c_s)+','+str(lf)
                        +','+str(col)+','+str(reh)+'\n')

            for key, value in input_list:
                # clk deletion
                c0 = clk()
                obj.delete(key)
                c_d = clk() - c0
                pp = obj.population
                lf = obj.current_alpha()
                col = obj.get_collision()
                reh = obj.num_rehash
                f.write(str(testname)+','+str(objname)+',Delete,'+str(s)+',');
                f.write(str(pp)+','+str(c_s)+','+str(lf)
                        +','+str(col)+','+str(reh)+'\n')

            del obj
            si += 1

"""----------------------------------------------------------------------------
                Factor 2 - Population (number of elements):
----------------------------------------------------------------------------"""
"""
T5.  How does the population affect batch operations time complexity?
T6.  How does the population affect the number of collisions?
T7.  How does the population affect the number of re-hash?

Assumptions for batch operations:
    - Fixed max load factor { 0.2, 0.5, 0.8 }
    - Populations { 1k, 2k, 3k, 5k, 8k, 13k, 20k, 35k, 60k, 100k }
    - search and delete non-existing keys not allowed - will throw exception
    - randomize seed (numpy): 33, 9723, 11937

"""
def t5t6t7(objname, testname, resetflag):
    # input parameters
    # test output
    filename = str(testname) + '_' + str(objname) + '.csv'

    with open(filename, 'w') as f:


        seeds = [33, 9723, 11937];
        si = 0

        t_inputs = [1000, 2000, 3000, 5000, 8000,
                    13000, 20000, 35000, 60000, 100000]

        columns = 'Test,Method,'
        columns += 'Seed,Population,AlphaMax,Insertion Time,Search Time,'
        columns += 'Deletion Time,Load Factor,Collision,Num-Rehash\n'

        f.write(columns)

        for sd in seeds:

            for gen in t_inputs:
                
                input_list = readInputs( gen, shuffle=True, s=sd )

                for alpha in [ 0.2, 0.5, 0.9 ]:

                    if resetflag == "lp":
                        obj = Lp.LinearProbing(alpha)
                    elif resetflag == "cn":
                        obj = Cn.Chaining(alpha)
                    elif resetflag == "cc":
                        obj = Cc.Cuckoo(alpha)
                    elif resetflag == "tb":
                        obj = Tb.Tabulation(alpha)

                    # clk insertion
                    c0 = clk()
                    for key, value in input_list:
                        obj.insert(key, value)
                    c_i = clk() - c0

                    # get data
                    pp = obj.population
                    lf = obj.current_alpha()
                    col = obj.get_collision()
                    reh = obj.num_rehash

                    # clk search
                    c0 = clk()
                    for key, value in input_list:
                        obj.search(key)
                    c_s = clk() - c0

                    # clk deletion
                    c0 = clk()
                    for key, value in input_list:
                        obj.delete(key)
                    c_d = clk() - c0

                    f.write(testname+','+objname+',')
                    f.write(str(sd)+','+str(pp)+','+str(alpha)+','+str(c_i)
                            +','+str(c_s)+','+str(c_d)+','+str(lf)+','
                            +str(col)+','+str(reh)+'\n')
                    del obj

"""----------------------------------------------------------------------------
                        Factor 3 - Pre-sorted keys:
----------------------------------------------------------------------------"""
"""
T8.  How does pre-sorting the keys affect batch operations time complexity?

Assumptions for batch operations:
    - Fixed max load factor { 0.2, 0.5, 0.9 }
    - Population = 4096 (2^12 just for fun)
    - search and delete non-existing keys not allowed - will throw exception
    - randomize seed (numpy): 33, 9723, 11937

"""

def t8t9t10(objname, testname, resetflag):

    filename = str(testname) + '_' + str(objname) + '.csv'

    with open(filename, 'w') as f:

        seeds = [33, 9723, 11937];
        si = 0

        t_shuffle = [True, False]

        columns = 'Test,Method,'
        columns += 'Seed,Sorted,Population,AlphaMax,Insertion Time,Search Time,'
        columns += 'Deletion Time,Load Factor,Collision,Num-Rehash\n'
        f.write(columns)

        for sd in seeds:
            for flag in t_shuffle:
                input_list = readInputs( 10000, shuffle=flag, s=sd )
                for alpha in [ 0.2, 0.5, 0.9 ]:

                    if resetflag == "lp":
                        obj = Lp.LinearProbing(alpha)
                    elif resetflag == "cn":
                        obj = Cn.Chaining(alpha)
                    elif resetflag == "cc":
                        obj = Cc.Cuckoo(alpha)
                    elif resetflag == "tb":
                        obj = Tb.Tabulation(alpha)

                    # clk insertion
                    c0 = clk()
                    for key, value in input_list:
                        obj.insert(key, value)
                    c_i = clk() - c0

                    # get data
                    pp = obj.population
                    lf = obj.current_alpha()
                    col = obj.get_collision()
                    reh = obj.num_rehash

                    # clk search
                    c0 = clk()
                    for key, value in input_list:
                        obj.search(key)
                    c_s = clk() - c0

                    # clk deletion
                    c0 = clk()
                    for key, value in input_list:
                        obj.delete(key)
                    c_d = clk() - c0

                    f.write(testname+','+objname+',')
                    f.write(str(sd)+','+str(flag)+','+str(pp)+','+str(alpha)
                            +','+str(c_i)+','+str(c_s)+','+str(c_d)+','
                            +str(lf)+','+str(col)+','+str(reh)+'\n')
                    del obj
