# IFT

`IFT` (pour _*I*FT *F*acilite *T*out_)  est un programme de suivi de traitements phytosanitaires adapté à la viticulture.
Il est notamment utile pour obtenir les scores d'IFT, qu'il est capable de calculer pour chaque parcelle ou sur l'ensemble de l'exploitation, et sur des périodes définies par l'utilisateur.
`IFT` vous permet d'enregistrer au format PDF un suivi complet de vos traitements (récapitulatif des traitements, indicateurs de fréquence de traitement (IFT), gestion des résistances).


## Dépendances python

`pip install babel fpdf fpdf2 openpyxl pandas tkcalendar`


## Créer un installateur Windows

Manipulations à réaliser sous Windows.

1) Créer un exécutable :
    - Décommenter les lignes `import pyi_splash` ; `pyi_splash.close()` et `fenetre.iconbitmap('icone.ico')` dans le script `main.py`
    - Lancer `cmd` en mode Administrateur
    - Se placer dans le dossier qui contient `main.py` (ex : `cd C:\Users\dougy147\Desktop\IFT` )
    - S'assurer d'avoir installer `pyinstaller` : ⚠ éviter `pip install pyinstaller`, et le compiler depuis la source (voir plus bas)
    - Lancer la commande : `pyinstaller main.py --onefile -w --splash splashscreen.png`
    - Déplacer `main.exe` (situé dans le dossier `dist`) dans le dossier principal des scripts et le renommer en `IFT.exe` (modifiable)
    - Supprimer `main.py`, `recherche_produit.py`, `update.py`, `main.spec` et les dossiers `build`, `dist` et `__pycache__`

2) Créer l'installateur :
    - Télécharger et installer NSIS (https://sourceforge.net/projects/nsis/)
    - Ouvrir le fichier `C:\Program Files\NSIS\Contrib\zip2exe\Modern.nsh`
    - Y ajoutez les lignes suivantes (cela permettra de créer un raccourci sur le bureau durant l'installation) :
      ```
      section "install"
      	SetOutPath "$INSTDIR"
      	CreateShortcut "$DESKTOP\IFT.lnk" "$INSTDIR\IFT.exe" "" "$INSTDIR\icone.ico"
      sectionEnd
      ```
    - Placer l'ensemble du contenu de `IFT` dans un fichier .zip
    - Lancer `NSIS` et choisir `Installer based on .ZIP file`
    - `Open` le fichier .zip
    - Choisir `Interface` > `Modern`
    - `Default Folder` > `$DESKTOP\IFT` (possible d'installer dans ProgramFiles, mais problèmes Administrateur pour écrire des fichiers #TODO)
    - `Output EXE File` > sur le bureau (endroit de sauvegarde de l'installateur)
    - Et enfin `Generate`

3) Enjoy!

### Compiler `pyinstaller` depuis la source

La compilation des scripts avec `pyinstaller` peut causer la détection de faux-positifs par les antivirus.
Pour tenter de l'éviter, il faut suivre les instructions de ce site : https://python.plainenglish.io/pyinstaller-exe-false-positive-trojan-virus-resolved-b33842bd3184



# Informations supplémentaires

La base de données utilisée provient du site [https://www.data-gouv.fr](https://www.data.gouv.fr/fr/datasets/donnees-ouvertes-du-catalogue-e-phy-des-produits-phytopharmaceutiques-matieres-fertilisantes-et-supports-de-culture-adjuvants-produits-mixtes-et-melanges/) .
Elle est certifiée par le gouvernement et est équivalente aux données [E-Phy](https://ephy.anses.fr).

L'adresse stable pour télécharger les données (qui peuvent être mises à jour via `IFT`) est :
https://www.data.gouv.fr/fr/datasets/r/98f7cac6-6b29-4859-8739-51b825196959
