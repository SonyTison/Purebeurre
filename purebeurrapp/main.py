#!/usr/bin/python
# -*- coding: utf-8 -*-

""" PureBeurrApp Application: The Aim of this application is to
suggest a healthiest food than the original choice of a user.

Script Python
Files: settings.py, config.py,  __main__.py, api.py, models.py, managers.py,
       database.py, product_management.py, views.py
"""

from .api_xchange.api import GetApiData
from .product.product_management import ProductCleaner
from .db_xchange.managers import ProductManager, CategoryManager
from .db_xchange.managers import BrandManager
from .db_xchange.managers import StoreManager
from .db_xchange.managers import ProductCategoryManager
from .db_xchange.managers import ProductBrandManager
from .db_xchange.managers import ProductStoreManager
from .user_interface.views import App


def main():
    """Method to launch the app."""

    content = ProductManager()
    if not content.is_database_empty():
        # Launching API request
        get_api_data = GetApiData()
        api_data = get_api_data.download_data()
        # Validation and Cleaning
        api_data_to_clean = ProductCleaner(api_data)
        list_data_to_valid = api_data_to_clean.clean_raw_data()
        product_validated = api_data_to_clean.valid(list_data_to_valid)
        # Creation and Loading Table Product
        product_to_load = ProductManager()
        product_to_load.insert_product(product_validated)
        # Creation and Loading Table Category
        category_to_load = CategoryManager()
        category_list = category_to_load.get_all_from_api(product_validated)
        category_to_load.insert_category(category_list)
        # Creation and Loading Table Brand
        brand_to_load = BrandManager()
        brand_list = brand_to_load.get_all_from_api(product_validated)
        brand_to_load.insert_brand(brand_list)
        # Creation and Loading Table Store
        store_to_load = StoreManager()
        store_list = store_to_load.get_all_from_api(product_validated)
        store_to_load.insert_store(store_list)
        # Creation and Loading Table ProductCategory
        prodcat_to_load = ProductCategoryManager()
        prodcat_list = prodcat_to_load.get_all_from_api(product_validated,
                                                        category_list)
        prodcat_to_load.insert_productcategory(prodcat_list)
        # Creation and Loading Table ProductStore
        prodstore_to_load = ProductStoreManager()
        prodstore_list = prodstore_to_load.get_all_from_api(product_validated,
                                                            store_list)
        prodstore_to_load.insert_productstore(prodstore_list)
        # Creation and Loading Table ProductBrand
        prodbrand_to_load = ProductBrandManager()
        prodbrand_list = prodbrand_to_load.get_all_from_api(product_validated,
                                                            brand_list)
        prodbrand_to_load.insert_productbrand(prodbrand_list)
    session = App()
    session.start()


if __name__ == '__main__':
    main()
