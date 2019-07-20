""" ===========================================================================
CompSci 261P Data Structures Project 1

Tests for hash methods (linear, chained, cuckoo, chained with tabulation)

Author: Qixiang Zhang (David)
Student ID: 70644128
Email: qixianz@uci.edu
=========================================================================== """

from test_script import tests

"""----------------------------------------------------------------------------
                            Factor 1 - Load Factor:
-------------------------------------------------------------------------------
T1. How does the preset load factor affect the time complexity for batch 
    operations?
"""
tests.t1("Linear", "Test 1", "lp")
tests.t1("Chained", "Test 1", "cn")
tests.t1("Cuckoo", "Test 1", "cc")
tests.t1("Tabulation", "Test 1", "tb")

"""
T2. How does the load factor affect the number of collisions?
T3. How does the load factor affect the number of re-hash?
T4. How does the load factor affect the time complexity for single operations?
"""
tests.t2t3t4("Linear", "Test 2-3-4", "lp")
tests.t2t3t4("Chained", "Test 2-3-4", "cn")
tests.t2t3t4("Cuckoo", "Test 2-3-4", "cc")
tests.t2t3t4("Tabulation", "Test 2-3-4", "tb")




"""----------------------------------------------------------------------------
                    Factor 2 - Population (number of elements):
-------------------------------------------------------------------------------
T5.  How does the population affect batch operations time complexity?
T6.  How does the population affect the number of collisions?
T7.  How does the population affect the number of re-hash?
"""
tests.t5t6t7("Linear", "Test 5-6-7", "lp")
tests.t5t6t7("Chained", "Test 5-6-7", "cn")
tests.t5t6t7("Cuckoo", "Test 5-6-7", "cc")
tests.t5t6t7("Tabulation", "Test 5-6-7", "tb")




"""----------------------------------------------------------------------------
                        Factor 3 - Pre-sorted keys:
-------------------------------------------------------------------------------
T8.  How does pre-sorting the keys affect batch operations time complexity?
"""
tests.t8t9t10("Linear", "Test 8-9-10", "lp")
tests.t8t9t10("Chained", "Test 8-9-10", "cn")
tests.t8t9t10("Cuckoo", "Test 8-9-10", "cc")
tests.t8t9t10("Tabulation", "Test 8-9-10", "tb")
