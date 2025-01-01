TDLOGPRJT: Vente et Achat de Voitures


#Description
Ce projet est une application web développée avec Django, permettant aux utilisateurs de consulter, filtrer et interagir avec des annonces de voitures 
et aussi de vendre des voitures pour des prestataires. Elle offre des fonctionnalités comme :

*Affichage des voitures disponibles.
*Filtrage et tri des résultats (par marque, prix, année, etc.).
*Création et gestion d'offres d'achat ou d'échange.
*Notifications pour les interactions liées aux annonces.
*Authentification et gestion des profils utilisateurs.

#Structure du Projet
*Backend :
Framework : Django
Base de données : SQLite
Application principale : cars
*Frontend :
Templates HTML avec héritage (e.g., base.html).
Fichiers statiques pour le style (CSS) et les interactions dynamiques (JavaScript).
Prérequis
Python : 3.8 ou supérieur
Django : 4.x
SQLite (installé par défaut avec Python)


#Installation

#Clonez le dépôt :


git clone <repository-url>
cd TDLOGPRJT
#Installez les dépendances :


pip install -r requirements.txt
#Appliquez les migrations :

python manage.py migrate

#Lancez le serveur local :

python manage.py runserver


#Fonctionnalités Principales
Filtrage et tri :
Les utilisateurs peuvent rechercher des voitures par marque ou trier les résultats par prix ou année et il en est de même pour le vendeur.

#Gestion des offres :
Les utilisateurs connectés peuvent soumettre, consulter ou accepter des offres pour les voitures listées.

#Notifications :
Les vendeurs reçoivent des notifications pour toutes les nouvelles interactions liées à leurs annonces.


