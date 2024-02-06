# genshin-map-tracker
Traque sa position sur genshin en utilisant la minimap pour suivre sa position sur la carte interactive hoyolab

Je n'ai pas fais d'interface, donc pour l'instant, il faut télécharger les fichiers mis a disposition, et dans un dossier "assets", placer le fichier ["map_kp_des.pkl"](https://drive.google.com/drive/folders/1xb6ttWdshIqvR4PT60sf34nLL0auhF-8?usp=sharing)
Pour le lancer, il faut executer main.py, un navigateur chrome se lancera sur la carte interactive. En vous déplaçant dans le jeu, le programme va faie une capture d'écran de la minimap, et en déduire les coordonnées, ainsi déplacer la carte interactive à ces mêmes coordonnées.