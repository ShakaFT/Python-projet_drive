import tkinter
from produit import Produit
from commande import Commande
from bd import *
from datetime import date, timedelta
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import DateEntry

class IHM_connexion:

    def __init__(self, root):
        
        #Affectation variables
        self.root = root
        self.root.title("Connexion")

        #Création styles
        style = ttk.Style()
        style.configure('frame.TFrame', background="SkyBlue3")
        style.configure('titre.TLabel', font="Arial 12 bold", background="SkyBlue3")
        style.configure('sous_titre.TLabel', font="Arial 10 bold", background="SkyBlue3")

        #Création de la frame principale
        self.frame = ttk.Frame(self.root, padding="3 3 3 3", style="frame.TFrame")
        self.frame.grid(row=0, column=0, stick="nsew")

        #Création/Mise en page des Widgets
        #---ligne 0
        label_titre = ttk.Label(self.frame, text="Connectez-vous !", style="titre.TLabel")
        label_titre.grid(row=0, column=0, columnspan=2, padx=100, pady=10)

        #---ligne 1
        label_email = ttk.Label(self.frame, text="email", style="sous_titre.TLabel")
        label_email.grid(row=1, column=0, sticky="e", padx=5, pady=10)

        self.entry_email = Entry(self.frame, bd=4)
        self.entry_email.grid(row=1, column=1, sticky="w", padx=5, pady=10)  
        self.entry_email.after(1, lambda:self.entry_email.focus_set())

        #---ligne 2
        button_connexion = ttk.Button(self.frame, text="Se connecter", command=self.connexion)
        button_connexion.grid(row=2, column=0, columnspan=2, pady=10)

        #En cas de fermeture de la fenêtre
        self.root.protocol("WM_DELETE_WINDOW", self.close)

    def connexion(self):

        email_client = self.entry_email.get()
        
        if email_client == "":
            messagebox.showerror("email manquant", "Veuillez entrer un email.")
            return
        elif "@" not in email_client:
            messagebox.showerror("email invalide", "Veuillez entrer un email valide.")
            return
        
        self.frame.destroy()
        IHM_accueil.get_instance(self.root, email_client)
        
    def close(self):

        self.root.quit()

class IHM_accueil:

    _is_setup = False
    email_client:str

    @staticmethod
    def get_instance(root, email_client=""):
        if not IHM_accueil._is_setup:
            IHM_accueil.email_client = email_client
            IHM_accueil._is_setup = True
        return IHM_accueil(root)

    def __init__(self, root):

        #Affectation variables
        self.root = root
        self.root.title("Accueil drive")
    
        #Création styles
        style = ttk.Style()
        style.configure('frame.TFrame', background="SkyBlue3")
        style.configure('titre.TLabel', font="Arial 12 bold", background="SkyBlue3")
        style.configure('sous_titre.TLabel', font="Arial 10 bold", background="SkyBlue3", foreground="snow")
        style.configure('button.TButton', width=22)

        #Création de la frame principale
        self.frame = ttk.Frame(self.root, padding="3 3 3 3", style='frame.TFrame')
        self.frame.grid(row=0, column=0, stick="nsew")

        #Création/Mise en page des Widgets
        #---ligne 0
        button_deconnexion = ttk.Button(self.frame, text="Se déconnecter", command=self.deconnexion)
        button_deconnexion.grid(row=0, column=1, sticky="e", padx=2, pady=2)

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

        #En cas de fermeture de la fenêtre
        self.root.protocol("WM_DELETE_WINDOW", self.close)

    def deconnexion(self):

        self.frame.destroy()
        IHM_accueil._is_setup = False
        IHM_connexion(self.root)

    def voir_commande(self):
        
        liste_commandes = charger_commande(IHM_accueil.email_client)
        if liste_commandes == []:
            messagebox.showerror("Aucune commande", "Vous n'avez aucune commande en cours")
            return

        self.frame.destroy()
        IHM_voir_commande(self.root, IHM_accueil.email_client)

    def passer_commande(self):

        self.frame.destroy()
        IHM_passer_commande.get_instance(self.root, IHM_accueil.email_client)
    
    def close(self):
        
        self.frame.destroy()
        IHM_accueil._is_setup = False
        IHM_connexion(self.root)


class IHM_voir_commande:

    email_client:str

    def __init__(self, root:tkinter, email_client:str):

        #Création de la fenêtre
        self.root = root
        self.root.title("Mes commandes")

        self.email_client = email_client

        #Création styles
        style = ttk.Style()
        style.theme_use("default")
        style.configure("frame.TFrame", background="SkyBlue3")
        style.configure('titre.TLabel', font="Arial 12 bold", background="SkyBlue3")
        style.configure('sous_titre.TLabel', font="Arial 10 bold", background="SkyBlue3")
        style.configure('treeview.Treeview', background="grey85")

        #Création de la frame principale
        self.frame = ttk.Frame(self.root, padding="3 3 3 3", style="frame.TFrame")
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
        
        self.treeview_commandes.heading("num_commande", text="Numéro de commande")
        self.treeview_commandes.heading("date_commande", text="Date de commande")
        self.treeview_commandes.heading("date_retrait", text="Date de retrait")
        self.treeview_commandes.heading("nb_produits", text="Nombre de produits")
        self.treeview_commandes.heading("prix_total", text="Prix total")

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
        self.treeview_commandes.bind("<<TreeviewOpen>>", self.remplir_treeview())
        self.treeview_commandes.bind("<Double-1>", self.afficher_commande)

        #En cas de fermeture de la fenêtre
        self.root.protocol("WM_DELETE_WINDOW", self.close)

    def remplir_treeview(self):

        liste_commandes = charger_commande(self.email_client)
        
        for (id_commande, date_commande, date_retrait) in liste_commandes:
            liste_produits_commande = charger_produits_commande(id_commande)
            valeurs = (id_commande, date_commande, date_retrait, len(liste_produits_commande),
                      sum( (produit.prix*quantite for (produit, quantite) in liste_produits_commande) ))
            self.treeview_commandes.insert("", "end", values=valeurs)

    def afficher_commande(self, *args):

        info_treeview = self.treeview_commandes.item(self.treeview_commandes.focus())
        self.frame.destroy()
        IHM_commande(self.root, self.email_client, info_treeview["values"][0]) #2e arg : id_commande

    def retour_accueil(self):

        self.frame.destroy()
        IHM_accueil.get_instance(self.root)

    def close(self):

        self.retour_accueil()


class IHM_commande:

    email_client:str
    id_commande:int

    def __init__(self, root:tkinter, email_client:str, id_commande:int):

        #Création de la fenêtre
        self.root = root
        self.root.title(f"Commande numéro {id_commande}")

        #Création styles
        style = ttk.Style()
        style.theme_use("default")
        style.configure('frame.TFrame', background="SkyBlue3")
        style.configure('titre.TLabel', font="Arial 12 bold", background="SkyBlue3")
        style.configure('sous_titre.TLabel', font="Arial 10 bold", background="SkyBlue3")
        style.configure('treeview.Treeview', background="grey85")
        style.configure('bouton.TButton', width=21)

        #Affectation variables d'instances
        self.email_client = email_client
        self.id_commande = id_commande

        #Création de la frame principale
        self.frame = ttk.Frame(self.root, padding="5 5 5 5", style="frame.TFrame")
        self.frame.grid(row=0, column=0, stick="nsew")

        #Création/Mise en page des Widgets
        #---Ligne 0
        label_titre = ttk.Label(self.frame, text=f"Commande numéro {self.id_commande}", style="titre.TLabel")
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
        self.treeview_commande = ttk.Treeview(self.frame, columns="produit prix_unitaire quantite prix_total",
                                               show="headings", style="treeview.Treeview")
        
        self.treeview_commande.heading("produit", text="Produit")
        self.treeview_commande.heading("prix_unitaire", text="Prix unitaire")
        self.treeview_commande.heading("quantite", text="Quantité")
        self.treeview_commande.heading("prix_total", text="Prix total")

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

        button_retour_commandes = ttk.Button(self.frame, text="Retour", command=self.retour_commandes, style="bouton.TButton")
        button_retour_commandes.grid(row=3, column=1, pady=5)

        button_annuler_commande = ttk.Button(self.frame, text="Annuler la commande", command=self.annuler_commande, style="bouton.TButton")
        button_annuler_commande.grid(row=3, column=2, sticky="w", pady=5)

        #Événements
        self.treeview_commande.bind("<<TreeviewOpen>>", self.remplir_treeview())

        #En cas de fermeture de la fenêtre
        self.root.protocol("WM_DELETE_WINDOW", self.retour_commandes)
    
    def remplir_treeview(self):
        
        (self.date_commande, self.date_retrait) = charger_une_commande(self.id_commande)
        self.liste_produits_commande = charger_produits_commande(self.id_commande)
        self.prix_total = 0
        
        for (produit, quantite) in self.liste_produits_commande:
            prix_total_produit = produit.prix*quantite
            self.prix_total += produit.prix*quantite
            valeurs = (produit.intitule, produit.prix, quantite, prix_total_produit)
            self.treeview_commande.insert("", "end", values=valeurs)
        
        self.stringvar_date_commande.set(f"Date de la commande : {self.date_commande.strftime('%d-%m-%Y')}")
        self.stringvar_date_retrait.set(f"Date de retrait : {self.date_retrait.strftime('%d-%m-%Y')}")
        self.stringvar_prix_total.set(f"Prix total : {self.prix_total} euro{'' if self.prix_total <= 1 else 's'}")
    
    def modifier_commande(self):

        msg = messagebox.askquestion(f"Modifier la commande {self.id_commande}", "Souhaitez-vous modifier votre commande ?")
        if msg == "yes":
            self.frame.destroy()
            IHM_passer_commande.get_instance(self.root, self.email_client, 
                                            (self.id_commande, self.date_retrait, self.prix_total, self.liste_produits_commande))

    def annuler_commande(self):
        
        msg = messagebox.askquestion(f"Annuler la commande {self.id_commande}", "Êtes-vous certain de vouloir annuler la commande ?")
        if msg == "yes":
            supprimer_commande(self.id_commande)
            messagebox.showinfo("Annulation réussie", "Votre commande a bien été annulée")
            self.retour_commandes()

    def retour_commandes(self):
        
        liste_commande = charger_commande(self.email_client)
        self.frame.destroy()
        if liste_commande == []:
            IHM_accueil.get_instance(self.root)
        else:
            IHM_voir_commande(self.root, self.email_client)


class IHM_passer_commande:

    commande = None
    _instance = None
    _is_setup = False
    liste_produit:list

    @staticmethod
    def get_instance(root:tkinter, email_client:str, tuple_commande_modif=None):

        if not IHM_passer_commande._is_setup and tuple_commande_modif is None:
            IHM_passer_commande.commande = Commande()
            IHM_passer_commande._is_setup = True
            IHM_passer_commande._instance = IHM_passer_commande(root, email_client, tuple_commande_modif)
        elif IHM_passer_commande._is_setup and tuple_commande_modif is None:
            IHM_passer_commande._instance = IHM_passer_commande(root, email_client, tuple_commande_modif)
            IHM_passer_commande.ancienne_commande()
        
        if tuple_commande_modif is not None:
            IHM_passer_commande.commande = Commande()
            IHM_passer_commande._instance = IHM_passer_commande(root, email_client, tuple_commande_modif)
            IHM_passer_commande._is_setup = False

        return IHM_passer_commande._instance
        
    
    def __init__(self, root:tkinter, email_client:str, tuple_commande_modif):

        #Affectation variables
        IHM_passer_commande.root = root
        IHM_passer_commande.root.title(("Passer une commande" if tuple_commande_modif is None else "Modifier votre commande"))
        IHM_passer_commande.email_client = email_client
        IHM_passer_commande.liste_produit = charger_liste_produit()
        liste_produit_intitule = [p.intitule for p in IHM_passer_commande.liste_produit]
        IHM_passer_commande.tuple_commande_modif = tuple_commande_modif

        #Création styles
        style = ttk.Style()
        style.theme_use("default")
        style.configure('frame.TFrame', background="SkyBlue3")
        style.configure('titre.TLabel', font="Arial 12 bold", background="SkyBlue3")
        style.configure('sous_titre.TLabel', font="Arial 10 bold", background="SkyBlue3")
        style.configure('texte.TLabel', background="SkyBlue3")
        style.configure('treeview.Treeview', background="grey85")
        style.configure('bouton.TButton', width=10)

        #Création de la frame principale
        IHM_passer_commande.frame = ttk.Frame(IHM_passer_commande.root, padding="3 3 3 3", style="frame.TFrame")
        IHM_passer_commande.frame.grid(row=0, column=0, stick="nsew")

        #Création/Mise en page des Widgets
        #---Ligne 0
        label_date_retrait = ttk.Label(IHM_passer_commande.frame, text="Date de retrait", style="sous_titre.TLabel")
        label_date_retrait.grid(row=0, column=0, sticky="w", padx=2, pady=2)

        IHM_passer_commande.dateEntry_date_retrait = DateEntry(IHM_passer_commande.frame)
        IHM_passer_commande.dateEntry_date_retrait.grid(row=0, column=1, sticky="ew", padx=2, pady=2)
        IHM_passer_commande.dateEntry_date_retrait.set_date(date.today()+timedelta(days=1))

        #---Ligne 1
        label_produit = ttk.Label(IHM_passer_commande.frame, text="Produits", style="titre.TLabel")
        label_produit.grid(row=1, column=0, columnspan=2, pady=5) 

        label_quantite = ttk.Label(IHM_passer_commande.frame, text="Quantité", style="titre.TLabel")
        label_quantite.grid(row=1, column=3, pady=5) 

        label_commande = ttk.Label(IHM_passer_commande.frame, text="Détail de la commande", style="titre.TLabel")
        label_commande.grid(row=1, column=4, columnspan=5, pady=5)

        #---Ligne 2
        stringVar_liste_produit = StringVar(value=liste_produit_intitule)
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
        IHM_passer_commande.treeview_commande.grid(row=2, column=4, columnspan=5, sticky="nsew", padx=2, pady=2)

        scrollbar_treeview_commande = Scrollbar(IHM_passer_commande.frame, orient="vertical", command=IHM_passer_commande.treeview_commande.yview)
        IHM_passer_commande.treeview_commande["yscrollcommand"] = scrollbar_treeview_commande.set
        scrollbar_treeview_commande.grid(row=2, column=9, sticky="ns", padx=2, pady=2)

        #---Ligne 3
        label_titre_prix_commande = ttk.Label(IHM_passer_commande.frame, text="Prix de la commande :", style="sous_titre.TLabel")
        label_titre_prix_commande.grid(row=3, column=4, sticky="e", padx=2, pady=2)
        IHM_passer_commande.stringvar_prix_commande = \
            StringVar(value=f"{IHM_passer_commande.commande.prix_total} euro{'' if IHM_passer_commande.commande.prix_total <= 1 else 's'}")
        label_prix_commande = ttk.Label(IHM_passer_commande.frame, textvariable=IHM_passer_commande.stringvar_prix_commande, style="texte.TLabel")
        label_prix_commande.grid(row=3, column=5, sticky="w", padx=2, pady=2)

        titre_bouton_accueil = ("Retourner à l'accueil" if IHM_passer_commande.tuple_commande_modif is None else "Retour")
        button_retour_accueil = ttk.Button(IHM_passer_commande.frame, text=titre_bouton_accueil, command=IHM_passer_commande.tester_retour, style="bouton.TButton")
        button_retour_accueil.grid(row=3, column=6, sticky="we", padx=2, pady=2)

        button_reset_commande = ttk.Button(IHM_passer_commande.frame, text="Réinitialiser la commande", command=IHM_passer_commande.reset_commande, style="bouton.TButton")
        button_reset_commande.grid(row=3, column=7, sticky="we", padx=2, pady=2)

        button_sauvegarder = ttk.Button(IHM_passer_commande.frame, text="Sauvegarder", command=IHM_passer_commande.sauvegarder_commande, style="bouton.TButton")
        button_sauvegarder.grid(row=3, column=8, sticky="we", padx=2, pady=2)

        #Événements
        IHM_passer_commande.treeview_commande.bind("<<TreeviewOpen>>", IHM_passer_commande.remplir_treeview_ouverture())
        IHM_passer_commande.listbox_produit.bind('<<ListboxSelect>>', IHM_passer_commande.set_quantite)
        IHM_passer_commande.listbox_quantite.bind('<<ListboxSelect>>', IHM_passer_commande.inserer_produit)

        #En cas de fermeture de la fenêtre
        IHM_passer_commande.root.protocol("WM_DELETE_WINDOW", IHM_passer_commande.tester_retour)

    def ancienne_commande():
        
        IHM_passer_commande.dateEntry_date_retrait.set_date(IHM_passer_commande.commande.date_retrait)
        IHM_passer_commande.remplir_treeview_commande()


    def inserer_produit(*args):
        
        index_produit = IHM_passer_commande.listbox_produit.curselection()[0]
        index_quantite = IHM_passer_commande.listbox_quantite.curselection()[0]
        
        IHM_passer_commande.commande.ajouter_produit(IHM_passer_commande.liste_produit[index_produit], index_quantite)
        IHM_passer_commande.remplir_treeview_commande()
        IHM_passer_commande.stringvar_prix_commande.set(f"{IHM_passer_commande.commande.prix_total} euro{'' if IHM_passer_commande.commande.prix_total <= 1 else 's'}")

    def remplir_treeview_ouverture(*args):

        if IHM_passer_commande.tuple_commande_modif is None:
            return
            
        _, date_retrait, prix_total, liste_produits_commande = IHM_passer_commande.tuple_commande_modif
        IHM_passer_commande.dateEntry_date_retrait.set_date(date_retrait)
        IHM_passer_commande.stringvar_prix_commande.set(f"{prix_total} euro{'' if prix_total <= 1 else 's'}")

        for (produit, quantite) in liste_produits_commande:
            IHM_passer_commande.commande.ajouter_produit(produit, quantite)
            valeurs = (produit.intitule, produit.prix, quantite, produit.prix*quantite)
            IHM_passer_commande.treeview_commande.insert("", "end", values=valeurs)

    def remplir_treeview_commande():

        IHM_passer_commande.treeview_commande.delete(*IHM_passer_commande.treeview_commande.get_children())
        
        for (produit, quantite) in IHM_passer_commande.commande:
            valeurs = (produit.intitule, produit.prix, quantite, produit.prix*quantite)
            IHM_passer_commande.treeview_commande.insert("", "end", values=valeurs)

    def set_quantite(*args):
        
        index_produit = IHM_passer_commande.listbox_produit.curselection()[0]
        produit = IHM_passer_commande.liste_produit[index_produit].intitule
        IHM_passer_commande.listbox_quantite.selection_clear(0, 'end')

        for child in IHM_passer_commande.treeview_commande.get_children():
            intitule, _, quantite, _ = IHM_passer_commande.treeview_commande.item(child)['values']
            if intitule == produit:
                IHM_passer_commande.listbox_quantite.select_set(quantite)
                break
        else:
            IHM_passer_commande.listbox_quantite.select_set(0)
        
    def sauvegarder_commande():

        if IHM_passer_commande.tuple_commande_modif is None:
            IHM_passer_commande.sauvegarder_ajout_commande()
        else:
            IHM_passer_commande.sauvegarder_modification_commande()

    def sauvegarder_ajout_commande():

        IHM_passer_commande.commande.date_retrait = IHM_passer_commande.dateEntry_date_retrait.get_date()
        IHM_passer_commande.commande.mail_client = IHM_passer_commande.email_client

        if not IHM_passer_commande.commande.finaliser() :
            messagebox.showerror("Erreur", "Une information est incohérente")
            return
        
        sauvegarder_commande()
        messagebox.showinfo("Youpi !", "Votre commande a bien été ajoutée !")
        IHM_passer_commande.retour_accueil()

    def reset_commande():
        
        IHM_passer_commande.treeview_commande.delete(*IHM_passer_commande.treeview_commande.get_children())
        IHM_passer_commande.commande.vider()
        IHM_passer_commande.listbox_produit.selection_clear(0, 'end')
        IHM_passer_commande.listbox_produit.select_set(0)
        IHM_passer_commande.listbox_quantite.selection_clear(0, 'end')
        IHM_passer_commande.listbox_quantite.select_set(0)
        IHM_passer_commande.stringvar_prix_commande.set("0 euro")

    def sauvegarder_modification_commande():

        IHM_passer_commande.commande.id_commande = IHM_passer_commande.tuple_commande_modif[0]
        IHM_passer_commande.commande.date_retrait = IHM_passer_commande.dateEntry_date_retrait.get_date()
        IHM_passer_commande.commande.mail_client = IHM_passer_commande.email_client

        if not IHM_passer_commande.commande.finaliser() :
            messagebox.showerror("Erreur", "Une information est incohérente")
            return
            
        sauvegarder_commande_modif(IHM_passer_commande.commande)
        messagebox.showinfo("Youpi !", "Votre commande a bien été modifiée !")
        IHM_passer_commande.retour_commande()

    def tester_retour():

        if IHM_passer_commande.tuple_commande_modif is None:
            IHM_passer_commande.retour_accueil()
        else:
            IHM_passer_commande.retour_commande()

    def retour_accueil():
        
        IHM_passer_commande.commande.date_retrait = IHM_passer_commande.dateEntry_date_retrait.get_date()
        IHM_passer_commande.frame.destroy()
        IHM_accueil.get_instance(IHM_passer_commande.root)

    def retour_commande():

        IHM_passer_commande.frame.destroy()
        IHM_voir_commande(IHM_passer_commande.root, IHM_passer_commande.email_client)