from random import randint
import locatorlib
import healthandinv
import roomslib

beasties_list = [
    ["skeleton", "slime", "imp", "dragon"],  # NAMES
    [2, 3, 4, 5],  # MAP VALUES
    [5, 4, 3, 18]  # HEALTH CONSTANTS
]
monster_health = [
            [100],  # FOR HEALTH VALUE
            ['64']  # FOR COORDINATES
]

monster_ferocity_count = 0


def monster_specifier():
    # CHECKING IF MONSTER IS PRESENT AT PLAYER'S COORDINATES
    y, x = locatorlib.find_coordinates()
    monster_value = locatorlib.locator[y][x] - 7
    if monster_value == 2:
        monster = "skeleton"
    elif monster_value == 3:
        monster = "slime"
    elif monster_value == 4:
        monster = "imp"
    elif monster_value == 5:
        monster = "dragon"
    else:
        monster = ""

    return monster


def print_monster():
    monster = monster_specifier()

    if monster == "imp":
        grammatical_n = "n"
    else:
        grammatical_n = ""

    return f"A{grammatical_n} {monster.upper()} is present."


def spawn():
    # DETERMINES WHETHER A MONSTER SPAWNS
    random_spawn = randint(0, 19)
    random_message = randint(0, 4)

    monster_text = ""

    # POTENTIALLY SPAWNS A MONSTER AT THE PLAYER'S CURRENT COORDINATE
    if monster_specifier():
        # MONSTER ALREADY PRESENT AT THAT COORDINATE
        monster_text = print_monster()
        random_spawn = 0
    else:
        if random_spawn == 2 or random_spawn == 3 or random_spawn == 4:
            y, x = locatorlib.find_coordinates()
            if y != 3 and x != 1:  # ONLY COORDINATE MONSTERS SHOULD NOT SPAWN
                # !!! METHOD BY WHICH WE INCREASE LOCATOR COORDINATE VALUES. IMPORTANT LINE OF CODE!
                locatorlib.locator[y][x] += random_spawn
            else:
                random_spawn = 0

    # RANDOM SPAWN MESSAGES
    if random_spawn == 2:  # SKELETON SPAWNS
        if random_message == 0:
            monster_text = "Bones from the floor begin to hover and dance like the limbs of a marionette. A" \
                           " SKELETON forms. It regards you with its dead, dusty sockets."
        elif random_message == 1:
            monster_text = "A disturbing, hollow clattering echoes from the dark. You spy a bleach white claw" \
                           " emerge from the shadow, followed by the anatomical monstrosity attached to it. A" \
                           " SKELETON crouches before you."
        elif random_message == 2:
            monster_text = "You hear debris rustling nearby and spin around to view a creaking mannequin of bone." \
                           " A SKELETON is watching you."
        elif random_message == 3:
            monster_text = "A broken, spindly figure approaches you from the inky black of your surroundings. A" \
                           " SKELETON. It silently stares."
        elif random_message == 4:
            monster_text = "You see bones from the floor begin to shudder and join like magnets. They come together" \
                           " to form a pitiful visage of death. A SKELETON has appeared."

    elif random_spawn == 3:  # SLIME SPAWNS
        if random_message == 0:
            monster_text = "You look up to see an oozing mass of sludge clinging to the ceiling. Its sticky," \
                           " amorphous arms are reaching for you. A SLIME draws near."
        elif random_message == 1:
            monster_text = "You step on a sticky, pulsating film covering the floor. It begins to recede toward a" \
                           " common epicentre of yellow goop, collecting itself until, finally, it has gathered into" \
                           " a giant, rippling droplet of acid hunger. A SLIME is in pursuit."
        elif random_message == 2:
            monster_text = "You stop just shy of something squirming on the floor. You look down to witness a blob" \
                           " of yellow sludge desperately struggling to attach to you. A SLIME is seeking you."
        elif random_message == 3:
            monster_text = "You come upon the scene of a SLIME feasting upon some hapless dungeon fauna. Pseudopods" \
                           " extend toward you. It is coming for you."
        elif random_message == 4:
            monster_text = "The floor pools with what looks like green, pulsating mould. A gelatinous blob forms" \
                           " from it. It begins toward you, extruding its uniform innards in a disgusting mockery" \
                           " of locomotion. A SLIME gives chase."

    elif random_spawn == 4:  # IMP SPAWNS
        if random_message == 0:
            monster_text = "You discern the unmistakable outline of a fiend lurking in the shadow. An IMP is close."
        elif random_message == 1:
            monster_text = "Your ear manages to distinguish a noise from the dungeon ambiance. A high-pitched," \
                           " deranged chittering emanating from the gloom. For a moment, you glimpse a wickedly" \
                           " sharp pitchfork in the shadows. An IMP is close."
        elif random_message == 2:
            monster_text = "You feel deep down that something is amiss. You anxiously pivot around, accidentally" \
                           " colliding with an IMP attempting to pickpocket you. It flutters frantically and" \
                           " raises its miniature pitchfork, ready to stab you."
        elif random_message == 3:
            monster_text = "You stumble upon the scene of an IMP tormenting a rat. It turns its attention" \
                           " toward you, peering into you with black, beady marbles. An IMP approaches."
        elif random_message == 4:
            monster_text = "Your surroundings are spontaneously drenched in a storm of fire as a hellish portal" \
                           " opens in front of you and spits out a tiny denizen of the underworld. An IMP" \
                           " was summoned."
    if monster_text:
        monster_text = "\n" + monster_text
    return monster_text


def calculate_monster_health(inflicted_damage):

    global monster_ferocity_count

    # SO THAT A MONSTER AT A SPECIFIC COORDINATE WILL RETAIN ITS HEALTH VALUE
    y, x = locatorlib.find_coordinates()
    monster = monster_specifier()
    concatenated_coordinates = str(y) + str(x)
    output = ""

    if concatenated_coordinates not in monster_health[1]:
        # APPENDING monster_health WITH COORDINATES
        monster_health[1].append(concatenated_coordinates)
        # SEARCHING HEALTH VALUE OF THE SPECIFIC MONSTER
        second_index = beasties_list[0].index(monster)
        # USING INDEX OF TOP ROW TO FIND HEALTH VALUE ON THIRD ROW (INDEX 2)
        monster_health[0].append(beasties_list[2][second_index])

    # LOOKING UP HEALTH VALUE OF MONSTER CURRENTLY AT PLAYER COORDINATES
    second_index = monster_health[1].index(concatenated_coordinates)

    # SUBTRACTING STORED HEALTH VALUE IN monster_health BY inflicted_damage
    if concatenated_coordinates in monster_health[1]:
        # SUBTRACTING STORED HEALTH VALUE IN monster_health BY inflicted_damage
        monster_health[0][second_index] -= inflicted_damage

    # REMOVING HEALTH VALUE AND concatenated_coordinated FROM monster_health IF IT IS BELOW 1.
    # NOTE: INDEX ERROR IF NO VALUE IS IN THE LIST!
    if monster_health[0][second_index] < 1:
        monster_health[0].remove(monster_health[0][second_index])
        monster_health[1].remove(monster_health[1][second_index])
        # !!! SUBTRACTING MONSTER MAP VALUE FROM PLAYER'S CURRENT COORDINATES
        second_index = beasties_list[0].index(monster)
        locatorlib.subtract_value(y, x, second_index)
        output = loot_drop(monster)
        # RESET MONSTER FEROCITY AFTER EACH MONSTER DEFEATED
        monster_ferocity_count = 0

    return output


coin_loot_obtained = False
imp_inventory = []


def loot_drop(monster):

    global coin_loot_obtained
    global defeated_dragon

    random_number = randint(0, 1)

    if monster == "skeleton":
        output = "The SKELETON's sinister will ceases to drive it. It finally collapses into a harmless pile of" \
                 f" bones. The {monster.upper()} is dead."
        if not coin_loot_obtained:  # ENSURES ONLY 1 COIN CAN BE OBTAINED
            output = output + " It dropped a COIN. You pick it up an put it in your pocket."
            coin_loot_obtained = True
            healthandinv.inventory_list[0].append("coin")
        output = output + "ske_dead_code"  # CHANGES ON-SCREEN IMAGE

    elif monster == "slime":
        output = "The SLIME bursts like a pustule and sags until it is nought but a deflated, sizzling bubble. The" \
                 f" {monster.upper()} is dead."
        # WHAT COULD A SLIME DROP, I WONDER!
        output = output + "sli_dead_code"  # CHANGES ON-SCREEN IMAGE

    elif monster == "imp":
        output = "Your attack causes the devil to plummet and splat on the ground. Its still body combusts into a" \
                 f" little bonfire and its ashes are carried away by an eerie wind. The {monster.upper()} is dead."
        if random_number == 1:
            if len(imp_inventory) > 0:
                reclaimed_item = imp_inventory.pop(0)
                output = output + f" It dropped a familiar looking {reclaimed_item.upper()}. You pick it up and" \
                                  f" put it in your pocket."
                healthandinv.inventory_list[1].append(reclaimed_item)
            else:
                output = output + " It dropped a BERRY. You pick it up and put it in your pocket."
                # PERHAPS EXPAND THE CODE SO THAT ITEMS CAN BE DROPPED AND RETRIEVED IN ANY ROOM ON LOCATOR
                healthandinv.inventory_list[1].append("berry")
        output = output + "imp_dead_code"  # CHANGES ON-SCREEN IMAGE

    elif monster == "dragon":
        output = "Your attack connects directly with the dragon's skull and a resounding crack follows the blow. The" \
                 " dragon lets out one final, exhausted roar before collapsing on top of itself.\nYou slew the dragon."
        defeated_dragon = True

    return "\n" + output


defeated_dragon = False


def monster_attack():

    global monster_ferocity_count
    global defeated_dragon

    monster = monster_specifier()
    random_number = randint(0, 5)
    critical_hit = False
    output = ""

    if not monster:
        return output

    elif monster == "skeleton":
        damage = 3
        if random_number > 3:  # HIGHER CRITICAL HIT RATE
            critical_hit = True
            output = "The SKELETON's dead stance suddenly jerks to life. It uses every limb at its disposal to" \
                     " grasp and mangle you."
            damage += 2  # SLIGHTLY LOWER CRITICAL HIT DAMAGE
        elif random_number == 0:
            output = "The SKELETON lunges towards you, but inertia blows its rickety body to pieces. It takes a" \
                     " moment for it to reassemble itself."
            damage = 0
        elif random_number == 1:
            output = "The SKELETON's idle facade suddenly vanishes. It takes a hold of you, raking at your skin with" \
                     "its claws."
        else:
            output = "Like a wind-up toy, the SKELETON bursts into action. It savagely mauls you, biting and" \
                     " battering without a hint of either mercy or motive."

    elif monster == "slime":
        damage = 1
        if random_number == 5:
            critical_hit = True
            if "enfeeblement" not in healthandinv.contracted_diseases:
                healthandinv.contracted_diseases.append("enfeeblement")
                output = "The SLIME's viscous form attaches to you and it begins sucking you into its jelly. Your" \
                         " flesh sears as the SLIME begins deconstructing and absorbing you at the molecular level." \
                         "\nCONTRACTED: ENFEEBLEMENT\n"
            else:  # IF ENFEEBLEMENT HAS ALREADY BEEN CONTRACTED
                damage *= 2
                output = "The SLIME latches itself onto you. You watch in horror as your flesh and blood dissipate" \
                         " in a watery cloud of particles in the SLIME's body. You wrench yourself free and clutch" \
                         " your newly bloodied appendage."
        elif random_number == 0:
            damage = 0
            output = "Though persistent, the SLIME's sluggish movements are failing to find purchase. You're able to " \
                     "evade its touch."
        elif random_number == 1:
            output = "Sticky, corrosive fluid squirts out at you from the SLIME's membrane. You frantically wipe" \
                     " at the sizzling stain while the SLIME mends itself."
        else:
            output = "You momentarily see the SLIME fold into itself. In an instant, it sprays out an  oppressive" \
                     " cloud of acid droplets that cling to your exposed flesh."

    elif monster == "imp":
        damage = 4
        if random_number == 5:
            # IMP WILL INFLICT DAMAGE IF PLAYER HAS NO CONSUMABLES TO STEAL
            if len(healthandinv.inventory_list[1]) < 1:
                critical_hit = True
                output = "You fail to adequately defend as the IMP darts directly for your throat, thrusting its" \
                         " jagged pitchfork inside and inflicting devastating lacerations. You desperately clasp" \
                         " your hands around the geyser of blood."
                damage *= 2
            else:
                pilfered_item = healthandinv.inventory_list[1].pop(-1)
                imp_inventory.append(pilfered_item)
                output = "The IMP swoops down, coming alarmingly close. Before you can even think to bat it away, it" \
                         f" flees.\nAN IMP HAS PILFERED YOUR {pilfered_item.upper()}."
                # REMOVING IMP FROM locator AND monster_health
                y, x = locatorlib.find_coordinates()
                locatorlib.subtract_value(y, x, 2)
                concatenated_coordinates = str(y) + str(x)
                damage = 0  # NO DAMAGE TO BE INFLICTED
                try:
                    second_index_hl = monster_health[1].index(concatenated_coordinates)
                    monster_health[0].remove(monster_health[0][second_index_hl])
                    monster_health[1].remove(monster_health[1][second_index_hl])
                except ValueError:  # !!! VALUE ERROR WOULD OCCUR IF IMP WAS NOT ATTACKED BEFORE IT TAKES AN ITEM
                    pass
        elif random_number == 0:
            output = "The IMP floats around above you, before plunging straight for your face. You instinctively swat" \
                     " at it, inadvertently sending its weapon flying. You disarmed the IMP. It hurries to retrieve" \
                     " its implement."
            damage = 0
        else:
            output = "The IMP makes a dash for your midriff, maliciously thrusting with its pitchfork all the while." \
                     " Your chest, hands and belly are punctured."

    elif monster == "dragon":
        if roomslib.shackles_health > 0:
            output, damage, critical_hit = dragon_attack()
        else:
            defeated_dragon = True
            return "The shackles around the dragon's limbs deform and the mechanisms finally fail. The dragon rears" \
                   " back to deliver fiery death, but stops itself midway as the shackles fall to the floor with a" \
                   " metallic clang."

    if "enfeeblement" in healthandinv.contracted_diseases:
        damage *= 2
    if "helmet" in healthandinv.inventory_list[0] and damage > 0:
        output = output + " Your HELMET reduced the damage by (2)."
        damage -= 2
    if damage < 0:
        damage = 0

    monster_ferocity_count += 1

    output = output + f" You receive ({damage}) damage."
    if critical_hit:
        output = output + f"{monster[:3]}_crit_code"
    healthandinv.subtract_health(damage)

    return "\n" + output


def dragon_attack():

    random_attack_number = randint(0, 23) + monster_ferocity_count
    random_severity_number = randint(0, 5)
    damage = 0
    critical_hit = False

    if 0 <= random_attack_number <= 17:  # REGULAR ATTACKS
        if random_severity_number == 0:
            output = "The DRAGON charges towards you like a steam locomotive. However, its attack is stifled by its" \
                     " chains and it is sent reeling backwards."
        elif random_severity_number == 1:
            output = "The DRAGON viciously slashes at you with its blunted claw."
            damage = 4
        elif random_severity_number == 2:
            output = "The DRAGON's clawed forelimb smashes into you and you are brutally thrown to the floor."
            damage = 4
        elif random_severity_number == 3:
            output = "The DRAGON's body turns and you fail to anticipate its attack before its long tail slams into" \
                     " you like a log."
            damage = 5
        elif random_severity_number == 4:
            output = "The DRAGON rushes you with gaping jaws and clamps down around your waist. It hurls you and" \
                     " you skid across the floor like a bleeding, helpless ragdoll."
            damage = 6
        elif random_severity_number == 5:
            output = "The DRAGON violently crushes you, pounding and dancing up and down on your tiny form.\n"
            damage = 6
            if "broken bone" not in healthandinv.contracted_diseases:
                healthandinv.contracted_diseases.append("broken bone")
                output = output + "SUFFERED: BROKEN BONE"

    elif 17 < random_attack_number < 25:  # WING BEAT.
        if random_severity_number > 1:
            output = "The DRAGON rears up for a second, beating its broken wings in the blink of an eye. A hurricane" \
                     " of hot, stale air batters you and"
            if len(healthandinv.inventory_list[0]) > 2:  # ENSURING THERE ARE 3+ ITEMS IN INVENTORY. HANDS SHOULD NEVER BE REMOVED
                removed_item1 = healthandinv.inventory_list[0].pop(-1)  # TEST!
                removed_item2 = healthandinv.inventory_list[0].pop(-1)
                roomslib.interactive_objects_list[6].append(removed_item1)
                roomslib.interactive_objects_list[6].append(removed_item2)
                output = output + f" your {removed_item1.upper()} and {removed_item2.upper()} fly from your possession."
            elif len(healthandinv.inventory_list[0]) > 1:
                removed_item1 = healthandinv.inventory_list[0].pop(-1)
                roomslib.interactive_objects_list[6].append(removed_item1)
                output = output + f" your {removed_item1.upper()} flies from your possession."
        else:
            output = "The DRAGON leaps forward to beat you with the remnants of a shredded wing membrane."
            if len(healthandinv.inventory_list[0]) > 2:
                removed_item1 = healthandinv.inventory_list[0].pop(1)
                removed_item2 = healthandinv.inventory_list[0].pop(1)
                roomslib.interactive_objects_list[6].append(removed_item1)
                roomslib.interactive_objects_list[6].append(removed_item2)
                output = output + f" Your {removed_item1.upper()} and {removed_item2.upper()} are sent flying from" \
                                  f" your possession."
            elif len(healthandinv.inventory_list[0]) > 1:
                removed_item1 = healthandinv.inventory_list[0].pop(1)
                roomslib.interactive_objects_list[6].append(removed_item1)
                output = output + f"Your {removed_item1.upper()} is sent flying from your possession."

    elif random_attack_number >= 25:  # FIRE BREATH
        critical_hit = True
        if random_severity_number <= 1:
            output = "The DRAGON's steamy maw becomes a glowing, red furnace. It spews a torrent of fire, drowning" \
                     " you in an inferno and turning the chamber into a smouldering tomb."
        elif random_severity_number <= 3:
            output = "The living volcano coughs a devastating cone of fiery death. Pyroclastic clouds blast forth," \
                     " vapourising flesh and blackening bone."
        elif random_severity_number >= 4:
            output = "Thick, black smoke leaks from the DRAGON, followed by dripping, molten fluid. The DRAGON's" \
                     " throat is an engine of annihilation as it floods the room in a maelstrom of fire."
        damage = 18
        if "necklace" in healthandinv.inventory_list[0]:
            output = output + " Your little NECKLACE partially negates the brutal attack."
            damage //= 3

    return output, damage, critical_hit


def encounter_dragon():

    # PLAYER LOCATION CHANGE
    locatorlib.locator[3][3] = 0
    locatorlib.locator[0][0] = 12

    # APPENDING monster_health WITH COORDINATES
    monster_health[1].append("00")
    # FUTURE PROOFING ON THE OFF CHANCE THAT MORE MONSTERS EVER GET ADDED
    index = beasties_list[0].index("dragon")
    monster_health[0].append(beasties_list[2][index])


liberated_dragon = ["The dragon's neck bows to silently view its raw, newly unbound ankles. It raises its head again"
                    " to look at you", "After a moment, it turns away, delicately shifting its weight toward an"
                    " opening in the wall. It disappears into a blanket of darkness.", "You follow. Down placid paths"
                    " and up serene staircases. Through quiet caverns and tranquil tunnels. Finally, you come to a"
                    " door. Daylight seeps through the cracks in the wood.", "You step through, out into the light. In"
                    " the distance, you spot what could be the gentle reunion between two dragons.", "You feel the wind"
                    "on your face and the sun in your eyes. You escaped."]

killed_dragon = ["You go forth, carefully stepping around the body of the dragon, finding an opening in the wall.",
                 " You proceed down paths and up staircases. You cross caverns and traverse tunnels before coming to a"
                 " door. Daylight seeps through the cracks in the wood.", "You step through, out into the light. The"
                 " mournful rumblings of a giant dragon resonate throughout the mountains like thunder.",
                 "You feel the wind on your face and the sun in your eyes. You escaped."]

