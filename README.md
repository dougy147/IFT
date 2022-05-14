# <img src="icone.ico" width='40px'> IFT Concept (version beta)

<p align="justify">
<code>IFT Concept</code> est un logiciel <b>gratuit</b> de suivi de traitements phytosanitaires adapté à la viticulture en Champagne.
Il est notamment utile pour obtenir les indicateurs de fréquence de traitement (IFT), qu'il est capable de calculer pour chaque traitement, parcelle et/ou sur l'ensemble de l'exploitation, ainsi que sur des périodes choisies.
<code>IFT Concept</code> permet d'enregistrer et d'imprimer des comptes rendus complets comportant : un récapitulatif des traitements sur la période et la parcelle choisies, les indicateurs de fréquence de traitement, un tableau de gestion des résistances.

![](iftconcept.gif)
</p>

## Informations supplémentaires

La base de données utilisée par `IFT Concept` provient du site [data-gouv.fr](https://www.data.gouv.fr/fr/datasets/donnees-ouvertes-du-catalogue-e-phy-des-produits-phytopharmaceutiques-matieres-fertilisantes-et-supports-de-culture-adjuvants-produits-mixtes-et-melanges/).
Elle est certifiée par le gouvernement et est équivalente aux données [E-Phy](https://ephy.anses.fr).
`IFT Concept` s'appuie sur [cette adresse stable](https://www.data.gouv.fr/fr/datasets/r/98f7cac6-6b29-4859-8739-51b825196959) pour récupérer les nouvelles données phytosanitaires.
Les produits et doses réglementaires seront donc toujours à jour (voir l'onglet `Édition > Mettre la base des produits à jour`).


⚠️ `IFT Concept` filtre automatiquement les produits `Retirés`. Cela peut représenter un problème pour enregistrer des traitements ayant eu lieu avant la date de retrait de ces produits. Une fonctionnalité sera bientôt ajoutée pour pouvoir les enregistrer.

⚠️ `IFT Concept` est en cours d'écriture et peut comporter quelques bugs ou manquer de certaines fonctionnalités utiles. N'hésitez pas à nous en faire part [ici](https://iftconcept.fr/contact.php).


# Installation

## Windows

### Télécharger l'installateur

La dernière version exécutable (Windows) est disponible à tout moment sur le [site officiel](https://iftconcept.fr) ou depuis le dossier `./installateur_windows/IFT.exe` de ce dépôt.

### (Alternative) Compiler depuis la source

- Cloner ce répertoire sur le Bureau
- Décommenter les lignes `import pyi_splash` ; `pyi_splash.close()` et `fenetre.iconbitmap('icone.ico')` dans le script `main.py`
- Lancer `cmd` en mode Administrateur
- Se placer dans le dossier qui contient `main.py` (ex : `cd C:\Users\dougy147\Desktop\IFT` )
- S'assurer d'avoir installer `pyinstaller` : ⚠ éviter `pip install pyinstaller`, et le compiler depuis la source (voir la raison plus bas)
- Lancer la commande : `pyinstaller main.py --onefile -w --splash splashscreen.png`
- Déplacer `main.exe` (situé dans le dossier `dist`) dans le dossier principal des scripts et le renommer en `IFT.exe` (selon convenance)
- Supprimer `main.py`, `recherche_produit.py`, `update.py`, `main.spec` et les dossiers `build`, `dist` et `__pycache__`
- Lancer `IFT.exe`

Si vous souhaitez créer votre propre installateur, poursuivez avec les étapes ci-dessous :

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


#### Compiler `pyinstaller` depuis la source

La compilation des scripts avec `pyinstaller` peut causer la détection de faux-positifs par les antivirus.
Cela est dû au fait que les pirates utilisent `pyinstaller` pour compiler des programmes malveillants.
Pour tenter d'éviter que `IFT Concept` ne soit reconnu comme une menace (le code reste open source...), il faut suivre les instructions de ce site : https://python.plainenglish.io/pyinstaller-exe-false-positive-trojan-virus-resolved-b33842bd3184

#TODO

## Linux

S'assurer d'avoir installer `python` ou `python3`.

### Depuis l'environnement virtuel

```
git clone https://github.com/dougy147/IFT
cd ./IFT
source ./env/bin/activate
python main.py
```

### Directement avec `python` (en installant les dépendances)

```
git clone https://github.com/dougy147/IFT
cd ./IFT
pip install -r requirements.txt
python main.py
```


# Thème utilisé

Azure-ttk-theme : [https://github.com/rdbende/Azure-ttk-theme](https://github.com/rdbende/Azure-ttk-theme)
