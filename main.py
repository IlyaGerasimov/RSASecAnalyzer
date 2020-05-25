# -*- coding: utf-8 -*-
from step import step
from po_pollard import po_pollard_brent
from pollard_p_1 import pollard_p_1
from small_exp import small_exp, reverse, CustomException
from wiener import wiener
from prime import is_prime, get_prime
import threading
import argparse
import math
import random
from calc import pow


def parse_init():
    parser = argparse.ArgumentParser(description='El-Gamal.')
    parser.add_argument(
        '-e',
        type=int,
        nargs='?',
        default=None,
        help='Public key.'
    )
    parser.add_argument(
        '-n',
        type=int,
        nargs='?',
        default=None,
        help='Module.'
    )
    parser.add_argument(
        '-l',
        type=int,
        nargs='?',
        default=None,
        help='Task difficulty. If specified, then it executes second mode.'
    )
    parser.add_argument(
        '-a', '--attacks',
        nargs='*',
        default=None,
        help='Attacks set.'
    )
    args = parser.parse_args()
    if args.l and args.attacks is not None:
        print("Second mode activated.")
        return args, True
    elif args.e is None or args.n is None:
        exit("Error: a tuple (e, N) is required.")
    return args, False


def execute(e, n, method, f):
    if method == '(p-1)-метод':
        p, q = pollard_p_1(n)
        f.write("The result of the algorithm is: {}*{}".format(p, q))
    elif method == 'ро-Поллард':
        p, q = po_pollard_brent(n)
        f.write("The result of the algorithm is: {}*{}".format(p, q))
    elif method == 'малый-модуль-шифрования':
        m_1 = random.randint(2, n - 2)
        a = random.randint(2, n - 2)
        b = random.randint(2, n - 2)
        m_2 = (a * m_1 + b) % n
        c_1 = pow(m_1, e, n)
        c_2 = pow(m_2, e, n)
        l = [b, a]
        f.write("Selected parameters:\n")
        f.write("First cipher-text: {}\n".format(c_1))
        f.write("Second cipher-text: {}\n".format(c_2))
        f.write("message relations: m_1 = {} * m_2 + {} mod {}\n".format(a, b, n))
        try:
            m_1, m_2 = small_exp(c_1, c_2, l, e, n)
        except CustomException as e:
            f.write("Found factor during the algorithm performance: {}*{}".format(e.message, n // e.message))
        else:
            f.write("The result of the algorithm is: {} and {}".format(m_1, m_2))
    elif method == 'атака-Винера':
        p, q = wiener(e, n)
        if p:
            f.write("The result of the algorithm is: {}*{}".format(p, q))
        else:
            f.write("Unable to achieve the result among the successive convergents.")
    elif method == 'итерация':
        m = random.randint(2, n - 2)
        c = pow(m, e, n)
        p, q = step(c, e, n)
        f.write("Used the cipher-text: {}\n".format(c))
        if q:
            f.write("The result of the algorithm is: {}*{}".format(p, q))
        else:
            f.write("The result is {}".format(p))
    else:
        exit("Unknown method")
    return 0


def weak_low_p_1(l):
    small_p = [[3], [5, 7], [11, 13], [17, 19, 23, 29, 31], [37, 41, 43, 47, 53, 59, 61], [67, 71, 73, 79, 83, 89, 97, 101]]
    p = 2
    size = [2, 3, 4, 5, 6, 7]
    cur_size = 2
    while True:
        if l - cur_size < 7:
            size = [elem for elem in size if elem <= l - cur_size]
        if len(size) == 0:
            p = 2
            cur_size = 2
            size = [2, 3, 4, 5, 6, 7]
            continue
        if len(size) == 1:
            next_size = 0
        else:
            next_size = random.randint(0, len(size) - 1)
        p = p * random.choice(small_p[next_size])
        cur_size = int(math.log2(p + 1) + 1)
        if int(math.log2(p + 1) + 1) == l:
            if is_prime(p + 1, l):
                return p
            p = 2
            cur_size = 2
            size = [2, 3, 4, 5, 6, 7]


def weak_forge(l, attacks):
    if '(p-1)-метод' or 'итерация' in attacks:
        p = weak_low_p_1(l)
        q = weak_low_p_1(l)
        n = p * q
    else:
        p = get_prime(l)
        q = get_prime(l)
        n = p * q
    if 'атака-Винера' in attacks:
        if 'малый-модуль-шифрования' in attacks:
            e = 2
            while True:
                if math.gcd(e, (p-1)*(q-1)) != 1:
                    e += 1
                    continue
                d = reverse(e, (p-1)*(q-1))
                if d < (1/3 * (n ** 0.25)):
                    print("Weak parameters: ({}, {})".format(e, n))
                    return 0
                e += 1
        else:
            d = 2
            while True:
                if math.gcd(d, (p-1)*(q-1)) != 1:
                    d += 1
                    continue
                e = reverse(d, (p-1)*(q-1))
                print("Weak parameters: ({}, {})".format(e, n))
                return 0
    elif 'малый-модуль-шифрования' in attacks:
        e = 3
        while math.gcd(e, (p-1)*(q-1)) != 1:
            e += 1
        print("Weak parameters: ({}, {})".format(e, n))
        return 0


if __name__ == '__main__':
    args, mode = parse_init()
    if mode:
        print(args.attacks)
        weak_forge(args.l, args.attacks)
    else:
        for method in ['(p-1)-метод', 'ро-Поллард', 'малый-модуль-шифрования', 'атака-Винера', 'итерация']:
            time = None
            print("Do you want to specify time limit for attack {}?".format(method))
            is_yes = False
            while True:
                answer = input().lower()
                if answer in ['n', 'no', 'нет', 'н']:
                    break
                elif answer in ['y', 'yes', 'да', 'д']:
                    is_yes = True
                    break
                else:
                    print("Please type [yes/no]")
            if is_yes:
                print("Please write time in seconds:")
                while True:
                    time = input()
                    try:
                        time = int(time)
                    except Exception:
                        print("Use integer for time in seconds.")
                    else:
                        break
            with open("./results/" + method + '.txt', 'w') as f:
                thread = threading.Thread(target=execute, args=(args.e, args.n, method, f))
                thread.daemon = True
                thread.start()
                thread.join(time if time else int(math.log2(args.n) * 60 * 60 / 32) + 5 * 60)
