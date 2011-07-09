'''Data transformation functions.

From bytes to a number, number to bytes, base64-like-encoding, etc.
'''

import math
import types

def bit_size(number):
    """Returns the number of bits required to hold a specific long number"""

    if number < 0:
        raise ValueError('Only nonnegative numbers possible: %s' % number)

    if number == 0:
        return 1
    
    return int(math.ceil(math.log(number, 2)))

def byte_size(number):
    """Returns the number of bytes required to hold a specific long number.
    
    The number of bytes is rounded up.
    """

    return int(math.ceil(bit_size(number) / 8.0))

def bytes2int(bytes):
    """Converts a list of bytes or an 8-bit string to an integer.

    When using unicode strings, encode it to some encoding like UTF8 first.

    >>> (((128 * 256) + 64) * 256) + 15
    8405007
    >>> l = [128, 64, 15]
    >>> bytes2int(l)              #same as bytes2int('\x80@\x0f')
    8405007

    """

    if not (type(bytes) is types.ListType or type(bytes) is types.StringType):
        raise TypeError("You must pass a string or a list")

    
    # Convert byte stream to integer
    integer = 0
    for byte in bytes:
        integer *= 256
        if type(byte) is types.StringType: byte = ord(byte)
        integer += byte

    return integer

def int2bytes(number, block_size=None):
    r'''Converts a number to a string of bytes.

    @param number: the number to convert
    @param block_size: the number of bytes to output. If the number encoded to
        bytes is less than this, the block will be zero-padded. When not given,
        the returned block is not padded.

    @throws OverflowError when block_size is given and the number takes up more
        bytes than fit into the block.


    >>> int2bytes(123456789)
    '\x07[\xcd\x15'
    >>> bytes2int(int2bytes(123456789))
    123456789

    >>> int2bytes(123456789, 6)
    '\x00\x00\x07[\xcd\x15'
    >>> bytes2int(int2bytes(123456789, 128))
    123456789

    >>> int2bytes(123456789, 3)
    Traceback (most recent call last):
    ...
    OverflowError: Needed 4 bytes for number, but block size is 3

    '''

    # Type checking
    if type(number) not in (types.LongType, types.IntType):
        raise TypeError("You must pass an integer for 'number', not %s" %
            number.__class__)

    # Do some bounds checking
    if block_size is not None:
        needed_bytes = byte_size(number)
        if needed_bytes > block_size:
            raise OverflowError('Needed %i bytes for number, but block size '
                'is %i' % (needed_bytes, block_size))
    
    # Convert the number to bytes.
    bytes = []
    while number > 0:
        bytes.insert(0, chr(number & 0xFF))
        number >>= 8

    # Pad with zeroes to fill the block
    if block_size is not None:
        padding = (block_size - needed_bytes) * '\x00'
    else:
        padding = ''

    return padding + ''.join(bytes)

def block_op(block_provider, block_size, operation):
    r'''Generator, applies the operation on each block and yields the result
    
    Each block is converted to a number, the given operation is applied and then
    the resulting number is converted back to a block of data. The resulting
    block is yielded.
    
    @param block_provider: an iterable that iterates over the data blocks.
    @param block_size: the used block size
    @param operation: a function that accepts an integer and returns an integer 
    
    >>> blocks = ['\x00\x01\x02', '\x03\x04\x05']
    >>> list(block_op(blocks, 3, lambda x: (x + 6)))
    ['\x00\x01\x08', '\x03\x04\x0b']
    
    '''

    for block in block_provider:
        number = bytes2int(block)
        print 'In : %i (%i bytes)' % (number, byte_size(number))
        after_op = operation(number)
        print 'Out: %i (%i bytes)' % (after_op, byte_size(after_op))
        yield int2bytes(after_op, block_size)

if __name__ == '__main__':
    import doctest
    doctest.testmod()

