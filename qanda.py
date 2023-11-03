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


class Qanda:
    '''
    Class to represent a test question.
    It includes a question, a answer type (c for checkbox / multiple choice, r for radio / single choice),
    the answers and the correct answers, separated by an @ and a newline.
    '''

    question = ''
    answer_type = ''
    answers = []
    correct_answers = []

    def __init__(self, question, answer_type, answers, correct_answers):
        self.question = question
        self.answer_type = answer_type
        self.answers = answers
        self.correct_answers = correct_answers

    def __str__(self):
        qanda_str = 'Question:\n'
        qanda_str += self.question
        qanda_str += '\n\n'
        qanda_str += 'Answer type: ' + 'radio' if self.answer_type == 'r' else 'checkbox'
        qanda_str += '\n\n'
        i = 1
        for a in self.answers:
            qanda_str += f'Answer {i}:\n'
            qanda_str += a
            i += 1
        qanda_str += '\n'
        qanda_str += 'Correct answer: ' + ' '.join(self.correct_answers)
        return qanda_str
