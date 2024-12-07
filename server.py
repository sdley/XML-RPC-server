from xmlrpc.server import SimpleXMLRPCServer
from queue import Queue
import mysql.connector
import socket

"""
    Modifiez le serveur pour qu'il enregistre les adresses IP des producteurs et des consommateurs lors de
     l'ajout ou de la récupération d'éléments dans le tampon.
"""

# Connexion à la base de données MySQL
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",  
    password="",  
    database="producteurdb"  
)
db_cursor = db_connection.cursor()

def insert_message(source_ip, message, dest_ip, etatMessage=None):
    """Enregistre le message dans la base de données."""
    # etatMessage est un attribut optionnel

    # Si l'etat du message est fournit => on est en consommation: recupere = OUI
    if etatMessage:
        sql = "INSERT INTO messages (source_ip, message, dest_ip, recupere) VALUES (%s, %s, %s, %s)"
        val = (source_ip, message, dest_ip, etatMessage)
    else:
        # Si l'etat du message n'est pas fournit => on est en production: recupere = NON
        sql = "INSERT INTO messages (source_ip, message, dest_ip) VALUES (%s, %s, %s)"
        val = (source_ip, message, dest_ip)
    db_cursor.execute(sql, val)
    db_connection.commit()

def recupere_item(item):
    """Recupere l'adresse IP source d'un item et modifie son statut (SET Recupere: OUI)"""
    # Mise a jour du statut
    message = item + " ajouté"
    sql = "UPDATE messages SET recupere = %s WHERE message = %s"
    # val = ("OUI", item)
    val = ("OUI", message)
    db_cursor.execute(sql, val)

    # Recuperation de l'IP source
    # message = item + " ajouté"
    sql = "SELECT source_ip FROM messages WHERE message = %s"
    val = (message,)

    db_cursor.execute(sql, val)
    result = db_cursor.fetchone()
    
    if result is None:
        raise ValueError("Aucune adresse IP source initiale trouvée dans la base de données.")
    
    source_ip = result[0]  # Extraction de l'adresse IP source initiale

    # print("resultats: ", result)
    # print("source ip: ", source_ip)

    # Enregitrement des modifications
    db_connection.commit()
    return source_ip

def get_local_ip():
    """Récupère l'adresse IP locale de la machine."""
    hostname = socket.gethostname()
    return socket.gethostbyname(hostname)

class Buffer:
    """Tampon partagé entre producteur et consommateur."""
    def __init__(self, max_size=10):
        self.queue = Queue(max_size)

    def put_item(self, item, producer_ip):
        """Ajoute un élément au tampon."""
        if not self.queue.full():
            self.queue.put(item)
            message = f"{item} ajouté"
            # Enregistrement du message dans la base de données avec les adresses IP dynamiques
            # insert_message(producer_ip, message, get_local_ip())  # IP destination est celle du serveur
            insert_message(producer_ip, message, "Unknown")  # IP destination est initialement inconnu
            return f"Item {item} ajouté au tampon."
        else:
            return "Tampon plein. Impossible d'ajouter l'élément."

    def get_item(self, consumer_ip):
        """Récupère un élément du tampon."""
        if not self.queue.empty():
            item = self.queue.get()
            message = f"{item} récupéré"

            # begin test
            # Recuperation de l'IP source de item
            source_ip = recupere_item(item)
            # Enregistrement du message dans la base de données avec les adresses IP dynamiques
            insert_message(source_ip, message, consumer_ip, "OUI")  # IP source est l'IP du producteur

            # end test

            # insert_message(get_local_ip(), message, consumer_ip)  # IP source est l'IP du producteur
            
            return f"Item {item} récupéré."
        else:
            return "Tampon vide. Impossible de récupérer un élément."
    
    
# Création et lancement du serveur XML-RPC
if __name__ == "__main__":
    buffer = Buffer(max_size=5)  # Taille maximale du tampon
    ip_server = get_local_ip()  # Récupération de l'adresse IP du serveur
    port = 8000  # Port d'écoute
    # En reseau
    # server = SimpleXMLRPCServer((ip_server, port))
    # En local
    server = SimpleXMLRPCServer(("localhost", port))
    server.register_instance(buffer)

    print("Serveur XML-RPC :")
    print("\tIP Address: ", ip_server, "\tPort: ", port)
    server.serve_forever()

