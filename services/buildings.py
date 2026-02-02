from database import get_buildings, get_city, update_city, update_buildings
from services.utils import clamp

MAX_LVL = 10

def upgrade_cost(level: int) -> int:
    return 500 * (level + 1)

def apply_upgrade(uid: int, building: str):
    h, s, ho, p = get_buildings(uid)
    levels = {"houses": h, "school": s, "hospital": ho, "police": p}
    lvl = levels[building]

    if lvl >= MAX_LVL:
        return False, "Max level reached"

    # Apply level up
    levels[building] += 1
    update_buildings(uid, **levels)

    # Effects
    cname, pop, happy = get_city(uid)
    if building == "houses":
        pop += 50
    if building in ("hospital", "police"):
        happy = clamp(happy + 3, 0, 100)

    update_city(uid, pop, happy)
    return True, levels[building]
