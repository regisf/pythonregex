# -*- coding: utf-8 -*-
#
# Python-regex.com : Regular expression as in Kodos3 but for the web
#
# (c) Régis FLORET 2013 and later - All right reserved
#

"""
Create the connection for all models

"""
from pymongo import MongoClient
import settings

_client = MongoClient('localhost')
database = _client[settings.DB_NAME]


