def solve(a, b, c):
    d = b ** 2 - 4 * a * c
    if d > 0:
        return [(- b + d ** 0.5) / (2 * a), (- b - d ** 0.5) / (2 * a)]
    elif d == 0:
        return [-b / (2 * a), -b / (2 * a)]
    return None


def check_frac(k, d, e, n):
    phi_n = (e * d - 1)/k
    solution = solve(1, - ((n - phi_n) + 1), n)
    if solution and n == solution[0] * solution[1]:
        return solution
    return None


def wiener(e, n):
    p = e
    q = n
    a, r = divmod(p, q)
    p = q
    num_prev = 1
    num = a
    div_prev = 0
    div = 1
    #print(num, div)
    while r > 0:
        temp_1 = r
        a, r = divmod(p, r)
        p = temp_1
        temp_1 = num
        temp_2 = div
        num = a * num + num_prev
        div = a * div + div_prev
        #print(num, div)
        num_prev = temp_1
        div_prev = temp_2
        d = check_frac(num, div, e, n)
        if d:
            return int(d[0]), int(d[1])
    return None, None

#print(wiener(1061933, 1329827))
