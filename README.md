# Dubois Bot


## Commandes

### Commandes de bases
- `/help` : liste des commandes
- `/quote` : dit une citation
- `/ping` : ping le bot

### Commandes SWS
- `/signme` : signe sur SWS
- `/autosignadd` : active la signature automatique
- `/autosignremove` : désactive la signature automatique
- `/autosignlist` : liste les personnes inscrites à la signature automatique
#### Admin seulement :
- `/signall` : signe manuellement les personnes en signature auto

## Installation et lancement

/!\ Fichiers à rajouter et nécessaire pour le fonctionement : 
 - data/token.txt : avec un token d'API Discord

 Pour l'utilisation de SWS : 
- admins.txt : avec les IDs Discord des admins (qui peuvent utiliser certaines commandes)
- signature.json : avec les codes SWS, la structure est présente dans "structSigature.json"

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
