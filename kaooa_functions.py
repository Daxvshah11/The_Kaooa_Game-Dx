import pygame
import sys

# ALL GLOBALS
global WHITE, BLACK, GREY, BLUE, RED, LIGHT_GREY, LIGHT_PINK, LIGHT_BLUE
global screen, screen_width, screen_height
global font
global p1, p2, p3, p4, p5, p6, p7, p8, p9, p10
global allButtons
global turn
global kaooaAlertPrinted
global baazAlertPrinted
global kaooaPlayer, baazPlayer, theBoard


# defining colors
WHITE = (230, 230, 230)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
LIGHT_GREY = (200, 200, 200, 100)
LIGHT_PINK = (255, 200, 200)
LIGHT_BLUE = (200, 200, 255)


# class for KAOOA
class KAOOA:
    def __init__(self, playerName):
        self.playerName = playerName
        self.kaooasPlaced = 0
        self.totalKaoos = 7
        self.chosenKaooaToMove = -1

    def myTurn(self, button, buttonName):
        global turn
        global kaooaAlertPrinted

        # checking if all kaooas are placed
        if self.kaooasPlaced == self.totalKaoos:
            # checking if clicked on a LIGHT_BLUE button
            if button["color"] == LIGHT_BLUE:
                # updating board
                theBoard.boardState[self.chosenKaooaToMove] = "*"

                # making choseKaooaToMove to -1 and GREY
                allButtons[self.chosenKaooaToMove]["color"] = GREY
                self.chosenKaooaToMove = -1

                # making all other LIGHT_BLUE to GREY
                for value in list(allButtons.values()):
                    if value["color"] == LIGHT_BLUE:
                        value["color"] = GREY

                # updating board
                theBoard.boardState[
                    list(allButtons.keys())[list(allButtons.values()).index(button)]
                ] = "K"

                # making clicked button to BLUE
                button["color"] = BLUE

                # resetting kaooaAlertPrinted
                kaooaAlertPrinted = False

                # changing turn
                turn = False

            elif button["color"] == BLUE:
                # moving the kaooas
                self.KaooaMovePlaces(button, buttonName)
            else:
                # ALERT BOX
                alertBoxMessage("Please click on a Kaooa to move it!")

        else:
            # checking if already something placed or empty
            if button["color"] == GREY:
                # placing blue color for a Kaooa
                button["color"] = BLUE

                # updating board state
                theBoard.boardState[
                    list(allButtons.keys())[list(allButtons.values()).index(button)]
                ] = "K"

                # updating kaooas count
                kaooaPlayer.kaooasPlaced += 1

                # changing turn
                turn = False

                # updating kaooaAlertPrinted
                kaooaAlertPrinted = False

            elif button["color"] == BLUE:
                # ALERT BOX
                alertBoxMessage(
                    "A Kaooa is already placed here! Please choose another place."
                )
            elif button["color"] == RED:
                # ALERT BOX
                alertBoxMessage(
                    "A Baaz is already placed here! Please choose another place."
                )

    def KaooaMovePlaces(self, button, buttonName):
        # checking if already chosenKaooaToMove
        if self.chosenKaooaToMove != -1:
            # making previous all LIGHT_BLUE to GREY
            for value in list(allButtons.values()):
                if value["color"] == LIGHT_BLUE:
                    value["color"] = GREY

        # setting chosenKaooaToMove
        self.chosenKaooaToMove = buttonName

        # finding all possible places the current clicked Kaooa can move
        for possibleMove in theBoard.lineGraph[buttonName]:
            if theBoard.boardState[possibleMove[0]] == "*":
                allButtons[possibleMove[0]]["color"] = LIGHT_BLUE


"""




























"""


# class for BAAZ
class BAAZ:
    def __init__(self, playerName):
        self.playerName = playerName
        self.kaooasKilled = 0
        self.baazPlaced = False
        self.optionsGiven = False

    def myTurn(self, button, buttonName):
        global turn
        global baazAlertPrinted

        # checking if to move Baaz or to place it
        if self.baazPlaced:
            # calling algorithm to find places to move Baaz
            self.BaazMovePlaces(button, buttonName)

        else:
            # checking if already something placed or empty
            if button["color"] == GREY:
                # placing red color for a Baaz
                button["color"] = RED

                # updating board state
                theBoard.boardState[
                    list(allButtons.keys())[list(allButtons.values()).index(button)]
                ] = "B"

                # updating baaz placed
                self.baazPlaced = True

                # changing turn
                turn = True

                # updating baazAlertPrinted
                baazAlertPrinted = False

            elif button["color"] == BLUE:
                # ALERT BOX
                alertBoxMessage(
                    "A Kaooa is already placed here! Please choose another place."
                )
            elif button["color"] == RED:
                # ALERT BOX
                alertBoxMessage(
                    "A Baaz is already placed here! Please choose another place."
                )

    def BaazMovePlaces(self, button, buttonName):
        global turn
        global baazAlertPrinted

        # checking if options already shown
        if self.optionsGiven:
            # checking if button clicked is LIGHT_PINK
            if button["color"] == LIGHT_PINK:
                # moving the Baaz to that place

                # finding current position of Baaz
                buttonNameOfBaaz = None
                for key, value in allButtons.items():
                    if value["color"] == RED:
                        buttonNameOfBaaz = key
                        break

                # checking if any Kaooa is in between the current and the new place
                buttonNameInBetween = -1
                for possibleMove in theBoard.lineGraph[buttonNameOfBaaz]:
                    if possibleMove[1] == buttonName:
                        buttonNameInBetween = possibleMove[0]
                        break

                # Kaooa in between then kill it
                if buttonNameInBetween != -1:
                    allButtons[buttonNameInBetween]["color"] = GREY
                    theBoard.boardState[buttonNameInBetween] = "*"
                    self.kaooasKilled += 1

                # current position of Baaz to GREY
                for value in list(allButtons.values()):
                    if value["color"] == RED:
                        value["color"] = GREY
                        theBoard.boardState[
                            list(allButtons.keys())[
                                list(allButtons.values()).index(value)
                            ]
                        ] = "*"
                        break

                # new position of Baaz in board
                theBoard.boardState[buttonName] = "B"

                # new position of Baaz
                button["color"] = RED

                # resetting all other LIGHT_PINK to GREY
                for value in list(allButtons.values()):
                    if value["color"] == LIGHT_PINK:
                        value["color"] = GREY

                # resetting optionsGiven and optionsGivenList
                self.optionsGiven = False

                # resetting baazAlertPrinted
                baazAlertPrinted = False

                # changing turn
                turn = True

            else:
                alertBoxMessage(
                    "Please click on a valid place where Baaz can move (shown in Light Pink color)!"
                )

        else:
            # checking if clicked on a Baaz
            if button["color"] == RED:
                # finding all possible movements from current clicked button
                mustMoveFound = False
                for possibleMove in theBoard.lineGraph[buttonName]:
                    # checking if kaooa at any neighbouring place
                    if (
                        theBoard.boardState[possibleMove[0]] == "K"
                        and possibleMove[1] != -1
                        and theBoard.boardState[possibleMove[1]] == "*"
                    ):
                        # changing color of the button next to the neighbouring kaooa
                        allButtons[possibleMove[1]]["color"] = LIGHT_PINK
                        mustMoveFound = True

                # iterating again for normal possible moves
                if not mustMoveFound:
                    for possibleMove in theBoard.lineGraph[buttonName]:
                        # checking if empty
                        if theBoard.boardState[possibleMove[0]] == "*":
                            # changing color of the button
                            allButtons[possibleMove[0]]["color"] = LIGHT_PINK

                # updating optionsGiven
                self.optionsGiven = True

            else:
                # ALERT BOX
                alertBoxMessage("Please click on a Baaz to move it!")


"""





























"""


class BOARD:
    def __init__(self):
        # creating state of this board
        # "*" means empty, "K" means KAOOA, "B" means BAAZ
        self.boardState = {
            "p1": "*",
            "p2": "*",
            "p3": "*",
            "p4": "*",
            "p5": "*",
            "p6": "*",
            "p7": "*",
            "p8": "*",
            "p9": "*",
            "p10": "*",
        }

        # creating graph map for the board for straight line connections
        self.lineGraph = {
            "p1": [["p2", "p8"], ["p6", "p10"]],
            "p2": [["p1", -1], ["p6", "p5"], ["p7", -1], ["p8", "p3"]],
            "p3": [["p4", "p10"], ["p8", "p2"]],
            "p4": [["p3", -1], ["p8", "p7"], ["p9", -1], ["p10", "p5"]],
            "p5": [["p6", "p2"], ["p10", "p4"]],
            "p6": [["p1", -1], ["p2", "p7"], ["p5", -1], ["p10", "p9"]],
            "p7": [["p2", "p6"], ["p8", "p4"]],
            "p8": [["p2", "p1"], ["p3", -1], ["p4", "p9"], ["p7", -1]],
            "p9": [["p4", "p8"], ["p10", "p6"]],
            "p10": [["p4", "p3"], ["p5", -1], ["p6", "p1"], ["p9", -1]],
        }

    def isKaooaWinner(self):
        # finding buttonName of Baaz position
        buttonNameOfBaaz = None
        for key, value in allButtons.items():
            if value["color"] == RED:
                buttonNameOfBaaz = key
                break

        # checking if Baaz is blocked to move
        if buttonNameOfBaaz == None:
            return

        for possibleMove in self.lineGraph[buttonNameOfBaaz]:
            if theBoard.boardState[possibleMove[0]] == "*" or (
                theBoard.boardState[possibleMove[0]] == "K"
                and possibleMove[1] != -1
                and theBoard.boardState[possibleMove[1]] == "*"
            ):
                return

        # ALERT BOX
        alertBoxMessage(
            f"Congrats {kaooaPlayer.playerName}!!! You have won as the Kaooas!!!"
        )
        print(f"Congratulations {kaooaPlayer.playerName}! You won the game!")
        pygame.quit()
        sys.exit()

    def isBaazWinner(self):
        if baazPlayer.kaooasKilled == 4:
            # ALERT BOX
            alertBoxMessage(
                f"Congrats {baazPlayer.playerName}!!! You have won as the Baaz!!!"
            )
            print(f"Congratulations {baazPlayer.playerName}! You won the game!")
            pygame.quit()
            sys.exit()


"""





























"""


# defining function to display alert box
def alertBoxMessage(message):
    # blurring the background
    blur_surface = pygame.Surface((screen_width, screen_height))
    blur_surface.set_alpha(150)
    blur_surface.fill(WHITE)
    screen.blit(blur_surface, (0, 0))

    # redering text onto a surface
    text_surface = font.render(message, True, BLACK)
    text_rect = text_surface.get_rect(center=(screen_width // 2, screen_height // 2))

    # blitting text surface onto the screen
    screen.blit(text_surface, text_rect)
    pygame.display.flip()

    # waiting for 2 secs
    pygame.time.wait(2000)


"""
































"""


# defining function for making a star
def makeStar():
    global screen, screen_width, screen_height
    global font
    global p1, p2, p3, p4, p5, p6, p7, p8, p9, p10
    global allButtons

    # initializing pygame
    pygame.init()

    # setting up the display (globally)
    screen_width = 1920
    screen_height = 1080
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("THE KAOOA GAME")

    # setting FONT
    font = pygame.font.SysFont("Arial", 48, italic=True)

    # defining coordinates for the star
    center_x = screen_width // 2
    center_y = screen_height // 2
    star_scale = 1
    p1 = (center_x - int(340.34 * star_scale), center_y - int(170.17 * star_scale))
    p2 = (center_x - int(80.34 * star_scale), center_y - int(170.17 * star_scale))
    p3 = (center_x + int(340.34 * star_scale), center_y - int(170.17 * star_scale))
    p4 = (center_x + int(130.00 * star_scale), center_y - int(17.35 * star_scale))
    p5 = (center_x - int(210.34 * star_scale), center_y + int(229.93 * star_scale))
    p6 = (center_x - int(130.00 * star_scale), center_y - int(17.35 * star_scale))
    p7 = (center_x - int(0.00 * star_scale), center_y - int(417.45 * star_scale))
    p8 = (center_x + int(80.34 * star_scale), center_y - int(170.17 * star_scale))
    p9 = (center_x + int(210.34 * star_scale), center_y + int(229.93 * star_scale))
    p10 = (center_x + int(0.00 * star_scale), center_y + int(77.10 * star_scale))

    # creating allButtons dictionary to store button objects (globally again)
    allButtons = {
        "p1": {"center": p1, "radius": 30, "color": GREY, "clicked": False},
        "p2": {"center": p2, "radius": 30, "color": GREY, "clicked": False},
        "p3": {"center": p3, "radius": 30, "color": GREY, "clicked": False},
        "p4": {"center": p4, "radius": 30, "color": GREY, "clicked": False},
        "p5": {"center": p5, "radius": 30, "color": GREY, "clicked": False},
        "p6": {"center": p6, "radius": 30, "color": GREY, "clicked": False},
        "p7": {"center": p7, "radius": 30, "color": GREY, "clicked": False},
        "p8": {"center": p8, "radius": 30, "color": GREY, "clicked": False},
        "p9": {"center": p9, "radius": 30, "color": GREY, "clicked": False},
        "p10": {"center": p10, "radius": 30, "color": GREY, "clicked": False},
    }


"""





























"""


def THE_GAME():
    # initializing objects
    global kaooaPlayer, baazPlayer, theBoard
    global turn
    global kaooaAlertPrinted, baazAlertPrinted

    # taking player name inputs
    print()
    kaooaPlayer = KAOOA(input("Enter kaooa player name : "))
    baazPlayer = BAAZ(input("Enter baaz player name : "))
    theBoard = BOARD()
    print()

    # setting current first turn
    turn = True

    # flags
    kaooaAlertPrinted = False
    baazAlertPrinted = False

    # MAIN GAME LOOP
    while True:
        # filling the screen with color
        screen.fill(WHITE)

        # drawing all the lines
        pygame.draw.line(screen, BLACK, p1, p2, 5)
        pygame.draw.line(screen, BLACK, p1, p6, 5)
        pygame.draw.line(screen, BLACK, p7, p2, 5)
        pygame.draw.line(screen, BLACK, p7, p8, 5)
        pygame.draw.line(screen, BLACK, p3, p8, 5)
        pygame.draw.line(screen, BLACK, p3, p4, 5)
        pygame.draw.line(screen, BLACK, p9, p4, 5)
        pygame.draw.line(screen, BLACK, p9, p10, 5)
        pygame.draw.line(screen, BLACK, p5, p10, 5)
        pygame.draw.line(screen, BLACK, p5, p6, 5)
        pygame.draw.line(screen, BLACK, p2, p6, 5)
        pygame.draw.line(screen, BLACK, p2, p8, 5)
        pygame.draw.line(screen, BLACK, p4, p8, 5)
        pygame.draw.line(screen, BLACK, p4, p10, 5)
        pygame.draw.line(screen, BLACK, p10, p6, 5)

        # drawing all the buttons
        for button in allButtons.values():
            pygame.draw.circle(
                screen, button["color"], button["center"], button["radius"]
            )

        # updating the display
        pygame.display.flip()

        # checking whose turn
        if turn:
            # KAOOA'S turn

            # ALERT BOX
            if not kaooaAlertPrinted:
                alertBoxMessage(
                    f"Kaooa's turn! {kaooaPlayer.kaooasPlaced} kaooas placed! {baazPlayer.kaooasKilled} kaooas killed!"
                )
                kaooaAlertPrinted = True

            # checking what event has happened
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("Sorry! The game was abruptly stopped. See you next time!")
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # checking if left Mouse button was clicked
                    if event.button == 1:
                        # getting which button was clicked
                        for button in allButtons.values():
                            if (
                                pygame.math.Vector2(event.pos).distance_to(
                                    button["center"]
                                )
                                <= button["radius"]
                            ):
                                # getting button's name
                                buttonName = list(allButtons.keys())[
                                    list(allButtons.values()).index(button)
                                ]
                                kaooaPlayer.myTurn(button, buttonName)
                                break

                        # checking if Kaooa is winner
                        theBoard.isKaooaWinner()

        else:
            # BAAZ'S turn

            # ALERT BOX
            if not baazAlertPrinted:
                alertBoxMessage(
                    f"Baaz's turn! {baazPlayer.kaooasKilled} kaooas are killed!"
                )
                baazAlertPrinted = True

            # checking what event has happened
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("Sorry! The game was abruptly stopped. See you next time!")
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # checking if left Mouse button was clicked
                    if event.button == 1:
                        # getting which button was clicked
                        for button in allButtons.values():
                            if (
                                pygame.math.Vector2(event.pos).distance_to(
                                    button["center"]
                                )
                                <= button["radius"]
                            ):
                                buttonName = list(allButtons.keys())[
                                    list(allButtons.values()).index(button)
                                ]
                                baazPlayer.myTurn(button, buttonName)
                                break

                        # checking if Baaz is winner
                        theBoard.isBaazWinner()
