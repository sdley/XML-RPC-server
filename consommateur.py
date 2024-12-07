import xmlrpc.client
import time
import random
import socket

"""
    Le consommateur doit également envoyer sa propre adresse IP lors de la récupération d'un élément.
"""

ip_server = "localhost"  # Remplacer par l'adresse IP réelle du serveur

proxy = xmlrpc.client.ServerProxy(f"http://{ip_server}:8000/")  # Remplacer par l' IP réelle du serveur
# proxy = xmlrpc.client.ServerProxy(f"http://10.163.8.61:8000/")  # Remplacer par l' IP réelle du serveur

def get_local_ip():
    """Récupère l'adresse IP locale de la machine."""
    hostname = socket.gethostname()
    return socket.gethostbyname(hostname)

def consumer():
    """Consomme des éléments du tampon de manière continue."""
    
    ip_consommateur = get_local_ip()  # Récupération de l'IP du consommateur
    
    while True:
        try:
            response = proxy.get_item(ip_consommateur)  # Envoi de l'IP du consommateur
            print(f"[Consommateur] {response}")
            time.sleep(random.uniform(0.5, 1.5))  # Simule un délai entre consommations
        except Exception as e:
            print(f"[Consommateur] Erreur: {e}")
            break  # Sort de la boucle en cas d'erreur

if __name__ == "__main__":
    consumer()

    """
        La condition if __name__ == "__main__": en Python est utilisée pour déterminer si un module 
        est exécuté directement ou s'il est importé dans un autre module. 
        Voici une explication détaillée de son fonctionnement :
            Explication de if __name__ == "__main__":
            - Variable spéciale __name__ :
            Chaque module en Python a une variable spéciale appelée __name__.
            Lorsque le module est exécuté directement (par exemple, via la ligne de commande), 
            Python attribue à __name__ la valeur "__main__".
            Si le module est importé dans un autre module, __name__ prend la valeur du nom du module.
            Utilisation de la condition :
            - La condition if __name__ == "__main__": permet d'exécuter un bloc de code uniquement 
            lorsque le module est exécuté comme programme principal, et non lorsqu'il est importé.
            Cela est particulièrement utile pour inclure des tests ou des exemples d'utilisation 
            qui ne devraient pas s'exécuter lors de l'importation du module.
    """