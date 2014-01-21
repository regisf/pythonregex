# -*- coding: utf-8 -*-
#
# Python-regex.com : Regular expression as in Kodos3 but for the web
#
# (c) Régis FLORET 2013 and later - All right reserved
#

"""
Settings file for Python-regex
"""

import os

from private_settings import *

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
ROOT_TEMPLATE_PATH = os.path.join(ROOT_PATH, "templates")
STATIC_FILES = os.path.join(ROOT_PATH, "assets")
DEBUG = True

