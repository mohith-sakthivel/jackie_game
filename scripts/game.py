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
    # Total Points
    total_points = 28
    # No players allowed in the game
    allowed_players = (4, 6, 8)
    # Point associated with each card key
    point_table = {"J": 3, "9": 2, "A": 1, "10": 1, "K": 0, "Q": 0}
    # Heirarchy of card keys in a suit
    heirarchy = {"J": 5, "9": 4, "A": 3, "10": 2, "K": 1, "Q": 0}
    suits = {"Spade": 0, "Heart": 1, "Club": 2, "Diamond": 3}
    # Base bet for the corresponding game
    base_bet = {2: 12, 3: 12, 4: 15, 6: 15, 8: 15}
    # Number of teams
    no_teams = 2
    # Variables to retrieve value from index
    suits_map = ("Spade", "Heart", "Club", "Diamond")
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
        self.team_plrs = [[], []]
        self.players = []
        self.start_plr_list = [i for i in range(no_players)]
        self.start_player = None
        self.no_rounds = 0
        self.rounds = []
        self.score = [[None, None], [0, 0]]
        self.plr_dict = {}
        # team format - (name, color)
        if teams is None:
            self.teams = (('Red', 'Red'), ('Blue', 'Blue'))
        else:
            self.teams = teams
        self.teams_dict = {}
        for i, team_data in enumerate(self.teams):
            self.teams_dict[team_data] = i
        for i in range(self.no_players):
            # Create the player objects
            self.players.append(Player(
                                       chr(ord('A') + i), i,
                                       self.teams[i % 2],
                                       self))
            self.plr_dict[chr(ord('A') + i)] = i
            self.team_plrs[i % 2].append(i)

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
        """
        self.no_rounds += 1
        self.rounds.append(Round(self))

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

    def update_score(self, wager_team, wager, outcome, goat, open_goat):
        """
        Update the game score with the round results
        """
        if outcome == 'N':
            self.post_round_process()
            return
        if open_goat:
            # Process points for open goat
            if outcome == 'W':
                pts = 4
            else:
                pts = -8
        else:
            # Find points for the set wager
            if wager >= 20:
                pts = 2
            else:
                pts = 1
            # Check for goat
            if goat:
                pts = pts+1
            # Update points based on win/loss
            if outcome == 'L':
                pts = - (pts+1)
        # Check what team is used in current score
        if self.score[0] == [None, None]:
            self.score[0] = [wager_team, 0]
        elif self.score[0][0] != wager_team:
            pts = -pts
        # Add the round's points to the score
        self.score[0][1] += pts
        # Convert positive score to negative
        if self.score[0][1] > 0:
            self.score[0][0] = int((self.score[0][0] + 1) % 2)
            self.score[0][1] = -self.score[0][1]
        # Fine tune score
        if self.score[0][1] <= -8:
            self.score[1][(self.score[0][0]+1) % 2] += 1
            self.score[0] = [None, None]
        elif self.score[0][1] == 0:
            self.score[0] = [None, None]
        self.post_round_process()   # Do post round cleanup

    def post_round_process(self):
        """Does post processing after a round is over"""
        # Set the choices for the next starting player
        self.start_player = None
        if self.score[0][0]:
            self.start_plr_list = self.team_plrs[(self.score[0][0]+1) % 2]
        # Clear the values stored in the player classses
        for plr in self.players:
            plr.clear_round_data()

    def select_start_player(self):
        """Selects a random start player from the available choices"""
        self.start_player = np.random.choice(self.start_plr_list)


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
        self.goat = False
        self.wager_player = self.session.start_player
        self.wager_team = self.session.players[self.wager_player].team
        self.wager_team = self.session.teams_dict[self.wager_team]
        self.wager_history = [(self.wager, self.wager_player, self.wager_team)]
        self.start_player = self.session.start_player
        self.next_player = self.session.start_player
        self.trump = None
        self.trump_open = False
        self.trump_open_at = (None, None)
        self.no_passes = self.session.total_cards//self.session.no_players
        self.suit_in_play = None
        self.passes_done = 0
        self.team_pts = [0, 0]
        self.team_trumps = [0, 0]
        self.play_history = [[]]

    def update_wager(self, Player_ID, wager):
        """
        Updates the new wager
        """
        self.wager_player = self.session.plr_dict[Player_ID]
        self.wager_team = self.session.players[self.wager_player].team
        self.wager_team = self.session.teams_dict[self.wager_team]
        if wager == "Open Goat":
            self.wager = 28
            self.open_goat = True
            self.start_player = self.wager_player
            self.next_player = self.start_player
        else:
            self.wager = wager
        self.wager_history.append(
            (self.wager, self.wager_player, self.wager_team))

    def get_wager_data(self):
        """
        Return the current wager data
        """
        plr = self.session.players[self.wager_player]
        if self.open_goat:
            return plr.ID, plr.team, "Open Goat"
        else:
            return plr.ID, plr.team, self.wager

    def get_wager_player(self):
        """
        Return the player who holds the current wager
        """
        return self.session.players[self.wager_player].ID

    def ask_trump(self, plr_index):
        """Return the trump of the current round"""
        if not self.trump_open:
            self.trump_open_at = (self.passes_done+1, plr_index)
            self.trump_open = True
        return self.trump

    def set_goat(self):
        """Player chooses to go for goat"""
        assert self.team_pts[(self.wager_team+1) % 2] == 0, \
            "Invalid conditions to go for goat"
        self.goat = True

    def set_play_card(self, plr_index, card):
        """Recieves the card played by the user"""
        assert plr_index == self.next_player, "Wrong player has played"
        assert card[0] in self.session.suits_map, "Invalid card"
        assert card[1] in self.session.key_map, "Invalid card"
        if not self.play_history[-1]:
            self.suit_in_play = card[0]
        self.play_history[-1].append((plr_index, card))
        # Set the next player to play
        if len(self.play_history[-1]) < self.session.no_players:
            self.next_player = (self.next_player + 1) % self.session.no_players
        else:
            self.next_player = None

    def process_pass(self):
        """
        Determine who won the pass and set the next the start player
        Also updates other round related data
        """
        assert len(self.play_history[-1]) == self.session.no_players, \
            "All players have not played their hand"
        self.passes_done += 1   # Increment passes completed
        max_card = self.play_history[-1][0]
        max_val = self.session.heirarchy[max_card[1][1]]
        result = (False, None)
        # Check for the max value/power card
        if self.trump_open and self.trump_open_at[0] < self.passes_done:
            trump_used = True
        else:
            trump_used = False
        for card_data in self.play_history[-1][1:]:
            if (not trump_used and
                    (self.passes_done, card_data[0]) == self.trump_open_at):
                trump_used = True
            card_val = self.session.heirarchy[card_data[1][1]]
            if (card_data[1][0] == self.suit_in_play
                    and card_val > max_val and
                    (max_card[1][0] != self.trump or
                     self.suit_in_play == self.trump)):
                max_card = card_data
                max_val = card_val
            # Add {not self.open_goat} to disable trump in open goat games
            elif (trump_used and card_data[1][0] == self.trump):
                if (max_card[1][0] != self.trump or card_val > max_val):
                    max_card = card_data
                    max_val = card_val
                    trump_used = True
        # Add points to the team that captured the round
        team_index = \
            self.session.teams_dict[self.session.players[max_card[0]].team]
        for card_data in self.play_history[-1]:
            self.team_pts[team_index] += \
                self.session.point_table[card_data[1][1]]
            if card_data[1][0] == self.trump:
                team_idx = self.session.teams_dict[
                    self.session.players[card_data[0]].team]
                self.team_trumps[team_idx] += 1
        # Check if one team has all trumps
        if ((max(self.team_trumps) == len(self.session.key_map)) or
                ((self.suit_in_play == self.trump)
                    and (min(self.team_trumps) == 0))):
            self.session.update_score(
                                      self.wager_team, self.wager, 'N',
                                      self.goat, self.open_goat)
            return (True, 'N')
        # Check condition for open goat
        if self.open_goat and max_card[0] != self.wager_player:
            self.session.update_score(
                                      self.wager_team, self.wager, 'L',
                                      self.goat, self.open_goat)
            return (True, 'L')
        # Check if game is over
        for i in range(2):
            if (i == self.wager_team and
                ((self.team_pts[i] >= self.wager and not self.goat
                    and self.team_pts[(i+1) % 2] > 0)
                 or (self.team_pts[i] == self.session.total_points))):
                self.session.update_score(
                                          self.wager_team, self.wager,
                                          'W', self.goat, self.open_goat)
                return (True, 'W')
            elif (i != self.wager_team and
                  ((self.team_pts[i] > 0 and self.goat) or
                   (self.session.total_points-self.team_pts[i]) < self.wager)):
                self.session.update_score(
                                          self.wager_team, self.wager,
                                          'L', self.goat, self.open_goat)
                return (True, 'L')
        # Process variables for the next pass
        self.play_history.append([])
        self.start_player = max_card[0]
        self.next_player = max_card[0]
        self.suit_in_play = None
        return result


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
    def __init__(self, ID, index, team, session):
        """
        Constructor for the player class

        Parameters:
        ID (string) - ID for the player
        """
        self.ID = ID
        self.index = index
        self.team = team
        self.session = session
        self.stake_player = False
        self.cards = []
        self.user_control = False

    def add_card(self, card):
        """
        Add a card to the player's hand
        """
        self.cards.append(card)

    def get_wager(self, wager_history):
        """
        Return a wager when requested
        """
        # Need advanced algorithms
        # Go for goat
        suit_count = [0] * len(self.session.suits_map)
        for card in self.cards:
            suit_count[self.session.suits[card[0]]] += \
                self.session.point_table[card[1]]
        max_suit = suit_count.index(max(suit_count))
        self.trump_choice = self.session.suits_map[max_suit]
        return False, None

    def set_wager_player(self):
        """set the player as the wager player in the current round"""
        self.stake_player = True

    def get_trump(self):
        """
        Gets the trump suit from the player
        """
        try:
            return self.trump_choice
        except NameError:
            print("Player not given a chance to set wager")
            raise

    def get_play_card(self, round_):
        """
        Select the card to play for the current round
        """
        # Need advanced algorithms
        if not round_.play_history[-1]:
            round_.set_play_card(self.index, self.cards.pop())
            return
        for i, card in enumerate(self.cards):
            if card[0] == round_.suit_in_play:
                self.cards = self.cards[:i] + self.cards[i+1:]
                round_.set_play_card(self.index, card)
                return
        trump_suit = round_.ask_trump(self.index)
        for i, card in enumerate(self.cards):
            if card[0] == trump_suit:
                self.cards = self.cards[:i] + self.cards[i+1:]
                round_.set_play_card(self.index, card)
                return
        round_.set_play_card(self.index, self.cards.pop())

    def clear_round_data(self):
        """Clear data related to specific round"""
        self.cards = []
        self.stake_player = False


def deal_cards(session):
    """
        Deal cards to the players in the game
    """
    values = np.arange(24)
    np.random.shuffle(values)
    i = 0
    # Shuffle and deal cards to all the players
    while i < 24:
        for player in session.players:
            player.add_card((
                            session.suits_map[values[i] // 6],
                            session.key_map[values[i] % 6]))
            i = i + 1
