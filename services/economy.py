import json, os

DB = "db/users.json"

def load():
    if not os.path.exists(DB):
        return {}
    return json.load(open(DB))

def save(d):
    json.dump(d, open(DB, "w"), indent=2)

def collect_tax(uid):
    data = load()
    u = data.setdefault(str(uid), {"coins": 0})
    tax = 20
    u["coins"] += tax
    save(data)
    return tax