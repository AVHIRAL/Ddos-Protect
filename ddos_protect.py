#!/usr/bin/env python3
import subprocess
import smtplib
import re
import time
import logging
from email.mime.text import MIMEText
from collections import defaultdict

# Configuration
SMTP_SERVER = "SERVEUR SMPT"
SMTP_PORT = 465
SMTP_USER = "email@email.com"
SMTP_PASS = "PASSWORD"
EMAIL_TO = "exemple@exemple.com"
INTERFACE = "eth0"
LOG_FILE = "/var/log/ddos_protect.log"
THRESHOLD_CONN = 100
PORTS = ["80", "443", "2001"]
BLOCK_DURATION = 3600

logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(asctime)s - %(message)s")
suspect_ips = defaultdict(list)
blocked_ips = {}

def send_email(ip, count):
    subject = "[AVHIRAL] DDoS détecté : IP %s bloquée" % ip
    body = "L'adresse IP %s a été détectée avec %d connexions anormales. Elle a été bloquée automatiquement." % (ip, count)
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = SMTP_USER
    msg["To"] = EMAIL_TO

    try:
        server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
        server.login(SMTP_USER, SMTP_PASS)
        server.sendmail(SMTP_USER, EMAIL_TO, msg.as_string())
        server.quit()
    except Exception as e:
        logging.error("Erreur lors de l'envoi d'email : %s" % str(e))

def block_ip(ip):
    if ip not in blocked_ips:
        for port in PORTS:
            subprocess.call(["iptables", "-I", "INPUT", "-s", ip, "-p", "tcp", "--dport", port, "-j", "DROP"])
        blocked_ips[ip] = time.time()
        logging.info("Bloqué %s" % ip)
        send_email(ip, len(suspect_ips[ip]))

def cleanup_blocks():
    now = time.time()
    to_remove = []
    for ip in blocked_ips:
        if now - blocked_ips[ip] > BLOCK_DURATION:
            to_remove.append(ip)
    for ip in to_remove:
        for port in PORTS:
            subprocess.call(["iptables", "-D", "INPUT", "-s", ip, "-p", "tcp", "--dport", port, "-j", "DROP"])
        del blocked_ips[ip]
        logging.info("Débloqué %s" % ip)

def monitor():
    while True:
        cleanup_blocks()
        try:
            output = subprocess.check_output(["netstat", "-ntu"])
            output = output.decode("utf-8")
            connections = re.findall(r'^tcp\s+\d+\s+\d+\s+[\d\.:]+\s+([\d\.]+):', output, re.MULTILINE)
            for ip in connections:
                suspect_ips[ip].append(time.time())

            for ip, times in suspect_ips.items():
                recent = [t for t in times if time.time() - t < 10]
                if len(recent) >= THRESHOLD_CONN:
                    block_ip(ip)
                    suspect_ips[ip] = []
        except Exception as e:
            logging.error("Erreur de surveillance : %s" % str(e))
        time.sleep(5)

if __name__ == "__main__":
    monitor()
