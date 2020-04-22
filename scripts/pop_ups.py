import tkinter as tk
from tkinter import ttk


class PlayerSelectDialog():
    """
        Creates a temporary popup box and returns the user
        input to the calling function
    """
    def __init__(self, text, options, result, op_type, root=None):

        assert len(options) != 0, "Empty choice list!"
        assert (
                op_type == 'checkbox' or
                op_type == 'radiobutton'), "Invalid choice type!"

        self.root = root
        self.top = tk.Toplevel(self.root)
        choices = []

        msg_frame = tk.Frame(self.top, borderwidth=5, relief='ridge')
        msg_frame.pack(fill='both', expand=True)

        label = tk.Label(msg_frame, text=text)
        label.pack(padx=4, pady=4)

        ok_btn = tk.Button(msg_frame, text="Ok", width=5, height=1)

        if op_type == 'checkbox':
            self.check_var = []
            for i, value in enumerate(options):
                self.check_var.append(tk.IntVar())
                choices.append(tk.Checkbutton(
                                              msg_frame, text="Player "+value,
                                              variable=self.check_var[i]))
                choices[i].deselect()
                choices[i].pack()
            ok_btn['command'] = lambda: self._cb_submit(result)
        else:
            self.var = tk.StringVar()
            for value in options:
                choices.append(tk.Radiobutton(
                                              msg_frame, text="Player "+value,
                                              variable=self.var,
                                              value=value, indicatoron=True))
                choices[-1].pack()
            self.var.set(options[0])
            ok_btn['command'] = lambda: self._rb_submit(result)

        ok_btn.pack(side=tk.BOTTOM, padx=4, pady=4)

        self.top.transient(self.root)
        self.top.grab_set()

    def _cb_submit(self, result):
        for var in self.check_var:
            result.append(var.get() == 1)
        self.top.destroy()

    def _rb_submit(self, result):
        result.append(self.var.get())
        self.top.destroy()


class GetNumInput():
    """
        Creates a temporary popup box to request the user
        to input a number
    """
    def __init__(self, text, range_, result, root):
        assert len(range_) != 0, "Empty choice list!"
        self.root = root
        self.top = tk.Toplevel(self.root)

        msg_frame = tk.Frame(self.top, borderwidth=5, relief='ridge')
        msg_frame.pack(fill='both', expand=True)

        label = tk.Label(msg_frame, text=text)
        label.pack(padx=4, pady=4)

        self.usr_input = tk.StringVar()
        choices = ttk.Combobox(
                               msg_frame, textvariable=self.usr_input,
                               values=range_, state="readonly")
        choices.current(0)
        choices.pack()

        ok_btn = tk.Button(msg_frame, text="Ok", width=5, height=1)
        ok_btn['command'] = lambda: self._choice_submit(result)
        ok_btn.pack(side=tk.BOTTOM, padx=4, pady=4)

        self.top.transient(self.root)
        self.top.grab_set()

    def _choice_submit(self, result):
        try:
            result.append(int(self.usr_input.get()))
        except ValueError:
            result.append(self.usr_input.get())
        self.top.destroy()
