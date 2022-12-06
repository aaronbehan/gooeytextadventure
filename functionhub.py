from random import randint
import monsterlib
import locatorlib
import roomslib
import inventorylib
import healthandinv


def options_input(user_input):

    output = "This command was not recognised."

    if "opt" in user_input or "2" in user_input:
        output = "NOT PROGRAMMED YET"
        # FONT SIZE (WILL PROBABLY AUTO RESIZE TEXT WIDGET, ANNOYINGLY)
        # FONT COLOUR
        # TEXT TO SPEECH FOR VISUALLY IMPAIRED
        # REDUCE SPAWN MESSAGE, ATTACK MESSAGE TEXT,

    return output


def process_input(user_input):

    output = "This command was not recognised."

    # OBSERVE
    if "2" in user_input or "obs" in user_input:
        inventorylib.inventory_variable_reset()
        output = roomslib.observe()

    # STATUS
    elif "stat" in user_input or "4" in user_input:
        inventorylib.inventory_variable_reset()
        output = "health"  # KEYWORD TO TRIGGER FUNCTION IN guidisplay

    # GO (PRESENT DIRECTIONS)
    elif user_input == "go" or "fle" in user_input or "1" in user_input:
        inventorylib.inventory_variable_reset()
        output = "Which direction?"

    # GO (CHANGE LOCATOR VALUE)
    # FUTURE PROOFING NOTE: MAKE SURE THERE IS NEVER AN ITEM/OBJECT/MONSTER THAT INCLUDES ANY OF THOSE LETTERS TOGETHER
    elif "nor" in user_input or "eas" in user_input or "sou" in user_input or "wes" in user_input:
        inventorylib.inventory_variable_reset()
        if monsterlib.monster_specifier():
            if randint(0, 2) == 0:
                return f"You fail to escape the {monsterlib.monster_specifier().upper()} this time. " \
                       f"{monsterlib.monster_attack()}"
            else:
                return f"You successfully escape the {monsterlib.monster_specifier().upper()}. " \
                       f"{locatorlib.move_player(user_input)}"
        output = locatorlib.move_player(user_input)
        output = output + monsterlib.spawn()

    # BACKING OUT OF INVENTORY
    elif "undo" in user_input:
        inventorylib.inventory_variable_reset()
        output = "Undone. What would you like to do?"

    # VIEW INVENTORY
    elif "inv" in user_input or "3" in user_input:
        inventorylib.change_viewing_inventory_true()
        output = "inventory"  # KEYWORD TO TRIGGER FUNCTION IN guidisplay

    # AFFECT INVENTORY ITEM
    elif "use" in user_input or "desc" in user_input or inventorylib.desired_item_check(user_input) \
            or inventorylib.affected_object_check(user_input):
        inventorylib.change_viewing_inventory_true()
        output = inventorylib.interact_inventory(user_input)

    return output


def yes_or_no_process_input(user_input):

    if inventorylib.fish_yes_or_no:
        if "1" in user_input or "y" in user_input:
            output = "You look further down the fish's gullet. There is a parasitic CRUSTACEAN clinging to a remnant" \
                     " of flesh and bone. You put the CRUSTACEAN in your pocket. The fish carcass finally becomes" \
                     " limp and falls to pieces in your HANDS."
            healthandinv.add_to_inventory("crustacean", 1)
            healthandinv.remove_from_inventory("fish")
            inventorylib.inspected_fish()
        else:
            output = "You do not inspect the FISH."

    elif roomslib.bookcase_yes_or_no:
        if "1" in user_input or "y" in user_input:
            output = "You heave the bookcase out of the way, allowing you to look behind. It was blocking a" \
                     " hidden FIREPLACE."
            roomslib.interactive_objects_list[0].remove("bookcase")
            roomslib.interactive_objects_list[0].append("fireplace")
            roomslib.interactive_objects_list[0].append("herb")
            roomslib.inspected_bookcase()
        else:
            output = "You opt to leave the BOOKCASE where it is."

    elif roomslib.trapdoor_yes_or_no:
        if "1" in user_input or "y" in user_input:
            roomslib.inspected_trapdoor()
            line1 = "You summon the courage to enter, delving downwards towards the fires of hell."
            line2 = "After an eternity of battling the oppressive, choking heat, you come upon a door. The distinct" \
                    " sound of rattling chains can be heard from behind."
            line3 = "You push the door open and witness the epicentre of the infernal blaze. A chained, stunted DRAGON" \
                    " glares at you, struggling to rise under the weight of its thick, iron SHACKLES. It begins" \
                    " dragging its emaciated bulk towards you."
            output = [line1, line2, line3]  # AFTER THIS, THE DRAGON SPRITE SHOULD APPEAR
        else:
            output = "You shut the TRAPDOOR."

    else:
        output = "DEVELOPER ERROR. COULD NOT FIND YES/NO VARIABLE"

    return output


def open_book(user_input):  # THIS IS NOT FINISHED
    if "ske" in user_input:
        output = '"SKELETONS\nAll attempts to vanquish the skeletons from this place have been in vain. These dogged' \
                 ' beasts are able to identify vulnerability with astonishing frequency, while also possessing' \
                 ' infuriating durability.\nAs unlikely as it may sound, the skeletons are animated by a form of' \
                 ' sorcery that is foreign to my esteemed expertise. More research will certainly be needed."'
    elif "sli" in user_input:
        output = '"SLIMES\nSlimes inhabit a subcategory in between pests and pest killers. They are sluggish,' \
                 ' and have low attacking potential, but serve as a reservoir species for a particularly nasty,' \
                 ' little pathogen.\nWhile they may feel unthreatening now, I have to wonder whether my safety is so' \
                 ' certain as my faculties are incessantly eroded by age."'
    elif "imp" in user_input:
        output = '"IMPS\nTame, playful and curious folk - imps are ever-loyal friends and the servants to Sir Belial.' \
                 ' They perform miracles, partake in trade and bravely seek and reclaim the missing assets of the' \
                 ' Netherrealms.\nAlways remember: if an imp gives you their trident, that means nothing less than a' \
                 ' declaration of immortal friendship."'
    elif "-" in user_input:
        output = '"I cannot control the beast any longer. I\'m not ashamed to say it. Tomorrow will have been the' \
                 ' last time I ever venture down there."'
    elif "enf" in user_input:
        output = '"ENFEEBLEMENT\nThough I have never, and may never contract this contagion, my studies on live' \
                 ' specimens have nevertheless granted fascinating insights! Sufferers of \'Enfeeblement\' appear to' \
                 ' acquire a debilitating frailty. Any bodily harm they sustain appears to be inflicted twofold.' \
                 '\nCuring this affliction requires a herb. Belial help you if are without one."'
    elif "unde" in user_input:
        output = '"UNDEAD\n\'Sufferers\' of this disease, though appearing malnourished and weak, adopt an' \
                 ' extraordinary tolerance for physical trauma. Rats afflicted with Undead have been observed' \
                 ' surviving ingestion by slimes for several minutes, occasionally even managing to struggle their' \
                 ' way back outside.\nAcquisition of this affliction may be linked to a certain aquatic parasite.' \
                 ' More research is needed."'
    else:
        output = "You stop reading."

    return output


# THERE IS PROBABLY A MUCH BETTER WAY TO DO THIS
npc_dialogue = [
    ["meeting", "name_request", "receive_name", "introduction", "closing_remark"],  # FIRST INSTANCE OF DIALOGUE
    ["return", "yes/no", "given_lute", "gratitude", "grant_reward", "empty_handed2", "empty_handed"],  # SECOND
    ["herb3", "herb2", "herb1"]  # THIRD
    ]
player_name = ""


def speak_with_npc(user_input):
    global player_name

    # FIRST INSTANCE OF DIALOGUE
    if npc_dialogue[0][0] == "meeting":
        output = '"Ahhh, what a nostalgic scent."\nA high-pitched, raspy voice comes from behind the fabric.'
        npc_dialogue[0].remove("meeting")
        return output, "ENTER [↵]"
    elif npc_dialogue[0][0] == "name_request":
        output = '"Wingless one. Who might you be?"'
        npc_dialogue[0].remove("name_request")
        return output, "ENTER NAME?"
    elif npc_dialogue[0][0] == "receive_name":
        if len(user_input) < 1:
            output = '"Mmm. Forgotten your name? ... That\'s alright. Sometimes I forget mine, too."'
            player_name = "Wingless one"
        else:
            player_name = user_input[:25]  # PREVENTING USER FROM ENTERING TOO LARGE A USERNAME
            output = f'"{player_name}? ... Mmm. Strange name."'
        npc_dialogue[0].remove("receive_name")
        return output, "ENTER [↵]"
    elif npc_dialogue[0][0] == "introduction":
        output = f'"Well {player_name}, come and visit me some time. I collect things. You could trade with me.' \
                 f' Mmm, yes..."\n"Especially if you find something musical. Oh how I long to hear the music of my' \
                 f' people again."'
        npc_dialogue[0].remove("introduction")
        return output, "ENTER [↵]"
    elif npc_dialogue[0][0] == "closing_remark":
        output = "You step away as the high-pitched, raspy voice begins humming a song out of tune. He no longer" \
                 " acknowledges your presence."
        npc_dialogue[0].remove("closing_remark")
        npc_dialogue[0] = [None]

    # SECOND INSTANCE OF DIALOGUE
    elif npc_dialogue[1][0] == "return" and "lute" in healthandinv.inventory_list[0]:
        output = '"Oh what\'s that? You have found something musical?"\nGive LUTE?'
        npc_dialogue[1].remove("return")
        return output, "1. Yes\n2. No"
    elif npc_dialogue[1][0] == "yes/no" and "lute" in healthandinv.inventory_list[0]:
        if "1" in user_input or "y" in user_input:
            output = 'You slide the lute underneath the tent and it\'s quickly snatched away.\n' \
                     f'"Oh Belial be praised! Where oh where did you find this, {player_name}?"'
            healthandinv.remove_from_inventory("lute")
            npc_dialogue[1].remove("yes/no")
            return output, "ENTER [↵]"
        else:
            output = f'"Mmm. Please no disturbing me, {player_name}."'
            npc_dialogue[1].insert(0, "return")
    elif npc_dialogue[1][0] == "given_lute":
        output = "You hear the joyful and enthusiastic strumming of a muted, out-of-tune lute. The tune doesn't seem" \
                 " to follow any notion of music theory..."
        npc_dialogue[1].remove("given_lute")
        return output, "ENTER [↵]"
    elif npc_dialogue[1][0] == "gratitude":
        output = f'"Oh {player_name}. Thank you for this kindness. Allow me to offer recompense."\nYou hear the' \
                 ' clattering of curiosities as the strange creature presumably rummages through myriad possessions.'
        npc_dialogue[1].remove("gratitude")
        return output, "ENTER [↵]"
    elif npc_dialogue[1][0] == "grant_reward":
        output = f'A POT slides out from underneath the fabric.\n"Mmm. Please enjoy my pot, {player_name}. Come back' \
                 ' whenever you would like to trade."\nYou stuff the POT inside your pocket.'
        healthandinv.inventory_list[0].append("pot")
        npc_dialogue[1] = [None]
    elif npc_dialogue[1][0] == "return" and "lute" not in healthandinv.inventory_list[0]:
        output = '"Oh what\'s that? Have you found something musical?"'
        npc_dialogue[1].remove("return")
        return output, "ENTER [↵]"
    elif npc_dialogue[1][-1] == "empty_handed":
        output = '"No? ..."'
        npc_dialogue[1].remove("empty_handed")
        return output, "ENTER [↵]"
    elif npc_dialogue[1][-1] == "empty_handed2":
        output = f'"Mmm. Please no disturbing me, {player_name}."'
        npc_dialogue[1].append("empty_handed")
        npc_dialogue[1].insert(0, "return")

    # THIRD INSTANCE OF DIALOGUE
    elif healthandinv.player_health[0] < 5 and npc_dialogue[-1] == "herb1":
        output = f'"Oh dear, {player_name}. You\'re looking very delicate..."'
        npc_dialogue[2].remove("herb1")
        return output, "ENTER [↵]"
    elif healthandinv.player_health[0] < 5 and npc_dialogue[-1] == "herb2":
        output = f"You see the earthy roots and stalk of a plant creep from underneath the fabric.\nYou take it and" \
                 f" put it in your pocket. You obtained a HERB."
        healthandinv.inventory_list[1].append("herb")
        npc_dialogue[2].remove("herb2")
        return output, "ENTER [↵]"
    elif healthandinv.player_health[0] < 5 and npc_dialogue[-1] == "herb3":
        output = '"Mmm. Take that. Please try not to die."trade£'
        npc_dialogue[2].remove("herb3")
        return output, "ENTER [↵]"
    elif randint(0, 3) == 0:
        output = f'"What\'s that, {player_name}? Found something nice?"\nThe voice speaks from behind the fabric.trade£'
        return output, "TRADE / UNDO"
    elif randint(0, 3) == 1:
        output = f'"Mmm. Good to see you, {player_name}."\n"Do you have something for me?" the voice speaks.trade£'
        return output, "TRADE / UNDO"
    elif randint(0, 3) == 2:
        output = f'You can hear the happy strumming of a lute coming from behind the fabric.trade£'
        return output, "TRADE / UNDO"
    else:
        output = f'"What can I do for you today, my wingless friend" the voice speaks.trade£'
        return output, "TRADE / UNDO"

    return output, "1. GO\n2. OBSERVE\n3. INVENTORY\n4. STATUS"


def offered_item_check(user_input):  # UNTESTED
    offered_item = ""

    tradable_items = ["snack", "broom", "coin", "larva", "matchbox", "bird", "flute"]

    if user_input in tradable_items:
        if user_input in healthandinv.inventory_list[0] or user_input in healthandinv.inventory_list[1]:
            offered_item = user_input

    return offered_item


def trade(user_input):

    offered_item = offered_item_check(user_input)
    if not offered_item:
        return f"You do not have a '{user_input}' to trade.", None

    if offered_item == "broom":
        output = f'"Oh good, my broom. Thank you for bringing it back, {player_name}.' \
                 f' Allow me to reward you with this map I drew."'
    elif offered_item == "larva":
        output = f'"Oh {player_name}, who is this cutesie little impling?"\n"I must have him. But I have nothing of' \
                 f' equivalent value at the moment. Will you accept this?"'
    elif offered_item == "bird":
        output = f'"My, {player_name}, how did you catch this...? I will accept it for my charm."'
    elif offered_item == "flute":
        output = f'"{player_name}, where did you find this treasure?"\n"Please {player_name}, I must have this. ' \
                 f'I will give you my most precious item in return.'
    else:
        output = f'"Oh what a lovely {offered_item}. I take."'

    return output, offered_item


# MAP FUNCTION (RENAME ROOMS)
# GAS BURNER FUNCTION (USE WHICH ITEM TO CREATE WHICH POTION?)
