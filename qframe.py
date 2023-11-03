"""
    Creates a GUI to practice tests.
    Copyright (C) 2023  nghfp9wa7bzq@gmail.com

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from tkinter import *
from tkinter import ttk


class QFrame(ttk.Frame):
    def __init__(self, master, qloader):
        super().__init__(master)

        self.qloader = qloader
        self.qanda = None
        self.answer_buttons = []
        self.answer_buttons_vars = []

        self.prev_scroll_frame_height = 0
        self.start_counter = 0

        self.style = ttk.Style()
        self.style.configure('TRadiobutton', font=('TkDefaultFont', 20), padding=10)
        self.style.configure('TCheckbutton', font=('TkDefaultFont', 20), padding=10)
        self.style.configure('BGRed.BT.TRadiobutton', background='red')
        self.style.configure('BGGreen.BT.TRadiobutton', background='green')
        self.style.configure('BGRed.BT.TCheckbutton', background='red')
        self.style.configure('BGGreen.BT.TCheckbutton', background='green')
        self.style.configure('BGGray.BT.TCheckbutton', background='#d9d9d9')
        self.style.configure('BT.TLabel', font=('TkDefaultFont', 20), padding=5)

        self.columnconfigure((0, 1), weight=1, uniform='a')

    def add_question_to_frame(self):
        l = ttk.Label(self, text=self.qanda.question, justify='left', style='BT.TLabel')
        l.grid(row=0, column=0, rowspan=len(self.qanda.answers), sticky='nw')

    def add_answers_to_frame(self):
        i = 0
        if self.qanda.answer_type == 'r':
            self.answer_buttons_vars.append(IntVar())
            for a in self.qanda.answers:
                b = ttk.Radiobutton(self, text=a.rstrip(), variable=self.answer_buttons_vars[0], value=i,
                                    style='BT.TRadiobutton')
                b.grid(row=i, column=1, padx=10, pady=5, sticky='nsew')
                i += 1
                self.answer_buttons.append(b)

        else:
            for a in self.qanda.answers:
                self.answer_buttons_vars.append(BooleanVar())
                b = ttk.Checkbutton(self, text=a.rstrip(), variable=self.answer_buttons_vars[i], onvalue=True,
                                    offvalue=False, style='BT.TCheckbutton')
                b.grid(row=i, column=1, padx=10, pady=5, sticky='nsew')
                i += 1
                self.answer_buttons.append(b)

    def clear_frame(self):
        for child in self.winfo_children():
            child.destroy()

    def calculate_height(self):
        '''Calculates the height of the frame inside the canvas (self).'''

        scroll_frame = self.master.master

        if self.prev_scroll_frame_height == scroll_frame.winfo_height():
            # Grow or shrink down the scrollable frame according to the qanda length
            if self.winfo_reqheight() > scroll_frame.winfo_height():
                height = self.winfo_reqheight()
            else:
                height = scroll_frame.winfo_height() - 2

        # window got smaller
        elif self.prev_scroll_frame_height > scroll_frame.winfo_height():
            # Grow or shrink down the scrollable frame according to the qanda length
            if self.winfo_reqheight() > scroll_frame.winfo_height():
                height = int(self.prev_scroll_frame_height / scroll_frame.winfo_height() * self.winfo_height() * 1.35)
            else:
                # height = scroll_frame.winfo_height() - 2
                height = scroll_frame.winfo_height() - 2

        # window got larger
        else:
            # Grow or shrink down the scrollable frame according to the qanda length
            if self.winfo_reqheight() > scroll_frame.winfo_height():
                height = int(self.prev_scroll_frame_height / scroll_frame.winfo_height() * self.winfo_height() * 0.8)
            else:
                # height = scroll_frame.winfo_height() - 2
                height = scroll_frame.winfo_height() - 2

        return height

    def update_size(self):
        '''This is called on window resize and it changes the internal frame's width and the text wraplengths.'''

        c = self.master
        scroll_frame = self.master.master

        # Update the window
        scroll_frame.master.update()

        # print('self.prev_scroll_frame_height', self.prev_scroll_frame_height)

        # special condition for start
        if self.start_counter < 2:
            # Grow or shrink down the scrollable frame according to the qanda length
            if self.winfo_reqheight() > scroll_frame.winfo_height():
                height = self.winfo_reqheight()
            else:
                height = scroll_frame.winfo_height() - 2

            self.start_counter += 1
        else:
            height = self.calculate_height()

        self.prev_scroll_frame_height = scroll_frame.winfo_height()

        # print('self.winfo_reqheight', self.winfo_reqheight())
        # print('self.winfo_height', self.winfo_height())
        # print('scroll_frame.winfo_reqheight', scroll_frame.winfo_reqheight())
        # print('scroll_frame.winfo_height', scroll_frame.winfo_height())
        # print('height', height)

        width = scroll_frame.winfo_width()

        # Recreate internal frame to resize it
        # -1 and + 2 for height, because otherwise strange 1 px black borders appear when an answer is clicked
        c.create_window((0, -1), window=self, anchor="nw", width=width, height=height + 2)

        # Calculate an approximate value to change wraplength to
        if width > 1000:
            wl = width // 3 + 50
        else:
            wl = width // 3 + 20

        wls = str(wl) + 'px'
        self.style.configure('BT.TLabel', wraplength=wls)

        wls = str(wl - 30) + 'px'
        # Because you can't normally set wraplength on a ttk.Radiobutton or ttk.Checkbutton
        # You have to use states to change the style to the same value, regardless of state
        self.style.map('BT.TRadiobutton', wraplength=[('active', wls), ('!active', wls)])
        self.style.map('BT.TCheckbutton', wraplength=[('active', wls), ('!active', wls)])

        c.configure(scrollregion=(0, 0, width, height))

        # scroll frame back to the top
        c.yview_moveto(0.0)

    def rebuild_frame(self, load_new_qanda=False):
        '''Refresh frame by removing and then readding elements.'''

        self.clear_frame()
        self.answer_buttons = []
        self.answer_buttons_vars = []

        if load_new_qanda:
            self.qanda = self.qloader.load_random_qanda()

        self.add_question_to_frame()
        self.add_answers_to_frame()
        self.update_size()

    def show_correct_answers(self):
        '''Colors the chosen answer(s) red if incorrect and colors the correct answer(s) green.'''

        if self.qanda.answer_type == 'r':
            self.answer_buttons[self.answer_buttons_vars[0].get()].configure(style='BGRed.BT.TRadiobutton')
            for ca in self.qanda.correct_answers:
                self.answer_buttons[ca].configure(style='BGGreen.BT.TRadiobutton')

        else:
            i = 0
            for ab in self.answer_buttons:
                if self.answer_buttons_vars[i].get():
                    if i in self.qanda.correct_answers:
                        ab.configure(style='BGGreen.BT.TCheckbutton')
                    else:
                        ab.configure(style='BGRed.BT.TCheckbutton')
                elif i in self.qanda.correct_answers:
                    ab.configure(style='BGGreen.BT.TCheckbutton')
                else:
                    ab.configure(style='BGGray.BT.TCheckbutton')

                i += 1
