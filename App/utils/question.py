# -*- coding: utf-8 -*-
#
# Python-regex.com : Regular expression as in Kodos3 but for the web
# (c) Régis FLORET 2013 and later
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

"""
The question. Ask a random question against robot
"""

__author__ = 'Regis FLORET'

import random

digits = {
    0: 'Zero',
    1: 'One',
    2: 'Two',
    3: 'Three',
    4: 'Four',
    5: 'Five',
    6: 'Six',
    7: 'Seven',
    8: 'Height',
    9: 'Nine',
}

class Question:
    """
    """
    def __init__(self):
        self.first = random.randint(0, 9)
        self.second = random.randint(0, 9)

    @property
    def answer(self):
        """
        Get the answer, usually set in a hidden input:
        eg: <input type="hidden" value="{{ question.answer }}" name="answer" />
        """
        return self.first + self.second

    @property
    def string(self):
        """
        Get the question
        """
        return "What is the sum between {first} and {second}".format(first=self.first, second=self.second)

