import tkinter as tk
from tkinter import ttk, Menu
from tkinter import messagebox as msg
from game_env import GameSession, allowed_players
# from help_text import help_text
from popups import PlayerSelectDialog
from round import ManageRound


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
    plr_space_wd = {4: 0.3, 6: 0.3, 8: 0.225}
    plr_space_ht = {4: 0.325, 6: 0.3, 8: 0.3}

    def __init__(self):
        self.game_sess = None
        self.root = tk.Tk()
        self.root.title("Jackie - Welcome")
        self.root.iconbitmap('Jackie.ico')
        self.root.geometry('300x300')
        self.__cur_frame = None
        self.__plr_count = 0
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
        self.__plr_count = int(self.plr_count_var.get())
        self.game_sess = GameSession(self.__plr_count)
        # Get the players controlled by the user
        players = [plr.ID for plr in self.game_sess.players]
        result = []
        popup = PlayerSelectDialog(
                               "Select the user-controlled players",
                               players, result, 'checkbox')
        self.root.wait_window(popup.top)
        if not(result == []):
            if not any(result):
                msg.showwarning(
                                'Alert! No user-controlled player.',
                                "All players in the game are contolled" +
                                "by the computer.")
            self.game_sess.set_user_player(result)
            # Destroy the current window
            if self.__cur_frame is not None:
                self.__cur_frame.destroy()
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
        pos = ['w'] + ['n']*(int(self.__plr_count//2)-1) + \
              ['e'] + ['s']*(int(self.__plr_count//2)-1)
        # Create space for all players
        r_width = self.plr_space_wd[self.__plr_count]
        r_height = self.plr_space_ht[self.__plr_count]
        r_xy = self.plr_space_pos[self.__plr_count]
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
        self.sb_team_lbl.grid(column=0, row=0)
        self.sb_pt_lbl.grid(column=0, row=1)
        # Display score if game is in progress
        if (self.game_sess.no_rounds != 0):
            self.sb_team_lbl['text'] = "Team " + self.game_sess.score[0][0]
            self.sb_team_lbl['foreground'] = self.game_sess.score[0][1]
            self.sb_pt_lbl['text'] = self.game_sess.score[1]
        else:
            if self.sb_team_lbl in self.scoreboard.grid_slaves():
                self.sb_team_lbl.grid_remove()
            self.sb_pt_lbl['text'] = '0'
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
                              anchor='nw', relwidth=0.1, relheight=0.225,
                              relx=0.01, rely=0)

        self.round_no_lbl = tk.Label(
                                     self.statboard, text='Round',
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
        self.rnd_pts_lbl[0].grid(row=3, column=0, columnspan=2, sticky=tk.W)
        self.rnd_pts[0].grid(row=3, column=2)
        self.rnd_pts_lbl[1].grid(row=4, column=0, columnspan=2, sticky=tk.W)
        self.rnd_pts[1].grid(row=4, column=2)

    def _start_round(self):
        """
        Starts a round of the game when the Start Round button is clicked
        """
        self.start_round.place_forget()
        self.round = ManageRound(self, self.game_sess)

    def _update_round_no(self, no):
        """Updates round number on the screen"""
        self.round_no['text'] = str(no)

    def _update_wager(self, round):
        """Updates round wager on the screen"""
        _, team, pts = round.get_wager_data()
        self.cur_wager_team['text'] = team[0]
        self.cur_wager_team['foreground'] = team[1]
        self.cur_wager_pts['text'] = pts
