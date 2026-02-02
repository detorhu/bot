from database import (
    get_buildings,
    get_city,
    update_city,
    update_buildings
)

MAX_LEVEL = 10


def upgrade_cost(level: int) -> int:
    """
    Returns upgrade cost based on current level
    """
    return 500 * (level + 1)


def upgrade_building(uid: int, building: str):
    """
    Upgrades a building and applies city effects
    """
    houses, school, hospital, police = get_buildings(uid)

    levels = {
        "houses": houses,
        "school": school,
        "hospital": hospital,
        "police": police,
    }

    if building not in levels:
        return False, "Invalid building"

    current_level = levels[building]
    if current_level >= MAX_LEVEL:
        return False, "🏗 Max level reached"

    # ---- LEVEL UP ----
    levels[building] += 1
    update_buildings(
        uid,
        levels["houses"],
        levels["school"],
        levels["hospital"],
        levels["police"],
    )

    # ---- APPLY EFFECTS ----
    name, population, happiness = get_city(uid)

    if building == "houses":
        population += 50
    elif building in ("hospital", "police"):
        happiness = min(100, happiness + 5)

    update_city(uid, population, happiness)

    return True, "Upgraded"
