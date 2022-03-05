import mysql.connector as m

def create_tables():

    connexion = m.connect(host='devbdd.iutmetz.univ-lorraine.fr', database='tornicel3u_Drive', user='tornicel3u_appli', port = '3306', password='32016359')
    curseur = connexion.cursor()
    requete = """
    DROP TABLE IF EXISTS contient;
    DROP TABLE IF EXISTS produit;
    DROP TABLE IF EXISTS commande;

    CREATE TABLE produit(
        idProduit VARCHAR(50) PRIMARY KEY,
        intitule VARCHAR(100) NOT NULL,
        prix FLOAT NOT NULL
    );

    CREATE TABLE commande(
        idCommande INT PRIMARY KEY AUTO_INCREMENT,
        dateCommande DATE NOT NULL,
        dateRetrait DATE NOT NULL,
        mailClient VARCHAR(100) NOT NULL
    );

    CREATE TABLE contient(
        idProduit VARCHAR(50),
        idCommande INT,
        quantite INT NOT NULL,
        PRIMARY KEY(idProduit, idCommande),
        FOREIGN KEY(idProduit) REFERENCES produit(idProduit),
        FOREIGN KEY(idCommande) REFERENCES commande(idCommande)
    );
    """
    curseur.execute(requete)
    curseur.close()
    connexion.close()

create_tables()