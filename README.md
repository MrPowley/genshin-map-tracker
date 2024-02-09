# Genshin map tracker [FR - EN]
## [FR]

Utilise la minimap de genshin pour trouver les coordonnées du joueur et les renvoyer sur la carte interactive pour suivre ses déplacements en temps réel 

Je n'ai pas fais d'interface et je n'ai pas encore écrit les intructions pour générer les données néccéssaires donc, pour l'instant, il faut télécharger les fichiers mis a disposition, et dans le dossier "assets", placer le fichier ["map_kp_des.pkl"](https://drive.google.com/drive/folders/1xb6ttWdshIqvR4PT60sf34nLL0auhF-8?usp=sharing)
Pour le lancer, il faut executer main.py, un navigateur chrome se lancera sur la carte interactive. En vous déplaçant dans le jeu, le programme va faire une capture d'écran de la minimap, et en déduire les coordonnées, et ainsi déplacer la carte interactive à ces mêmes coordonnées.

### A faire:
- Utiliser une librairire plus rapide pour le knn
- Executer le knn en parralèle sur différents morceaux de la carte
- Essayer de faire une détéction par couches (Waypoints>Routes>batiments>topologie)

### Fonctionnement (sans trop de détails)
1. Le programme récupère la résolution de l'écran (win32api GetSystemMetrics)
2. Il ouvre une version de chrome faite pour les scriptes automatisée(Donc pas de connexion automatique à son compte hoyoverse) (selenium webdriver)
3. Il verifie que l'interface de jeu(minimap, team à droite, menues en haut) sont visibles : à l'aide de pyautogui, on prend une capture d'écran de la zone où se trouve bouton de messages en bas à gauche de l'interface, avec opencv il teste si il y a un rectangle à cet emplacement, si non, il attends 2 secondes, si oui, il lance le programme de localisation (pyautogui, time, opencv)
4. Le programme fait une capture d'écran de la minicarte, la plus grande possible, et envoye cette image à la fonction locate() qui s'occupe du reste (pyautogui)
5. la fonction locate() commence par initialiser le detecteur SIFT d'opencv (opencv)
6. il calcule des points clées et descripteurs de l'image de la minimap (opencv)
7. il charge les points clés et descripteurs de la map complète, pré-calculés par mes soins (j'expliquerai plus tard comment s'y prendre)
8. il prépare les paramètres flann, le nombre de trees (ici il est à 1 pour accelerer le processus), le nombre de verifications à faire (ici 1000 pour compenser le manque de précision du seul tree) (opencv)
9. il vas ensuite initialiser le "matcheur" flann et executer un knn en comparant les descripteurs de la map complète et de la minimap (opencv)
10. les bons matchs sont triés pour garder les meilleurs
11. le programme verifie que le nombre de bon matchs est au dessus d'un seuil minimum prédéfini
12. il vas ensuite, par de la magie noire que je ne comprends pas : numpy, calculer des coordonnées du joueur à l'aide des points comparés (numpy, opencv)
13. il renvoye les coordonnées si elles ont bien été calculées, sans erreures, si les coordonnées n'ont pas pu être calculées ou qu'une erreur est survenue, il renvoye -9999, -9999 (coordonnées hors de la carte du jeu) pour indiquer à la suite du programme de passer cette detection
14. avec les coordonnées calculées, le programme execute la fonction de mise à jour de la carte interactive
15. le programme calcule le décalage entre les coordonnées calculées par rapport a la carte .png et les coordonnées du site de la carte interactive
16. il modifie l'url de base de la carte interactive pour y integrer les nouvelles coordonnées, puis met a jour le site


## [EN]

Uses the genshin minimap to find the player's coordinates and send them back onto the interactive map to follow the players movements in realtime

I haven't made an interface and I haven't written the instructions to generates the neccessary data so, for now, you have to download "map_kp_des.pkl" into the "assets" folder, with this link ["map_kp_des.pkl"](https://drive.google.com/drive/folders/1xb6ttWdshIqvR4PT60sf34nLL0auhF-8?usp=sharing)
To start it, you have to run main.py, a chrome tab will open directly on the genshin interactive map website. The programm will screenshot the genshin minimap to determin coordonates, then move the interactive map to follow your movements

### To-do
- Use a faster knn library
- Execute knn in parallel on diffrent parts of the map
- Try to make a by-layer detection (Waypoints>paths>buildings>topology)
  
### How it works (without too much details)
1. The programm gets the screen resolution (win32api GetSystemMetrics)
2. It opens a chrome version made for scripts automation (So no automatic login to your hoyoverse account) (selenium webdriver)
3. It checks il the game interface(Minimap, teams on the right, menues at the top) are visible: using pyautogui, it takes a screenshot where we should find a message button in the botton left corner, with opencv it tests if there is a rectangle in this area, if there's none, it waits 2 seconds, if there is one, il run the localisation programm (pyautogui, time, opencv)
4. The programm takes a screenshot of the minimap, the biggest possible, and send this image to the locate() function which takes care of the rest
5. the locate() function stars by initializing the opencv SIFT detector
6. It calculates keypoints and decriptors of the minimap image
7. It loads the keypoints and descriptors of the full map, that i pre calculated 
8. It prepares the flann parameters, number of trees (here, it's at 1 to speed-up the process), the number of checks (here 1000 to compensate for the lack of precision of the single tree)
9. It then initialise the flann matcher and execute a knn comparing the full map descriptors to the minimap descriptors
10. The good matchs are sorted to only keep the best ones
11. The programme verifies that the number of good matches is above a minimum predefined threshold
12. I will then, by an black magic i dont understand : numpy, calculate the player's coordinates using the compares points
13. It returns the coordinates if the have been corectly calculated, without errors, is the coordinates couldn't be calculated or and error happend, it returns -9999, -9999 (cordinates off map) to indicate to the rest of the programm to skip this detecion
14. With the calculated coordinates, the programm executes the function to update the interactive map
15. the programm calculates the offset beetwin the coordinates calculated in relation with the .png map, and the websites coordinates
16. It modifies the original url to include the new coordinates, the updates the website
