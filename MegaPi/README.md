# Code MegaPi

Ce code ouvre une communication série et écoute les messages.
Un message se structure ainsi :

Trame de début : commande : trame de fin
La trame de début est arbitraire et est fixé à 0x02. De même pour la trame de fin, 0x03.
Il y a actuellement 5 messages en place :
    - 'S' (STOP) : Arrête les moteurs
    - 'F' (FORWARD) : Fais tourner les moteurs de manière à avancer en ligne droite
    - 'B' (BACKWARD) : Fais tourner les moteurs de manière à reculer en ligne droite
    - 'L' (LEFT) : Fais tourner les moteurs de manière à tourner sur soi-même vers la gauche
    - 'R' (RIGHT) : Fais tourner les moteurs de manière à tourner sur soi-même vers la droite

Exemple :
    - Octet 1 : 0x02
    - Octet 2 : 'S'
    - Octet 3 : 0x03
--> Le robot s'arrête