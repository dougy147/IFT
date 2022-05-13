# IFT Concept

`IFT Concept` (pour _**I**FT **F**acilite **T**out Concept_) est un programme de suivi de traitements phytosanitaires adapté à la viticulture.
Il est notamment utile pour obtenir les indicateurs de fréquence de traitement (IFT), qu'il est capable de calculer pour chaque traitement, parcelle et/ou sur l'ensemble de l'exploitation, ainsi que sur des périodes choisies par l'utilisateur.
`IFT Concept` vous permet d'enregistrer au format `.pdf` un suivi complet de vos traitements (récapitulatif des traitements sur la période et la parcelle choisies, indicateurs de fréquence de traitement, tableau de gestion des résistances).



## Créer un installateur Windows

Manipulations à réaliser sous Windows.

1) Créer un exécutable :
    - Cloner ce répertoire sur le Bureau
    - Décommenter les lignes `import pyi_splash` ; `pyi_splash.close()` et `fenetre.iconbitmap('icone.ico')` dans le script `main.py`
    - Lancer `cmd` en mode Administrateur
    - Se placer dans le dossier qui contient `main.py` (ex : `cd C:\Users\dougy147\Desktop\IFT Concept` )
    - S'assurer d'avoir installer `pyinstaller` : ⚠ éviter `pip install pyinstaller`, et le compiler depuis la source (voir la raison plus bas)
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
      	CreateShortcut "$DESKTOP\IFT Concept.lnk" "$INSTDIR\IFT.exe" "" "$INSTDIR\icone.ico"
      sectionEnd
      ```
    - Placer l'ensemble du contenu du dossier `IFT` dans un fichier .zip
    - Lancer `NSIS` et choisir `Installer based on .ZIP file`
    - `Open` le fichier .zip
    - Choisir `Interface` > `Modern`
    - `Default Folder` > `$DESKTOP\IFT` (possible d'installer dans Program Files, mais problèmes Administrateur pour écrire des fichiers #TODO)
    - `Output EXE File` > sur le bureau (endroit de sauvegarde de l'installateur)
    - Et enfin `Generate`

3) Enjoy!

### Compiler `pyinstaller` depuis la source

La compilation des scripts avec `pyinstaller` peut causer la détection de faux-positifs par les antivirus.
Pour tenter de l'éviter, il faut suivre les instructions de ce site : https://python.plainenglish.io/pyinstaller-exe-false-positive-trojan-virus-resolved-b33842bd3184


## Lancer `IFT Concept` sous Linux

- Installer `python` et les dépendances requises avec `pip`:

`pip install babel fpdf fpdf2 openpyxl pandas tkcalendar`
#TODO

- Puis exécuter les commandes suivantes :
```
git clone https://github.com/dougy147/IFT
cd ./IFT
python main.py
```


# Informations supplémentaires

La base de données utilisée provient du site [https://www.data-gouv.fr](https://www.data.gouv.fr/fr/datasets/donnees-ouvertes-du-catalogue-e-phy-des-produits-phytopharmaceutiques-matieres-fertilisantes-et-supports-de-culture-adjuvants-produits-mixtes-et-melanges/) .
Elle est certifiée par le gouvernement et est équivalente aux données [E-Phy](https://ephy.anses.fr).

L'adresse stable pour télécharger les données (qui peuvent être mises à jour via `IFT`) est :
https://www.data.gouv.fr/fr/datasets/r/98f7cac6-6b29-4859-8739-51b825196959
