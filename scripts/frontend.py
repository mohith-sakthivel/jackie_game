import tkinter as tk
from tkinter import ttk, Menu
from tkinter import messagebox as msg
from game import GameSession, allowed_players
from roundhandler import ManageRound
from popups import SelectDialog
from PIL import Image, ImageTk


class GameGUI:
    """
    Class containing the GUI for the game
    """
    btn_wd = 80
    btn_ht = 40
    plr_space_pos = {4: ((0.025, 0.5), (0.5, 0), (0.975, 0.5), (0.5, 1)),
                     6: ((0.025, 0.5), (0.3, 0), (0.7, 0), (0.975, 0.5),
                         (0.7, 1), (0.3, 1)),
                     8: ((0.05, 0.5), (0.25, 0), (0.5, 0), (0.75, 0),
                         (0.95, 0.5), (0.75, 1), (0.5, 1), (0.25, 1))}
    plr_space_wd = {4: 0.4, 6: 0.3, 8: 0.23}
    plr_space_ht = {4: 0.225, 6: 0.3, 8: 0.3}
    card_size = {4: (76, 114), 6: (88, 132), 8: (88, 132)}
    card_loc = {4: ((-0.04, 0), (0, -0.175), (0.04, 0), (0, 0.175)),
                6: ((-0.125, 0), (-0.04, -0.1), (0.04, -0.1), (0.125, 0),
                    (0.04, 0.1), (-0.04, 0.1)),
                8: ((-0.175, 0), (-0.08, -0.1), (0, -0.1), (0.08, -0.1),
                    (0.175, 0), (0.08, 0.1), (0, 0.1), (-0.08, 0.1))}

    game_mode_options = ("Bot vs Users", "User vs Bots", "Bots Only")

    def __init__(self):
        self.game_sess = None
        self.root = tk.Tk()
        self.root.title("Jackie - Welcome")
        self.root.iconbitmap('Jackie.ico')
        self.root.geometry('300x300')
        self.__cur_frame = None
        self.plr_count = 0
        self.game_mode = []
        self.__card_imgs = {}
        self.__suit_imgs = {}
        self.__card_back = None
        # Create the menu widgets
        self._create_menu()
        # Start the application
        self._start_screen()

    def _quit(self):
        answer = msg.askyesno(
                              "Warning!",
                              "Are you sure that you want to close " +
                              "the application?")
        if answer:
            self.root.quit()
            self.root.destroy()
            exit()

    def _about(self):
        msg.showinfo('About',
                     "This game was created by Mohith Sakthivel in 2020")

    def _new_game(self):
        answer = msg.askyesno("Warning!",
                              "Are you sure that you want to cancel the "
                              "current session and start a new game?")
        if answer:
            self.__init__()

    def _create_menu(self):
        """Creates all menu bar for the entire application"""
        self.menu_bar = Menu(self.root)
        self.root.config(menu=self.menu_bar)
        # Create menus in the menu bar
        self.file_menu = Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="New Game", command=self._new_game)
        self.file_menu.add_command(label="Exit", command=self._quit)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.help_menu = Menu(self.menu_bar, tearoff=0)
        self.help_menu.add_command(label="About", command=self._about)
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)

    def _start_screen(self):
        """
        Displays start screen and also recieves the player count form the user
        """
        # Start the game window
        self.__cur_frame = ttk.Frame(self.root, width=250, height=250)
        self.__cur_frame.pack()
        # Create label requesting player count
        plr_count_lbl = ttk.Label(
                    self.__cur_frame, text="Enter the number of players: ")
        plr_count_lbl.config(font=("Arial", 10))
        plr_count_lbl.place(
                relheight=0.25, relwidth=0.75,
                rely=0.5, relx=0.05, anchor=tk.W)
        # Create a drop down for number of players
        self.plr_count_var = tk.StringVar()
        plr_count_ety = ttk.Combobox(
                                     self.__cur_frame,
                                     textvariable=self.plr_count_var,
                                     state="readonly")
        plr_count_ety['values'] = allowed_players
        plr_count_ety.current(0)
        plr_count_ety.place(
                relheight=0.1, relwidth=0.2,
                rely=0.5, relx=0.75, anchor=tk.W)
        # Create 'Begin' button
        enter_btn = tk.Button(
                    self.__cur_frame, text="Begin",
                    bd=4, command=self._usr_ctrl_players)
        enter_btn.place(
                relheight=0.1, relwidth=0.2,
                rely=0.65, relx=0.75, anchor=tk.W)

    def _usr_ctrl_players(self):
        """
        Window to select players controlled by user
        """
        # Destroy the current window
        if self.__cur_frame is not None:
            self.__cur_frame.destroy()
        # Select game mode
        while (not self.game_mode):
            popup = SelectDialog(
                                "Select game mode",
                                self.game_mode_options,
                                self.game_mode,
                                'radiobutton')
            self.root.wait_window(popup.top)
        self.game_mode = self.game_mode[0]
        self.plr_count = int(self.plr_count_var.get())
        self.game_sess = GameSession(self.plr_count)
        # Get the players controlled by the user
        if self.game_mode != "Bots Only":
            players = ["Player " + plr.ID for plr in self.game_sess.players]
            result = []
            if self.game_mode == "Bot vs Users":
                tmp = "bot"
            else:
                tmp = "user"
            while(not result):
                popup = SelectDialog(
                                    "Select the " + tmp + "-controlled player",
                                    players, result, 'radiobutton')
                self.root.wait_window(popup.top)
                if not(result):
                    msg.showerror(
                                'No selection made',
                                "You did not select any " + tmp +
                                "-controlled player")
            _, ID = result[0].split("Player ")
            if self.game_mode == "Bot vs Users":
                result = [ID != plr.ID for plr in self.game_sess.players]
            else:
                result = [ID == plr.ID for plr in self.game_sess.players]
            self.game_sess.set_user_player(result)
        self._create_game_screen()

    def _create_game_screen(self):
        """
            Builds the main game screen
        """
        self.root.geometry('1280x720')
        self.root.title("Jackie")
        self.__cur_frame = tk.Frame(self.root, width=1280, height=720, pady=20)
        self.__cur_frame.pack()
        self.plr_space = []
        pos = ['w'] + ['n']*(int(self.plr_count//2)-1) + \
              ['e'] + ['s']*(int(self.plr_count//2)-1)
        # Create space for all players
        r_width = self.plr_space_wd[self.plr_count]
        r_height = self.plr_space_ht[self.plr_count]
        r_xy = self.plr_space_pos[self.plr_count]
        for i, player in enumerate(self.game_sess.players):
            self.plr_space.append(tk.LabelFrame(
                                                self.__cur_frame,
                                                text="Player " + player.ID,
                                                font=('Helvetica', 13, 'bold'),
                                                bd=5, labelanchor='n',
                                                foreground=player.team[1]))
            self.plr_space[i]['font'] = ('Helvetica', 11, 'bold')
            self.plr_space[i].place(
                                    anchor=pos[i],
                                    relwidth=r_width, relheight=r_height,
                                    relx=r_xy[i][0], rely=r_xy[i][1])
        # Setup the scoreboard
        self.scoreboard = tk.LabelFrame(
                                         self.__cur_frame, text="Scoreboard",
                                         bd=8, labelanchor='n')
        self.scoreboard.place(
                              anchor='ne', relwidth=0.1, relheight=0.15,
                              relx=0.99, rely=0)
        self.scoreboard.grid_rowconfigure(0, weight=1)
        self.scoreboard.grid_columnconfigure(0, weight=1)
        self.scoreboard['font'] = ('Helvetica', 13, 'bold')

        self.sb_team_lbl = tk.Label(
                                    self.scoreboard,
                                    font=('Helvetica', 12, 'bold'))
        self.sb_pt_lbl = tk.Label(
                                  self.scoreboard,
                                  font=('Helvetica', 12, 'bold'))
        self.sb_pt_lbl['text'] = '0'
        self.sb_pt_lbl.grid(column=0, row=0, sticky=(tk.N, tk.S))
        # Create a button to start the round
        self.start_round = tk.Button(
                                     self.__cur_frame, text="Start Round",
                                     command=self._start_round, bd=5)
        self.start_round.place(
                               anchor='se', relwidth=0.1,
                               relheight=0.05, relx=0.975, rely=1)
        # Create a panel to display round stats
        self.statboard = tk.LabelFrame(
                                       self.__cur_frame, text="Round Stats",
                                       font=('Helvetica', 11, 'bold'),
                                       bd=8, labelanchor='n')
        self.statboard.place(
                              anchor='nw', relwidth=0.1, relheight=0.25,
                              relx=0.01, rely=0)

        self.round_no_lbl = tk.Label(
                                     self.statboard, text='Round No. :',
                                     font=('Helvetica', 11, 'bold'))
        self.round_no = tk.Label(
                                 self.statboard, text='---',
                                 font=('Helvetica', 11, 'normal'))

        self.cur_wager_lbl = tk.Label(
                                      self.statboard, text='Wager :',
                                      font=('Helvetica', 11, 'bold'))
        self.cur_wager_team = tk.Label(
                                  self.statboard, text='---',
                                  font=('Helvetica', 11, 'normal'))
        self.cur_wager_pts = tk.Label(
                                  self.statboard, text='---',
                                  font=('Helvetica', 11, 'normal'))
        self.cur_wager_plr = tk.Label(
                                  self.statboard, text='---',
                                  font=('Helvetica', 11, 'normal'))

        self.rnd_pts_lbl = []
        self.rnd_pts_lbl.append(tk.Label(
                                    self.statboard,
                                    text="Team "+self.game_sess.teams[0][0],
                                    foreground=self.game_sess.teams[0][1],
                                    font=('Helvetica', 11, 'bold')))
        self.rnd_pts_lbl.append(tk.Label(
                                self.statboard,
                                text="Team "+self.game_sess.teams[1][0],
                                foreground=self.game_sess.teams[1][1],
                                font=('Helvetica', 11, 'bold')))

        self.rnd_pts = []
        self.rnd_pts.append(tk.Label(
                                     self.statboard, text='---',
                                     font=('Helvetica', 11, 'normal')))
        self.rnd_pts.append(tk.Label(
                                     self.statboard, text='---',
                                     font=('Helvetica', 11, 'normal')))
        # Place the statboard items on the grid
        self.round_no_lbl.grid(row=0, column=0, columnspan=2, sticky=tk.W)
        self.round_no.grid(row=0, column=2)
        self.cur_wager_lbl.grid(row=1, column=0, columnspan=3, sticky=tk.W)
        self.cur_wager_team.grid(row=2, column=0)
        self.cur_wager_pts.grid(row=2, column=1,  columnspan=2)
        self.cur_wager_plr.grid(row=3, column=0, columnspan=3)
        self.rnd_pts_lbl[0].grid(row=4, column=0, columnspan=2, sticky=tk.W)
        self.rnd_pts[0].grid(row=4, column=2)
        self.rnd_pts_lbl[1].grid(row=5, column=0, columnspan=2, sticky=tk.W)
        self.rnd_pts[1].grid(row=5, column=2)
        # Load images of the cards
        self._load_cards()
        # Build the trump display area
        self.trump_data = tk.LabelFrame(
                                       self.__cur_frame, text="Trump",
                                       font=('Helvetica', 11, 'bold'),
                                       bd=8, labelanchor='n')
        self.trump_data.place(
                              anchor='sw', relwidth=0.1, relheight=0.2,
                              relx=0.01, rely=1)
        self.get_trump = tk.Button(
                                   self.trump_data, text='Show Trump',
                                   font=('Helvetica', 10, 'bold'),
                                   command=self.show_trump)
        self.cur_trump = tk.Label(self.trump_data)

    def show_trump(self):
        """Displays the trump on the GUI on request from the user"""
        if self.get_trump in self.trump_data.pack_slaves():
            self.get_trump.pack_forget()
        self.cur_trump['image'] = \
            self.__suit_imgs[self.active_round.ask_trump(self.active_player)]
        self.cur_trump.pack(expand=True)

    def update_trump(self, trump):
        """Updates the opened trump in the GUI when trump is opened by a bot"""
        self.cur_trump['image'] = self.__suit_imgs[trump]
        self.cur_trump.pack(expand=True)

    def show_get_trump(self):
        """Displays the button to request for trump"""
        if self.cur_trump in self.trump_data.pack_slaves():
            print("Error")
            exit()
        self.get_trump.pack(expand=True)

    def _start_round(self):
        """
        Starts a round of the game when the Start Round button is clicked
        """
        self.start_round.place_forget()
        self.round = ManageRound(self, self.game_sess)
        self.start_round.place(
                               anchor='se', relwidth=0.1,
                               relheight=0.05, relx=0.975, rely=1)

    def update_round_no(self, no):
        """Updates round number on the screen"""
        self.round_no['text'] = str(no)

    def update_wager(self, round):
        """Updates round wager on the screen"""
        plr, team, pts = round.get_wager_data()
        self.cur_wager_team['text'] = team[0]
        self.cur_wager_team['foreground'] = team[1]
        self.cur_wager_pts['text'] = pts
        self.cur_wager_plr['text'] = "Player "+plr
        self.cur_wager_plr['foreground'] = team[1]

    def _play_card(self, obj, card):
        """
        Delete the card played by the user from the GUI and
        return the card details to the program
        """
        obj.pack_forget()
        obj.destroy()
        self.usr_card = card
        self.usr_sel_done.set(True)

    def display_cards(self):
        """Display the cards in the game screeen"""
        start = self.game_sess.start_player
        self.played_cards = []
        count = 0
        no_cards = self.game_sess.rounds[-1].no_passes
        blvar = tk.BooleanVar()
        self.plr_cards = [[] for _ in range(self.plr_count)]
        while (count < 2):
            for i in range(start, start + self.plr_count):
                i = i % self.plr_count
                plr = self.game_sess.players[i]
                for j in range(int(count*(no_cards//2)), len(plr.cards)):
                    if (not plr.user_control or
                            (self.game_mode != "User vs Bots")):
                        self.plr_cards[i].append(tk.Label(
                                                    self.plr_space[i],
                                                    image=self.__card_back))
                    else:
                        self.plr_cards[i].append(tk.Button(
                                        self.plr_space[i],
                                        image=self.__card_imgs[plr.cards[j]]))
                        self.plr_cards[i][j]['command'] = \
                            lambda obj=self.plr_cards[i][j], cd=plr.cards[j]: \
                            self._play_card(obj, cd)
                        self.plr_cards[i][j]['state'] = 'disabled'
                    self.plr_cards[i][j].pack(
                                            side=tk.LEFT,
                                            padx=1, pady=1)
                    if (j+1) == (no_cards//2):
                        break
                # Add a wait
                self.root.after(
                                250,
                                lambda: blvar.set(not blvar.get()))
                self.root.wait_variable(blvar)
            # Add a wait
            self.root.after(
                            250,
                            lambda: blvar.set(not blvar.get()))
            self.root.wait_variable(blvar)
            count = count+1

    def _load_cards(self):
        """Loads the image of the card"""
        size = self.card_size[self.plr_count]
        for suit in self.game_sess.suits_map:
            for key in self.game_sess.key_map:
                path_ = 'cards\\' + suit + '\\' + suit[0]+key+'.png'
                self.__card_imgs[(suit, key)] = ImageTk.PhotoImage(
                        Image.open(path_).resize(size, Image.ANTIALIAS))
        self.__card_back = ImageTk.PhotoImage(Image.open(
                                'cards\\misc\\gray_back.png').resize(
                                        size, Image.ANTIALIAS))
        self.__card_back = (self.__card_back)
        for suit in self.game_sess.suits_map:
            self.__suit_imgs[suit] = ImageTk.PhotoImage(Image.open(
                                        'cards\\suits\\'+suit+'.png').resize(
                                            (70, 85), Image.ANTIALIAS))

    def update_bot_play(self, card_data):
        """
        Updates the GUI when the bot plays a card
        """
        plr_index = card_data[0]
        card = card_data[1]
        self.plr_cards[plr_index].pop().pack_forget()
        self.played_cards.append(tk.Label(
                                          self.__cur_frame,
                                          image=self.__card_imgs[card]))
        self.played_cards[-1].place(
                        anchor=tk.CENTER,
                        relx=0.5+self.card_loc[self.plr_count][plr_index][0],
                        rely=0.5+self.card_loc[self.plr_count][plr_index][1])

    def get_user_play_card(self, plr_index, round_, plr):
        """
        Recieves the card to play from the user
        """
        self.active_player = plr_index
        self.active_round = round_
        no_suit = True
        if self.game_mode == "User vs Bots":
            for suit, _ in self.game_sess.players[plr_index].cards:
                if suit == round_.suit_in_play or not round_.suit_in_play:
                    no_suit = False
                    break
        if (self.game_mode == "Bot vs Users" or
                (no_suit and not round_.trump_open)):
            self.show_get_trump()
        self.usr_card = None
        self.usr_sel_done = tk.BooleanVar()
        self.usr_sel_done.set(False)
        no_match_suit = True
        # Enable cards matching with current suit in play
        for i, card_obj in enumerate(self.plr_cards[plr_index]):
            if ((not round_.suit_in_play and
                    (plr.cards[i][0] != round_.trump or round_.trump_open
                     or not plr.stake_player))
                    or plr.cards[i][0] == round_.suit_in_play):
                card_obj['state'] = 'normal'
                no_match_suit = False
        # If there is no matching card enable all cards
        if no_match_suit:
            for card_obj in self.plr_cards[plr_index]:
                card_obj['state'] = 'normal'
        self.root.wait_variable(self.usr_sel_done)
        # Delete the played card from the player object and the GUI card list
        for i, card in enumerate(plr.cards):
            if card == self.usr_card:
                plr.cards = plr.cards[:i] + plr.cards[i+1:]
                self.plr_cards[plr_index] = \
                    self.plr_cards[plr_index][:i] + \
                    self.plr_cards[plr_index][i+1:]
                break
        for card_obj in self.plr_cards[plr_index]:
            card_obj['state'] = 'disabled'
        # Display the played card in the played cards area
        self.played_cards.append(tk.Label(
                                        self.__cur_frame,
                                        image=self.__card_imgs[self.usr_card]))
        self.played_cards[-1].place(
                        anchor=tk.CENTER,
                        relx=0.5+self.card_loc[self.plr_count][plr_index][0],
                        rely=0.5+self.card_loc[self.plr_count][plr_index][1])
        # Disable show get trump
        if self.get_trump in self.trump_data.pack_slaves():
            self.get_trump.pack_forget()
        return self.usr_card

    def post_pass_update(self, round_):
        """
        Updates the GUI based on the latest pass of the round
        """
        for card in self.played_cards:
            card.place_forget()
            card.destroy()
        self.played_cards = []
        self.rnd_pts[0]['text'] = round_.team_pts[0]
        self.rnd_pts[1]['text'] = round_.team_pts[1]

    def post_round_update(self, round_):
        """
        Updates the GUI based on the latest round
        """
        for index in range(len(self.plr_cards)):
            for card_obj in self.plr_cards[index]:
                card_obj.pack_forget()
                card_obj.destroy()
        self.cur_wager_team['text'] = "---"
        self.cur_wager_team['foreground'] = None
        self.cur_wager_pts['text'] = "---"
        self.cur_wager_plr['text'] = "---"
        self.cur_wager_plr['foreground'] = None
        self.rnd_pts[0]['text'] = "---"
        self.rnd_pts[1]['text'] = "---"
        # Display score
        if self.game_sess.score[0] == [None, None]:
            if self.sb_team_lbl in self.scoreboard.grid_slaves():
                self.sb_team_lbl.grid_forget()
            self.sb_pt_lbl.grid(column=0, row=0, sticky=(tk.N, tk.S))
            self.sb_pt_lbl['text'] = 0
        else:
            self.sb_team_lbl['text'] = "Team " + \
                self.game_sess.teams[self.game_sess.score[0][0]][0]
            self.sb_team_lbl['foreground'] = \
                self.game_sess.teams[self.game_sess.score[0][0]][1]
            self.sb_pt_lbl['text'] = self.game_sess.score[0][1]
            self.sb_team_lbl.grid(column=0, row=0, sticky=(tk.N, tk.S))
            self.sb_pt_lbl.grid(column=0, row=1, sticky=(tk.N, tk.S))
        if self.cur_trump in self.trump_data.pack_slaves():
            self.cur_trump.pack_forget()
