from PIL import Image, ImageGrab, ImageOps, PyAccess
import cv2
# https://pillow.readthedocs.io/en/stable/reference/Image.html


# vision processing to determine what state the game is in
# returns 1 if talking, 0 if silent, 2 for game end
def get_game_state(frame):
    if frame == 2:
        return 1
    return 0


# get frame from game
def get_frame():
    screen = ImageGrab.grab()


class AmongUs:

    def __init__(self, players):
        super().__init__()
        self.players = {}
        self.running = False

        for player in players:
            self.players.update({player: True})

    # game setup
    def start_game(self):
        self.running = True
        self.get_colors()

    def end_game(self):
        self.running = False

    def play(self):
        self.start_game()
        last_state = 0

        while self.running:
            frame = get_frame()
            state = get_game_state(frame)

            if last_state != state and state == 1:
                # TODO: un-mute alive players
                pass
            elif last_state != state and state == 0:
                # TODO: mute all players
                pass
            elif state == 2:
                self.end_game()

    # vision processing to associate colors to players
    def get_colors(self):
        pass

    # vision processing to check who is dead
    # returns list of players' discord ids
    def get_dead(self, frame):
        pass
