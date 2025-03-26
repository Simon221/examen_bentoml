# Examen BentoML - Author

* Nom : DIOUF
* Prenom : Simon Pierre 
* Repository Location : https://github.com/Simon221/examen_bentoml.git


# How To ?
Vous pouvez executer le projet en suivant les etapes suivantes

## Etape 1: Décompresser l'archive du projet
Si vous avez reçu l'archive du Projet (examen_BentoML_SimonPierreDIOUF.zip), vous devez d'abord la decompresser.
``` unzip examen_BentoML_SimonPierreDIOUF.zip ```

Vous trouverez alors
- Une image bento_image.tar : qui represente l'image dockerisé
- Un fichier test_api.py : pour tester l'api et le service, une fois qu'il sera lancé
- Un ficher test_unitaire.py : pour faire les tests unitaires

## Etape 2 : Lancement de l'image bento_image.tar
``` docker image load --input bento_image.tar ```

## Etape 3 : Lancement du container 
``` docker run --rm -p 3000:3000 simonpierrediouf_rf_admissions_service:fnucyjqkqk5ula6j ```

## Etape 4 : Test du bon fonctionnement 
Pour cela vous pourrer utiliser le fichier test_api.py.
Ouvrez un autre terminal et lancer la commande suivante
``` python test_api.py ```

# Etape 5 : Lancer les tests unitaires
Tous les tests unitaires ont été regroupés dans le fichier test_unitaire.py.
Pour le lancer, ouvrez un terminal et executer la commande suivante
``` python test_unitaire.py -v ```

