# -*- coding: utf-8 -*-
"""
@author: aclute & shaka
"""

class Produit:
    """ Cette classe modélise la notion de produit dans un supermarché.

    Un produit est décrit par un identifiant textuel (SODA_01), un intitulé (Sprite) et un prix (3).
    La classe est immuable: les variables d'instance sont "privatisée" et accès uiquement en lecture.
    La notion d'égalité porte seulement sur l'identifiant du produit.
    Le calcul du code de hachage doit être implémenté.
    """
    _id_produit: str
    _intitule: str
    _prix: float 
    
    def __init__(self, id_produit: str, intitule: str, prix: float) -> None:
        """ La fonction constructrice initialise les trois variables d'instance
        
        :param id_produit: un identifiant textuel (exemple: SODA_01)
        :param intitule: un intitulé (exemple: "Sprite")
        :param prix: un nombre réel
        """
        self._id_produit = id_produit
        self._intitule = intitule
        self._prix = prix
        
    @property
    def id_produit(self) -> str:
        """ accès lecture à l'identifiant du produit
        
        :return: l'identifiant
        """
        return self._id_produit
    
    @property
    def intitule(self) -> str:
        """ accès lecture à l'intitulé
        
        :return: l'intitulé
        """
        return self._intitule
    
    @property
    def prix(self) -> float:
        """ accès lecture au prix
        
        :return: le prix
        """
        return self._prix
    
    def __eq__(self, autre: object) -> bool:
        """ l'égalité ne porte que sur les identifiants des deux produits.
        
        :param autre: un produit (ou autre chose)
        :return: bolléenne indiquant l'égalité'
        """
        if not isinstance(autre, Produit):
            return NotImplemented

        return self._id_produit == autre._id_produit
    
    def __hash__(self) -> int:
        """ le code de hachage doit être cohérent avec la notion d'égalité.
        Le code de hachage doit être identique tout au long de la durée de vie de l'objet.
        '
        :return: le code de hachage
        """
        return hash(self._id_produit)
    
    def __str__(self) -> str:
        """ une chaine représentant l'objet
        
        :return: exemple "SODA_01: Sprite - 3 euros"
        """
        return f"{self._id_produit} : {self._intitule} - {self._prix} euro{'' if self._prix <= 1 else 's'}"