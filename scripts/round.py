from pop_ups import PlayerSelectDialog, GetNumInput
from tkinter import messagebox as msg


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
        self._get_start_player()
        self.__round = self.__game_sess.start_round()
        self.__gui._update_round_no(self.__game_sess.no_rounds)
        self._run_wager_round()

    def _get_start_player(self):
        """
        If start player is not set get the input from the user
        """
        if self.__game_sess.get_start_player() is None:
            result = []
            players = [plr.ID for plr in self.__game_sess.players]
            popup = PlayerSelectDialog(
                            "Select which player to deal cards first to",
                            players, result, 'radiobutton')
            self.__gui.root.wait_window(popup.top)
            self.__game_sess.set_start_player(result[0])

    def _run_wager_round(self):
        """
        Ask players if they want to set a wager
        """
        str_plr = self.__game_sess.start_player
        no_plrs = self.__game_sess.no_players
        for i in range(str_plr, str_plr + no_plrs):
            player = self.__game_sess.players[i % no_plrs]
            if not (player.user_control):
                set_wager, value = player.get_wager()
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
            self.__gui._update_wager(self.__round)
            if self.__round.open_goat:
                break
