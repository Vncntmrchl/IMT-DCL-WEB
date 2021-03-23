# Contexte

Ce projet est lié à l'UE WEB de la TAF DCL à IMT Atlantique. Le but de ce projet est de concevoir une application
fonctionnant sur le même principe que le service Instagram.

# Repository

Sur la branche master se trouve la version stable la plus récente de notre projet. Toutes les autres branches sont des
branches de développement.

# Technologies utilisées

Nous avons utilisé différents packages et technologies au cours de ce projet :

- SQLAlchemy pour la base de données
- flask-login pour le système d'authentification
- flask-uploads pour la gestion des uploads d'images
- flask-wtf et wtforms pour les formulaires et leur vérification

# Structure du projet

Le projet est organisé comme suit :

    - "auth" : dossier contenant le code relatif au système d'authentification
    - "database" : dossier contenant le code relatif à la base de données
    - "models" : dossier contenant les modèles Python (classes) utilisés dans le projet et appelés à différents endroits de l'application
    - "routes" : dossier contenant le code relatif aux différentes pages de l'application (page feed, page profil...) ou fonctionnalités (ajouter un post, commenter...°
    - "static" : dossier contenant les feuilles de style CSS, le logo de l'application, le favicon, certains scripts JavaScript et le répertoire où sont stockées les images postées
    - "templates" : dossier où sont stockées l'ensemble des templates html des différentes pages de l'application, organisées par thèmes
    - "uploads" : dossier contenant une partie du code relatif au système d'upload d'images lors de la création de posts
    - app.py : base de l'application, fichier où elle est initialisée avec tous ses composants, ainsi que les autres éléments (base de données, login manager...)
    - config.py : fichier de configuration de l'application Flask
    - main.py : fichier de lancement de l'application

# Fonctionnalités

L'application dispose des fonctionnalités suivantes :

- Système d'authentification
- Création de posts avec image, description et mots-clés ("tags")
- Like/Unlike de posts
- Système d'abonnements entre utilisateurs ("follow")
- Suppression de ses propres posts
- Commenter des posts
- Système de recherche par mots-clés
- Tableau de bord utilisateur