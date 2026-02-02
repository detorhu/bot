import json, os, random

DB = "db/wars.json"

def start_war(uid):
    win = random.choice([True, False])
    if win:
        return "⚔️ WAR WON! +50 coins"
    return "💀 WAR LOST! Base damaged"