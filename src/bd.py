# -*- coding: utf-8 -*-
"""
@author: aclute & shaka
"""
import mysql.connector as m
from mysql.connector import errorcode
from produit import Produit
from commande import Commande

def creer_connexion(): #-> connexion
    
    try:
        connexion = m.connect(host="", user="", password="", database="")
    except m.Error as err:
        
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Erreur: login ou mot de passe incorrect")
            return
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Erreur: la base de données n'existe pas")
            return
        else:
            print(err)
            return
    
    return connexion

def charger_liste_produit() -> list[Produit]: #[(idProduit1, intitule1, prix1), (idProduit2, intitule2, prix2), (), ...]
    connexion = creer_connexion()
    curseur = connexion.cursor()
    curseur.execute("SELECT * FROM produit ORDER BY intitule;")
    liste_produit = curseur.fetchall()
    curseur.close()
    connexion.close()

    return ([Produit(t[0], t[1], t[2]) for t in liste_produit])

def charger_commande(id_commande):
    connexion = creer_connexion()
    curseur = connexion.cursor()
    curseur.execute(f"SELECT dateCommande, dateRetrait FROM commande WHERE idCommande = {id_commande};")
    commande = curseur.fetchone()
    curseur.close()
    connexion.close()
    
    return commande

def charger_liste_commande(email_client):
    connexion = creer_connexion()
    curseur = connexion.cursor()
    requete = f"""
        SELECT idCommande, dateCommande, dateRetrait
        FROM commande
        WHERE mailClient = '{email_client}' AND dateRetrait >= NOW()
        ORDER BY dateCommande DESC, dateRetrait DESC;
        """
    curseur.execute(requete)
    liste_commande = curseur.fetchall()
    curseur.close()
    connexion.close()

    return liste_commande

def charger_produits_commande(id_commande):
    connexion = creer_connexion()
    curseur = connexion.cursor()
    requete = f"""
        SELECT idProduit, intitule, prix, quantite
        FROM contient JOIN produit USING(idProduit)
        WHERE idCommande = {id_commande}
        ORDER BY intitule;
        """
    curseur.execute(requete)
    liste_produit_commande = curseur.fetchall()
    curseur.close()
    connexion.close()

    return ([(Produit(t[0], t[1], t[2]), t[3]) for t in liste_produit_commande])

def sauvegarder_ajout_commande(commande:Commande) -> None:
    connexion = creer_connexion()
    curseur = connexion.cursor()
    requete_commande = f"""INSERT INTO commande(dateCommande, dateRetrait, mailClient)
                           VALUES{(commande.date_commande, commande.date_retrait, commande.mail_client)};"""
    curseur.execute(requete_commande)
    commande.id_commande = curseur.lastrowid

    remplir_contient(connexion, commande)

    connexion.commit()
    curseur.close()
    connexion.close()

def sauvegarder_modification_commande(commande:Commande):

    connexion = creer_connexion()
    curseur = connexion.cursor()

    curseur.execute(f"""UPDATE commande SET dateCommande = '{commande.date_commande}', dateRetrait = '{commande.date_retrait}' 
                        WHERE idCommande = {commande.id_commande};""")

    curseur.execute(f"DELETE FROM contient WHERE idCommande = {commande.id_commande};")

    remplir_contient(connexion, commande)    
    
    connexion.commit()
    curseur.close()
    connexion.close()

def supprimer_commande(id_commande:int):

    connexion = creer_connexion()
    curseur = connexion.cursor()
    curseur.execute(f"DELETE FROM contient WHERE idCommande = {id_commande};")
    curseur.execute(f"DELETE FROM commande WHERE idCommande = {id_commande};")
    connexion.commit()
    curseur.close()
    connexion.close()

def remplir_contient(connexion, commande:Commande):

    curseur = connexion.cursor()
    for (produit, quantite) in commande:
        requete = f"""INSERT INTO contient(idProduit, idCommande, quantite)
                      VALUES{(produit.id_produit, commande.id_commande, quantite)};"""
        curseur.execute(requete)
    connexion.commit()
    curseur.close()