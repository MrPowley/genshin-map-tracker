# genshin-map-tracker
Traque sa position sur genshin en utilisant la minimap pour suivre sa position sur la carte interactive hoyolab

Je n'ai pas fais d'interface, donc pour l'instant, il faut télécharger les fichiers mis a disposition, et dans un dossier "assets", placer le fichier ["map_kp_des.pkl"](https://drive.google.com/drive/folders/1xb6ttWdshIqvR4PT60sf34nLL0auhF-8?usp=sharing)
Pour le lancer, il faut executer main.py, un navigateur chrome se lancera sur la carte interactive. En vous déplaçant dans le jeu, le programme va faie une capture d'écran de la minimap, et en déduire les coordonnées, ainsi déplacer la carte interactive à ces mêmes coordonnées.

Ne fonctionne qu'avec un écran 1440x2560 (désolé, j'ai fait avec mon écran, je modifierai plus tard)

A faire:
- Utiliser une librairire plus rapide pour le knn
- Executer le knn en parralèl sur différents morceaux de la carte
- Essayer de faire une détéction par couches (Waypoints>Routes>batiments>topologie)
