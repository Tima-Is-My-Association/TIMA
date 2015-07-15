from os import urandom

def s64():
    return abs(9223372036854775807 - int(''.join(['%02x' % h for h in urandom(8)]), 16))

def u32():
    return abs(2147483647 - int(''.join(['%02x' % h for h in urandom(4)]), 16))
