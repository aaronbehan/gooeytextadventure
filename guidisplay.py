from tkinter import *
from PIL import ImageTk
import functionhub
import locatorlib
import inventorylib
import healthandinv
import monsterlib
import roomslib

# TO DO:
# IMPROVE BOOK READING SO THAT MENU DOESN'T GO AWAY. MUST BE CLEAR HOW TO EXIT
# AMEND THE DISPARITY BETWEEN USERS TYPING "HAND" VERSUS "HANDS"
# ALL INPUT SHOULD NOT BE CONVERTED TO LOWERCASE WHEN TYPING IN YOUR NAME

# DEFINING WINDOW CHARACTERISTICS
root = Tk()
root.title("Gooey Text Adventure")
root.iconbitmap('image assets/gooeyicon.ico')
width = "720"
height = "522"
root.geometry(f"{width}x{height}")
root.resizable(width=False, height=False)  # UNCOMMENT THIS ONCE FINISHED


def inventory_display():

    inventory = healthandinv.inventory_list

    if len(inventory[0]) > len(inventory[1]):
        repetitions = len(inventory[0])
    else:
        repetitions = len(inventory[1])

    number_of_spaces = 22
    index = 0
    numerical_constant = 1
    numerical_consumable = 1

    # INSERT ITEMS ONTO SCREEN
    for _ in range(repetitions):
        if index == 9:
            number_of_spaces = 21
        # ENSURING THE RIGHT AMOUNT OF BLANK SPACE IS FOLLOWING CONSTANT ITEMS
        try:
            put_spaces = number_of_spaces - len(inventory[0][index])
        except IndexError:
            # TO COMPENSATE FOR THE SPACE THE NUMBERS TAKE UP BEFORE ITEMS
            number_of_spaces += 3

        # PRINTING CONSTANT ITEMS (FROM INVENTORY[0])
        try:
            text_window.insert(END, f"\n{numerical_constant}. {inventory[0][index].capitalize()}{' ' * put_spaces}")
            numerical_constant += 1
        except IndexError:
            text_window.insert(END, f"\n{' ' * number_of_spaces}")

        # PRINTING CONSUMABLE ITEMS (FROM INVENTORY[1])
        try:
            text_window.insert(END, f"{numerical_consumable + len(healthandinv.inventory_list[0])}. "
                                    f"{inventory[1][index].capitalize()} (Consumable)")
        except IndexError:
            pass
        numerical_consumable += 1
        index += 1


def display_tradable_items():
    tradable_items = ["snack", "broom", "coin", "larva", "matchbox", "bird", "flute"]

    text_window.insert(END, "\nYour tradable items:")
    for item in healthandinv.inventory_list[1]:
        if item in tradable_items:
            text_window.insert(END, f"\n{item.capitalize()}")
    for item in healthandinv.inventory_list[0]:
        if item in tradable_items:
            text_window.insert(END, f"\n{item.capitalize()}")


def health_display():
    text_window.insert(END, f"\nHealth: {healthandinv.player_health[0]}")
    if healthandinv.player_health[0] > 14:
        text_window.insert(END, " (MAX)")

    if len(healthandinv.contracted_diseases) > 0:
        for index, affliction in enumerate(healthandinv.contracted_diseases):
            if index == 0:
                text_window.insert(END, f"\nAffliction(s): {affliction.capitalize()}")
            else:
                text_window.insert(END, f"\n               {affliction.capitalize()}")
    else:
        text_window.insert(END, f"\nAffliction(s): None")


# FOR SLOWLY PRINTING OUT A DIGESTIBLE SEQUENCE OF PARAGRAPHS
list_of_strings = []


def await_user_confirmation():
    global list_of_strings

    output = list_of_strings[0]
    list_of_strings.remove(list_of_strings[0])
    return output


def update_player_display():
    global player_image
    global player_label
    global player_display_window

    player_image = PhotoImage(file="image assets/avatar/avatar regular.png")

    if not healthandinv.alive():  # USER'S HEALTH FULLY DEPLETED
        player_image = PhotoImage(file="image assets/avatar/avatar dead.png")
    elif "helmet" in healthandinv.inventory_list[0]:
        player_image = PhotoImage(file="image assets/avatar/avatar bucket.png")
    elif "undead" in healthandinv.contracted_diseases:
        player_image = PhotoImage(file="image assets/avatar/avatar undead.png")
    elif "monocle" in healthandinv.inventory_list[0]:
        player_image = PhotoImage(file="image assets/avatar/avatar monocle.png")

    player_label = Label(bd=0, image=player_image)
    player_display_window = canvas.create_window(333, 423, window=player_label)


def update_monster_display(output):

    global monster_image_png
    global monster_label
    global monster_display_window

    monster = monsterlib.monster_specifier()
    monster_image_png = PhotoImage(file=f"image assets/monsters/{monster}_regular.png")

    if "dead_code" in output or "crit_code" in output:
        image_title = output[-13:]  # RESPECTIVE CODE (dead/crit) SHOULD ALWAYS COME AT THE END OF THE RETURNED OUTPUT
        output = output[:-13]
        monster_image_png = PhotoImage(file=f"image assets/monsters/{image_title}.png")
    elif isinstance(output, list):  # UNLIKELY BUT NOT IMPOSSIBLE THAT OUTPUT WILL BE A LIST
        if "dead_code" in output or "crit_code" in output[-1]:
            image_title = output[-13:]
            output = output[:-13]
            monster_image_png = PhotoImage(file=f"image assets/monsters/{image_title}.png")

    monster_label = Label(bd=0, image=monster_image_png)
    monster_display_window = canvas.create_window(554, 411, window=monster_label)

    return output


start_menu = True
yes_or_no = False
direction_prompt = False
reading_book = False
npc_dialogue = False
trading = False
dead = False


def false_booleans():
    global yes_or_no
    global direction_prompt
    global reading_book
    global npc_dialogue
    global trading
    global dead

    yes_or_no = False
    direction_prompt = False
    reading_book = False
    npc_dialogue = False
    trading = False
    dead = False


def update_numbered_menu():
    if npc_dialogue:
        return

    numbered_menu.delete("1.0", "end")
    if dead:
        numbered_menu.insert(INSERT, "Press ENTER to return to menu")
    elif inventorylib.viewing_inventory:
        numbered_menu.insert(INSERT, "USE / DESCRIBE / UNDO")
    elif list_of_strings or monsterlib.defeated_dragon:
        numbered_menu.insert(INSERT, "ENTER [↵]")
    elif yes_or_no:
        numbered_menu.insert(INSERT, "1. YES\n2. NO")
    elif direction_prompt:
        numbered_menu.insert(INSERT, "1. NORTH   3. SOUTH\n2. EAST    4. WEST\n\n           5. UNDO")
    elif monsterlib.monster_specifier():
        numbered_menu.insert(INSERT, "1. FLEE\n2. OBSERVE\n3. INVENTORY\n4. STATUS")
    else:
        numbered_menu.insert(INSERT, "1. GO\n2. OBSERVE\n3. INVENTORY\n4. STATUS")


npc_is_offering = ""
npc_line_of_dialogue = ""
user_offered_item = ""


def trading_process_input(user_input):
    global npc_is_offering
    global npc_line_of_dialogue
    global user_offered_item

    if user_input == "undo":
        false_booleans()
        numbered_menu.delete("1.0", "end")
        numbered_menu.insert(INSERT, "1. GO\n2. OBSERVE\n3. INVENTORY\n4. STATUS")
        text_window.insert(END, "\n" + f"Undone. What would you like to do?")
        text_window.see(END)
        return

    trading_table = [
        ["snack", "broom", "coin", "larva", "matchbox", "bird", "flute"],
        ["herb", "map", "potion", "iou", "potion", "charm", "pitchfork"]
    ]

    if not npc_line_of_dialogue and not npc_is_offering:

        output, user_offered_item = functionhub.trade(user_input)
        if user_offered_item is None:  # USER DID NOT TYPE IN AN ITEM THAT THEY POSSESS
            numbered_menu.delete("1.0", "end")
            numbered_menu.insert(INSERT, "SELECT ITEM TO TRADE / UNDO")
            if len(user_input) > 0:
                text_window.insert(END, "\n" + f"You do not possess a {user_input} to trade.")
            else:
                text_window.insert(END, "\n" + f"Enter the name of an item you wish to trade or type UNDO to go back.")
            display_tradable_items()
        else:  # USER TYPED IN AN ITEM THAT THEY POSSESS
            npc_line_of_dialogue = output
            numbered_menu.delete("1.0", "end")
            numbered_menu.insert(INSERT, "ENTER[↵]")
            text_window.insert(END, "\n" + f"You tuck your {user_offered_item.upper()} under the fabric for the "
                                           f"mysterious voice to inspect.")

    elif npc_is_offering:
        if "yes" in user_input or "1" in user_input:
            text_window.insert(END, "\n" + f"You trade your {user_offered_item.upper()} for"
                                           f" the {npc_is_offering.upper()}")
            healthandinv.append_traded_item(npc_is_offering)
            healthandinv.remove_from_inventory(user_offered_item)
        else:
            text_window.insert(END, "\n" + "You opt not to trade.")
        display_tradable_items()
        npc_is_offering = ""
        npc_line_of_dialogue = ""
        user_offered_item = ""
        numbered_menu.delete("1.0", "end")
        numbered_menu.insert(INSERT, "SELECT ITEM TO TRADE / UNDO")

    elif npc_line_of_dialogue:
        # DETERMINING WHAT NPC WILL OFFER IN RETURN
        index = trading_table[0].index(user_offered_item)
        npc_is_offering = trading_table[1][index]
        # UPDATING TEXT WINDOW
        text_window.insert(END, "\n" + npc_line_of_dialogue)
        text_window.insert(END, "\n" + f"Trade your {user_offered_item.upper()} for a {npc_is_offering.upper()}?")
        numbered_menu.delete("1.0", "end")
        numbered_menu.insert(INSERT, "1. YES\n2. NO")

    text_window.see(END)


def receive_input(event):

    global start_menu
    global yes_or_no
    global list_of_strings
    global direction_prompt
    global reading_book
    global npc_dialogue
    global trading
    global dead
    global map_image

    original_user_input = user_input_gui.get()
    user_input_gui.delete(0, "end")
    user_input = original_user_input.lower().strip()

    # UPDATE MAIN TEXT WINDOW
    text_window.tag_config("echo_input", foreground="green")
    text_window.insert(END, "\n>" + original_user_input, "echo_input")

    if not start_menu:

        if not list_of_strings and monsterlib.defeated_dragon:  # BEATEN FINAL BOSS AND READ ENDING TEXT
            reset_all_variables()
            return

        # CHECKING HOW TO PROCESS user_input
        if dead:
            second_life_check()
            return
        elif trading:  # USER IS TRADING WITH NPC
            trading_process_input(user_input)
            return
        elif npc_dialogue:  # USER IS SPEAKING TO THE NPC
            output, numbered_menu_output = functionhub.speak_with_npc(user_input)
            if "trade£" in output:
                output = output[:-6]
                trading = True
            text_window.insert(END, "\n" + output)
            if trading:
                display_tradable_items()
            text_window.see(END)
            numbered_menu.delete("1.0", "end")
            numbered_menu.insert(INSERT, numbered_menu_output)
            if numbered_menu_output == "1. GO\n2. OBSERVE\n3. INVENTORY\n4. STATUS":
                false_booleans()
            return
        elif list_of_strings:  # LOTS OF TEXT HAS BEEN RETURNED AND WILL GRADUALLY FED INTO THE text_window
            output = await_user_confirmation()
            if output[:22] == "You push the door open":
                monsterlib.encounter_dragon()
        elif yes_or_no:  # USER IS BEING ASKED A YES OR NO QUESTION
            output = functionhub.yes_or_no_process_input(user_input)
        elif reading_book:  # USER HAS OPENED BOOK
            output = functionhub.open_book(user_input)
            if output == "You stop reading.":
                false_booleans()
            text_window.insert(END, "\n" + output)
            text_window.see(END)
            return
        else:  # PROCESS INPUT NORMALLY
            output = functionhub.process_input(user_input)

        update_player_display()
        output = update_monster_display(output)

        if output == "inventory":
            inventory_display()
            false_booleans()
        elif output == "health":
            health_display()
            false_booleans()
        elif output == "Which direction?":  # PRESENTING USER WITH DIRECTIONAL OPTIONS
            text_window.insert(END, "\n" + output)
            false_booleans()
            direction_prompt = True
        elif "display_map" in output:  # PLAYER USES MAP
            output = output[11:]
            text_window.insert(END, '\n')
            map_image = PhotoImage(file="image assets/map.png")
            text_window.image_create(END, image=map_image)
            if output:
                text_window.insert(END, '\n' + output)
        elif "yes/no" in output:  # PROMPTING USER TO MAKE YES/NO DECISION
            output = output[:-6]
            false_booleans()
            yes_or_no = True
            text_window.insert(END, "\n" + output)
        elif "npc_dialogue" in output:  # USER IS SPEAKING TO NPC
            output = output[12:]
            false_booleans()
            npc_dialogue = True
            text_window.insert(END, '\n' + output)
            numbered_menu.delete("1.0", "end")
            numbered_menu.insert(INSERT, "ENTER [↵]")
        elif "read_book" in output:  # USER HAS CHOSEN TO READ BOOK
            output = output[9:]
            false_booleans()
            reading_book = True
            text_window.insert(END, "\n" + output)
        elif isinstance(output, list):  # LIST RECEIVED
            list_of_strings = output
            false_booleans()
            text_window.insert(END, "\n" + list_of_strings[0])
            list_of_strings.remove(list_of_strings[0])
            # THE NEXT INSTANCE OF USER INPUT GOES TO THE ELSE STATEMENT
        else:
            text_window.insert(END, "\n" + output)
            false_booleans()

        if not healthandinv.alive():  # USER'S HEALTH FULLY DEPLETED
            dead = True
            text_window.insert(INSERT, "\n" + "You died.")
        if monsterlib.defeated_dragon and not list_of_strings:  # USER HAS JUST KILLED DRAGON
            if roomslib.shackles_health < 1:
                list_of_strings = monsterlib.liberated_dragon
            else:
                list_of_strings = monsterlib.killed_dragon

        update_numbered_menu()

    else:

        if "sta" in user_input or "1" in user_input:
            # UPDATING TEXT BOXES
            update_numbered_menu()
            text_window.insert(END, "\n" + "You wake up on a stone floor.")
            update_player_display()
            start_menu = False
        elif "opt" in user_input or "2" in user_input:
            output = functionhub.options_input(user_input)
            text_window.insert(END, "\n" + output)
        else:
            text_window.insert(END, "\n" + "This command was not recognised.")

    text_window.see(END)


# DEFINING BACKGROUND
background = ImageTk.PhotoImage(file="image assets/background.png")

# DEFINING CANVAS
canvas = Canvas(root, width=width, height=height)
canvas.pack(expand=True, fill=BOTH)
canvas.create_image(0, 0, image=background, anchor="nw")

# DEFINING USER ENTRY
user_input_gui = Entry(root, bg="#464646", width=67, bd=0, font="Terminal 22", fg="white")
user_input_gui.bind('<Return>', receive_input)
user_input_gui.pack(side="bottom")
user_input_gui.focus_set()
user_input_gui.grab_set()

# DEFINING MAIN TEXT DISPLAY
main_frame = Frame(root)
text_window = Text(main_frame, bg="#464646", width=51, height=13, bd=0, font="Terminal 22", fg="white", wrap=WORD)
text_window.insert(INSERT, "\n\n\n\n\n\n\n\n\n\n")
title_image = PhotoImage(file="image assets/title screen.png")
map_image = PhotoImage(file="image assets/map.png")
text_window.image_create(END, image=title_image)
text_window.pack()

# DEFINING NUMBERED MENU TEXT DISPLAY
numbered_menu = Text(root, bg="#464646", width=22, height=4, bd=0, font="Terminal 20", fg="white")
numbered_menu.insert(INSERT, "1. START\n2. OPTIONS")
numbered_menu.pack()

# DEFINING PLAYER DISPLAY
player_image = PhotoImage(file="image assets/avatar/door.png")
player_label = Label(bd=0, image=player_image)

# DEFINING MONSTER DISPLAY
monster_image_png = PhotoImage(file="image assets/monsters/_regular.png")
monster_label = Label(bd=0, image=monster_image_png)

# CREATE WINDOWS
entry_window = canvas.create_window(367, 513, anchor="s", window=user_input_gui)
main_frame_window = canvas.create_window(282, 174, window=main_frame)
numbered_menu_window = canvas.create_window(135, 424, window=numbered_menu)
player_display_window = canvas.create_window(333, 423, window=player_label)
monster_display_window = canvas.create_window(554, 411, window=monster_label)


def second_life_check():
    if "iou" not in healthandinv.player_health:
        reset_all_variables()
    else:
        text_window.insert(INSERT, "\n" + "A new body is painstakingly assembled in the void. Your replacement vessel"
                                          " independently crawls out of an interdimensional rift and your consciousness"
                                          " awakens inside it. You hear a familiar voice echo to you through space and"
                                          " time.")
        text_window.see(END)
        list_of_strings.append(f'"Mmm. Our deal is now fulfilled, {functionhub.player_name}. I hope this suffices."')
        healthandinv.player_health.remove("iou")
        healthandinv.player_health[0] = 1
        healthandinv.contracted_diseases = []
        false_booleans()  # NOT CONSIDERED POSSIBLE REPERCUSSIONS OF THIS CHOICE. TEST!


def reset_all_variables():
    global start_menu
    global player_image
    global player_label
    global player_display_window
    global monster_image_png
    global monster_label
    global monster_display_window

    false_booleans()
    start_menu = True
    monsterlib.defeated_dragon = False

    # RESETTING NUMBERED MENU AND TEXT WINDOW
    numbered_menu.delete("1.0", "end")
    numbered_menu.insert(INSERT, "1. START\n2. OPTIONS\n3. CREDITS")
    text_window.insert(INSERT, "\n")
    text_window.image_create(END, image=title_image)
    text_window.see(END)
    # RESETTING AVATAR IMAGE
    player_image = PhotoImage(file="image assets/avatar/door.png")
    player_label = Label(bd=0, image=player_image)
    player_display_window = canvas.create_window(333, 423, window=player_label)
    # RESETTING MONSTER IMAGE
    monster_image_png = PhotoImage(file=f"image assets/monsters/_regular.png")
    monster_label = Label(bd=0, image=monster_image_png)
    monster_display_window = canvas.create_window(554, 411, window=monster_label)

    # MONSTERLIB VARIABLES RESET
    monsterlib.monster_health = [
        [100],
        ['64']
    ]
    monsterlib.monster_ferocity_count = 0
    monsterlib.coin_loot_obtained = False
    monsterlib.imp_inventory = []
    # LOCATORLIB VARIABLES RESET
    locatorlib.locator = [
        [1, 1, 1, 1, 1],
        [1, 1, 7, 0, 1],
        [1, 1, 0, 1, 1],
        [1, 0, 0, 0, 1],
        [1, 1, 0, 0, 1],
        [1, 1, 0, 1, 1],
        [1, 1, 1, 1, 1]
    ]
    # ROOMSLIB VARIABLES RESET
    roomslib.interactive_objects_list = [
        ["bookcase", "desk", "nest", "nest (aggressive)", "book", "bucket", "slingshot", "larva"],
        ["broom", "bell"],
        ["trapdoor", "trapdoor (locked)", "ladder", "ladder (broken)", "spade", "kindling", "lock"],
        ["herb", "soil", "soil (undisturbed)", "well", "well (unfilled)", "water", "rung", "bird", "fish"],
        ["burner", "spider", "item", "matchbox"],
        ["mushroom"],
        ["shackles"]
    ]
    roomslib.pot = [None]
    roomslib.shackles_health = [20]
    # INVENTORYLIB VARIABLES RESET
    inventorylib.viewing_inventory = False
    inventorylib.verb = ""
    inventorylib.desired_item = ""
    inventorylib.affected_object = ""
    # HEALTHANDINV VARIABLES RESET
    healthandinv.player_health = [10]
    healthandinv.contracted_diseases = []
    healthandinv.inventory_list = [
        ["hands"],  # CONSTANTS
        ["snack"]]  # CONSUMABLES
    # FUNCTIONHUB VARIABLES RESET
    functionhub.npc_dialogue = [
        ["meeting", "name_request", "receive_name", "introduction", "closing_remark"],
        ["return", "yes/no", "given_lute", "gratitude", "grant_reward", "empty_handed2", "empty_handed"],
        ["herb3", "herb2", "herb1"]
    ]
    functionhub.player_name = ""


root.mainloop()
