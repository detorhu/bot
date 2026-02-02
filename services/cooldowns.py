import time
COOLDOWNS = {}

def check(uid, key, sec):
    now = time.time()
    last = COOLDOWNS.get((uid, key), 0)
    if now - last < sec:
        return False
    COOLDOWNS[(uid, key)] = now
    return True