from random import randint
import roomslib
import monsterlib
import locatorlib
import healthandinv

viewing_inventory = False


def change_viewing_inventory_true():
    global viewing_inventory
    viewing_inventory = True


def inventory_variable_reset():

    global viewing_inventory
    global verb
    global desired_item
    global affected_object

    viewing_inventory = False
    verb = ""
    desired_item = ""
    affected_object = ""


verb = ""
desired_item = ""
# IF USER TYPES A VALID OBJECT, OBLIVIOUS TO HOW THEY CAN INTERACT WITH IT, AN INVENTORY PROMPT SHOULD SHOW
affected_object = ""


def desired_item_check(user_input):

    global desired_item

    inventory = healthandinv.inventory_list

    input_to_list = user_input.split()

    # SEARCHING input_to_list INDICES FOR desired_item
    if len(input_to_list) < 1:
        pass
    elif len(input_to_list) == 1:
        if input_to_list[0] in inventory[0] or input_to_list[0] in inventory[1]:
            desired_item = input_to_list[0]
    else:
        if input_to_list[0] in inventory[0] or input_to_list[0] in inventory[1]:
            desired_item = input_to_list[0]
        elif input_to_list[1] in inventory[0] or input_to_list[1] in inventory[1]:
            desired_item = input_to_list[1]
        elif input_to_list[-1] in inventory[0] or input_to_list[-1] in inventory[1]:
            desired_item = input_to_list[-1]

    return desired_item


def affected_object_check(inventory_input):

    global affected_object

    flattened_list = []

    # CHECKING THAT affected_object EXISTS IN THE GAME
    for indented_list in roomslib.interactive_objects_list:
        for interactive_object in indented_list:
            flattened_list.append(interactive_object)

    input_to_list = inventory_input.split()

    # SEARCHING INDICES: 0 AND -1 IN input_to_list FOR affected_object
    if len(input_to_list) < 1:
        pass
    elif len(input_to_list) == 1:
        if input_to_list[0] in monsterlib.beasties_list[0]:
            affected_object = input_to_list[0]
        elif input_to_list[0] in flattened_list:
            affected_object = input_to_list[0]
    else:
        if input_to_list[-1] in monsterlib.beasties_list[0]:
            affected_object = input_to_list[-1]
        elif input_to_list[-1] in flattened_list:
            affected_object = input_to_list[-1]

    if desired_item == affected_object:  # AM I SURE ABOUT THIS??????????????????????????????????????????????????????????
        affected_object = ""

    return affected_object


def print_item_desc(item_name):
    obtainable_items_descriptions = {
        "berry": "It's an unearthly, pink fruit. Something has obviously been nibbling it.",
        "bird": "It's the still, broken body of a black and white magpie.",
        "broom": "It's tired and worn. Most of its bristles are gone.",
        "bucket": "It's an empty, decrepit tub, made useless because of the large hole you put in it. USE it to equip.",
        "helmet": "An improvised bucket helmet. You're just able to peep out of the hole in the side. Reduces damage.",
        "charm": "It's a necklace with a carved, bone sculpture. Touching it chills your fingers. USE it to equip.",
        "circle": "It's an eyeball-sized, circular piece of glass with a metal rim. USE it to equip.",
        "coin": "It's a heavy, blank, circular piece of metal. You get the mad impression it wants to escape...",
        "crustacean": "A tiny arthropod. It's hooked legs and sharp mouth parts flail desperately. USE it to equip.",
        "fish": "It's a slimy, rotten carcass of a carp. It is still flopping about. "
                "There is something down its throat.",
        "flute": "A primitive wind instrument made from bone. It does not seem to produce any remotely musical noise.",
        "hands": "They're versatile, little appendages. Use them to grab and inspect.",
        "herb": "It's a misshapen and rather sun-starved plant. Nutritious.",
        "iou": "A crumpled piece of paper with the acronym: 'I.O.U' scrawled on it.",
        "kindling": "It's a modest pile of dried wood. Ideal for burning.",
        "key": "It's heavy and metal. What could it be for?",
        "larva": "It's a fat, squirming, biting grub. Why would you pick this up?",
        "lute": "An egg-shaped, stringed instrument. It is not intact and horribly out of tune.",
        "map": "A tattered and torn piece of paper. There is a rough drawing of a series of chambers on there.",
        "matchbox": "It's a dusty, old box of matches. There are still a couple left.",
        "monocle": "It is a tiny window into a new realm of astonishing clarity. "
                   "Increases accuracy and critical hit rate.",
        "mushroom": "It has a thick stalk with a squishy, bulbous cap. How might this taste?",
        "necklace": "It's an ice-cold charm on a string. You feel like you could withstand the fires of hell. "
                    "Suppresses fire.",
        "parasite": "It's a tiny arthropod. The finger it's attached to blackens with decay. "
                    "Significantly increases damage threshold.",
        "pitchfork": "It's a little rod with two menacingly sharp ends. It looks very dangerous.",
        "pot": "It's a stout, ceramic pot with a lip and a dainty handle. You do not enjoy its smell.",
        "potion": "It's a glittering flask of fluid in perpetual motion. Do you dare drink this?",
        "rung": "It's a warped, wooden cylinder from a LADDER. It's quite damp.",
        "slingshot": "It's a wooden, Y-shaped weapon. Hornet wax is still attached to it. "
                     "Effective against winged foes.",
        "snack": "It might have expired... Use it to restore a small amount of health.",
        "spade": "It's a digging tool. Its rusted, metal edge looks quite formidable."
    }

    return obtainable_items_descriptions[item_name]


def use_consumable(item_name):

    consumable_values = {
        "berry": 2,
        "bird": 2,
        "fish": -1,
        "herb": 5,
        "mushroom": 3,
        "potion": 7,
        "snack": 2
    }

    if item_name in consumable_values:
        if "parasite" not in healthandinv.inventory_list[0]:
            healthandinv.plus_health(consumable_values[item_name])
            output = f"You consume your {item_name.upper()} and gain ({consumable_values[item_name]}) health."
        else:
            healthandinv.plus_health(consumable_values[item_name] - 1)
            output = f"The PARASITE nibbles at your {item_name.upper()} first and diminishes it by (1). You consume " \
                     f"your {item_name.upper()} and gain ({consumable_values[item_name] - 1}) health."

    if item_name == "herb":
        if "enfeeblement" in healthandinv.contracted_diseases:
            output = output + "\nCURED: ENFEEBLEMENT"
            healthandinv.contracted_diseases.remove("enfeeblement")

    elif item_name == "bucket":
        output = "You put the bucket over your head, wearing it like a HELMET."
        healthandinv.add_to_inventory("helmet", 0)

    elif item_name == "circle":
        output = "You put the tiny, circular window over your eye. The world viewed by your right eye instantly " \
                 "adopts finer, sharper characteristics and you finally understand what it means to see without " \
                 "impairment."
        healthandinv.add_to_inventory("monocle", 0)

    elif item_name == "crustacean":
        output = "The take the crustacean out of your pocket and it immediately latches, painfully, onto your finger." \
                 " Your blood chills in your veins. Your heart freezes. Your breathing stops. Your very spirit " \
                 "escapes out of you like a calm cloud of fog."
        healthandinv.add_to_inventory("parasite", 0)

    elif item_name == "charm":
        output = "You put the charm around your head and wear it like a NECKLACE. The air around you feels frosty and" \
                 " your skin begins to ice over."
        healthandinv.add_to_inventory("necklace", 0)

    elif item_name == "iou":
        output = "You consume your crumpled piece of paper and gain (0) health."
        healthandinv.player_health.append("iou")

    healthandinv.remove_from_inventory(item_name)
    return output


fish_yes_or_no = False


def interact_inventory(user_input):

    global verb
    global desired_item
    global affected_object
    global fish_yes_or_no

    if "use" in user_input:
        verb = "use"
    elif "desc" in user_input:
        verb = "describe"

    desired_item_check(user_input)
    affected_object_check(user_input)

    if affected_object and not desired_item and not verb:
        output = f"Use which item on {affected_object.upper()}?"
        verb = "use"
        return output
    elif affected_object and desired_item and not verb:
        verb = "use"

    if affected_object and not desired_item:
        output = f"USE which item on the {affected_object.upper()}?"
        return output

    if not desired_item:
        output = f"Which item would you like to {verb.upper()}?"
        return output

    if not verb:
        output = f"Do what with your {desired_item.upper()}?"
        return output

    if verb == "describe":
        random_descriptors = ["useful", "trusty", "reliable", "dependable", "practical", "nifty", "helpful"]
        output = f"You take your {random_descriptors[randint(0, 6)]} {desired_item.upper()} out of your pocket.\n" \
                 + print_item_desc(desired_item)
        if desired_item == "fish":
            output = output + " Inspect? yes/no"
            fish_yes_or_no = True
            inventory_variable_reset()
            return output

    elif verb == "use":

        if desired_item in healthandinv.inventory_list[1]:  # CHECKING IF CONSUMABLE FIRST
            output = use_consumable(desired_item)
        elif desired_item == "map":
            output = "display_map"

        elif affected_object_check(user_input):
            affected_object = affected_object_check(user_input)

            if affected_object in monsterlib.beasties_list[0]:  # USER IS TARGETING MONSTER
                output = player_attack(desired_item, affected_object)
            else:  # USER IS INTERACTING WITH AN OBJECT
                output = roomslib.room_contents_check(desired_item, affected_object)
        else:
            output = f"What would you like to USE your {desired_item.upper()} on?"
            return output

    inventory_variable_reset()
    if "yes/no" not in output:  # yes/no MUST COME AT END OF STRING SO IT CAN BE SPLICED OFF IN guidisplay
        monster_attack_text = monsterlib.monster_attack()
        if isinstance(output, list):  # ANTICIPATING CONCATINATION OF LIST WITH STRING
            if monster_attack_text:
                output.append(monster_attack_text)  # TEST THIS!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        else:
            output = output + monster_attack_text

    return output


def player_attack(desired_item_local, affected_object_local):

    attacking_items = [
        ["hands", "broom", "spade", "slingshot", "pitchfork"],  # REMOVE GUN AND ITS VARIOUS STATS
        [1, 2, 3, 2, 4],  # ASSOCIATED ATTACK VALUES
        ["clobber", "jab", "batter", "pelt", "stab"]  # ASSOCIATED VERB
    ]
    random_attacking_verbs = ["smash", "strike", "crack", "bludgeon", "thump", "smack", "assault", "pound", "pummel"]

    # DETERMINING DAMAGE
    try:
        second_index = attacking_items[0].index(desired_item_local)
        base_damage = attacking_items[1][second_index]
        associated_verb = attacking_items[2][second_index]
    except ValueError:
        base_damage = 1  # IF desired_item IS NOT IN attacking_items LIST

    random_number = randint(0, 8)
    if "monocle" in healthandinv.inventory_list[0]:
        random_number += 1

    # ESTABLISHING WHETHER THERE IS A MONSTER PRESENT AND WHETHER THEY'RE TARGETING THE CORRECT MONSTER
    monster = monsterlib.monster_specifier()
    if monster != affected_object_local:
        output = f"There is no {affected_object_local.upper()} present. You clumsily swat at thin air with" \
                 f" your {desired_item_local.upper()}."
        return output

    else:
        if desired_item_local not in attacking_items[0]:
            output = f"You {random_attacking_verbs[random_number]} the {affected_object_local.upper()} with your" \
                     f" {desired_item_local.upper()}."

        elif desired_item == "slingshot" and affected_object_local == "imp":
            base_damage = 3
            output = "You quickly fetch a stone from the floor and pinch it in your SLINGSHOT. You shoot a rock hard" \
                     " projectile at the IMP."

        elif random_number == 0:
            base_damage = 0
            if monster == "skeleton":
                output = f"Your {desired_item_local.upper()} makes contact, pulverising a petrified bone into dust." \
                         " The SKELETON appears unfazed. A different bone springs from the floor to instantly" \
                         " replace it."
            elif monster == "slime":
                output = "Your attack lacks absolute conviction and goes off-kilter. It slides right off the" \
                         " SLIME's smooth exterior."
            elif monster == "imp":
                output = "The IMP's movements are erratic and you find it difficult to land a hit against your" \
                         " little, aerial foe."
            elif monster == "dragon":
                output = "Your attack makes contact with a particularly tough bit of hide. The DRAGON barely flinches."

        elif random_number > 6:
            output = "CRITICAL HIT! DOUBLE DAMAGE. You summon every modicum of strength to deliver a terrifying" \
                     f" blow against the {affected_object_local.upper()} with your {desired_item_local.upper()}."
            base_damage *= 2

        else:
            output = f"You {associated_verb} the {affected_object_local.upper()} with" \
                     f" your {desired_item_local.upper()}."

    if "broken bone" in healthandinv.contracted_diseases:
        base_damage -= 1
        output = output + " Your BROKEN BONE diminishes your attack."

    if base_damage < 0:
        base_damage = 0

    output = output + f" You inflict ({base_damage}) damage."
    output = output + monsterlib.calculate_monster_health(base_damage)
    return output


def inspected_fish():
    global fish_yes_or_no
    fish_yes_or_no = False


