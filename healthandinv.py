
# CONTAINED IN LISTS SO THAT THEY CAN BE EASILY AFFECTED FROM WITHIN FUNCTIONS
player_health = [10]  # health points
contracted_diseases = []

inventory_list = [
    ["hands"],  # CONSTANTS
    ["snack"]]  # CONSUMABLES


def append_traded_item(item):
    consumables = [
        "berry", "bucket", "charm", "circle", "crustacean", "fish", "herb", "iou", "mushroom", "potion", "snack"
    ]

    if item in consumables:
        inventory_list[1].append(item)
    else:
        inventory_list[0].append(item)


def alive():
    alive_state = True

    if not undead():
        if player_health[0] < 1:
            alive_state = False

    else:
        if player_health[0] < -9:
            alive_state = False

    return alive_state


def undead():
    if "parasite" in inventory_list[0]:
        undead_state = True
        if "undead" not in contracted_diseases:
            contracted_diseases.append("undead")

    else:
        undead_state = False
        if "undead" in contracted_diseases:
            contracted_diseases.remove("undead")

    return undead_state


def plus_health(value):
    player_health[0] += value

    # PREVENTING HEALTH FROM EXCEEDING 15
    if player_health[0] > 15:
        player_health[0] = 15


def subtract_health(value):
    player_health[0] -= value


def remove_from_inventory(item_name):
    try:
        inventory_list[0].remove(item_name)
    except ValueError:
        inventory_list[1].remove(item_name)


def add_to_inventory(item_name: str, inventory_number: int):
    inventory_list[inventory_number].append(item_name)

