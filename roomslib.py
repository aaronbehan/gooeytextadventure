import locatorlib
import healthandinv
import monsterlib

interactive_objects_list = [
    ["bookcase", "desk", "nest", "nest (aggressive)", "book", "bucket", "slingshot", "larva"],  # LIBRARY [0]
    ["broom", "bell"],  # FORT ROOM [1]
    ["trapdoor", "trapdoor (locked)", "ladder", "ladder (broken)", "spade", "kindling", "lock"],  # TRAPDOOR ROOM [2]
    ["herb", "soil", "soil (undisturbed)", "well", "well (unfilled)", "water", "rung", "bird", "fish"],  # GARDEN [3]
    ["burner", "spider", "item", "matchbox"],  # POTION ROOM [4]
    ["mushroom"],  # LOWER HALLWAY [5]
    ["shackles"]  # DRAGON ROOM [6]
]


def room_contents_check(desired_item, affected_object):

    locator = locatorlib.locator

    # CHECKING THAT THE affected_object IS PRESENT IN THE ROOM THE USER IS IN.
    output = f'You attempted to use your {desired_item.upper()} on a {affected_object.upper()} but there is no' \
             f' accessible {affected_object.upper()} in this room.'

    if locator[1][3] >= 7:  # LIBRARY
        if affected_object in interactive_objects_list[0]:
            output = affect_object_library(desired_item, affected_object)
    elif locator[3][1] >= 7:  # FORT ROOM
        if affected_object in interactive_objects_list[1]:
            output = affect_object_fort_room(desired_item, affected_object)
    elif locator[3][3] >= 7:  # TRAPDOOR ROOM
        if affected_object in interactive_objects_list[2]:
            output = affect_object_trapdoor_room(desired_item, affected_object)
    elif locator[4][3] >= 7:  # GARDEN
        if affected_object in interactive_objects_list[3]:
            output = affect_object_garden(desired_item, affected_object)
    elif locator[5][2] >= 7:  # POTION ROOM
        if affected_object in interactive_objects_list[4]:
            output = affect_object_potion_room(desired_item, affected_object)
    elif locator[4][2] >= 7:  # LOWER HALLWAY
        if affected_object in interactive_objects_list[5]:
            output = affect_object_lower_hallway(desired_item, affected_object)
    elif locator[0][0] >= 7:  # DRAGON ROOM
        if affected_object in interactive_objects_list[6]:
            output = affect_object_dragon_room(desired_item, affected_object)

    return output


def observe():
    locator = locatorlib.locator

    if locator[1][2] >= 7:  # UPPER HALLWAY CORNER
        output = "You are standing at the upper end of a corridor. Long stretches of darkness punctuate the" \
                 " passageway in between lit, consecutive torches. There is a door to the WEST. The corridor goes" \
                 " NORTH. "
    elif locator[1][3] >= 7:  # LIBRARY
        output = observe_library()
    elif locator[2][2] >= 7:  # UPPER HALLWAY
        output = "You are standing in the upper corridor. The stone floor is littered with bones and mould and" \
                 " droppings. Occasional cockroaches weave in and out of the darkness. The corridor continues both" \
                 " NORTH and SOUTH. "
    elif locator[3][1] >= 7:  # PILLOW FORT ROOM
        output = observe_fort_room()
    elif locator[3][2] >= 7:  # MIDDLE HALLWAY
        output = "You are standing in the middle corridor. Waning torches provide just enough light to illuminate" \
                 " two heavy, wooden doors on either side of you. There is a door to the WEST and a door to the" \
                 " EAST. The corridor continues NORTH and SOUTH. "
    elif locator[3][3] >= 7:  # TRAPDOOR ROOM
        output = observe_trapdoor_room()
    elif locator[4][2] >= 7:  # LOWER HALLWAY
        output = observe_lower_hallway()
    elif locator[4][3] >= 7:  # GARDEN
        output = observe_garden()
    elif locator[5][2] >= 7:  # POTION ROOM
        output = observe_potion_room()
    elif locator[0][0] >= 7:  # DRAGON ROOM
        output = observe_dragon_room()

    if monsterlib.monster_specifier():
        output = output + monsterlib.print_monster()

    return output


def observe_library():

    output = "You are standing in a room. Giant bookcases are strewn about the dingy, little chamber - some toppled."

    # CONSTRUCTING ROOM DESCRIPTION BY CONSIDERING HOW USER HAS AFFECTED THE ROOM.
    if "bookcase" in interactive_objects_list[0]:
        output = output + " Only one BOOKCASE appears to have been purposefully placed against a wall."
    else:  # FIREPLACE REVEALED
        output = output + " One bookcase has been pushed, revealing"
        if "kindling (burning)" not in interactive_objects_list[0]:
            output = output + " a long-extinguished, hidden FIREPLACE. "
        else:
            output = output + " an inviting, burning FIREPLACE."

    if "kindling (fireplace)" in interactive_objects_list[0]:
        output = output + " Your KINDLING is set inside it."

    # AMEND SO THAT BOOK ISN'T IMMEDIATELY OBVIOUS. MUST INSPECT DESK WITH HANDS. REDUCE TEXT.
    output = output + f" A writing DESK is nearby."

    if "nest" in interactive_objects_list[0]:
        nest = "NEST"
    else:
        nest = "nest"

    if "nest (aggressive)" in interactive_objects_list[0]:
        output = output + f" There is an active hornets {nest} humming from the corner above a table."
    elif "nest (pacified)" in interactive_objects_list[0]:
        output = output + f" There is an inactive hornets {nest}. Stunned hornets litter the floor."

    if "kindling (nest)" in interactive_objects_list[0]:
        output = output + " Your KINDLING is set below it."

    # ADD THIS TO AFFECT OBJECT: NEST
    if "nest" in interactive_objects_list[0]:
        output = output + " Something appears to be inside."

    if "bucket (grounded)" in interactive_objects_list[0]:
        output = output + " There is a BUCKET on the floor."
    elif "bucket" in interactive_objects_list[0]:
        output = output + " There is a BUCKET situated high on a bookcase."

    output = output + " You came from the EAST."

    return output


bookcase_yes_or_no = False


def inspected_bookcase():
    global bookcase_yes_or_no
    bookcase_yes_or_no = False


def affect_object_library(desired_item, affected_object):

    global bookcase_yes_or_no
    output = f"You tap the {affected_object.upper()} with your {desired_item.upper()}. Nothing happens."

    # AFFECTING DESK
    if affected_object == "desk":
        if desired_item == "hands":  # WITH HANDS
            output = "You inspect the DESK. There is an old BOOK lying open, caked in dust."

    # AFFECTING BOOK
    if affected_object == "book":
        if desired_item == "hands":  # WITH HANDS
            output = "read_book" \
                     "You inspect the BOOK. You rub the dust off and find that the faded words are still " \
                     "legible. You begin reading. What would you like to read about?\n\n" \
                     "Monsters             Afflictions\n" \
                     "-Skeletons           -Enfeeblement\n" \
                     "-Slimes              -Undead\n" \
                     "-Imps\n" \
                     "-                    -Undo"
        elif desired_item == "matchbox":  # WITH MATCHBOX
            output = "You light a match and set the book on fire, wondering intently about what that could have" \
                     " possibly accomplished."
            interactive_objects_list[0].remove("book")

    # AFFECTING HERB
    elif affected_object == "herb":
        if desired_item == "hands":  # WITH HANDS
            output = "You scoop up the green HERB and cram it into your pocket - roots, soil and all. "
            interactive_objects_list[0].remove("herb")
            healthandinv.inventory_list[1].append("herb")

    # AFFECTING BOOKCASE
    elif affected_object == "bookcase":
        if desired_item == "hands":  # WITH HANDS
            output = "You inspect the BOOKCASE. It appears to be blocking some kind of opening in the wall.\nPush " \
                     "the BOOKCASE? yes/no"
            bookcase_yes_or_no = True

    # AFFECTING FIREPLACE
    elif affected_object == "fireplace":
        if desired_item == "hands":  # WITH HANDS
            if "kindling (burning)" not in interactive_objects_list[0]:
                output = "You inspect the FIREPLACE. A precious beam of sunlight seeps through the partially" \
                         " collapsed chimney"
                if "herb" in interactive_objects_list[0]:
                    output = output + " onto a single green HERB. It clings to a meagre pile of soil."
                else:
                    output = output + "."
            else:
                output = "The FIREPLACE is still burning. The tender flames warm your very soul. You gain (3) health."
                healthandinv.plus_health(3)
        elif desired_item == "matchbox":  # WITH MATCHBOX
            if "kindling (fireplace)" not in interactive_objects_list[0]:
                output = "You light a match and try to ignite the FIREPLACE but there is nothing to burn."
            else:
                output = "You light a match and ignite the FIREPLACE. The tender flames warm your very soul. You" \
                         " gain (3) health."
                interactive_objects_list[0].remove("kindling")
                interactive_objects_list[0].remove("kindling (fireplace)")
                interactive_objects_list[0].append("kindling (burning)")
                healthandinv.plus_health(3)
                if "herb" in interactive_objects_list[0]:
                    output = output + "The herb inside was incinerated."
                    interactive_objects_list[0].remove("herb")
        elif desired_item == "kindling":  # WITH KINDLING
            output = "You place the KINDLING inside the FIREPLACE."
            interactive_objects_list[0].append("kindling")
            interactive_objects_list[0].append("kindling (fireplace)")
            healthandinv.inventory_list[0].remove("kindling")

    # AFFECTING BUCKET
    elif affected_object == "bucket":
        # BUCKET IN REACH
        if "bucket (grounded)" in interactive_objects_list[0]:
            if desired_item == "hands":  # WITH HANDS
                output = "You pick up the wooden BUCKET and put it in your pocket."
                healthandinv.inventory_list[1].append("bucket")
                interactive_objects_list[0].remove("bucket")
                interactive_objects_list[0].remove("bucket (grounded)")
            elif desired_item == "slingshot":  # WITH SLINGSHOT
                output = "You continue to use your SLINGSHOT to pelt the grounded BUCKET with stones."
        # BUCKET NOT IN REACH
        else:
            if desired_item == "hands":  # WITH HANDS
                output = "You reach for the BUCKET but it is far too high up for you to grab."
            elif desired_item == "broom":  # WITH BROOM
                output = "You attempt to knock the BUCKET off its lofty perch with your BROOM but find that it is" \
                         " still too high up!"
            elif desired_item == "slingshot":  # WITH SLINGSHOT
                output = "You pick up a stone from the floor and shoot it at the BUCKET. It clatters to the floor."
                interactive_objects_list[0].append("bucket (grounded)")  # BUCKET KNOCKED OFF BOOKCASE
            else:
                output = f"You throw your {desired_item.upper()} at the BUCKET but miss. You  retrieve your" \
                         f" {desired_item.upper()} and put it back in your pocket."

    # AFFECTING KINDLING
    elif affected_object == "kindling":
        if desired_item == "hands":  # WITH HANDS
            output = "You retrieve your KINDLING."
            interactive_objects_list[0].remove("kindling")
            healthandinv.inventory_list[0].append("kindling")
            try:
                interactive_objects_list[0].remove("kindling (nest)")
            except ValueError:
                interactive_objects_list[0].remove("kindling (fireplace)")
        elif desired_item == "matchbox":  # WITH MATCHBOX
            output = "You strike a match and ignite the kindling, gently nurturing the flame. "
            if "kindling (nest)" in interactive_objects_list[0]:
                output = output + "After stepping away, a plume of smoke gradually rises and enters the NEST." \
                                  " Stunned and docile hornets drop out one by one until the NEST is silent," \
                                  " inactive and harmless."
                interactive_objects_list[0].remove("kindling (nest)")
                interactive_objects_list[0].remove("nest (aggressive)")
                interactive_objects_list[0].append("nest (pacified)")
            elif "kindling (fireplace)" in interactive_objects_list[0]:
                output = output + "After stepping away, the fire consumes the kindling. The wood crisps and crackles" \
                                  " and you are gently caressed by the warmth. You gain (3) health."
                healthandinv.plus_health(3)
                interactive_objects_list[0].remove("kindling (fireplace)")
                interactive_objects_list[0].append("kindling (burning)")
            interactive_objects_list[0].remove("kindling")

    # AFFECTING NEST
    elif affected_object == "nest":
        if "nest (aggressive)" in interactive_objects_list[0]:  # UNABLE TO INTERACT WITH NEST
            if desired_item == "hands":  # WITH HANDS
                output = "You tentatively extend your hand towards the hive of angry, flying needles. The hornets" \
                         " become agitated and begin to swarm. You wisely retreat."
            elif desired_item == "matchbox":  # WITH MATCHBOX
                output = "You ignite a match and attempt to set the NEST ablaze. You are unable to cause the flame" \
                         " to catch."
            elif desired_item == "kindling":  # WITH KINDLING
                output = "You place the KINDLING beneath the hornets NEST."
                interactive_objects_list[0].append("kindling")
                interactive_objects_list[0].append("kindling (nest)")
                healthandinv.remove_from_inventory("kindling")
            else:
                output = f"You poke at the hornets NEST with your {desired_item.upper()}. The item inside does not" \
                         " budge. The hornets become agitated and you retreat."
        else:  # ABLE TO INTERACT
            if desired_item == "hands":  # WITH HANDS
                if "slingshot" in interactive_objects_list[0]:
                    output = "You extend your hand towards the inactive hive. The hornets do not react. Your hand" \
                             " enters the still, squirming, waxy interior and you pull the item out. You obtained a" \
                             " SLINGSHOT. What was it doing in there? You put it in your pocket."
                    interactive_objects_list[0].remove("slingshot")
                    healthandinv.inventory_list[0].append("slingshot")
                elif "larva" in interactive_objects_list[0]:
                    output = "You extend your hand towards the inactive hive. The hornets do not react. Your hand" \
                             " enters the squirming, waxy interior again and you pull another item out. You obtained" \
                             " a hornet LARVA. You put it in your pocket."
                    interactive_objects_list[0].remove("larva")
                    interactive_objects_list[0].remove("nest")
                    healthandinv.inventory_list[0].append("larva")

    return output


def observe_fort_room():

    output = "You are standing in a room. Little, bone talismans dangle from the ceiling to the floor on long" \
             " threads. The walls are covered with painted, foreign runes. In the far corner, a large, moth-eaten" \
             " sheet of fabric stands propped up in a pentahedrical formation like a tent. A BELL dangles on" \
             " a stick outside it."

    if "broom" in interactive_objects_list[1]:
        output = output + " A BROOM leans against the wall near you."

    output = output + " You came from the WEST."

    return output


def affect_object_fort_room(desired_item, affected_object):

    # AFFECTING BELL
    if affected_object == "bell":
        output = "npc_dialogue" \
                 f"You ring the BELL with your {desired_item.upper()}."

    # AFFECTING BROOM
    elif affected_object == "broom":
        if desired_item == "hands":  # WITH HANDS
            output = "You take the BROOM and put it in your pocket."
            healthandinv.inventory_list[0].append("broom")
            interactive_objects_list[1].remove("broom")
        else:
            output = f"You tap the BROOM with your {desired_item.upper()}."

    return output


def observe_trapdoor_room():

    output = "You are standing in a room. Bits of straw and hay litter the largely empty space and a closed" \
             " TRAPDOOR is in the middle of the stone floor. Waves of suffocating heat blast you from beneath."

    if "spade" in interactive_objects_list[2]:
        output = output + " There is a SPADE mounted high up, out of reach."

    if "ladder" in interactive_objects_list[2]:
        ladder = "LADDER"
    else:
        ladder = "ladder"

    if "ladder (broken)" in interactive_objects_list[2]:
        output = output + f" A broken {ladder} leans against the wall."
    else:
        output = output + f" A fixed {ladder} leans against the wall."

    if "kindling" in interactive_objects_list[2]:
        output = output + " A pile of dried KINDLING lies on the floor."

    output = output + " You came from the EAST."

    return output


trapdoor_yes_or_no = False


def inspected_trapdoor():
    global trapdoor_yes_or_no
    trapdoor_yes_or_no = False


def affect_object_trapdoor_room(desired_item, affected_object):
    global trapdoor_yes_or_no

    output = f"You tap the {affected_object.upper()} with your {desired_item.upper()}. Nothing happens."

    # AFFECTING LOCK
    if affected_object == "lock":
        if desired_item == "key":  # WITH KEY
            output = "You give your KEY one final wipe before inserting it into the lock. You rotate it and the" \
                     " lock springs open with a clunk."
            healthandinv.inventory_list[0].remove("key")
            interactive_objects_list[2].remove("trapdoor (locked)")
            interactive_objects_list[2].remove("lock")
        else:
            output = f"You fervently attempt to pick the LOCK with your {desired_item.upper()}.\n...\nIt doesn't work."

    # AFFECTING KINDLING
    elif affected_object == "kindling":
        if desired_item == "hands":  # WITH HANDS
            output = "You pick up some KINDLING."
            healthandinv.inventory_list[0].append("kindling")
            interactive_objects_list[2].remove("kindling")
        elif desired_item == "matchbox":  # WITH MATCHBOX
            output = "You light the kindling on fire with a match. It creates a tall tower of smoke."
            interactive_objects_list[2].remove("kindling")

    # AFFECTING LADDER
    elif affected_object == "ladder":
        if desired_item == "hands":  # WITH HANDS
            if "ladder (broken)" in interactive_objects_list[2]:
                output = "You inspect the LADDER. It is missing a RUNG, preventing you from climbing very high."
            else:
                output = "You cautiously test the integrity of the rung you installed. After confirming that it" \
                         " holds your weight, you climb. You reach for the SPADE and lift it from its mount. You" \
                         " obtained a SPADE. You put it in your pocket."
                healthandinv.inventory_list[0].append("spade")
                interactive_objects_list[2].remove("ladder")
                interactive_objects_list[2].remove("spade")
        elif desired_item == "rung":
            output = "You gently pry the LADDER apart and slot the rung into two empty holes on either side. You" \
                     " silently hope that it supports your weight."
            interactive_objects_list[2].remove("ladder (broken)")
            healthandinv.remove_from_inventory("rung")

    # AFFECTING TRAPDOOR
    elif affected_object == "trapdoor":
        if desired_item == "hands":  # WITH HANDS
            if "trapdoor (locked)" in interactive_objects_list[2]:
                output = "You go to open the TRAPDOOR but a heavy LOCK impedes your attempt."
            else:
                output = "With the lock defeated, you lift the TRAPDOOR open. You are greeted by an immense," \
                         " growing heat erupting from the depths. The open TRAPDOOR reveals a set of stone steps" \
                         " leading downwards. You might hear the heavy rattling of chains echoing from below. Go in?" \
                         " yes/no"
                trapdoor_yes_or_no = True
        elif desired_item == "key":  # WITH KEY
            output = "You give your KEY one final wipe before inserting it into the TRAPDOOR. You rotate it inside" \
                     " the lock and it springs open with a clunk."
            healthandinv.inventory_list[0].remove("key")
            interactive_objects_list[2].remove("trapdoor (locked)")
            interactive_objects_list[2].remove("lock")

    # AFFECTING SPADE
    elif affected_object == "spade":
        if desired_item == "hands":  # WITH HANDS
            if "ladder (broken)" in interactive_objects_list[2]:
                output = "You reach for the SPADE. It is far too high for you to touch."
            else:
                output = "You cautiously test the integrity of the rung you installed. After confirming that it" \
                         " holds your weight, you climb. You reach for the SPADE and lift it from its inconvenient" \
                         " mount. You obtained a SPADE. You put it in your pocket."
                healthandinv.inventory_list[0].append("spade")
                interactive_objects_list[2].remove("ladder")
                interactive_objects_list[2].remove("spade")
        elif desired_item == "broom":
            output = "You innovatively employ the BROOM's extended reach and poke at the mounted SPADE. However," \
                     " your BROOM lacks the dexterity to budge it significantly."
        elif desired_item == "slingshot":
            output = "You shoot a projectile at the SPADE. It does not budge."
        else:
            output = f"You try to reach the SPADE with your {desired_item.upper()}. It doesn't work."

    return output


def observe_lower_hallway():
    output = "You are standing at the lower end of a corridor. The damp, stone floor sucks any memory of warmth from" \
             " your bare feet."
    if "mushroom" in interactive_objects_list[5]:
        output = output + " A MUSHROOM is growing on the floor."
    output = output + " There is a door to the NORTH and a door to the WEST. The corridor goes SOUTH."

    return output


def affect_object_lower_hallway(desired_item, affected_object):

    # AFFECTING MUSHROOM
    if affected_object == "mushroom":
        if desired_item == "hands":  # WITH HANDS
            output = "You harvest the MUSHROOM and put it in your pocket."
            healthandinv.inventory_list[1].append("mushroom")
            interactive_objects_list[5].remove("mushroom")

    return output


def observe_garden():

    output = "You are standing in a room. Invading plant life has transformed this chamber into a thriving bed of" \
             " nature. A gentle stream of WATER is pouring inside from a large hole in the ceiling, before trickling" \
             " down a grid."

    if "soil (undisturbed)" in interactive_objects_list[3]:
        output = output + " Sunlight shines upon a large patch of SOIL in the middle of the room."
    elif "soil (disturbed)" in interactive_objects_list[3]:
        output = output + " Sunlight shines upon a hole in the SOIL in the middle of the room."
    else:
        output = output + " Sunlight shines upon an excavated patch of soil in the middle of the room."

    if "bird" in interactive_objects_list[3]:
        if "bird (dead)" in interactive_objects_list[3]:
            output = output + " A dead BIRD lies on the floor."
        else:
            output = output + " A BIRD flutters about the ceiling."

    if "herb" in interactive_objects_list[3]:
        output = output + " A HERB is growing."
    output = output + " There is a stone WELL in the corner of the room."
    output = output + " You came from the EAST."

    return output


pot = [None]


def affect_object_garden(desired_item, affected_object):

    output = f"You tap the {affected_object.upper()} with your {desired_item.upper()}. Nothing happens. "

    # AFFECTING HERB
    if affected_object == "herb":
        if desired_item == "hands":  # WITH HANDS
            output = "You scoop the HERB up and stuff it into your pocket. "
            healthandinv.inventory_list[1].append("herb")
            interactive_objects_list[3].remove("herb")

    # AFFECTING BIRD
    if affected_object == "bird":
        if "bird (dead)" not in interactive_objects_list[3]:  # BIRD ALIVE
            if desired_item == "larva":  # WITH LARVA
                output = ["You take out the squirming hornet grub and hold it out in your open palm. The bird spots"
                          " it and cautiously lands nearby, gradually inching closer while inspecting you.",
                          "After  a moment of hesitation, it flies up to your hand and swallows the grub, whole. The"
                          " bird is clutching a shiny, glass, circular object with a chain. You take it and spook"
                          " the bird. It flies off. You put the glass CIRCLE in your pocket."]  # TEST THIS!!!!!!!!
                healthandinv.inventory_list[1].append("circle")
                healthandinv.inventory_list[0].remove("larva")
                interactive_objects_list[3].remove("bird")
            elif desired_item == "slingshot":  # WITH SLINGSHOT
                output = "You fire a projectile at the BIRD with your slingshot. The shot connects and you hear" \
                         " something glass shattering. The BIRD drops to the floor."
                interactive_objects_list[3].append("bird (dead)")
            else:
                output = f"You try to catch the BIRD with your {desired_item.upper()} but it is far too swift."
        else:  # BIRD DEAD
            if desired_item == "hands":  # WITH HANDS
                output = "You go to pick the dead BIRD up. Shards of a glass object are scattered about the its" \
                         " body. You take the dead BIRD and put it in your pocket."
                healthandinv.inventory_list[1].append("bird")
                interactive_objects_list[3].remove("bird")
            else:
                output = f"You poke the dead BIRD with your {desired_item.upper()}."

    # AFFECTING FISH
    elif affected_object == "fish":
        if desired_item == "larva":  # WITH LARVA
            output = ["You take out the squirming larva and hold it at the water's surface. The FISH notices. It swims"
                      " closer and closer to the larva. Your other hand patiently hovers above the surface.",
                      "The FISH's head finally breaks the water's surface and, as it comes into contact with the air,"
                      " you see its shining, golden scales transmute into a pale, hollow skull, right before your eyes."
                      " The bare fish skull gulps the larva down. You grab the FISH and put it into your pocket."]
            healthandinv.inventory_list[1].append("fish")
            healthandinv.inventory_list[0].remove("larva")
            interactive_objects_list[3].remove("fish")
        elif desired_item == "hands":  # WITH HANDS
            output = "You reach for the FISH but it is far too deep."
        elif desired_item == "pot" or desired_item == "helmet":
            output = f"You try to scoop the FISH up with your {desired_item.upper()} but it easily evades you."

    # AFFECTING WELL
    elif affected_object == "well":
        if desired_item == "hands":  # WITH LARVA
            output = "You inspect the WELL. It is narrow, but deep. "
            if "rung" in interactive_objects_list[3]:
                output = output + "You see that there is a wooden ladder RUNG floating on the water's surface. "
            if "fish" in interactive_objects_list[3]:
                output = output + "There is a beautiful, golden FISH swimming in the depths."
        elif desired_item == "pot":
            if "water" in pot:
                output = "You dump the water into the WELL. The water level rises slightly."
                pot.remove("water")
                try:
                    interactive_objects_list[3].remove("well (unfilled)")
                except ValueError:
                    pass
            else:
                output = "You use your empty POT on the WELL. Nothing happened."
        elif desired_item == "coin":
            output = "You flick your coin in to the WELL and make a wish."
            healthandinv.inventory_list[0].remove("coin")

    # AFFECTING RUNG
    elif affected_object == "rung":
        if "well (unfilled)" in interactive_objects_list[3]:  # WELL NOT FILLED
            if desired_item == "hands":  # WITH HANDS
                output = "You stick your arm into the WELL to reach the RUNG. You strain your arm and fingers towards" \
                         " it but you are only able to briefly touch it as it bobs about. The RUNG still evades your" \
                         " grasp."
            elif desired_item == "pot" or desired_item == "helmet":
                output = f"With your {desired_item.upper()} granting slightly longer reach, you scoop the RUNG up" \
                         " with it. After fishing the RUNG out, you give it a shake and put it in your pocket."
                healthandinv.inventory_list[0].append("rung")
                interactive_objects_list[3].remove("rung")
            else:
                output = f"You try to obtain the ladder RUNG with your {desired_item.upper()} but your attempt is" \
                         " in vain."
        else:  # WELL FILLED
            if desired_item == "hands":  # WITH HANDS
                output = "You reach your arm into the WELL to reach the RUNG. The water level has risen just enough" \
                         " that you can now grab the RUNG. You pull it up, shake it dry and put it in your pocket."
                healthandinv.inventory_list[0].append("rung")
                interactive_objects_list[3].remove("rung")
            elif desired_item == "pot" or desired_item == "helmet":
                output = f"You scoop up the ladder RUNG with your {desired_item.upper()}. You shake it dry and put" \
                         " the RUNG in your pocket."
                healthandinv.inventory_list[0].append("rung")
                interactive_objects_list[3].remove("rung")

    # AFFECTING SOIL
    elif affected_object == "soil":
        if desired_item == "hands":  # WITH HANDS
            output = "You get on your hands and knees and rake at the dirt with your fingers. They quickly tire. If" \
                     " only you had a digging implement..."
        elif desired_item == "spade":  # WITH SPADE
            if "soil (undisturbed)" in interactive_objects_list[3]:
                output = "You thrust your SPADE into the patch of SOIL and heave up a clump of dirt. You repeat this" \
                         " motion again and again until, finally, you discover something. It's small and hard, like" \
                         " metal. Upon wiping the dirt off, you manage to identify it. It's a KEY. You put it in your" \
                         " pocket."
                healthandinv.inventory_list[0].append("key")
                interactive_objects_list[3].remove("soil (undisturbed)")
                interactive_objects_list[3].append("soil (disturbed)")
            elif "soil (disturbed)" in interactive_objects_list[3]:
                output = "You continue industriously excavating the earth with renewed vigor. You stop, however," \
                         " when you see something white sticking out of the soil. After scraping the dirt off it," \
                         " you discover that it's a FLUTE made from bone. You put the FLUTE into your pocket."
                healthandinv.inventory_list[0].append("flute")
                interactive_objects_list[3].remove("soil (disturbed)")
                interactive_objects_list[3].remove("soil")

    # AFFECTING WATER
    elif affected_object == "water":
        if desired_item == "hands":
            output = "You touch the falling WATER. It's very cold."
        elif desired_item == "pot":
            output = "You hold your POT out to catch the falling WATER. Your POT is filled."
            pot.append("water")
        elif desired_item == "helmet":
            output = "You take the bucket off your head and catch the WATER. It spills straight out of the hole in" \
                     " the side. You despondently put your dripping HELMET back on your head."
        else:
            output = f"You rinse your {desired_item.upper()} in the water."

    return output


def observe_potion_room():

    output = "You are standing in a room bathed in the blue, ambient glow of a single GAS BURNER flame." \
             " It is connected to a complex network of steamy, glass tubes and bubbling flasks."

    if "matchbox" in interactive_objects_list[4]:
        output = output + " A MATCHBOX lies underneath."

    if "spider" in interactive_objects_list[4]:
        adjective = "glossy, black SPIDER"
        verb = "sits"
    else:
        # CHANGE SO THAT GAME CAN BE COMPLETED TOTALLY PACIFISTICALLY
        adjective = "dead spider"
        verb = "lies"

    output = output + f" The corner of the room is smothered by spiderwebs and a giant, {adjective} {verb}" \
                      f" in its funnel web lair. "

    if "item" in interactive_objects_list[4]:
        output = output + " An unidentifiable ITEM seems to be wrapped up in the silk."
    elif "lute" in interactive_objects_list[4]:
        output = output + " A LUTE has been freed from the silk."

    output = output + " You came from the SOUTH."

    return output


def affect_object_potion_room(desired_item, affected_object):

    output = f"You tap the {affected_object.upper()} with your {desired_item.upper()}. Nothing happens."

    # AFFECTING SPIDER
    if affected_object == "spider":
        if desired_item == "broom":
            base_damage = 2
        else:
            base_damage = 1
        output = f"You bat the unsuspecting arachnid with your {desired_item.upper()}. You inflict ({base_damage})" \
                 " damage.\nThe spider perishes and its legs slowly curl inwards like gnarled fingers."
        interactive_objects_list[4].remove("spider")

    # AFFECTING GAS BURNER (YET TO PROGRAMME)
    elif affected_object == "burner":
        if desired_item == "hands":
            output = "You inspect the GAS BURNER. How or why this antiquated piece of equipment is burning is a" \
                     " mystery. Your hands have come to rest upon a mortar and pestle."
            # "It appears as though alchemy can be practiced here."
            # gas_burner()

    # AFFECTING ITEM
    elif affected_object == "item":
        if desired_item == "hands":
            if "spider" in interactive_objects_list[4]:
                output = "Your hand gravitates towards the concealed ITEM. As soon as you make contact, the giant" \
                         " SPIDER lunges. You retract your hand just in time and the SPIDER skitters back to its lair."
            else:
                output = "You go to touch the ITEM. You can neither identify it, nor take it while it is concealed" \
                         " by webbing. Perhaps if you had some sort of sweeping implement..."
        elif desired_item == "broom":
            if "spider" in interactive_objects_list[4]:
                output = "You use your BROOM to sweep at the item. The startled SPIDER flinches, before lunging" \
                         " for you. You are unable to contend with the SPIDER's fierce defence of its loot and you" \
                         " withdraw your BROOM."
            else:
                output = "You use your BROOM to sweep the item clean. You find that the item was a LUTE."
                interactive_objects_list[4].remove("item")
                interactive_objects_list[4].append("lute")

    # AFFECTING LUTE
    elif affected_object == "lute":
        if desired_item == "hands":
            output = "You pull the LUTE from its cocoon and jam it into your pocket."
            healthandinv.inventory_list[0].append("lute")
            interactive_objects_list[4].remove("lute")
        elif affected_object == "lute":
            output = "You sweep at a few more wisps of webbing on the LUTE with your BROOM."

    # AFFECTING MATCHBOX
    elif affected_object == "matchbox":
        if desired_item == "hands":
            output = "You take the MATCHBOX and put it in your pocket."
            healthandinv.inventory_list[0].append("matchbox")
            interactive_objects_list[4].remove("matchbox")

    return output


def observe_dragon_room():
    # FUTUREPROOFING NOTE: IF DRAGON IS DEAD, USER CANNOT OBSERVE THIS ROOM.
    output = ""

    if locatorlib.locator[0][0] == 12:
        output = output + "You are standing in a room. An enraged DRAGON is chained to the wall with enormous" \
                          " SHACKLES. There is nowhere to run."

    for item in interactive_objects_list[6]:
        if item == "shackles":
            pass
        else:
            output = output + f" There is a {item.upper()} lying on the floor."

    return output


shackles_health = 20


def affect_object_dragon_room(desired_item, affected_object):

    global shackles_health

    output = f"You tried to use your {desired_item.upper()} on the {affected_object.upper()}."

    attacking_items = [
        ["hands", "broom", "spade", "slingshot", "pitchfork"],
        [1, 2, 3, 2, 4]  # ASSOCIATED ATTACK VALUES
    ]

    # PUTTING THIS IF STATEMENT AT THE TOP WILL PREVENT PLAYER FROM APPENDING SHACKLES TO INVENTORY.
    if affected_object == "shackles":
        index = attacking_items[0].index(desired_item)
        base_damage = attacking_items[1][index]

        output = f"You attack the SHACKLES with your {desired_item.upper()}. "

        if "broken bone" in healthandinv.contracted_diseases:
            base_damage -= 1
            output = output + "Your BROKEN BONE suppresses your attack by (1)."

        output = output + f"You inflict {base_damage} damage. "
        shackles_health -= base_damage

    elif desired_item == "hands":
        # FUTURE PROOFING NOTE: WILL NOT WORK IF CONSUMABLES ARE LATER DECIDED TO BE VULNERABLE TO WING BEATS
        if affected_object in interactive_objects_list[6]:
            healthandinv.inventory_list[0].append(affected_object)
            interactive_objects_list[6].remove(affected_object)
            output = f"You take the {affected_object.upper()} and put it in your pocket."

    return output
