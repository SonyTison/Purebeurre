#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module content all the constant values defined for the App."""

# Number of product retrieved by page after a API call """
NBR_PRODUCT_PER_PAGE = 50  # 20, or 50, or 100, or 250, or 500 or 1000

# URL link for API call
URL = 'https://fr.openfoodfacts.org/cgi/search.pl'

# Categories used as parameters for the API OpenFoodFact request
param_categories = ['Snacks',
                    'Fromages',
                    'Boissons',
                    'Plats préparés',
                    'Tartes salées',
                    'Biscuits et gâteaux',
                    'Glaces']

# Categories family choices for the user
CATEGORIES_FOR_USER = {'1': 'Snacks',
                       '2': 'Fromages',
                       '3': 'Boissons',
                       '4': 'Plats Préparés',
                       '5': 'Tartes Salées',
                       '6': 'Biscuits et gâteaux',
                       '7': 'Glaces et sorbets'}
