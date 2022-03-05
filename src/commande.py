# -*- coding: utf-8 -*-
"""
@author: aclute & shaka
"""

from datetime import date, datetime
from types import NoneType
from typing import Generator

from produit import Produit

class Commande:
    """ Cette classe modélise la notion de commande dans un supermarché.
    
    Une commande est décrit par un identifiant entier (autoincrémenté par la BD),
    une date de commande (datetime), une date de retrait (date),
    le mail du client (une chaine de caractères), 
    un dictionnaire qui associe à chaque produit la quantité commandée.
    """
    _id_commande: int
    _date_commande: datetime
    _date_retrait: date
    _mail_client: str
    _produit_quantite: dict[Produit, int]
    
    def __init__(self) -> None:
        """ La fonction constructrice initialise le dictionnaire vide
        et appelle la méthode vider
        """
        self._produit_quantite = {}
        self.vider()
        
    def vider(self) -> None:
        """ Cette méthode vide le dictionnaire _produit_quantite
        """
        self._produit_quantite.clear()
        
    def ajouter_produit(self, produit: Produit, quantite: int = 1) -> bool:
        """ Cette méthode ajoute un produit dans le dictionnaire
        si il n'existe pas, modifie la quantité associée à un produit déjà existant,
        supprime un produit si la nouvelle quantité vaut 0.
        
        :param produit: le produit à ajouter, supprimer ou modifier quantité
        :param quantite: la nouvelle quantité (0 suprression du produit)
        :return: False si la quantité est négative, True sinon
        """

        self._produit_quantite[produit] = quantite
        
        if self._produit_quantite[produit] == 0:
            self._produit_quantite.pop(produit)

        return quantite >= 0

    @property
    def id_commande(self) -> int:
        """ accès lecture à l'identifiant entier de la commande (un entier produit par la bd)
        
        :return: l'identifiant
        """
        return self._id_commande
    
    @id_commande.setter
    def id_commande(self, id_commande: int) -> None:
        """ accès en écriture à l'identifiant de la commande
        
        :param id_commande: l'identifiant entier
        """
        self._id_commande = id_commande
    
    @property
    def date_commande(self) -> datetime:
        """ accès lecture à la date de commande
        
        :return: la date de commande (datetime)
        """
        return self._date_commande
    
    def finaliser(self) -> bool:
        """ cette méthode finalise une commande.
        A appeler avant une insertion de la commande dans la base de données.
        Elle vérifie que la date de retrait est fixée et est postérieure à la date actuelle,
        que le mail client existe et est de longueur différente de 0,
        et enfin que la commande contient au moins un produit.
        
        La date de la commande est alors fixée à la datetime actuelle.
        
        :return: True si tout est OK (et la date de commande a été fixée), False sinon
        """
        auj = datetime.today().date()
        if self._date_retrait > auj and "@" in self._mail_client and len(self._produit_quantite) >= 1:
            self._date_commande = auj.strftime("%Y-%m-%d")
            self._date_retrait = self._date_retrait.strftime("%Y-%m-%d")
            return True
        else:
            return False
    
    @property
    def date_retrait(self) -> date:
        """ accès lecture à la date de retrait
        
        :return: date de retrait de la commande (date)
        """
        return self._date_retrait
        
    @date_retrait.setter
    def date_retrait(self, date_retrait) -> None:
        """ accès en écriture à la date de retrait
        
        :param date_retrait: la date de retrait
        """
        
        self._date_retrait = date_retrait
    
    @property
    def mail_client(self) -> str:
        """ accès lecture au mail du client
        
        :return: le mail
        """
        return self._mail_client
        
    @mail_client.setter
    def mail_client(self, mail_client) -> None:
        """ accès en écriture au mail du client.
        On pourra utiliser strip pour supprimer les espaces aux extrémités.
        
        :param mail_client: le mail du client
        """
        self._mail_client = mail_client.strip()
    
    @property
    def prix_total(self) -> float:
        """ accès lecture au prix total de la commande
        
        :return: le prix total de la commande
        """
        return sum( (key.prix*value for key, value in self._produit_quantite.items()) )
    
    def __len__(self) -> int:
        """ nombre de produits distincts dans la commande (on ne compte pas les doublons)
        
        :return: le nombre de produits distincts
        """
        return len(self._produit_quantite)
    
    def __iter__(self) -> Generator[tuple[Produit, int], None, None]:
        """ renvoie un générateur (yield) qui produit des tuples (produit, quantité)
        
        :return: un tuple (produit, quantité)
        """
        for k, v in self._produit_quantite.items():
            yield (k, v)