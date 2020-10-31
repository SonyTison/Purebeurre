#  !/usr/bin/python
# -*- coding: utf-8 -*-
""" Dcostring """

from datetime import datetime

from mysql.connector import Error

from purebeurrapp.db_xchange.database import db

from purebeurrapp.db_xchange.models import Product, Category, Store, Brand


class ProductManager:
    """
    Manage association product table and method
    associated
    """

    def __init__(self):
        self.table_name = "`purebeurredbv5`.`Product`"
        self.model = "Product"
        cursor = db.cursor()
        cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {self.table_name} (
                `idProduct` INT UNSIGNED NOT NULL AUTO_INCREMENT,
                `name` VARCHAR(200) NOT NULL,
                `description` VARCHAR(400) NOT NULL,
                `nutriscore` CHAR(1) NOT NULL,
                `url` VARCHAR(200) NULL,
                PRIMARY KEY (`idProduct`))
                ENGINE = InnoDB;
            """)
        cursor.close()

    def get_all(self):
        """ return all product from database"""

        cursor = db.cursor()
        cursor.execute(
            f"""
            SELECT idProduct, name, description, nutriscore, url
             FROM {self.table_name}
            """)
        collection_tuple = cursor.fetchall()
        cursor.close()
        return [Product(*data) for data in collection_tuple]

    def get_by_category(self, category_selected):
        """ return all product by category selected"""

        cursor = db.cursor()
        query = (f"""SELECT p.*,
                  GROUP_CONCAT(DISTINCT b.name SEPARATOR ", ") as Brands,
                   GROUP_CONCAT(DISTINCT s.name SEPARATOR ", ") as Stores
                    FROM {self.table_name} p
                     join productbrand prodbd
                      on p.idProduct = prodbd.Product_idProduct
                      join brand b on b.idBrand = prodbd.Brand_idBrand
                       join productstore ps
                        on ps.Product_idProduct = p.idProduct
                        join store s
                         on s.idStore = ps.Store_idStore
                         join productcategory pc
                          on pc.Product_idProduct = p.idProduct
                          join category c
                           on c.idCategory = pc.Category_idCategory
                           WHERE c.name like %s GROUP BY p.idProduct""")
        cursor.execute(query, (category_selected,))
        collection_tuple = cursor.fetchall()
        cursor.close()
        return [Product(*data) for data in collection_tuple]

    def insert_product(self, product_list):
        """ insert product in product table"""

        cursor = db.cursor()
        try:
            for i, _value in enumerate(product_list):
                query = (
                    f"""
                    INSERT INTO {self.table_name}
                     (name, description, nutriscore, url)
                      VALUES ("{product_list[i].name}",
                       "{product_list[i].description}",
                        "{product_list[i].nutriscore}",
                         "{product_list[i].url}")
                         """)
                data = product_list[i]
                cursor.execute(query, data)
                db.commit()
            cursor.close()
            print(f'Data successfully inserted in table: {self.table_name}')
        except Error as err:
            print(f'Failed to insert data in MySQL table: {err}')

    def suggest_substitute(self, product_origin, category_selected):
        """
        suggest a substitute with a better nutriscore than the product
        selected by the user.
        """

        cursor = db.cursor()
        query = (f"""SELECT p.*,
                  GROUP_CONCAT(DISTINCT b.name SEPARATOR ", ") as Brands,
                   GROUP_CONCAT(DISTINCT s.name SEPARATOR ", ") as Stores,
                    GROUP_CONCAT(DISTINCT c.name SEPARATOR ", ") as Categories
                     FROM {self.table_name} p
                      join productbrand prodbd
                       on p.idProduct = prodbd.Product_idProduct
                       join brand b
                       on b.idBrand = prodbd.Brand_idBrand
                       join productstore ps
                        on ps.Product_idProduct = p.idProduct
                        join store s
                         on s.idStore = ps.Store_idStore
                         join productcategory pc
                          on pc.Product_idProduct = p.idProduct
                          join category c
                           on c.idCategory = pc.Category_idCategory
                           WHERE
                            (p.nutriscore <= %s AND c.name like
                             '{category_selected}%')
                              GROUP BY p.idProduct""")
        cursor.execute(query, (product_origin.nutriscore,))
        result = cursor.fetchall()
        cursor.close()
        return [Product(*data) for data in result]

    def is_database_empty(self):
        """return if product table  is empty."""

        cursor = db.cursor()
        query = (f"""SELECT 1 FROM {self.table_name} LIMIT 1""")
        cursor.execute(query)
        return cursor.fetchall()

    def get_by_id(self, idprod):
        """ return a product by id"""

        cursor = db.cursor()
        query = (f"""SELECT p.*,
                  GROUP_CONCAT(DISTINCT b.name SEPARATOR ", ") as Brands,
                   GROUP_CONCAT(DISTINCT s.name SEPARATOR ", ") as Stores
                    FROM {self.table_name} p
                     join productbrand prodbd
                      on p.idProduct = prodbd.Product_idProduct
                      join brand b
                       on b.idBrand = prodbd.Brand_idBrand
                       join productstore ps
                        on ps.Product_idProduct = p.idProduct
                        join store s
                         on s.idStore = ps.Store_idStore
                         join productcategory pc
                          on pc.Product_idProduct = p.idProduct
                          join category c
                           on c.idCategory = pc.Category_idCategory
                            WHERE p.idProduct = %s""")
        cursor.execute(query, (idprod,))
        product_tuple = cursor.fetchone()
        cursor.close()
        return Product(*product_tuple)


class CategoryManager:
    """
    Class to create CAtegory table and manage the
    associated data.
    """

    def __init__(self):
        self.table_name = "`purebeurredbv5`.`Category`"
        self.model = "Category"
        self.category_list = []
        cursor = db.cursor()
        cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {self.table_name} (
                `idCategory` INT UNSIGNED NOT NULL AUTO_INCREMENT,
                `name` VARCHAR(400) NOT NULL,
                PRIMARY KEY (`idCategory`))
                ENGINE = InnoDB;
            """)
        cursor.close()

    def get_all_from_database(self):
        """ return all the category information from database"""

        cursor = db.cursor()
        cursor.execute(
            f"""
            SELECT idCategory, name FROM {self.table_name}
            """)
        collection_tuple = cursor.fetchall()
        cursor.close()
        return [Category(*data) for data in collection_tuple]

    def get_all_from_api(self, product_list):
        """return list of tuple(idcategory, idprod)"""

        list_temp2 = []
        for i, _value in enumerate(product_list):
            list_temp1 = []
            list_temp1 = product_list[i].categories.replace(', ',
                                                            ',').split(',')
            for cat in list_temp1:
                if cat not in list_temp2:
                    list_temp2.append(cat)
        self.category_list = [Category(name=cat) for cat in list_temp2]
        self.category_list = list(set(self.category_list))
        return self.category_list

    def insert_category(self, category_list):
        """insert data in table category"""

        cursor = db.cursor()
        try:
            for i, _value in enumerate(category_list):
                query = (
                    f"""INSERT INTO {self.table_name} (name)
                     VALUES ("{category_list[i].name}") """)
                data = category_list[i]
                cursor.execute(query, data)
                db.commit()
            cursor.close()
            print(f'Data successfully inserted in table: {self.table_name}')
        except Error as err:
            print(f'Failed to insert data in MySQL table: {err}')

    def get_by_id(self, idcat):
        """ return a list of category by id"""

        cursor = db.cursor()
        cursor.execute(
            f"""
            SELECT idCategory, name FROM {self.table_name}
            WHERE idCategory = %(category_id)
            """,
            {"category_id": idcat}
        )
        category_tuple = cursor.fetchone()
        cursor.close()
        return Category(*category_tuple)


class BrandManager:
    """
    Class to create Brand table and manage the
    associated data.
    """

    def __init__(self):
        self.table_name = "`purebeurredbv5`.`Brand`"
        self.model = "Brand"
        self.brand_list = []
        cursor = db.cursor()
        cursor.execute(f"""CREATE TABLE IF NOT EXISTS {self.table_name} (
            `idBrand` INT UNSIGNED NOT NULL AUTO_INCREMENT,
            `name` VARCHAR(45) NOT NULL,
            PRIMARY KEY (`idBrand`))
            ENGINE = InnoDB;
        """)
        cursor.close()

    def get_all(self):
        """ return all the brand information from database"""

        cursor = db.cursor()
        cursor.execute(
            f"""
            SELECT idBrand, name FROM {self.table_name}
            """)
        collection_tuple = cursor.fetchall()
        cursor.close()
        return [Brand(*data) for data in collection_tuple]

    def get_by_id(self, idbra):
        """ return a list of brand retrieved by id"""

        cursor = db.cursor()
        cursor.execute(
            f"""
            SELECT idBrand, name FROM {self.table_name}
            WHERE idBrand = %(brand_id)
            """,
            {"brand_id": idbra}
        )
        brand_tuple = cursor.fetchone()
        cursor.close()
        return Brand(*brand_tuple)

    def get_all_from_api(self, product_list):
        """return list of tuple(idbrand, idprod)"""

        list_temp2 = []
        for i, _value in enumerate(product_list):
            list_temp1 = []
            list_temp1 = product_list[i].brands.replace(', ',
                                                        ',').split(',')
            for bra in list_temp1:
                if bra not in list_temp2:
                    list_temp2.append(bra)
        self.brand_list = [Brand(name=bra) for bra in list_temp2]
        self.brand_list = list(set(self.brand_list))
        return self.brand_list

    def insert_brand(self, brand_list):
        """ insert data in table brand """

        cursor = db.cursor()
        try:
            for i, _value in enumerate(brand_list):
                query = (
                    f"""
                    INSERT INTO {self.table_name} (name)
                     VALUES ("{brand_list[i].name}") """)
                data = brand_list[i]
                cursor.execute(query, data)
                db.commit()
            cursor.close()
            print(f'Data successfully inserted in table: {self.table_name}')
        except Error as err:
            print(f'Failed to insert data in MySQL table: {err}')


class StoreManager:
    """
    Class to create Store table and manage the
    associated data.
    """

    def __init__(self):
        self.table_name = "`purebeurredbv5`.`Store`"
        self.model = "Store"
        self.store_list = []
        cursor = db.cursor()
        cursor.execute(f"""CREATE TABLE IF NOT EXISTS {self.table_name} (
            `idStore` INT UNSIGNED NOT NULL AUTO_INCREMENT,
            `name` VARCHAR(45) NOT NULL,
            PRIMARY KEY (`idStore`))
            ENGINE = InnoDB;
        """)
        cursor.close()

    def get_all(self):
        """ return all the store from table database """

        cursor = db.cursor()
        cursor.execute(
            f"""
            SELECT idStore, name FROM {self.table_name}
            """)
        collection_tuple = cursor.fetchall()
        cursor.close()
        return [Store(*data) for data in collection_tuple]

    def get_by_id(self, idstor):
        """ return a store by id provided """

        cursor = db.cursor()
        cursor.execute(
            f"""
            SELECT idStore, name FROM {self.table_name}
            WHERE idStore = %(store_id)
            """,
            {"idStore": idstor}
        )
        store_tuple = cursor.fetchone()
        cursor.close()
        return Store(*store_tuple)

    def get_all_from_api(self, product_list):
        """
        return tuple idprod, idstore for the association table
        """

        list_temp2 = []
        for i, _value in enumerate(product_list):
            list_temp1 = []
            list_temp1 = product_list[i].stores.replace(', ',
                                                        ',').split(',')
            for sto in list_temp1:
                if sto not in list_temp2:
                    list_temp2.append(sto)
        self.store_list = [Store(name=sto) for sto in list_temp2]
        self.store_list = list(set(self.store_list))
        return self.store_list

    def insert_store(self, store_list):
        """ insert data in store table """

        cursor = db.cursor()
        try:
            for i, _value in enumerate(store_list):
                query = (
                    f"""
                    INSERT INTO {self.table_name} (name)
                     VALUES ("{store_list[i].name}") """)
                data = store_list[i]
                cursor.execute(query, data)
                db.commit()
            cursor.close()
            print(f'Data successfully inserted in table: {self.table_name}')
        except Error as err:
            print(f'Failed to insert data in MySQL table: {err}')


class FavoriteManager:
    """
    Class to create favorite table and manage the
    associated data.
    """

    def __init__(self):
        self.table_name = "`purebeurredbv5`.`Favorite`"
        self.model = "Favorite"
        cursor = db.cursor()
        cursor.execute(f"""CREATE TABLE IF NOT EXISTS {self.table_name} (
            `idProductOrigin` INT UNSIGNED NOT NULL,
            `idProductSubstitute` INT UNSIGNED NOT NULL,
            `requestDate` DATETIME NOT NULL,
            INDEX `fk_Favorite_Product1_idx` (`idProductOrigin` ASC),
            INDEX `fk_Favorite_Product2_idx` (`idProductSubstitute` ASC),
            CONSTRAINT `fk_Favorite_Product1`
            FOREIGN KEY (`idProductOrigin`)
            REFERENCES `purebeurredbv5`.`Product` (`idProduct`)
            ON DELETE NO ACTION
            ON UPDATE NO ACTION,
            CONSTRAINT `fk_Favorite_Product2`
            FOREIGN KEY (`idProductSubstitute`)
            REFERENCES `purebeurredbv5`.`Product` (`idProduct`)
            ON DELETE NO ACTION
            ON UPDATE NO ACTION)
            ENGINE = InnoDB;
        """)
        cursor.close()

    def get_all(self):
        """ get all favorites from database"""

        cursor = db.cursor()
        cursor.execute(f"""SELECT
                        idProductOrigin, idProductSubstitute, requestDate
                         FROM {self.table_name}""")
        collection_tuple = cursor.fetchall()
        cursor.close()
        favorites = []
        for data in collection_tuple:
            idProductOrigin, idProductSubstitute, requestDate = data
            productf, substitutef = ProductManager(), ProductManager()
            product = productf.get_by_id(idProductOrigin)
            substitute = substitutef.get_by_id(idProductSubstitute)
            favorites.append((product, substitute, requestDate))
        return favorites

    def save_substitute(self, product_origin, product_substitute):
        """ save product origin and product substitute in database """

        date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor = db.cursor()
        try:
            query = (f"""INSERT INTO {self.table_name}
                      (idProductOrigin, idProductSubstitute, requestDate)
                       VALUES (%s, %s, %s)""")
            data = (product_origin.idProduct, product_substitute.idProduct,
                    date_time)
            cursor.execute(query, data)
            db.commit()
            cursor.close()
        except Error as err:
            print(f'Failed to insert data in MySQL table: {err}')


class ProductBrandManager:
    """
    Class to create Productbrand table and manage the
    associated data.
    """
    def __init__(self):
        self.table_name = "`purebeurredbv5`.`ProductBrand`"
        self.model = "ProductBrand"
        cursor = db.cursor()
        cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {self.table_name} (
                `Brand_idBrand` INT UNSIGNED NOT NULL,
                `Product_idProduct` INT UNSIGNED NOT NULL,
                PRIMARY KEY (`Brand_idBrand`, `Product_idProduct`),
                INDEX `fk_Brand_has_Product_Product1_idx`
                 (`Product_idProduct` ASC),
                INDEX `fk_Brand_has_Product_Brand_idx`
                 (`Brand_idBrand` ASC),
                CONSTRAINT `fk_Brand_has_Product_Brand`
                FOREIGN KEY (`Brand_idBrand`)
                REFERENCES `purebeurredbv5`.`Brand` (`idBrand`)
                ON DELETE NO ACTION
                ON UPDATE NO ACTION,
                CONSTRAINT `fk_Brand_has_Product_Product1`
                FOREIGN KEY (`Product_idProduct`)
                REFERENCES `purebeurredbv5`.`Product` (`idProduct`)
                ON DELETE NO ACTION
                ON UPDATE NO ACTION)
                ENGINE = InnoDB;
            """)
        cursor.close()

    def get_all_from_api(self, product_list, brand_list):
        """ return a list of tuple (idprod, name_cat) """

        list_temp2 = []
        for i in range(len(product_list)):
            list_temp1 = []
            list_temp1 = product_list[i].brands.replace(', ',
                                                        ',').split(',')
            for cat in list_temp1:
                list_temp2.append((i+1, cat))
        liste2 = [(i+1, str(brand_list[i]))
                  for i in range(len(brand_list))]
        return [(list_temp2[i][0], liste2[v][0])
                for i in range(len(list_temp2))
                for v in range(len(liste2))
                if list_temp2[i][1] == liste2[v][1]]

    def insert_productbrand(self, prodstore_list):
        """ insert data in association table productbrand"""

        cursor = db.cursor()
        try:
            for i, _value in enumerate(prodstore_list):
                query = (f"""INSERT INTO {self.table_name}
                          (product_idProduct, brand_idBrand)
                           VALUES (%s, %s)""")
                data = prodstore_list[i]
                cursor.execute(query, data)
                db.commit()
            cursor.close()
            print(f'Data successfully inserted in table: {self.table_name}')
        except Error as err:
            print(f'Failed to insert data in MySQL table: {err}')


class ProductStoreManager:
    """
    Class to create ProductSotre table and manage the
    associated data.
    """

    def __init__(self):
        self.table_name = "`purebeurredbv5`.`ProductStore`"
        self.model = "ProductStore"
        cursor = db.cursor()
        cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {self.table_name} (
                `Product_idProduct` INT UNSIGNED NOT NULL,
                `Store_idStore` INT UNSIGNED NOT NULL,
                PRIMARY KEY (`Product_idProduct`,
                 `Store_idStore`),
                INDEX `fk_Product_has_Store_Store1_idx`
                 (`Store_idStore` ASC),
                INDEX `fk_Product_has_Store_Product1_idx`
                 (`Product_idProduct` ASC),
                CONSTRAINT `fk_Product_has_Store_Product1`
                FOREIGN KEY (`Product_idProduct`)
                REFERENCES `purebeurredbv5`.`Product`
                 (`idProduct`)
                ON DELETE NO ACTION
                ON UPDATE NO ACTION,
                CONSTRAINT `fk_Product_has_Store_Store1`
                FOREIGN KEY (`Store_idStore`)
                REFERENCES `purebeurredbv5`.`Store` (`idStore`)
                ON DELETE NO ACTION
                ON UPDATE NO ACTION)
                ENGINE = InnoDB;
            """)
        cursor.close()

    def get_all_from_api(self, product_list, store_list):
        """ return a list of tuple (idprod, name_cat) """

        list_temp2 = []
        for i in range(len(product_list)):
            list_temp1 = []
            list_temp1 = product_list[i].stores.replace(', ',
                                                        ',').split(',')
            for cat in list_temp1:
                list_temp2.append((i+1, cat))
        liste2 = [(i+1, str(store_list[i]))
                  for i in range(len(store_list))]
        return [(list_temp2[i][0], liste2[v][0])
                for i in range(len(list_temp2))
                for v in range(len(liste2))
                if list_temp2[i][1] == liste2[v][1]]

    def insert_productstore(self, prodstore_list):
        """ Insert tuple (idprod, idstore in association table
        productstore """

        cursor = db.cursor()
        try:
            for i, _value in enumerate(prodstore_list):
                query = (f"""INSERT INTO {self.table_name}
                          (product_idProduct, store_idStore)
                           VALUES (%s, %s)""")
                data = prodstore_list[i]
                cursor.execute(query, data)
                db.commit()
            cursor.close()
            print(f'Data successfully inserted in table: {self.table_name}')
        except Error as err:
            print(f'Failed to insert data in MySQL table: {err}')


class ProductCategoryManager:
    """
    Manage association productcategory table and method
    associated
    """

    def __init__(self):
        self.table_name = "`purebeurredbv5`.`ProductCategory`"
        self.model = "ProductCategory"
        cursor = db.cursor()
        cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {self.table_name} (
                `Category_idCategory` INT UNSIGNED NOT NULL,
                `Product_idProduct` INT UNSIGNED NOT NULL,
                PRIMARY KEY (`Category_idCategory`,
                 `Product_idProduct`),
                INDEX `fk_Category_has_Product_Product1_idx`
                 (`Product_idProduct` ASC),
                INDEX `fk_Category_has_Product_Category1_idx`
                 (`Category_idCategory` ASC),
                CONSTRAINT `fk_Category_has_Product_Category1`
                FOREIGN KEY (`Category_idCategory`)
                REFERENCES `purebeurredbv5`.`Category` (`idCategory`)
                ON DELETE NO ACTION
                ON UPDATE NO ACTION,
                CONSTRAINT `fk_Category_has_Product_Product1`
                FOREIGN KEY (`Product_idProduct`)
                REFERENCES `purebeurredbv5`.`Product` (`idProduct`)
                ON DELETE NO ACTION
                ON UPDATE NO ACTION)
                ENGINE = InnoDB;
            """)
        cursor.close()

    def get_all_from_api(self, product_list, category_list):
        """
        return tuple (idprod, name_cat) to insert
        association table productcategory
        """

        list_temp2 = []
        for i in range(len(product_list)):
            list_temp1 = []
            list_temp1 = product_list[i].categories.replace(', ',
                                                            ',').split(',')
            for cat in list_temp1:
                list_temp2.append((i+1, cat))
        liste2 = [(i+1, str(category_list[i]))
                  for i in range(len(category_list))]
        return [(list_temp2[i][0], liste2[v][0])
                for i in range(len(list_temp2))
                for v in range(len(liste2))
                if list_temp2[i][1] == liste2[v][1]]

    def insert_productcategory(self, prodcat_list):
        """INSERT data in association table productcategory"""

        cursor = db.cursor()
        try:
            for i, _value in enumerate(prodcat_list):
                query = (
                    f"""
                    INSERT INTO {self.table_name}
                     (product_idProduct, category_idCategory)
                      VALUES (%s,%s)""")
                data = prodcat_list[i]
                cursor.execute(query, data)
                db.commit()
            cursor.close()
            print(f'Data successfully inserted in table: {self.table_name}')
        except Error as err:
            print(f'Failed to insert data in MySQL table: {err}')
