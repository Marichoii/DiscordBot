import time

_mod_until = 0

def activate_mod(seconds=10):
    global _mod_until
    _mod_until = time.time() + seconds

def is_mod():
    return time.time() < _mod_until
