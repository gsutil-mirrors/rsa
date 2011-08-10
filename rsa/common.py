# -*- coding: utf-8 -*-
#
#  Copyright 2011 Sybren A. Stüvel <sybren@stuvel.eu>
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

'''Common functionality shared by several modules.'''


import math

def bit_size(number):
    '''Returns the number of bits required to hold a specific long number.

    >>> bit_size(1023)
    10
    >>> bit_size(1024)
    11
    >>> bit_size(1025)
    11

    >>> bit_size(1 << 1024)
    1025
    >>> bit_size((1 << 1024) + 1)
    1025
    >>> bit_size((1 << 1024) - 1)
    1024

    '''

    if number < 0:
        raise ValueError('Only nonnegative numbers possible: %s' % number)

    if number == 0:
        return 1
    
    # This works, even with very large numbers. When using math.log(number, 2),
    # you'll get rounding errors and it'll fail.
    bits = 0
    while number:
        bits += 1
        number >>= 1

    return bits


def byte_size(number):
    """Returns the number of bytes required to hold a specific long number.
    
    The number of bytes is rounded up.

    >>> byte_size(1 << 1023)
    128
    >>> byte_size((1 << 1024) - 1)
    128
    >>> byte_size(1 << 1024)
    129
    """

    return int(math.ceil(bit_size(number) / 8.0))

def gcd(p, q):
    """Returns the greatest common divisor of p and q

    >>> gcd(48, 180)
    12
    """

    while q != 0:
        if p < q: (p,q) = (q,p)
        (p,q) = (q, p % q)
    return p
    

def extended_gcd(a, b):
    """Returns a tuple (r, i, j) such that r = gcd(a, b) = ia + jb
    """
    # r = gcd(a,b) i = multiplicitive inverse of a mod b
    #      or      j = multiplicitive inverse of b mod a
    # Neg return values for i or j are made positive mod b or a respectively
    # Iterateive Version is faster and uses much less stack space
    x = 0
    y = 1
    lx = 1
    ly = 0
    oa = a                             #Remember original a/b to remove 
    ob = b                             #negative values from return results
    while b != 0:
        q = a // b
        (a, b)  = (b, a % b)
        (x, lx) = ((lx - (q * x)),x)
        (y, ly) = ((ly - (q * y)),y)
    if (lx < 0): lx += ob              #If neg wrap modulo orignal b
    if (ly < 0): ly += oa              #If neg wrap modulo orignal a
    return (a, lx, ly)                 #Return only positive values

def inverse(x, n):
    '''Returns x^-1 (mod n)
    
    >>> inverse(7, 4)
    3
    >>> (inverse(143, 4) * 143) % 4
    1
    '''

    (divider, inv, _) = extended_gcd(x, n)

    if divider != 1:
        raise ValueError("x (%d) and n (%d) are not relatively prime" % (x, n))

    return inv


def crt(a_values, modulo_values):
    '''Chinese Remainder Theorem.

    Calculates x such that x = a[i] (mod m[i]) for each i.

    :param a_values: the a-values of the above equation
    :param modulo_values: the m-values of the above equation
    :returns: x such that x = a[i] (mod m[i]) for each i
    

    >>> crt([2, 3], [3, 5])
    8

    >>> crt([2, 3, 2], [3, 5, 7])
    23

    >>> crt([2, 3, 0], [7, 11, 15])
    135
    '''

    m = 1
    x = 0 

    for modulo in modulo_values:
        m *= modulo

    for (m_i, a_i) in zip(modulo_values, a_values):
        M_i = m // m_i
        inv = inverse(M_i, m_i)

        x += a_i * M_i * inv

    return x % m

if __name__ == '__main__':
    import doctest
    doctest.testmod()

