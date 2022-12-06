locator = [
    [1, 1, 1, 1, 1],
    [1, 1, 7, 0, 1],
    [1, 1, 0, 1, 1],
    [1, 0, 0, 0, 1],
    [1, 1, 0, 0, 1],
    [1, 1, 0, 1, 1],
    [1, 1, 1, 1, 1]
]


def subtract_value(y, x, index):
    beasties_list = [
        ["skeleton", "slime", "imp", "dragon"],  # NAMES
        [2, 3, 4, 5],  # MAP VALUES
        [5, 4, 3, 18]  # HEALTH CONSTANTS
    ]
    locator[y][x] -= beasties_list[1][index]


def find_coordinates():
    # RETURNS PLAYER'S Y & X COORDINATES
    row, column = 0, 0
    for _ in locator:
        column = 0
        for _ in locator[row]:
            if 7 <= locator[row][column]:
                return row, column
            column += 1
        row += 1


def move_player(user_input):
    y, x = find_coordinates()

    wall_detection_message = "A wall obstructs your way. You could not go this direction. "

    # USER INPUT NORTH
    if "nor" in user_input or "1" in user_input:
        wall_detection = locator[y + 1][x] == 1
        if wall_detection or locator[3][3] >= 7:
            return wall_detection_message
        locator[y][x] -= 7
        locator[y + 1][x] += 7
        output = "You went NORTH. "

    # USER INPUT SOUTH
    elif "sou" in user_input or "3" in user_input:
        wall_detection = locator[y - 1][x] == 1
        if wall_detection or locator[4][3] >= 7:
            return wall_detection_message
        locator[y][x] -= 7
        locator[y - 1][x] += 7
        output = "You went SOUTH. "

    # USER INPUT EAST
    elif "eas" in user_input or "2" in user_input:
        wall_detection = locator[y][x - 1] == 1
        if wall_detection:
            return wall_detection_message
        locator[y][x] -= 7
        locator[y][x - 1] += 7
        output = "You went EAST. "

    # USER INPUT WEST
    elif "wes" in user_input or "4" in user_input:
        wall_detection = locator[y][x + 1] == 1
        if wall_detection:
            return wall_detection_message
        locator[y][x] -= 7
        locator[y][x + 1] += 7
        output = "You went WEST. "

    return output
