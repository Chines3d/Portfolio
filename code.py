import socket
import logging
from datetime import datetime

# --- CONFIGURATION DU LOGGING ---
# Génère automatiquement le fichier de log mentionné dans les "Résultats"
logging.basicConfig(
    filename='/var/log/surveillance_ports.log', # Chemin typique Linux
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def verifier_port(ip_cible, port):
    """Vérifie l'état d'un port spécifique avec gestion des exceptions."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2.0) # Timeout pour éviter les blocages
    
    try:
        # connect_ex renvoie 0 si la connexion réussit (port ouvert)
        resultat = sock.connect_ex((ip_cible, port))
        
        if resultat == 0:
            msg = f"Port {port} OUVERT sur l'hôte {ip_cible}"
            print(f"[+] {msg}")
            logging.info(msg)
        else:
            msg = f"Port {port} FERMÉ ou filtré sur l'hôte {ip_cible}"
            print(f"[-] {msg}")
            logging.warning(msg)
            
    except socket.timeout:
        msg = f"Délai d'attente dépassé pour le port {port} (Timeout)"
        print(f"[!] {msg}")
        logging.error(msg)
    except socket.error as e:
        # Gestion complexe des exceptions réseau mentionnée dans le "Ressenti"
        msg = f"Erreur réseau sur le port {port} : {e}"
        print(f"[!] {msg}")
        logging.error(msg)
    finally:
        sock.close()

def lancer_surveillance(ip_cible, liste_ports):
    print(f"=== Début de la surveillance : {ip_cible} à {datetime.now().strftime('%H:%M:%S')} ===")
    logging.info(f"--- DÉMARRAGE DU SCAN POUR {ip_cible} ---")
    
    for port in liste_ports:
        verifier_port(ip_cible, port)
        
    print("=== Fin de la surveillance ===")

if __name__ == "__main__":
    # Définition de la cible et des ports critiques (SSH, HTTP, HTTPS, RDP)
    CIBLE_IP = "192.168.10.50"
    PORTS_CRITIQUES = [22, 80, 443, 3389]
    
    lancer_surveillance(CIBLE_IP, PORTS_CRITIQUES)