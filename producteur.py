import xmlrpc.client
import time
import random
import socket

"""
    Le producteur doit envoyer sa propre adresse IP lors de l'ajout d'un élément au tampon.
"""

def get_local_ip():
    """Récupère l'adresse IP locale de la machine."""
    hostname = socket.gethostname()
    return socket.gethostbyname(hostname)

ip_server = "localhost"  # Remplacer par l'adresse IP réelle du serveur

proxy = xmlrpc.client.ServerProxy(f"http://{ip_server}:8000/")

def producer():
    """Produit des éléments et les envoie au tampon de manière continue."""
    
    ip_producteur = get_local_ip()  # Récupération de l'IP du producteur
    
    i = 1
    while True:
        item = f"Item-{i}"  # Produit un élément 
        response = proxy.put_item(item, ip_producteur)  # Envoi de l'IP du producteur
        print(f"[Producteur] {response}")
        
        time.sleep(random.uniform(0.5, 1.0))  # Simule un délai entre productions
        i += 1

        # test
        # reponse = proxy.put_item("test item", ip_producteur)
        # print("Reponse: ", reponse)
        # print("ip_producteur: ", ip_producteur)
        # print("get_local_ip: ", get_local_ip())

if __name__ == "__main__":
    producer()
    
