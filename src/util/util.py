import random
import csv

def isPrime(num):
    if num == 2:
        return True
    elif num > 2:
        if num % 2 == 0:
            return False
        for i in range(3, int(num**(0.5))+2, 2):
            if num % i == 0:
                return False
        return True
    else:
        return False

def generateInputs(x, s):
    random.seed(s)
    filename = "./inputs/"+str(x)+".txt"
    with open(filename, 'w') as fo:                                              
        w = csv.writer(fo)                                                       
        k = 1
        for i in range(x): 
            k += random.randint(1, 20)
            w.writerow([k, i])                                             
    fo.close()

def readInputs(x, shuffle, s):
    random.seed(s)
    input_list = []
    filename = "./inputs/"+str(x)+".txt"
    generateInputs(x, s)
    with open(filename, 'r') as fi:
        r = csv.reader(fi)
        for row in r:
            if len(row) == 2:
                input_list.append([int(row[0]), int(row[1])])
    fi.close()

    if (shuffle):
        random.shuffle(input_list)
        return input_list
    else:
        return input_list


