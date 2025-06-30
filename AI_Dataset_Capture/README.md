# Code AI_Dataset_Capture

Application en python à exécuter sur le Raspberry PI de la voiture.
Expose un serveur sur 5000 avec un panneau de contrôle et un flux vidéo temps réel du point de vue de la voiture.
Ce code sert principalement à prendre en photo les panneaux de la maquette dans le but d'entraîner une IA de classification / détection.

Le code envoie des trames série au MegaPi en fonction des inputs de l'utilisateur. S'il maintient la flèche du haut, alors le robot avance, s'il maintient la flèche droite, alors il tourne à droite, s'il relâche une touche, le robot s'arrête etc...

Les photos prises sont téléchargées sur l'ordinateur client, et non sur le Raspberry (pour éviter de saturer le disque).