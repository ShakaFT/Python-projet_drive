from produit import Produit
from commande import Commande
from bd import *
import tkinter
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import DateEntry
import smtplib
import ssl
from datetime import datetime, date, timedelta

class App:

    _is_setup:bool = False
    _root:tkinter
    _mail_client:str

    @staticmethod
    def launch_app():
        if not App._is_setup:
            App._root = root = Tk()
            App._is_setup = True
        return App()
    
    def __init__(self):
        App._root.resizable(False, False)
        IHM_connexion.launch_IHM_connexion()
        App._root.mainloop()
    
    def root():
        return App._root
    
    @property
    def mail_client():
        return App._mail_client
    
    @mail_client.setter
    def mail_client(mail_client):
        App._mail_client = mail_client


class IHM_connexion:

    _is_setup = False
    _root:tkinter

    @staticmethod
    def launch_IHM_connexion():
        if not IHM_connexion._is_setup:
            IHM_connexion._root = App.root()
            IHM_connexion._is_setup = True
        return IHM_connexion()

    def __init__(self):
        
        IHM_connexion._root.title("Connexion")

        #Création des styles
        style = ttk.Style()
        style.configure('frame.TFrame', background="SkyBlue3")
        style.configure('titre.TLabel', font="Arial 12 bold", background="SkyBlue3")
        style.configure('sous_titre.TLabel', font="Arial 10 bold", background="SkyBlue3")

        #Création de la frame principale
        self.frame = ttk.Frame(IHM_connexion._root, padding="3 3 3 3", style="frame.TFrame")
        self.frame.grid(row=0, column=0, stick="nsew")

        #Création/Mise en page des Widgets
        #---ligne 0
        label_titre = ttk.Label(self.frame, text="Connectez-vous !", style="titre.TLabel")
        label_titre.grid(row=0, column=0, columnspan=2, padx=100, pady=10)

        #---ligne 1
        label_email = ttk.Label(self.frame, text="Email", style="sous_titre.TLabel")
        label_email.grid(row=1, column=0, sticky="e", padx=5, pady=10)

        self.entry_email = Entry(self.frame, bd=4)
        self.entry_email.grid(row=1, column=1, sticky="w", padx=5, pady=10)  
        self.entry_email.after(1, self.entry_email.focus_set)

        #---ligne 2
        button_connexion = ttk.Button(self.frame, text="Se connecter", command=self.connexion)
        button_connexion.grid(row=2, column=0, columnspan=2, pady=10)

        #On centre la fenêtre au milieu de l'écran
        IHM_connexion._root.geometry(center_window(self.frame))

        #En cas de fermeture de la fenêtre
        IHM_connexion._root.protocol("WM_DELETE_WINDOW", self.close)

    def connexion(self):

        mail_client = self.entry_email.get().replace(" ", "")
        
        if mail_client == "":
            messagebox.showerror("Email manquant", "Veuillez entrer un email.")
            return
        elif "@" not in mail_client:
            messagebox.showerror("Email invalide", "Veuillez entrer un email valide.")
            return
        
        App.mail_client = mail_client
        self.frame.destroy()
        IHM_accueil.launch_IHM_accueil()
        
    def close(self):

        IHM_connexion._root.quit()


class IHM_accueil:

    _is_setup = False
    _root:tkinter
    _mail_client:str

    @staticmethod
    def launch_IHM_accueil():
        if not IHM_accueil._is_setup:
            IHM_accueil._mail_client = App.mail_client
            IHM_accueil._root = App.root()
            IHM_accueil._is_setup = True
        return IHM_accueil()

    def __init__(self):

        IHM_accueil._root.title("Accueil drive")
    
        #Création des styles
        style = ttk.Style()
        style.configure('frame.TFrame', background="SkyBlue3")
        style.configure('titre.TLabel', font="Arial 12 bold", background="SkyBlue3")
        style.configure('sous_titre.TLabel', font="Arial 10 bold", background="SkyBlue3", foreground="snow")
        style.configure('button.TButton', width=22)

        #Création de la frame principale
        self.frame = ttk.Frame(IHM_accueil._root, padding="5 5 5 5", style='frame.TFrame')
        self.frame.grid(row=0, column=0, stick="nsew")

        #Création/Mise en page des Widgets
        #---ligne 0
        button_deconnexion = ttk.Button(self.frame, text="Se déconnecter", command=self.deconnexion)
        button_deconnexion.grid(row=0, column=1, sticky="e", padx=5, pady=2)

        #---ligne 1
        label_titre2 = ttk.Label(self.frame, text="Que souhaitez-vous faire ?", style="titre.TLabel")
        label_titre2.grid(row=1, column=0, columnspan=2)

        #---ligne 2
        label_sous_titre1 = ttk.Label(self.frame, text="Voir mes commandes", style="sous_titre.TLabel")
        label_sous_titre1.grid(row=2, column=0, padx=5, pady=5)

        label_sous_titre2 = ttk.Label(self.frame, text="Passer une commande", style="sous_titre.TLabel")
        label_sous_titre2.grid(row=2, column=1, padx=5, pady=5)

        #---ligne 3
        button_voir_commande = ttk.Button(self.frame, text="Voir commandes", command=self.voir_commande, style="button.TButton")
        button_voir_commande.grid(row=3, column=0, padx=5, pady=5)
        
        button_passer_commande = ttk.Button(self.frame, text="Passer commande", command=self.passer_commande, style="button.TButton")
        button_passer_commande.grid(row=3, column=1, padx=5, pady=5)

        #On centre la fenêtre au milieu de l'écran
        IHM_accueil._root.geometry(center_window(self.frame))

        #En cas de fermeture de la fenêtre
        IHM_accueil._root.protocol("WM_DELETE_WINDOW", self.deconnexion)

    def deconnexion(self):

        App.mail_client = ""
        self.frame.destroy()
        IHM_accueil._is_setup = False
        IHM_passer_commande._is_setup = False
        IHM_connexion.launch_IHM_connexion()

    def voir_commande(self):
        
        liste_commandes = charger_liste_commande(IHM_accueil._mail_client)
        if liste_commandes == []:
            messagebox.showerror("Aucune commande", "Vous n'avez aucune commande en cours")
            return

        self.frame.destroy()
        IHM_voir_commande()

    def passer_commande(self):

        self.frame.destroy()
        IHM_passer_commande.launch_IHM_passer_commande()

class IHM_voir_commande:

    _root:tkinter
    _mail_client:str

    def __init__(self, liste_commandes:list=[]):

        #Affectation des variables d'instance
        self._root = App.root()
        self._root.title("Mes commandes")
        self._mail_client = App.mail_client
        self.liste_commandes = liste_commandes

        #Création des styles
        style = ttk.Style()
        style.theme_use("default")
        style.configure("frame.TFrame", background="SkyBlue3")
        style.configure('titre.TLabel', font="Arial 12 bold", background="SkyBlue3")
        style.configure('sous_titre.TLabel', font="Arial 10 bold", background="SkyBlue3")
        style.configure('treeview.Treeview', background="grey85")

        #Création de la frame principale
        self.frame = ttk.Frame(self._root, padding="3 3 3 3", style="frame.TFrame")
        self.frame.grid(row=0, column=0, stick="nsew")

        #Création/Mise en page des Widgets
        #---Ligne 0
        label_titre = ttk.Label(self.frame, text="Vos commandes", style="titre.TLabel")
        label_titre.grid(row=0, column=0, columnspan=2, pady=2)

        #---Ligne 1
        label_sous_titre = ttk.Label(self.frame, text="Double-cliquez sur une commande pour voir le détail", style="sous_titre.TLabel")
        label_sous_titre.grid(row=1, column=0, columnspan=2, pady=3)

        #---Ligne 2
        self.treeview_commandes = ttk.Treeview(self.frame, columns="num_commande date_commande date_retrait nb_produits prix_total",
                                               show="headings", style="treeview.Treeview")
        #On nomme les headings du treeview
        self.treeview_commandes.heading("num_commande", text="Numéro de commande")
        self.treeview_commandes.heading("date_commande", text="Date de commande")
        self.treeview_commandes.heading("date_retrait", text="Date de retrait")
        self.treeview_commandes.heading("nb_produits", text="Nombre de produits")
        self.treeview_commandes.heading("prix_total", text="Prix total")
        #On centre le contenu du treeview
        self.treeview_commandes.column("num_commande", anchor="center")
        self.treeview_commandes.column("date_commande", anchor="center")
        self.treeview_commandes.column("date_retrait", anchor="center")
        self.treeview_commandes.column("nb_produits", anchor="center")
        self.treeview_commandes.column("prix_total", anchor="center")

        self.treeview_commandes.grid(row=2, column=0, sticky="nsew", padx=5, pady=3)

        scrollbar_treeview_commandes = Scrollbar(self.frame, orient="vertical", command=self.treeview_commandes.yview)
        self.treeview_commandes["yscrollcommand"] = scrollbar_treeview_commandes.set
        scrollbar_treeview_commandes.grid(row=2, column=1, sticky="ns", padx=5)

        button_retour_accueil = ttk.Button(self.frame, text="Retourner à l'accueil", command=self.retour_accueil)
        button_retour_accueil.grid(row=3, column=0, columnspan=2, pady=3)

        #Événements
        self.remplir_treeview()
        self.treeview_commandes.bind("<Double-1>", self.afficher_commande) #double click

        #On centre la fenêtre au milieu de l'écran
        self._root.geometry(center_window(self.frame))

        #En cas de fermeture de la fenêtre
        self._root.protocol("WM_DELETE_WINDOW", self.retour_accueil)

    def remplir_treeview(self):
        
        if self.liste_commandes == []:
            self.liste_commandes = charger_liste_commande(self._mail_client)
        
        for (id_commande, date_commande, date_retrait) in self.liste_commandes:
            liste_produits_commande = charger_produits_commande(id_commande)
            nb_produit = sum( (quantite for (produit, quantite) in liste_produits_commande) )
            prix_total = sum( (produit.prix*quantite for (produit, quantite) in liste_produits_commande) )
            valeurs = (id_commande, date_commande.strftime('%d-%m-%Y'), date_retrait.strftime('%d-%m-%Y'), nb_produit, prix_total)
            self.treeview_commandes.insert("", "end", values=valeurs)

    def afficher_commande(self, *args):

        info_treeview = self.treeview_commandes.item(self.treeview_commandes.focus())
        self.frame.destroy()
        IHM_commande(info_treeview["values"][0]) #id_commande

    def retour_accueil(self):

        self.frame.destroy()
        IHM_accueil.launch_IHM_accueil()


class IHM_commande:

    _root:tkinter
    _mail_client:str
    _id_commande:int

    def __init__(self, id_commande:int):

        #Affectation variables d'instances
        self._root = App.root()
        self._root.title(f"Commande numéro {id_commande}")
        self._mail_client = App.mail_client
        self._id_commande = id_commande

        #Création des styles
        style = ttk.Style()
        style.theme_use("default")
        style.configure('frame.TFrame', background="SkyBlue3")
        style.configure('titre.TLabel', font="Arial 12 bold", background="SkyBlue3")
        style.configure('sous_titre.TLabel', font="Arial 10 bold", background="SkyBlue3")
        style.configure('treeview.Treeview', background="grey85")
        style.configure('bouton.TButton', width=21)

        #Création de la frame principale
        self.frame = ttk.Frame(self._root, padding="5 5 5 5", style="frame.TFrame")
        self.frame.grid(row=0, column=0, stick="nsew")

        #Création/Mise en page des Widgets
        #---Ligne 0
        label_titre = ttk.Label(self.frame, text=f"Commande numéro {self._id_commande}", style="titre.TLabel")
        label_titre.grid(row=0, column=0, columnspan=3, pady=5)

        #---Ligne 1
        self.stringvar_date_commande = StringVar()
        label_date_commande = ttk.Label(self.frame, textvariable=self.stringvar_date_commande, style="sous_titre.TLabel")
        label_date_commande.grid(row=1, column=0, pady=3)

        self.stringvar_date_retrait = StringVar()
        label_date_retrait = ttk.Label(self.frame, textvariable=self.stringvar_date_retrait, style="sous_titre.TLabel")
        label_date_retrait.grid(row=1, column=1, pady=3)

        self.stringvar_prix_total = StringVar()
        label_prix_total = ttk.Label(self.frame, textvariable=self.stringvar_prix_total, style="sous_titre.TLabel")
        label_prix_total.grid(row=1, column=2, pady=3)

        #---Ligne 2
        self.treeview_commande = ttk.Treeview(self.frame, columns="produit prix_unitaire quantite prix_total", show="headings",
                                              style="treeview.Treeview")
        #On nomme les headings du treeview#On centre le contenu du treeview
        self.treeview_commande.heading("produit", text="Produit")
        self.treeview_commande.heading("prix_unitaire", text="Prix unitaire")
        self.treeview_commande.heading("quantite", text="Quantité")
        self.treeview_commande.heading("prix_total", text="Prix total")
        #On centre le contenu du treeview
        self.treeview_commande.column("produit", anchor="center")
        self.treeview_commande.column("prix_unitaire", anchor="center")
        self.treeview_commande.column("quantite", anchor="center")
        self.treeview_commande.column("prix_total", anchor="center")

        self.treeview_commande.grid(row=2, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)

        scrollbar_treeview_commande = Scrollbar(self.frame, orient="vertical", command=self.treeview_commande.yview)
        self.treeview_commande["yscrollcommand"] = scrollbar_treeview_commande.set
        scrollbar_treeview_commande.grid(row=2, column=3, sticky="ns", padx=2, pady=2)

        #---Ligne 3
        button_modifier_commande = ttk.Button(self.frame, text="Modifier la commande", command=self.modifier_commande, style="bouton.TButton")
        button_modifier_commande.grid(row=3, column=0, sticky="e", pady=5)

        button_annuler_commande = ttk.Button(self.frame, text="Annuler la commande", command=self.annuler_commande, style="bouton.TButton")
        button_annuler_commande.grid(row=3, column=1, pady=5)

        button_retour_commandes = ttk.Button(self.frame, text="Retour", command=self.retour, style="bouton.TButton")
        button_retour_commandes.grid(row=3, column=2, sticky="w", pady=5)   

        #Événements
        self.remplir_treeview()

        #On centre la fenêtre au milieu de l'écran
        self._root.geometry(center_window(self.frame))

        #En cas de fermeture de la fenêtre
        self._root.protocol("WM_DELETE_WINDOW", self.retour)
    
    def remplir_treeview(self):
        
        (date_commande, self.date_retrait) = charger_commande(self._id_commande)
        self.liste_produits_commande = charger_produits_commande(self._id_commande)
        self.prix_total = 0
        
        for (produit, quantite) in self.liste_produits_commande:
            prix_total_produit = round(produit.prix*quantite, 2)
            self.prix_total += produit.prix*quantite
            valeurs = (produit.intitule, produit.prix, quantite, prix_total_produit)
            self.treeview_commande.insert("", "end", values=valeurs)
        
        self.stringvar_date_commande.set(f"Date de la commande : {date_commande.strftime('%d-%m-%Y')}")
        self.stringvar_date_retrait.set(f"Date de retrait : {self.date_retrait.strftime('%d-%m-%Y')}")
        self.stringvar_prix_total.set(f"Prix total : {self.prix_total} euro{'' if self.prix_total <= 1 else 's'}")
    
    def modifier_commande(self):
        
        self.frame.destroy()
        IHM_passer_commande._is_setup = False
        commande = Commande()
        commande.id_commande, commande.mail_client, commande.date_retrait = self._id_commande, self._mail_client, self.date_retrait
        for (produit, quantite) in self.liste_produits_commande:
            commande.ajouter_produit(produit, quantite)
        IHM_passer_commande.launch_IHM_passer_commande(commande)

    def annuler_commande(self):
        
        msg = messagebox.askquestion(f"Annuler la commande {self._id_commande}", "Êtes-vous certain de vouloir annuler votre commande ?")
        if msg == "yes":
            supprimer_commande(self._id_commande)
            messagebox.showinfo("Annulation réussie", "Votre commande a bien été annulée")
            self.retour()

    def retour(self):
        
        liste_commande = charger_liste_commande(self._mail_client)
        self.frame.destroy()
        if liste_commande == []:
            IHM_accueil.launch_IHM_accueil()
        else:
            IHM_voir_commande(liste_commande)


class IHM_passer_commande:

    button_supprimer_exist = False
    supprime_le_bouton = False
    _is_setup = False
    _root:tkinter
    _commande:Commande
    _liste_produit:list

    @staticmethod
    def launch_IHM_passer_commande(commande:Commande=None):
        
        if not IHM_passer_commande._is_setup:
            IHM_passer_commande._root = App.root()
            IHM_passer_commande._liste_produit = charger_liste_produit()

            if commande is None: #passer commande
                IHM_passer_commande._commande = Commande()
                IHM_passer_commande._commande.mail_client = App.mail_client
                IHM_passer_commande._is_setup = True

            else: #modifier commande 
                IHM_passer_commande._root = App.root()
                IHM_passer_commande._commande = commande

        return IHM_passer_commande()
        
    
    def __init__(self):

        #Affectation variables
        IHM_passer_commande._root.title(("Passer une commande" if IHM_passer_commande._is_setup == True else "Modifier votre commande"))
        IHM_passer_commande.liste_produit_intitule = [produit.intitule for produit in IHM_passer_commande._liste_produit]

        #Création des styles
        style = ttk.Style()
        style.theme_use("default")
        style.configure('frame.TFrame', background="SkyBlue3")
        style.configure('titre.TLabel', font="Arial 12 bold", background="SkyBlue3")
        style.configure('sous_titre.TLabel', font="Arial 10 bold", background="SkyBlue3")
        style.configure('texte.TLabel', background="SkyBlue3")
        style.configure('treeview.Treeview', background="grey85")
        style.configure('bouton.TButton', width=12)

        #Création de la frame principale
        IHM_passer_commande.frame = ttk.Frame(IHM_passer_commande._root, padding="3 3 3 3", style="frame.TFrame")
        IHM_passer_commande.frame.grid(row=0, column=0, stick="nsew")

        #Création/Mise en page des Widgets
        #---Ligne 0
        label_search_bar = ttk.Label(IHM_passer_commande.frame, text="Rechercher", style="sous_titre.TLabel")
        label_search_bar.grid(row=0, column=0, padx=2, pady=2)

        IHM_passer_commande.entry_search_bar = Entry(IHM_passer_commande.frame)
        IHM_passer_commande.entry_search_bar.grid(row=0, column=1, sticky="w", padx=2, pady=2)

        label_date_retrait = ttk.Label(IHM_passer_commande.frame, text="Date de retrait", style="sous_titre.TLabel")
        label_date_retrait.grid(row=0, column=2, columnspan=2, padx=2, pady=2)

        IHM_passer_commande.dateEntry_date_retrait = DateEntry(IHM_passer_commande.frame)
        IHM_passer_commande.dateEntry_date_retrait.grid(row=0, column=4, sticky="ew", padx=2, pady=2)
        IHM_passer_commande.dateEntry_date_retrait.set_date(date.today()+timedelta(days=1))

        #---Ligne 1
        label_produit = ttk.Label(IHM_passer_commande.frame, text="Produits", style="titre.TLabel")
        label_produit.grid(row=1, column=0, columnspan=2, pady=5) 

        label_quantite = ttk.Label(IHM_passer_commande.frame, text="Quantité", style="titre.TLabel")
        label_quantite.grid(row=1, column=3, pady=5) 

        label_commande = ttk.Label(IHM_passer_commande.frame, text="Détail de la commande", style="titre.TLabel")
        label_commande.grid(row=1, column=4, columnspan=5, pady=5)

        #---Ligne 2
        stringVar_liste_produit = StringVar(value=IHM_passer_commande.liste_produit_intitule)
        IHM_passer_commande.listbox_produit = Listbox(IHM_passer_commande.frame, selectmode=SINGLE, exportselection=False, listvariable=stringVar_liste_produit)
        IHM_passer_commande.listbox_produit.select_set(0)
        IHM_passer_commande.listbox_produit.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=2, pady=2)

        scrollbar_listbox_produit = Scrollbar(IHM_passer_commande.frame, orient="vertical", command=IHM_passer_commande.listbox_produit.yview)
        IHM_passer_commande.listbox_produit["yscrollcommand"] = scrollbar_listbox_produit.set
        scrollbar_listbox_produit.grid(row=2, column=2, sticky="ns", padx=2, pady=2)

        stringvar_quantite = StringVar(value=[i for i in range(10)])
        IHM_passer_commande.listbox_quantite = Listbox(IHM_passer_commande.frame, selectmode=SINGLE, exportselection=False, listvariable=stringvar_quantite)
        IHM_passer_commande.listbox_quantite.configure(justify='center', width=5)
        IHM_passer_commande.listbox_quantite.select_set(0)
        IHM_passer_commande.listbox_quantite.grid(row=2, column=3, sticky="ns", padx=2, pady=2)
        
        IHM_passer_commande.treeview_commande = ttk.Treeview(IHM_passer_commande.frame, columns="intitule prix_unitaire quantite prix_total",
                                              show="headings", style="treeview.Treeview")
        IHM_passer_commande.treeview_commande.heading("intitule", text="Intitulé")
        IHM_passer_commande.treeview_commande.heading("prix_unitaire", text="Prix unitaire")
        IHM_passer_commande.treeview_commande.heading("quantite", text="Quantité")
        IHM_passer_commande.treeview_commande.heading("prix_total", text="Prix total")
        IHM_passer_commande.treeview_commande.column("intitule", anchor="center")
        IHM_passer_commande.treeview_commande.column("prix_unitaire", anchor="center")
        IHM_passer_commande.treeview_commande.column("quantite", anchor="center")
        IHM_passer_commande.treeview_commande.column("prix_total", anchor="center")
        IHM_passer_commande.treeview_commande.grid(row=2, column=4, columnspan=6, sticky="nsew", padx=2, pady=2)

        scrollbar_treeview_commande = Scrollbar(IHM_passer_commande.frame, orient="vertical", command=IHM_passer_commande.treeview_commande.yview)
        IHM_passer_commande.treeview_commande["yscrollcommand"] = scrollbar_treeview_commande.set
        scrollbar_treeview_commande.grid(row=2, column=10, sticky="ns", padx=2, pady=2)

        #---Ligne 3
        label_titre_prix_commande = ttk.Label(IHM_passer_commande.frame, text="Prix de la commande :", style="sous_titre.TLabel")
        label_titre_prix_commande.grid(row=3, column=4, sticky="e", padx=2, pady=2)
        IHM_passer_commande.stringvar_prix_commande = \
            StringVar(value=f"{IHM_passer_commande._commande.prix_total} euro{'' if IHM_passer_commande._commande.prix_total <= 1 else 's'}")
        label_prix_commande = ttk.Label(IHM_passer_commande.frame, textvariable=IHM_passer_commande.stringvar_prix_commande, style="texte.TLabel")
        label_prix_commande.grid(row=3, column=5, sticky="w", padx=2, pady=2)

        titre_button_retour = ("Retourner à l'accueil" if IHM_passer_commande._is_setup else "Retour")
        button_retour = ttk.Button(IHM_passer_commande.frame, text=titre_button_retour, command=IHM_passer_commande.tester_retour, style="bouton.TButton")
        button_retour.grid(row=3, column=7, sticky="we", padx=2, pady=2)

        button_reset_commande = ttk.Button(IHM_passer_commande.frame, text="Réinitialiser", command=IHM_passer_commande.reset_commande, style="bouton.TButton")
        button_reset_commande.grid(row=3, column=8, sticky="we", padx=2, pady=2)

        button_sauvegarder = ttk.Button(IHM_passer_commande.frame, text="Sauvegarder", command=IHM_passer_commande.sauvegarder_commande, style="bouton.TButton")
        button_sauvegarder.grid(row=3, column=9, sticky="we", padx=2, pady=2)

        #On centre la fenêtre au milieu de l'écran
        self._root.geometry(center_window(self.frame))

        #Événements
        IHM_passer_commande.remplir_treeview_ouverture()
        IHM_passer_commande.entry_search_bar.bind("<KeyRelease>", self.chercher_produits)
        IHM_passer_commande.listbox_produit.bind('<<ListboxSelect>>', IHM_passer_commande.set_quantite)
        IHM_passer_commande.listbox_quantite.bind('<<ListboxSelect>>', IHM_passer_commande.inserer_produit)
        IHM_passer_commande.treeview_commande.bind('<<TreeviewSelect>>', IHM_passer_commande.afficher_bouton_supprimer)

        #En cas de fermeture de la fenêtre
        IHM_passer_commande._root.protocol("WM_DELETE_WINDOW", IHM_passer_commande.tester_retour)
    
    def afficher_bouton_supprimer(*args):
        
        if IHM_passer_commande.button_supprimer_exist or IHM_passer_commande.supprime_le_bouton:
            IHM_passer_commande.supprime_le_bouton = False
            return

        IHM_passer_commande.button_supprimer = ttk.Button(IHM_passer_commande.frame, text="Supprimer", 
                                                          command=IHM_passer_commande.supprimer_produit, style="bouton.TButton")
        IHM_passer_commande.button_supprimer.grid(row=3, column=6, sticky="we", padx=2, pady=2)
        IHM_passer_commande.button_supprimer_exist = True

    def supprimer_bouton_supprimer():

        IHM_passer_commande.button_supprimer.destroy()
        IHM_passer_commande.supprime_le_bouton = True
        IHM_passer_commande.button_supprimer_exist = False

    def supprimer_produit():

        liste_produit_suppr = []
        for selected_item in IHM_passer_commande.treeview_commande.selection():
            intitule_produit = IHM_passer_commande.treeview_commande.item(selected_item)["values"][0]
            for (produit, quantite) in IHM_passer_commande._commande:
                if produit.intitule == intitule_produit:
                    liste_produit_suppr.append(produit)
            IHM_passer_commande.treeview_commande.delete(selected_item)
        for produit in liste_produit_suppr:
            IHM_passer_commande._commande.ajouter_produit(produit, 0) #équivaut à supprimer le produit
        IHM_passer_commande.stringvar_prix_commande.set(f"{IHM_passer_commande._commande.prix_total} euro{'' if IHM_passer_commande._commande.prix_total <= 1 else 's'}")
        IHM_passer_commande.listbox_produit.selection_clear(0, 'end')
        IHM_passer_commande.listbox_produit.select_set(0)
        IHM_passer_commande.listbox_quantite.selection_clear(0, 'end')
        IHM_passer_commande.set_quantite()
        IHM_passer_commande.supprimer_bouton_supprimer()

    def chercher_produits(*args):
        
        valeur = IHM_passer_commande.entry_search_bar.get()

        if valeur == "":
            donnees = IHM_passer_commande.liste_produit_intitule
        else:
            donnees = []
            for produit_intitule in IHM_passer_commande.liste_produit_intitule:
                if valeur.lower() in produit_intitule.lower():
                    donnees.append(produit_intitule)
        IHM_passer_commande.afficher_produits(donnees)

    def afficher_produits(donnees):
            IHM_passer_commande.listbox_produit.delete(0,END)

            for produit_intitule in donnees:
                IHM_passer_commande.listbox_produit.insert(END, produit_intitule)

    def remplir_treeview_ouverture():
        
        #Erreur si c'est la première fois que l'utilisateur veut passer une commande
        try:
            IHM_passer_commande.dateEntry_date_retrait.set_date(IHM_passer_commande._commande.date_retrait)
        except:
            pass

        IHM_passer_commande.stringvar_prix_commande.set(f"{IHM_passer_commande._commande.prix_total} euro{'' if IHM_passer_commande._commande.prix_total <= 1 else 's'}")
        IHM_passer_commande.remplir_treeview_commande()
        IHM_passer_commande.set_quantite()

    def inserer_produit(*args):

        produit_intitule = IHM_passer_commande.listbox_produit.get(ACTIVE)
        index_produit = IHM_passer_commande.liste_produit_intitule.index(produit_intitule)
        produit = IHM_passer_commande._liste_produit[index_produit]
        quantite = IHM_passer_commande.listbox_quantite.curselection()[0]
        
        if IHM_passer_commande.button_supprimer_exist:
            IHM_passer_commande.supprimer_bouton_supprimer()

        IHM_passer_commande._commande.ajouter_produit(produit, quantite)
        IHM_passer_commande.remplir_treeview_commande()
        IHM_passer_commande.stringvar_prix_commande.set(f"{IHM_passer_commande._commande.prix_total}euro{'' if IHM_passer_commande._commande.prix_total <= 1 else 's'}")

    def remplir_treeview_commande():

        IHM_passer_commande.treeview_commande.delete(*IHM_passer_commande.treeview_commande.get_children())
        
        for (produit, quantite) in sorted([(produit, quantite) for (produit, quantite) in IHM_passer_commande._commande], \
                                            key=lambda t: t[0].intitule):
            valeurs = (produit.intitule, produit.prix,
                       quantite, round(produit.prix*quantite, 2))
            IHM_passer_commande.treeview_commande.insert("", "end", values=valeurs)

    def set_quantite(*args):
        
        index_produit = IHM_passer_commande.listbox_produit.curselection()[0]
        produit = IHM_passer_commande._liste_produit[index_produit].intitule
        IHM_passer_commande.listbox_quantite.selection_clear(0, 'end')

        for child in IHM_passer_commande.treeview_commande.get_children():
            intitule, _, quantite, _ = IHM_passer_commande.treeview_commande.item(child)['values']
            if intitule == produit:
                IHM_passer_commande.listbox_quantite.select_set(quantite)
                break
        else:
            IHM_passer_commande.listbox_quantite.select_set(0)
        
    def sauvegarder_commande():

        IHM_passer_commande._commande.date_retrait = IHM_passer_commande.dateEntry_date_retrait.get_date()

        if IHM_passer_commande._is_setup:
            IHM_passer_commande.sauvegarder_ajout_commande()
        else:
            IHM_passer_commande.sauvegarder_modification_commande()

    def sauvegarder_ajout_commande():

        if not IHM_passer_commande._commande.finaliser():
            return

        msg = messagebox.askquestion(f"Valider la commande", "Êtes-vous certain de vouloir valider la commande ?")
        if msg == "no":
            return

        sauvegarder_ajout_commande(IHM_passer_commande._commande)
        send_mail(IHM_passer_commande._commande)
        messagebox.showinfo("Youpi !", "Votre commande a bien été ajoutée !")
        IHM_passer_commande._is_setup = False
        IHM_passer_commande.retour_accueil()
    
    def sauvegarder_modification_commande():

        if not IHM_passer_commande._commande.finaliser():
            return

        msg = messagebox.askquestion(f"Valider la modification", "Êtes-vous certain de vouloir modifier la commande ?")
        if msg == "no":
            return
            
        sauvegarder_modification_commande(IHM_passer_commande._commande)
        messagebox.showinfo("Youpi !", "Votre commande a bien été modifiée !")
        IHM_passer_commande.retour_commande()

    def reset_commande():
        
        msg = messagebox.askquestion(f"Réinitialiser la commande", "Êtes-vous certain de vouloir réinitialiser la commande ?")
        if msg == "no":
            return

        IHM_passer_commande.treeview_commande.delete(*IHM_passer_commande.treeview_commande.get_children())
        IHM_passer_commande._commande.vider()
        IHM_passer_commande.listbox_produit.selection_clear(0, 'end')
        IHM_passer_commande.listbox_produit.select_set(0)
        IHM_passer_commande.listbox_quantite.selection_clear(0, 'end')
        IHM_passer_commande.listbox_quantite.select_set(0)
        IHM_passer_commande.stringvar_prix_commande.set("0 euro")

        if IHM_passer_commande.button_supprimer_exist:
            IHM_passer_commande.supprimer_bouton_supprimer()

    def tester_retour():

        if IHM_passer_commande._is_setup:
            IHM_passer_commande.retour_accueil()
        else:
            IHM_passer_commande.retour_commande()

    def retour_accueil():
        
        IHM_passer_commande._commande.date_retrait = IHM_passer_commande.dateEntry_date_retrait.get_date()
        IHM_passer_commande.frame.destroy()
        IHM_passer_commande.button_supprimer_exist = False
        IHM_accueil.launch_IHM_accueil()

    def retour_commande():
        
        IHM_passer_commande.frame.destroy()
        IHM_voir_commande()


def center_window(frame:ttk):
    """
    Cette fonction retourne la géométrie nécéssaire pour centrer la fenêtre au milieu de l'écran
    """
    frame.update()
    window_width, window_height = frame.winfo_width(), frame.winfo_height()
    screen_width,screen_height = frame.winfo_screenwidth(), frame.winfo_screenheight()
    center_x, center_y = int(screen_width/2 - window_width / 2), int(screen_height/2 - window_height / 2)
    return f'{window_width}x{window_height}+{center_x}+{center_y}'

def send_mail(commande:Commande):
    ssl_context = ssl.create_default_context()
    serveur = smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ssl_context)
    serveur.login("driveprojetpython@gmail.com", "drivepython")
    sujet_mail = "Récapitulatif de la commande"
    contenu_commande = ""
    for (produit, quantite) in commande:
        #on change le format des dates
        date_commande_split = commande.date_commande.split("-")
        date_commande = date(int(date_commande_split[0]), int(date_commande_split[1]), int(date_commande_split[2])).strftime("%d-%m-%Y")
        date_retrait_split = commande.date_retrait.split("-")
        date_retrait = date(int(date_retrait_split[0]), int(date_retrait_split[1]), int(date_retrait_split[2])).strftime("%d-%m-%Y")
        
        contenu_commande += f"- {quantite} {produit.intitule} : {round(produit.prix*quantite, 2)}€\n"
    contenu_mail = f"""
Vous avez effectué votre commande le {date_commande} à {datetime.now().strftime("%H:%M").replace(":","h")}.

Vous avez commandé :
{contenu_commande}
Total : {commande.prix_total}€

N'oubliez pas de venir la retirer le {date_retrait}.

Merci pour votre confiance !
À bientôt !

Votre application drive préférée
    """
    serveur.sendmail("driveprojetpython@gmail.com", commande.mail_client, f"Subject: {sujet_mail}\n{contenu_mail}".encode("utf-8"))
    serveur.quit()