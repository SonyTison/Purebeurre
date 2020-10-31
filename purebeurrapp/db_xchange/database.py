#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
# -*- coding: utf-8 -*-
"""This module manage the database information connexion."""

from mysql.connector import connect
from purebeurrapp import config

db = connect(
    user=config.DB_USER,
    password=config.DB_PASSWORD,
    host=config.DB_HOST,
    database=config.DB_NAME,
    charset=config.DB_CHARSET
)
