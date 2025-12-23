import time

_offended_until = 0

def offend(seconds=30):
    global _offended_until
    _offended_until = time.time() + seconds

def is_offended():
    return time.time() < _offended_until
