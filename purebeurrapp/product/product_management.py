#  !/usr/bin/python
# -*- coding: utf-8 -*-
"""This module manage selection and validation of the product
    received from API."""

from purebeurrapp.settings import NBR_PRODUCT_PER_PAGE, param_categories
from purebeurrapp.db_xchange.models import Product


class ProductCleaner:
    """
    Class responsible of the selection and validation of the product
    received from API.
    """

    def __init__(self, api_data):
        self.api_data = api_data
        self.products_list = []  # list of all the cleaned product
        self.cleaned_list = []
        self.listemp = []
        self.final_list = []

    def clean_raw_data(self):
        """Return a list of clean product  """

        for nbcat in range(len(param_categories)):
            for numprod in range(NBR_PRODUCT_PER_PAGE):
                product = {"name": "", "description": "", "nutriscore": "",
                           "url": "", "categories": "", "stores": "",
                           "brands": ""}
                try:
                    product.update({"name": self.api_data[nbcat]
                                    ["products"][numprod]["product_name"]})
                    product.update({"description": self.api_data[nbcat]
                                    ["products"][numprod]["generic_name"]})
                    if product["description"] == "":
                        product.update({"description": self.api_data[nbcat]
                                        ["products"][numprod]["product_name"]})
                    product.update({"nutriscore": self.api_data[nbcat]
                                    ["products"][numprod]["nutriscore_grade"]})
                    product.update({"url": self.api_data[nbcat]["products"]
                                    [numprod]["url"]})
                    product.update({"categories": self.api_data[nbcat]
                                    ["products"][numprod]["categories"]})
                    product.update({"stores": self.api_data[nbcat]["products"]
                                    [numprod]["stores"]})
                    product.update({"brands": self.api_data[nbcat]["products"]
                                    [numprod]["brands"]})
                except (KeyError, TypeError):
                    pass
                self.products_list.append(product)
        return self.products_list

    def valid(self, cleaned_list):
        """Return a list of product validated """

        for product in self.products_list:
            if all(product.values()):
                self.listemp.append(product)
        for product_data in self.listemp:
            product = Product(**product_data)
            self.cleaned_list.append(product)
        return self.cleaned_list
