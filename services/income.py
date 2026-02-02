import time

def calculate_hours_passed(last_collect: int) -> int:
    """
    Returns full hours passed since last collection
    """
    now = int(time.time())
    seconds_passed = now - last_collect

    if seconds_passed < 3600:
        return 0

    return seconds_passed // 3600
