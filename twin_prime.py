""" Twin prime generator implemented with the miller rabin algorithm.
 A twin prime is a prime number that is either 2 less or 2 more than another prime number.
"""

from random import randrange
import math
import sys


def modulo_exponentiation(base, exponent, mod):
    """ Performs modulo exponentiation via repeated squaring
    and returns the value of (base ** exponent) % mod """
    result = 1
    term = base % mod
    while exponent > 0:
        if exponent & 1 == 1:
            result = (result * term) % mod
        term = (term * term) % mod
        exponent >>= 1
    return result


def miller_rabin(n, num_witness):
    """ Given n, the number to be tested and num_witness, the number of witnesses
    needed, returns True if n is probably a prime, False if n is definitely not a prime.
    """
    if n == 2 or n == 3:
        return True
    elif n & 1 == 0:
        return False

    s = 0
    t = n - 1
    while t & 1 == 0:
        s += 1
        t //= 2

    for i in range(num_witness):
        a = randrange(2, n - 1)
        final_term = modulo_exponentiation(a, n - 1, n)
        if final_term == 1:
            first_term = modulo_exponentiation(a, t, n)
            for j in range(s):
                next_term = (first_term * first_term) % n
                if first_term != 1 and first_term != n - 1 and next_term == 1:
                    return False
                first_term = next_term
        else:
            return False

    return True


def determine_num_witness(n):
    """ Returns the number of witnesses needed based on n,
    the value to be tested for its primality """
    return max(int(math.log(n)), 1)


def twin_prime(m):
    """ Given an integer m, returns a twin prime pair where at least
    one of the prime numbers are in the range [2^{m -1} ,(2^m) -1].
    """
    min_bound = 1 << (m - 1)
    max_bound = (1 << m) - 1

    if min_bound % 6 != 0:
        min_bound += 6 - min_bound % 6

    while True:
        n = randrange(min_bound, max_bound + 1, 6)
        if miller_rabin(n - 1, determine_k(n - 1)) \
                and miller_rabin(n + 1, determine_k(n + 1)):
            return n - 1, n + 1


def twin_prime_driver(m):
    """ Given an integer m, generates a twin prime pair where at least
    one of the prime numbers are in the range [2^{m -1} ,(2^m) -1],
    and writes them into a text file. """
    output = twin_prime(m)

    with open("output_twin_prime.txt", "w") as f:
        f.write(str(output[0]) + "\n")
        f.write(str(output[1]))


if __name__ == "__main__":
    argv_m = sys.argv[1]
    twin_prime_driver(int(argv_m))



