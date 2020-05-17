import math
import random

# Решето Эратосфена
def calculate_b_primes(b):
    prime_set = [True] * (b // 2)
    for i in range(3, int(b ** 0.5) + 1, 2):
        if prime_set[i // 2]:
            prime_set[i // 2 + i::i] = [False] * len(prime_set[i // 2 + i::i])
    return [2] + [2 * i + 1 for i in range(1, b // 2) if prime_set[i]]


def calculate_m(prime_set, b):
    m = 1
    for prime in prime_set:
        m = m * prime
    return m


def calculate_a(a, m, n):
    return math.gcd(pow(a, m, n) - 1, n)


def pollard_p_1(n, ps=[]):
    b = int(math.log2(n))
    #print(b)
    is_given_ps = True if ps else False
    if not is_given_ps:
        ps = calculate_b_primes(b)
    #print("ok")
    a_base = 2
    a = a_base
    for p in ps:
        step = int(math.log(n, p))
        for i in range(step):
            a = pow(a, p, n)
    gcd = math.gcd(a - 1, n)
    #print("ok3")
    #print("gcd:", gcd)
    while gcd == 1 or gcd == n:
        if gcd == n:
            a_base += 1
            a = a_base
            for p in ps:
                a = pow(a, p, n)
            gcd = math.gcd(a - 1, n)
        else:
            a_base = 2
            b = b * 2
            #print("b:", b)
            ps = calculate_b_primes(b)
            a = a_base
            for p in ps:
                a = pow(a, p, n)
            gcd = math.gcd(a - 1, n)
        #print("gcd:", gcd)
    return gcd, n // gcd


#pr = calculate_b_primes(2**15)

#n = 566118277*765162023
#print(n)
#print(pollard_p_1(1329827))
