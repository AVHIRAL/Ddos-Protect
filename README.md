# 🛡️ AVHIRAL - Protection DDoS automatique (Debian + iptables)

Ce projet fournit un script Python autonome permettant de détecter et bloquer automatiquement des attaques DDoS sur un serveur Debian utilisant `iptables`.

## 🔧 Fonctionnalités

- Détection de pics de connexions réseau anormaux (via `netstat`).
  
- Blocage automatique des IPs suspectes sur les ports sensibles (HTTP, HTTPS, custom).
  
- Envoi d'un email de notification avec l'IP bloquée.
  
- Service `systemd` pour démarrer automatiquement au boot.
  
- Compatible avec **Python 3.4+** (version rétro compatible).

## 📁 Installation pas à pas

### 1. Copier le script

Copiez le script Python ddos_protect.py dans `/usr/local/bin/` :

sudo cp ddos_protect.py /usr/local/bin/

sudo chmod +x /usr/local/bin/ddos_protect.py

### 2. Copier le fichier systemd

sudo cp ddos_protect.service /etc/systemd/system/

### 3. Configurer les paramètres SMTP

Éditez le script avec votre configuration email :

sudo nano /usr/local/bin/ddos_protect.py

Puis modifiez la section suivante :

# Configuration
SMTP_SERVER = "ssl0.ovh.net"     # << METTRE SERVEUR MAIL

SMTP_PORT = 465                  # << PORT EMAIL SSL

SMTP_USER = "email@email.com"    # << User Serveur Mail

SMTP_PASS = "1234"               # << Mot de passe

EMAIL_TO = "email@email.com"     # << envoyer log attaque à l'email que vous souhaitez

INTERFACE = "eth0"

### 4. Activer et lancer le service

sudo systemctl daemon-reexec

sudo systemctl daemon-reload

sudo systemctl enable ddos_protect.service

sudo systemctl start ddos_protect.service

### ✅ Vérification

sudo systemctl status ddos_protect.service

Vous devez obtenir une sortie similaire à :

● ddos_protect.service - Protection DDoS automatique AVHIRAL

   Loaded: loaded (/etc/systemd/system/ddos_protect.service; enabled)
   
   Active: active (running) since dim. 2025-05-25 10:13:07 CEST; 13min ago
   
 Main PID: 657 (python3)
 
   CGroup: /system.slice/ddos_protect.service
   
           └─657 /usr/bin/python3 /usr/local/bin/ddos_protect.py

mai 25 10:13:07 serveur.com systemd[1]: Started Protection DDoS automatique AVHIRAL.

## 📄 Log d'activité

Les événements sont journalisés dans :

/var/log/ddos_protect.log

DON PAYPAL : https://www.paypal.com/donate/?hosted_button_id=FSX7RHUT4BDRY

© AVHIRAL CyberDefense 2025 
