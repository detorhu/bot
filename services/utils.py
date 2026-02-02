def clamp(value: int, min_value: int, max_value: int) -> int:
    """
    Keep value between min and max
    """
    return max(min_value, min(value, max_value))


def format_cash(amount: int) -> str:
    """
    Format cash nicely
    """
    return f"${amount:,}"
