#  !/usr/bin/python
# -*- coding: utf-8 -*-
"""
This module manage definition and representation of
product, category, brand, store, favorite, productbrand,
productcategory and productstore
"""


class Product:
    """A class to define and represent a product"""

    def __init__(self,
                 idProduct=None,
                 name=None,
                 description=None,
                 nutriscore=None,
                 url=None,
                 brands=None,
                 stores=None,
                 categories=None,
                 ):
        self.idProduct = idProduct
        self.name = name
        self.description = description
        self.nutriscore = nutriscore
        self.url = url
        self.brands = brands
        self.stores = stores
        self.categories = categories

    def __repr__(self):
        """display of product more userfrienldy.."""

        return f"""nom        : {self.name}
        description: {self.description}
        nutriscore  : {self.nutriscore}
        lien url  : <{self.url}>
        Marque(s)     : {self.brands}
        Magasin(s)     : {self.stores}
        Categories : {self.categories}\n"""


class Category:
    """A class to define and represent a Category """

    def __init__(self, idCategory=None, name=None):
        self.idCatecory = idCategory
        self.name = name

    def __repr__(self):
        """display of category more userfrienldy.."""

        return f"{self.name}"


class Brand:
    """A class to define and represent a Brand """

    def __init__(self, idBrand=None, name=None):
        self.idBrand = idBrand
        self.name = name

    def __repr__(self):
        """display of brand more userfrienldy.."""

        return f"{self.name}"


class Store:
    """A class to define and represent a store """

    def __init__(self, idStore=None, name=None):
        self.idStore = idStore
        self.name = name

    def __repr__(self):
        """display of a store more userfrienldy.."""

        return f"{self.name}"


class Favorite:
    """A class to define and represent a favorite """

    def __init__(self, idProductOrigin=None,
                 idProductSubstitute=None,
                 requestDate=None):
        self.idProductOrigin = idProductOrigin
        self.idProductSubstitute = idProductSubstitute
        self.requestDate = requestDate


class ProductBrand:
    """A class to define and represent a productbrand  """

    def __init__(self, brand_idBrand=None, product_idProduct=None):
        self.brand_idBrand = brand_idBrand
        self.product_idProduct = product_idProduct


class ProductStore:
    """A class to define and represent a productstore """

    def __init__(self, product_idProduct=None, store_idStore=None):
        self.product_idProduct = product_idProduct
        self.store_idStore = store_idStore


class ProductCategory:
    """A class to define and represent a productcategory """

    def __init__(self, product_idProduct=None, category_idCategory=None):
        self.product_idProduct = product_idProduct
        self.category_idCategory = category_idCategory
