import requests
import os
import zipfile
import pandas as pd
from urllib.request import urlopen
from os.path import basename

chemin_actuel=os.getcwd() #dossier de travail en cours pour le script
chemin_mise_a_jour=str(chemin_actuel)+str("/mise_a_jour_bdd")


def mettre_a_jour():
    # Adresse de la BDD
    url = 'https://www.data.gouv.fr/fr/datasets/r/98f7cac6-6b29-4859-8739-51b825196959'

    # Obtenir le nom du fichier et vérifier s'il correspond avec celui stocké dans 'mise_a_jour_bdd/info'
    nom_du_fichier = basename(urlopen(url).url)
    # Lire le contenu de 'info'
    fichier_infos = open("mise_a_jour_bdd/infos","r")
    ancienne_version = fichier_infos.read()
    print(nom_du_fichier, ancienne_version)
    fichier_infos.close()

    if nom_du_fichier in ancienne_version :
        print("La base est déjà à jour")
        infos_mise_a_jour = "Votre base de données de produits est déjà à jour."
        return(infos_mise_a_jour)

    # Mettre le nom de la nouvelle version dans 'infos'
    remplacer_infos = open("mise_a_jour_bdd/infos","w+")
    remplacer_infos.write(nom_du_fichier)
    remplacer_infos.close()


    # Télécharger le fichier avec la date (pour pouvoir comparer à la date de la BDD actuelle)
    requete = requests.get(url, allow_redirects=True)
    open('mise_a_jour_bdd/'+str(nom_du_fichier), 'wb').write(requete.content)


    # Dézipper le dossier :
    os.chdir(chemin_mise_a_jour)
    for item in os.listdir(chemin_mise_a_jour):
        if item.endswith(".zip"):
            file_name = os.path.abspath(item)
            zip_ref = zipfile.ZipFile(file_name)
            zip_ref.extractall(chemin_mise_a_jour)
            zip_ref.close()
            os.remove(file_name)

    # Si le nom du fichier téléchargé diffère du précédent, alors poursuivre (garder_le_fichier_utile()) sinon c'est à jour
    #print("ok")

    fichier_nouvelle_base = [i for i in os.listdir(chemin_mise_a_jour) if os.path.isfile(os.path.join(chemin_mise_a_jour,i)) and \
         'usages_des_produits_autorises' in i] #garde les fichiers qui contiennent 'produit_usages_'
    fichier_nouvelle_base = [j for j in list(fichier_nouvelle_base) if 'utf8.csv' in j] # on ne garde que 'utf8.csv'
    fichier_nouvelle_base = fichier_nouvelle_base[0]
    if not fichier_nouvelle_base :
        print("Erreur. Nouvelle BDD introuvable.") # que faire dans ce cas-là ? TODO
    else :
        print("Nouvelle base trouvée.")
    # Suppression des autres fichiers (à l'exception de celui-ci et du fichier 'infos' qui contiendra la date pour comparaison
    os.chdir(chemin_mise_a_jour)
    for fichier in os.listdir(chemin_mise_a_jour): # loop through items in dir
        if fichier == fichier_nouvelle_base :
            print("fichier gardé")
        elif fichier == "infos" :
            print("fichier non supprimé")
        else :
            chemin_du_fichier_a_supprimer=str(chemin_mise_a_jour)+str("/")+str(fichier)
            os.remove(chemin_du_fichier_a_supprimer)

    # Ici je veux ne garder que les lignes qui parlent des vignes
    chemin_fichier_nouvelle_base = str(chemin_mise_a_jour)+str("/")+str(fichier_nouvelle_base)
    bdd_complete = pd.read_csv(chemin_fichier_nouvelle_base, sep=';')
    # Retirer ce qui ne contient pas "vigne"
    recherche = ['vigne', 'traitements', 'adjuvants']
    #recherche = ['vigne', 'adjuvants']
    nouvelle_bdd=bdd_complete[bdd_complete['identifiant usage'].str.contains('|'.join(recherche), na=False, case=False)]

    # NEW 2022
    # si dans la colonne "(produit) seconds noms commerciaux" il y a des noms de produits ajouter des lignes à la BDD
    # for each line of "(produit) seconds noms commerciaux"
        # if is not empty
            # for each NAME (separator = "|" )
                # copy this line to BDD as new line, replacing "(produit) nom produit" by NAME
    for ligne in range(len(nouvelle_bdd)):
        new_line = nouvelle_bdd.iloc[ligne]
        noms_produits = str(new_line['(produit) seconds noms commerciaux'])
        if not noms_produits == "nan" :
            nom_primaire = str(new_line['(produit) nom produit'])
            liste_noms_produits = noms_produits.split(' | ')
            for nom in liste_noms_produits :
                #print(nom)
                ligne_en_cours = new_line
                ligne_en_cours['(produit) nom produit'] = nom
                ligne_en_cours['(produit) seconds noms commerciaux'] = nom_primaire + " (nom primaire)"
                nouvelle_bdd = nouvelle_bdd.append(ligne_en_cours, ignore_index=True)


    # Remplace l'ancienne BDD
    chemin_enregistrement = str(chemin_actuel)+str("/bdd_phyto.csv")
    # Changer les en-tête ?
    nouvelle_bdd.to_csv(chemin_enregistrement, sep=';', index = False)
    infos_mise_a_jour="La base a bien été mise à jour."
    os.chdir(chemin_actuel)
    return(infos_mise_a_jour)
