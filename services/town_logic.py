import json, os

DB = "db/towns.json"

def load():
    if not os.path.exists(DB):
        return {}
    return json.load(open(DB))

def save(d):
    json.dump(d, open(DB, "w"), indent=2)

def get_or_create_town(uid, name):
    data = load()
    uid = str(uid)

    if uid not in data:
        data[uid] = {
            "name": f"{name}'s Town",
            "level": 1,
            "citizens": 10,
            "coins": 100,
            "ships": 0,
            "cops": 5
        }
        save(data)

    return data[uid]

def add_ship(uid):
    data = load()
    town = data[str(uid)]
    town["ships"] += 1
    save(data)
    return town["ships"]

def patrol(uid):
    data = load()
    town = data[str(uid)]
    town["coins"] += 10
    save(data)
    return "👮 Police stopped criminals (+10 coins)"