import vision
from tkinter import messagebox as msg
from popups import GetNumInput, SelectDialog
from game import deal_cards


class ManageRound():
    """
    This class manages each game round by interacting with the
    game session and the front end app

    Attributes:
        gui - GameFUI instance to call necessary methods
        game_sess - GameSession instance to manage the game
    """

    def __init__(self, gui, game_sess):
        self.__gui = gui
        self.__game_sess = game_sess
        self.plr_count = self.__gui.plr_count
        self.goat_on = False

    def start_round(self):
        """Start a round of play"""
        self._get_start_player()
        self.__game_sess.start_round()
        self.__round = self.__game_sess.rounds[-1]
        self.__gui.update_round_no(self.__game_sess.no_rounds)
        deal_cards(self.__game_sess)
        self.__gui.display_cards()
        self._run_wager_round()
        self._start_play()

    def _get_start_player(self):
        """
        If start player is not set get the input from the user
        """
        while (self.__game_sess.get_start_player() is None):
            result = []
            players = [self.__game_sess.players[i].ID
                       for i in self.__game_sess.start_plr_list]
            popup = SelectDialog(
                            "Select which player to deal cards first to",
                            players, result, 'radiobutton')
            self.__gui.root.wait_window(popup.top)
            if (len(result) == 0):
                msg.showerror(
                              "No Selection made!",
                              "You did not select a start player")
                continue
            self.__game_sess.set_start_player(result[0])

    def _run_wager_round(self):
        """
        Ask players if they want to set a wager
        """
        start_plr = self.__game_sess.start_player
        for i in range(start_plr, start_plr + self.plr_count):
            player = self.__game_sess.players[i % self.plr_count]
            if not (player.user_control):
                set_wager, value = player.get_wager(self.__round.wager_history)
                if set_wager:
                    self.__round.update_wager(player.ID, value)
            else:
                usr_inp = True
                while (usr_inp):
                    if player.ID == self.__game_sess.get_start_player():
                        usr_inp = msg.askyesno(
                                    "Call Wager", "Player "+player.ID + "\n" +
                                    "Do you want to raise your base wager?")
                    else:
                        usr_inp = msg.askyesno(
                                        "Call Wager", "Player " + player.ID +
                                        "\nDo you want to set a wager?")
                    if usr_inp:
                        vals = [i for i in range(self.__round.wager+1, 29)]
                        vals.append("Open Goat")
                        result = []
                        popup = GetNumInput(
                                        "Select your wager from the list",
                                        vals, result, self.__gui.root)
                        self.__gui.root.wait_window(popup.top)
                        if len(result) == 0:
                            msg.showerror(
                                            "Wager not set!",
                                            "You did not submit a wager")
                            continue
                        self.__round.update_wager(player.ID, result[-1])
                        break
            # Update the wager set by the last player
            self.__gui.update_wager(self.__round)
            if self.__round.open_goat:
                break
        self.__game_sess.players[self.__round.wager_player].set_wager_player()
        # Ask for the trump suit
        if self.__game_sess.players[self.__round.wager_player].user_control:
            result = []
            while not result:
                popup = SelectDialog("Select the trump suit",
                                     self.__game_sess.suits_map,
                                     result, 'radiobutton', self.__gui.root)
                self.__gui.root.wait_window(popup.top)
                if result:
                    self.__round.trump = result[0]
        else:
            self.__round.trump = \
                self.__game_sess.players[self.__round.start_player].get_trump()

    def _start_play(self):
        """
        Start playing the round until a win/loss
        """
        for pass_ in range(1, self.__round.no_passes+1):
            # Start the turn with the current start player
            for i in range(
                           self.__round.start_player,
                           self.__round.start_player + self.plr_count):
                plr_index = i % self.plr_count
                plr = self.__game_sess.players[plr_index]
                if not plr.user_control:
                    # Get card played by the bot
                    plr.get_play_card(self.__round)
                    # Update GUI if trump was opened by bot
                    if (self.__round.trump_open and
                            self.__round.trump_open_at == (pass_, plr_index)):
                        self.__gui.update_trump(self.__round.trump)
                    # Check if bot opted for goat
                    if (not self.goat_on and self.__round.goat
                            and not self.__round.open_goat):
                        self.__gui.go_for_goat(None, True)
                        self.goat_on = True
                    # Show the card played by the bot in the GUI
                    self.__gui.update_bot_play(
                                self.__round.play_history[pass_-1][-1])
                elif self.__gui.game_mode == "Bot vs Users":
                    # Get card played by the user through camera
                    self.__round.set_play_card(
                                               plr_index,
                                               vision.get_card_input())
                else:
                    # Get card played by the user through the GUI
                    card = self.__gui.get_user_play_card(
                                                         plr_index,
                                                         self.__round, plr)
                    self.__round.set_play_card(plr_index, card)
                    # Check if bot opted for goat
                    if (not self.goat_on and self.__round.goat):
                        self.goat_on = True
                # Add a wait after each player plays his card
                self.__gui.add_wait_time(1500)
            # Add a wait at the end of the round
            self.__gui.add_wait_time(1000)
            # Update the round for the cards played
            round_status = self.__round.process_pass()
            self.__gui.post_pass_update(self.__round)
            if round_status[0]:             # Check if game is won
                break
        # Print goat status
        text = ""
        if ((self.__round.goat or self.__round.open_goat)
                and round_status != 'N'):
            if round_status[1] == 'W':
                text = "Goat Successful!\n"
            elif round_status[1] == 'L':
                text = "Goat Unsuccessful!\n"
            if self.__round.open_goat:
                text = "Open " + text
        # Display the round result
        team = self.__game_sess.teams[self.__round.wager_team][0]
        if (round_status[1] == 'W'):
            text = text + "Team " + team + " won the round."
        elif (round_status[1] == 'L'):
            text = text + "Team " + team + " lost the round."
        else:
            text = "One team had all trump cards. Round is invalid."
        msg.showinfo("Round Over!", text)
        # Update GUI and game_sess at the end of the round
        self.__gui.post_round_update(self.__round)
        self.__game_sess.select_start_player()
