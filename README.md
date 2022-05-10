# NOM_DU_PROGRAMME

NOM_DU_PROGRAMME est un programme de suivi de traitements phytosanitaires adapté à la viticulture.
Il est notamment utile pour obtenir les scores d'IFT, qu'il est capable de calculer pour chaque parcelle ou sur l'ensemble de l'exploitation, et sur des périodes définies par l'utilisateur.
NOM_DU_PROGRAMME vous permet d'enregistrer au format PDF un suivi complet de vos traitements (récapitulatif des traitements, scores d'IFT, gestion des résistances).


## Dépendances python

`pip install babel fpdf fpdf2 openpyxl pandas tkcalendar`


## Créer un installateur Windows

1) Créer un exécutable :
    - Décommenter les lignes `import pyi_splash` ; `pyi_splash.close()` et `fenetre.iconbitmap('icone.ico')` dans le script `main.py`
    - Lancer `cmd` en mode Administrateur
    - Se placer dans le dossier qui contient `main.py` (ex : `cd C:\Users\dougy147\Desktop\IFT` )
    - Lancer la commande suivante : `pyinstaller main.py --onefile -w --splash splashscreen.png`
    - Le fichier `main.exe` se trouve dans le dossier `dist`.
    - Le placer dans le dossier principal et le renommer en `IFT.exe` (modifiable)
    - On peut supprimer `main.py`, `recherche_produit.py`, `update.py`, `main.spec` et les dossiers `build`, `dist` et `__pycache__`

2) Créer l'installateur :
    - Télécharger et installer NSIS (https://sourceforge.net/projects/nsis/)
    - Ouvrir le fichier `C:\Program Files\NSIS\Contrib\zip2exe\Modern.nsh`
    - Y ajoutez les lignes suivantes (cela permettra de créer un raccourci sur le bureau durant l'installation) :
      ```
      section "install"
      	SetOutPath "$INSTDIR"
      	CreateShortcut "$DESKTOP\NOM_DU_PROGRAMME.lnk" "$INSTDIR\IFT.exe" "" "$INSTDIR\icone.ico"
      sectionEnd
      ```
    - Placer l'ensemble du contenu de NOM_DU_PROGRAMME dans un fichier .zip
    - Lancer `NSIS` et choisir `Installer based on .ZIP file`
    - `Open` le fichier .zip
    - Choisir `Interface` > `Modern`
    - `Default Folder` > `$DESKTOP\NOM_DU_PROGRAMME` (possible d'installer dans ProgramFiles, mais problèmes Administrateur pour écrire des fichiers #TODO)
    - `Output EXE File` > sur le bureau (endroit de sauvegarde de l'installateur)
    - Et enfin `Generate`

3) Enjoy!



# Informations supplémentaires

La base de données utilisée provient du site https://www.data-gouv.fr .
Elle est certifiée par le gouvernement (qui utilise les données Ephy).
https://www.data.gouv.fr/fr/datasets/donnees-ouvertes-du-catalogue-e-phy-des-produits-phytopharmaceutiques-matieres-fertilisantes-et-supports-de-culture-adjuvants-produits-mixtes-et-melanges/

L'adresse stable pour télécharger les données (qui peuvent être mises à jour via NOM_DU_PROGRAMME) est :
https://www.data.gouv.fr/fr/datasets/r/98f7cac6-6b29-4859-8739-51b825196959
