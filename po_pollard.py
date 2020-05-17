import math
import random
from prime import get_prime

def f(x, n):
    return (x ** 2 - 1) % n


def po_pollard_brent(n):
    x = random.randint(2, n - 2)
    x_next = f(x, n)
    d = math.gcd(n, (x_next - x) % n)
    if d > 1:
        return d, n // d
    k = 1
    x_compare = x_next
    i = 2
    while True:
        x = x_next
        x_next = f(x, n)
        if i < 2 ** (k+1):
            d = math.gcd(n, (x_compare - x_next) % n)
            if d > 1:
                return d, n // d
            i += 1
        else:
            x_compare = x_next
            i += 1
            k += 1


#res = po_pollard_brent(1329827)
#print(res)