# imports

class AmongUs:

    def __init__(self, players):
        super().__init__()
        self.players = players
        pass

    def start_game(self):
        pass

    def end_game(self):
        pass

    def play_jester(self):
        pass

    def play_vanilla(self):
        pass

    # vision processing to associate colors to players
    def get_colors(self):
        pass

    # vision processing to determine what state the game is in
    def get_game_state(self):
        pass

    # vision processing to check who is dead
    def get_dead(self):
        pass

    # vision processing to see who voted for who
    def get_voted(self):
        pass

    # get frame from game
    def get_frame(self):
        pass