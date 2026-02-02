from config import BASE_INCOME_PER_POP

def calculate_income(population: int, school_level: int) -> int:
    """
    Calculate hourly income based on population and school bonus
    """
    if population <= 0:
        return 0

    # Base income
    income = population * BASE_INCOME_PER_POP

    # School bonus: +5% per level
    bonus_multiplier = 1 + (school_level * 0.05)

    final_income = int(income * bonus_multiplier)
    return final_income
