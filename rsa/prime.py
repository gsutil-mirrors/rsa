'''Numerical functions related to primes.'''

__all__ = [ 'getprime', 'are_relatively_prime']

import rsa.randnum

def gcd(p, q):
    """Returns the greatest common divisor of p and q

    >>> gcd(48, 180)
    12
    """

    while q != 0:
        if p < q: (p,q) = (q,p)
        (p,q) = (q, p % q)
    return p
    

def jacobi(a, b):
    """Calculates the value of the Jacobi symbol (a/b) where both a and b are
    positive integers, and b is odd
    """

    if a == 0: return 0
    result = 1
    while a > 1:
        if a & 1:
            if ((a-1)*(b-1) >> 2) & 1:
                result = -result
            a, b = b % a, a
        else:
            if (((b * b) - 1) >> 3) & 1:
                result = -result
            a >>= 1
    if a == 0: return 0
    return result

def jacobi_witness(x, n):
    """Returns False if n is an Euler pseudo-prime with base x, and
    True otherwise.
    """

    j = jacobi(x, n) % n
    f = pow(x, (n - 1) // 2, n)

    if j == f: return False
    return True

def randomized_primality_testing(n, k):
    """Calculates whether n is composite (which is always correct) or
    prime (which is incorrect with error probability 2**-k)

    Returns False if the number is composite, and True if it's
    probably prime.
    """

    # 50% of Jacobi-witnesses can report compositness of non-prime numbers

    for _ in range(k):
        x = rsa.randnum.randint(n-1)
        if jacobi_witness(x, n): return False
    
    return True

def is_prime(number):
    """Returns True if the number is prime, and False otherwise.

    >>> is_prime(42)
    0
    >>> is_prime(41)
    1
    """

    if randomized_primality_testing(number, 6):
        # Prime, according to Jacobi
        return True
    
    # Not prime
    return False

    
def getprime(nbits):
    """Returns a prime number that can be stored in 'nbits' bits.

    >>> p = getprime(128)
    >>> is_prime(p-1)
    0
    >>> is_prime(p)
    1
    >>> is_prime(p+1)
    0
    
    >>> from rsa import common
    >>> common.bit_size(p) <= 128
    True
    
    """

    while True:
        integer = rsa.randnum.read_random_int(nbits)

        # Make sure it's odd
        integer |= 1

        # Test for primeness
        if is_prime(integer):
            return integer

        # Retry if not prime


def are_relatively_prime(a, b):
    """Returns True if a and b are relatively prime, and False if they
    are not.

    >>> are_relatively_prime(2, 3)
    1
    >>> are_relatively_prime(2, 4)
    0
    """

    d = gcd(a, b)
    return (d == 1)
    
if __name__ == '__main__':
    print 'Running doctests 1000x or until failure'
    import doctest
    
    for count in range(1000):
        (failures, tests) = doctest.testmod()
        if failures:
            break
        
        if count and count % 100 == 0:
            print '%i times' % count
    
    print 'Doctests done'
