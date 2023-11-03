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

import os
import random
from qanda import Qanda


class Qloader:
    '''This class loads files from a folder and converts them to Qanda objects.'''

    def __init__(self, folder):
        self.file_list = []
        self.load_file_list(folder)

    def load_file_list(self, folder):
        with os.scandir(folder) as it:
            for entry in it:
                self.file_list.append(entry)

    def read_file(self, file_path):
        with open(file_path, 'r') as file:
            file_txt = file.read()
        return file_txt

    def load_qanda(self, file_path):
        qanda_text = self.read_file(file_path)
        qanda_text = 'Q' + file_path.name.rstrip('.tx') + ': ' + qanda_text
        qanda_parts = qanda_text.split('@\n')
        return Qanda(qanda_parts[0].rstrip(), qanda_parts[1].rstrip(), qanda_parts[2:-1],
                     list(map(int, qanda_parts[-1].rstrip().split(' '))))

    def load_random_qanda(self):
        random_file = random.choice(self.file_list)
        return self.load_qanda(random_file)
