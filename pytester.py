#!/usr/bin/env python3

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
from qloader import Qloader
from qframe import QFrame

TEST_FOLDER = './test'

window = Tk()
window.title('My test app')
window.minsize(800, 600)

scroll_frame = ttk.Frame(window)
scroll_frame.pack(side='top', expand=True, fill='both')

sb = ttk.Scrollbar(scroll_frame, orient='vertical')
sb.pack(side='right', fill='y')

c = Canvas(scroll_frame)
c.pack(side='left', expand=True, fill='both')

sb.configure(command=c.yview)
c.configure(yscrollcommand=sb.set)

qanda_frame = QFrame(c, Qloader(TEST_FOLDER))
qanda_frame.rebuild_frame(load_new_qanda=True)

button_frame = ttk.Frame(window)
button_frame.configure(padding='0 10')
button_frame.pack(side='bottom', fill='x')
ttk.Button(button_frame, text='Next',
           command=lambda: qanda_frame.rebuild_frame(load_new_qanda=True)).pack(side='right', padx=10)
ttk.Button(button_frame, text='Check', command=lambda: qanda_frame.show_correct_answers()).pack(side='right', padx=10)
ttk.Button(button_frame, text='Quit', command=exit).pack(side='left', padx=10)

# Bind the scroll wheel to move the canvas
window.bind('<Button-4>', lambda event: c.yview('scroll', '-1', 'units'))
window.bind('<Button-5>', lambda event: c.yview('scroll', '1', 'units'))

c.bind('<Configure>', lambda event: qanda_frame.rebuild_frame())

window.mainloop()
