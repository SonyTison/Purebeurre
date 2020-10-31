#!/usr/bin/python
# -*- coding: utf-8 -*-
"""This module manage all the input and print from the user."""

import random

from colorama import Fore, init

from purebeurrapp.db_xchange.managers import ProductManager, FavoriteManager
from purebeurrapp.settings import CATEGORIES_FOR_USER

init()


class App:
    """Management of the application."""

    def __init__(self):
        self.launched = True
        self.display_prod_list = {}
        self.id_product_origin = ()
        self.product_origin = None
        self.product_substitute = None
        self.category_selected = None
        self.display_substitute_list = {}

    def intro(self):
        """This method will manage the first screen displayed after launching
        the program."""

        print("\n\n")
        print("                               -----------------------------")
        print("                                Bienvenue sur PureBeurrApp !")
        print("                               -----------------------------")
        print("\n\n")
        print(Fore.YELLOW + " Vous avez décidé de mieux consommer "
              "pour votre santé,"
              " PureBeurrApp (basé sur l'API OpenFoodFact)\n"
              " vous aidera à selectionner les meilleurs produits.")
        print(Fore.RESET)

    def category_choice(self):
        """display category choice."""
        print(Fore.CYAN)
        print("\n        *** Que souhaitez-vous faire ? *** \n\n")
        print(Fore.RESET)
        print("        1  - Quel aliment souhaitez-vous remplacer ?")
        print("        2  - Retrouver mes aliments substitués.")
        print("        3  - Quitter")
        authorised_answer_list, user_answer = ['1', '2', '3'], '0'
        while user_answer not in authorised_answer_list:
            print(Fore.GREEN)
            user_answer = input("       Entrer votre choix : ")
            print(Fore.RESET)
        if user_answer == '1':
            self.category_choice_display()
            self.display_selected_prod()
            self.display_substitute()
            self.display_save_substitute()
        elif user_answer == '2':
            self.favorites_display()
        elif user_answer == '3':
            self.quit_message()
            self.launched = False
        else:
            self.category_choice()
            print(user_answer)
        print(Fore.RESET)

    def category_choice_display(self):
        """display the choice of the categories."""

        print("       ---------------------------------")
        print("                  Catégories ")
        print("       ---------------------------------\n")
        for key, value in CATEGORIES_FOR_USER.items():
            print(f"          {key} -  {value}")
        authorised_answer_list, user_answer = [
            '1', '2', '3', '4', '5', '6', '7'], None
        while user_answer not in authorised_answer_list:
            print(Fore.GREEN)
            user_answer = input("       Entrer un numero de categorie : ")
            print(Fore.RESET)
        if user_answer in authorised_answer_list:
            self.category_selected = CATEGORIES_FOR_USER[user_answer]
            self.display_prod_by_category()
        else:
            self.category_choice_display()

    def display_prod_by_category(self):
        """display 7 products from the selected category."""

        print("       -------------------------------------")
        print(f"         Categorie {self.category_selected}")
        print("       ------------------------------------- \n")
        temp_var1 = ProductManager()
        result_1 = temp_var1.get_by_category(self.category_selected)
        selected = random.sample(result_1, 7)
        for index, product in enumerate(selected, 1):
            print(f"        {index} - Nom        : {product.name}"
                  f"  (Marque: * {product.brands} *)  -> Disponible chez:"
                  f" ({product.stores})\n"
                  f"            Description: {product.description}"
                  f"   (Nutriscore : {product.nutriscore})\n"
                  f"            Lien url   : {product.url}\n")
            self.display_prod_list.update({index: product})

    def display_selected_prod(self):
        """ask to the user to choose a product."""

        authorised_answer_list = ['1', '2', '3', '4', '5', '6', '7']
        user_answer = None
        while user_answer not in authorised_answer_list:
            print(Fore.GREEN)
            user_answer = input(
                "       Entrer un numéro de produit à remplacer: ")
            print(Fore.RESET)
        if user_answer in authorised_answer_list:
            self.product_origin = self.display_prod_list[int(user_answer)]
            return self.product_origin

    def display_substitute(self):
        """display 3 substitutes suggested."""
        cat_select = None
        cat_select = self.category_selected
        self.display_prod_list,  self.display_substitute_list = {}, {}
        result1, selected1 = None, None
        temp_var = ProductManager()
        result1 = temp_var.suggest_substitute(self.product_origin, cat_select)
        selected1 = random.sample(result1, 3)
        for index, product in enumerate(selected1, 1):
            print(f"        {index} - Nom        : {product.name}"
                  f"  (Marque: * {product.brands} *)  "
                  f"-> Disponible chez: ({product.stores})\n"
                  f"            Description: {product.description}"
                  f"   (Nutriscore : {product.nutriscore})\n"
                  f"            Lien url   : {product.url}\n")
            self.display_substitute_list.update({index: product})

    def display_save_substitute(self):
        """suggest to save a substitute."""

        authorised_answer_list, user_answer = ['N', 'n', '1', '2', '3'], None
        while user_answer not in authorised_answer_list:
            print(Fore.GREEN)
            user_answer = input(
                "\n       Enter le numéro du produit à sauvegarder ou N "
                "pour une nouvelle recherche. [1/2/3/N] :").strip()
            print(Fore.RESET)
        if user_answer in ['1', '2', '3']:
            temp_var = FavoriteManager()
            product_origin = self.product_origin
            product_substitute = self.display_substitute_list[int(user_answer)]
            temp_var.save_substitute(product_origin, product_substitute)
            print(' \n       Sauvegarde effectuée avec succès! \n')
        elif user_answer == ('N' or 'n'):
            print("       OK! :)")

    def start(self):
        """Main loop of the application."""

        self.intro()
        while self.launched:
            self.category_choice()

    def favorites_display(self):
        """display favorites content."""

        temp_var1 = FavoriteManager()
        result_1 = temp_var1.get_all()
        if not result_1:
            print("       Vous n'avez pas encore d'enregistrement"
                  " dans vos favoris. ;)")
        else:
            print(Fore.YELLOW)
            print("       ----------------------------")
            print("        Consultations des favoris :")
            print("       ----------------------------\n")
            print(Fore.RESET)
        for index, product in enumerate(result_1, 1):
            print(f"        {index} - Choix initial        : {product[0].name}"
                  f" (Nutriscore : {product[0].nutriscore})\n"
                  f"            Suggestion validée   : "
                  f"{product[1].name} (Nutriscore : {product[1].nutriscore})\n"
                  f"            Date de consultation : "
                  f"{product[2].strftime('%Y-%m-%d %H:%M:%S'):>10}\n")

    def quit_message(self):
        """quit the app."""

        print(Fore.YELLOW)
        print("\n       ***  Merci pour l'utilisation de nos services."
              " A tout bientôt!  **** \n")
        print(Fore.RESET)
