import time

user_memory = {}
last_used = {}

COOLDOWN = 60  # segundos

def remember(user, msg):
    words = msg.split()
    if words:
        user_memory[user] = words[-1]

def can_recall(user):
    now = time.time()
    last = last_used.get(user, 0)
    if now - last > COOLDOWN:
        last_used[user] = now
        return True
    return False

def recall_user(user):
    return user_memory.get(user)
