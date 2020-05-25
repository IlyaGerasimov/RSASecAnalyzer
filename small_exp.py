import math
from calc import pow


class CustomException(Exception):
    def __init__(self, message):
        self.message = message;


def reverse(a, b):
    #print("GCD: ", a, b, math.gcd(a, b))
    if math.gcd(a, b) != 1:
        raise CustomException(math.gcd(a, b))
    n = b
    res = 1
    prev = 0
    i = 0
    while a != 1:
        temp = res
        res = res * (b // a) + prev
        prev = temp
        a_1 = b%a
        b = a
        a = a_1
        i += 1
    return res if i % 2 == 0 else -res+n


def zero_poly(f):
    while f and f[-1] == 0:
        f.pop()
    if not f:
        return [0]
    return f


def poly_div(f, g, n):
    m = len(f) - 1
    h = len(g) - 1
    q = [0] * (m - h + 1)
    counter = 0
    #g = g + (m - h) * [0]
    for k in range(m - h, -1, -1):
        counter += 1
        #print(f[h + k], g[h])
        #print(f[h + k] % g[h])
        if math.gcd(g[h], n) == 1:
            #print(reverse(g[h], n))
            q[k] = (f[h + k] * reverse(g[h], n)) % n
            #print("coeff:", q[k])
            for j in range(h + k, k - 1, -1):
                f[j] = (f[j] - q[k] * g[j - k]) % n
        else:
            raise CustomException(math.gcd(g[h], n))
            #q[k] = f[h + k] // g[h]
            #for j in range(h + k - 1, k - 1, -1):
            #    f[j] = (f[j] - q[k] * g[j - k]) % n
            #break
    return zero_poly(q), zero_poly(f)


def poly_mul(f, g, n):
    m = len(f) - 1
    h = len(g) - 1
    q = [0] * (m + h + 1)
    for i in range(h + 1):
        for j in range(m + 1):
            q[i + j] = (q[i + j] + g[i] * f[j]) % n
    return q

def poly_sum(f, g, n):
    m = len(f) - 1
    h = len(g) - 1
    q = [0] * (max(m, h) + 1)
    for i in range(min(m, h) + 1):
        q[i] = (f[i] + g[i]) % n
    for i in range(min(m, h) + 1, max(m, h) + 1):
        q[i] = f[i]
    return zero_poly(q)


def poly_euclid(f, g, n):
    #f_prev = f
    #g_prev = g
    while g != [0]:
        #print("QWF")
        #print("in:", f, g)
        q, r = poly_div(f, g, n)
        #print("out:", q, r)
        f = g
        g = r
    return f


def poly_step(f, e, n):
    if e == 0:
        return [1]
    if e == 1:
        return f
    s = [1]
    while e > 1:
        if e % 2 == 1:
            s = poly_mul(s, f, n)
        f = poly_mul(f, f, n)
        e = e // 2
    return poly_mul(f, s, n)


def calc_poly(f, x, n):
    res = 0
    for i in range(len(f)):
        res = (res + f[i] * (x ** i)) % n
    return res


def small_exp(c_1, c_2, l, e, n):
    f = poly_sum(poly_step([0, 1], e, n), [(-c_1) % n], n)
    g = poly_sum(poly_step(l, e, n), [(-c_2) % n], n)
    #print("poly f", f)
    #print("poly g:", g)
    #print(g)
    d = poly_euclid(g, f, n)
    #print("done")
    #print(d)
    rev = reverse(d[1], n)
    for i in range(len(d)):
        d[i] = d[i] * rev
    if len(d) == 2:
        return (-d[0]) % n, (calc_poly(l, (-d[0]) % n, n))
    else:
        if math.gcd(len(d) - 1, n) == 1:
            k = reverse(len(d) - 1, n)
            return (n - k * d[len(d) - 2]) % n, calc_poly(l, (n - k * d[len(d) - 2]) % n, n)
    return 0


#print(poly_div([0, 1, 2, 3, 4, 5, 6], [0, 7, 8, 9, 10, 11, 12]))
#print(poly_mul([1, 2,3,4,5], [6,7,8,9,10,11]))
#print(poly_euclid([0, 0, 2], [0, 1]))
#print(poly_div([-632,8,24,32,16],[-86, 0,0,0,1],))
#print(poly_div([-86,0,0,0,1],[744, 8]))
