from prime import is_prime
import math
import random

def step(c, e, n):
    c_init = c
    c_prev = c
    c = pow(c, e, n)
    #print(c, c_init, c_prev)
    i = 1
    while c != c_init and (math.gcd((c - c_init) % n, n) != 1 or math.gcd((c - c_init) % n, n) != n):
        c_prev = c
        #print(math.gcd((c - c_init) % n, n))
        c = pow(c, e, n)
        #print(c, c_init, c_prev)
        i += 1
        #print(i)
    if c == c_init:
        return c_prev, None
    if math.gcd((c - c_init) % n, n) > 1 and math.gcd((c - c_init) % n, n) < n:
        d = math.gcd((c - c_init) % n, n)
        return d, n // d
    return None, None


def weak_step(l):
    small_p = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101]
    p = 2
    while True:
        p = p * random.choice(small_p)
        if int(math.log2(p + 1)) >= l:
            if is_prime(p + 1, l):
                return p
            p = 2


#print(step(2, 1061933, 1329827))