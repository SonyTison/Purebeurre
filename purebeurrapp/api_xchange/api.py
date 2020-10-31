#!/usr/bin/python
# -*- coding: utf-8 -*-
"""This module manage the request of the OpenFoodFact API."""

import requests

from purebeurrapp.settings import NBR_PRODUCT_PER_PAGE, URL, param_categories


class GetApiData:
    """Download a list of products from the OpenFoodfacts API."""

    def __init__(self):
        self.api_result = []

    def download_data(self):
        """Return products from API OpenFoodfacts by Category."""

        print("Importation des produits...")
        for param_category in param_categories:
            payload = {
                'action': 'process',
                'tagtype_0': 'categories',
                'tag_contains_0': 'contains',
                'tag_0': param_category,
                'sort_by': 'unique_scans_n',
                'countries': 'France',
                'page_size': str(NBR_PRODUCT_PER_PAGE),
                'json': True,
                }
            response = requests.get(URL, params=payload)  # API request
            self.api_result.append(response.json())
        return self.api_result
