import numpy as np

# No players allowed in the game
allowed_players = (4, 6, 8)


class GameSession:
    """
    This class creates a game session with a fixed number of players.
    It also maintains score, allows access general game settings.

    Attributes:
        no_players (int) - Number of players in the game session
        players (Player) - List containing instances of the player object
        user_players (string) - List containing the ID of the players
                                controlled by the user
        start_player (string) - player who will start the next round
        round_outcomes (tuple) - A list of tuples containing
                                the outcome of each round
    """
    # Total cards
    total_cards = 24
    # No players allowed in the game
    allowed_players = (4, 6, 8)
    # Point associated with each card key
    point_table = {"J": 3, "9": 2, "A": 1, "10": 1, "K": 0, "Q": 0}
    # Heirarchy of card keys in a suit
    heirarchy_table = {"J": 5, "9": 4, "A": 3, "10": 2, "K": 1, "Q": 0}
    suits = {"Spade": 0, "Heart": 1, "Clubs": 2, "Diamond": 3}
    # Base bet for the corresponding game
    base_bet = {2: 12, 3: 12, 4: 15, 6: 15, 8: 15}

    # Variables to retrieve value from index
    suits_map = ("Spade", "Heart", "Clubs", "Diamond")
    key_map = ("Q", "K", "10", "A", "9", "J")

    def __init__(self, no_players, teams=None):
        """
        Constructor for the game_session class

        Parameters:
            no_players (int) - number of players in the game
        """
        assert no_players in self.allowed_players, "Invalid number of players"
        assert teams is None or len(teams) == 2, "Invalid teams input"
        self.no_players = no_players
        self.players = []
        self.start_player = None
        self.no_rounds = 0
        self.rounds = []
        self.score = [None, 0]
        self.plr_dict = {}
        if teams is None:
            self.teams = (('Red', 'Red'), ('Blue', 'Blue'))
        else:
            self.teams = teams

        for i in range(self.no_players):
            # Create the player objects
            self.players.append(Player(chr(ord('A') + i), self.teams[i % 2]))
            self.plr_dict[chr(ord('A') + i)] = i

    def set_user_player(self, is_user):
        """
        set the players controlled by the user
        Parameters:
            is_user - list of booleans indicating user
                      user control for each player
        """
        assert len(is_user) == self.no_players,\
            "Argument length does not match with the player count"
        for i, player in enumerate(self.players):
            if is_user[i]:
                player.user_control = True

    def start_round(self):
        """
        Start a round of the game.
        Also returns an instance of the class Round.
        """
        self.rounds.append(Round(self))
        return self.rounds[-1]

    def get_start_player(self):
        """
        Returns the start player for the next/current round
        """
        if self.start_player is None:
            return None
        else:
            return self.players[self.start_player].ID

    def set_start_player(self, ID):
        """
        Sets the start player for the next/current round
        """
        self.start_player = self.plr_dict[ID]


class Round:
    """
    This class starts a round of the game

    Attributes:
    game (game_session) - game session in which the round is started
    wager (int) - target wager set for the session
    open_goat (bool) - has the player called for an open goat
    """
    def __init__(self, game):
        """
        Constructor for the class round

        Parameters:
        game (game_session) - game session in which the round is started
        """
        self.session = game
        self.wager = self.session.base_bet[self.session.no_players]
        self.open_goat = False
        self.wager_player = self.session.start_player
        self.deal_cards()

    def deal_cards(self):
        """
            Deal cards to the players in the game
        """
        values = np.arange(24)
        np.random.shuffle(values)
        i = 0
        # Shuffle and deal cards to all the players
        while i < 24:
            for player in self.session.players:
                player.add_card((
                                 self.session.suits_map[values[i] // 6],
                                 self.session.key_map[values[i] % 6]))
                i = i + 1

    def update_wager(self, Player_ID, wager):
        """
        Updates the new wager
        """
        self.wager_player = self.session.plr_dict[Player_ID]
        if wager == "Open Goat":
            self.wager = 28
            self.open_goat = True
        else:
            self.wager = wager

    def get_wager_data(self):
        """
        Return the current wager data
        """
        plr = self.session.players[self.wager_player]
        if self.open_goat:
            return plr.ID, plr.team, "Open Goat"
        else:
            return plr.ID, plr.team, self.wager

    def show_cards(self):
        """
            Show the cards in all players' hand
        """
        for player in self.session.players:
            player.show_cards()


class Player:
    """
    This class creates an object to represent a player in the game

    Attributes:
        ID (string) - ID of the player in the game
        wager_player (bool) - Has the player set the active wager
        wager_team (bool) - Has the player's team set the active wager
        cards (tuple) - List of cards in the player's hand
        user_control (bool) - Is the player controlled by the user
    """
    def __init__(self, ID, team):
        """
        Constructor for the player class

        Parameters:
        ID (string) - ID for the player
        """
        self.ID = ID
        self.team = team
        self.stake_player = False
        self.stake_team = False
        self.cards = []
        self.user_control = False

    def add_card(self, card):
        """
        Add a card to the player's hand
        """
        self.cards.append(card)

    def get_wager(self):
        """
        Return a wager when requested
        """
        return False, None

    def show_cards(self):
        """
            Show the cards in the player's hand
        """
        print("Player " + self.ID + ":")
        for card in self.cards:
            print(card[0] + " " + card[1], end='\n')
        print()


# game_sess = GameSession(4)
# game_sess.start_round()
