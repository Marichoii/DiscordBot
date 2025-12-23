FEARS = ["aspirador", "fogos", "banho", "veterinário"]

def scared_by(msg):
    return any(fear in msg for fear in FEARS)
