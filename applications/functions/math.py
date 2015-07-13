from os import urandom

def get_random_64bit():
    return 9223372036854775807 - int(''.join(['%02x' % h for h in urandom(8)]), 16)
