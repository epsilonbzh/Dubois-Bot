# Dubois Bot


## Commandes
- `/help` : liste des commandes
- `/quote` : dit une citation
- `/ping` : ping le bot

## Installation et lancement

/!\ Il faut créer un fichier "token.txt" à la racine du projet et y écrire le token dedans pour que le bot puisse s'identifier sur l'API. 

### Installation classique
```bash
# Nécessite python 3.8 ou supérieur
# Installation :
pip3 install discord.py
# Lancement :
python3 src/dubois.py
```

### Avec Docker
```bash
# Nécessite les droits root
# Installation :
docker build . -t dubois-bot

#Lancement :
docker run --name dubois -d dubois-bot

# Actualisation des sources :
docker cp . dubois:/app
docker restart dubois

# Les logs sont accessibles avec : 
docker logs dubois
```
