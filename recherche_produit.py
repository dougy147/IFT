import pandas as pd
import os
from tkinter import filedialog
import fpdf
from fpdf import *
from fpdf import FPDF, HTMLMixin
from datetime import date
import time

# Rechercher le produit

df = pd.read_csv ('bdd_phyto.csv',sep=';')

def backslasher_les_caracteres_speciaux(variable_a_backslasher):
    variable_originale=variable_a_backslasher
    variable_backslashee = variable_originale.translate(str.maketrans({"-":  r"\-",
                                                       "]":  r"\]",
                                                       "\\": r"\\",
                                                       "^":  r"\^",
                                                       "$":  r"\$",
                                                       "*":  r"\*",
                                                       "(":  r"\(",
                                                       ")":  r"\)",
                                                       "|":  r"|)",
                                                       ".":  r"\."}))
    return(variable_backslashee , variable_originale)

def produits_possibles(produit_a_chercher):
    df = pd.read_csv ('bdd_phyto.csv',sep=';')
    lignes_qui_contiennent_le_nom_du_produit=df[df['(produit) nom produit'].str.contains(produit_a_chercher, na=False, case=False)]
    if lignes_qui_contiennent_le_nom_du_produit.empty:
        liste_produits_possibles=["Le produit n'est pas trouvé."]
        return(liste_produits_possibles)
        return
    lignes_indiquant_le_retrait_du_produit=lignes_qui_contiennent_le_nom_du_produit[lignes_qui_contiennent_le_nom_du_produit['etat usage'].str.contains("Retrait", na=False, case=False)]
    lignes_indiquant_autorisation=lignes_qui_contiennent_le_nom_du_produit[lignes_qui_contiennent_le_nom_du_produit['etat usage'].str.contains("Autorisé", na=False, case=False)]
    if not lignes_indiquant_le_retrait_du_produit.empty:
        if lignes_indiquant_autorisation.empty:
            liste_produits_possibles=["Le produit a été retiré."]
            return(liste_produits_possibles)
            return
        else :
            lignes_qui_contiennent_le_nom_du_produit=lignes_indiquant_autorisation
    if len(lignes_qui_contiennent_le_nom_du_produit) > 1:
        noms_de_produits=[]
        produits_differents=0
        for ligne in range(len(lignes_qui_contiennent_le_nom_du_produit)):
            noms_de_produits.append(lignes_qui_contiennent_le_nom_du_produit['(produit) nom produit'].iloc[ligne])
        for item in range(len(noms_de_produits)-1):
            if noms_de_produits[item] != noms_de_produits[item+1]:
                produits_differents=1
                break
        if produits_differents == 1:
            liste_produits_possibles=[]
            for produit in range(len(lignes_qui_contiennent_le_nom_du_produit)):
                liste_produits_possibles.append(lignes_qui_contiennent_le_nom_du_produit['(produit) nom produit'].iloc[produit])
        else :
            liste_produits_possibles=[lignes_qui_contiennent_le_nom_du_produit['(produit) nom produit'].iloc[0]]
    else :
        liste_produits_possibles=[lignes_qui_contiennent_le_nom_du_produit['(produit) nom produit'].iloc[0]]
    # Retirer les doublons de la liste 'liste_des_produits_possibles'
    item_en_cours=[]
    for item in list(liste_produits_possibles):
        if not item in item_en_cours:
            item_en_cours.append(item)
    liste_produits_possibles=item_en_cours
    return(liste_produits_possibles)
    liste_produits_possibles=[] # permet de vider la liste une fois la fonction finie

def verifier_si_meme_doses(produit_choisi):
    liste_utilisations_pour_le_produit=[]
    liste_doses_pour_le_produit=[]
    lignes_qui_contiennent_le_nom_du_produit=df[df['(produit) nom produit'].str.contains(produit_choisi, na=False)]
    lignes_qui_contiennent_le_nom_du_produit=lignes_qui_contiennent_le_nom_du_produit[lignes_qui_contiennent_le_nom_du_produit['etat usage'].str.contains("Autorisé", na=False, case=False)]
    for ligne in range(len(lignes_qui_contiennent_le_nom_du_produit)):
        liste_doses_pour_le_produit.append(lignes_qui_contiennent_le_nom_du_produit['dose retenue'].iloc[ligne])
        liste_utilisations_pour_le_produit.append(lignes_qui_contiennent_le_nom_du_produit['identifiant usage'].iloc[ligne]) # récupérer les utilisations
    return(liste_doses_pour_le_produit, liste_utilisations_pour_le_produit)

def choisir_ligne_en_fonction_dose(produit_choisi,dose_choisie,utilisation_choisie):
    lignes_qui_contiennent_le_nom_du_produit=df[df['(produit) nom produit'].str.contains(produit_choisi, na=False)]
    lignes_qui_contiennent_le_nom_du_produit=lignes_qui_contiennent_le_nom_du_produit[lignes_qui_contiennent_le_nom_du_produit['etat usage'].str.contains("Autorisé", na=False, case=False)]
    lignes_qui_contiennent_le_nom_du_produit = lignes_qui_contiennent_le_nom_du_produit[lignes_qui_contiennent_le_nom_du_produit['dose retenue'].eq(float(dose_choisie))]
    utilisation_choisie_sans_caracteres_speciaux = utilisation_choisie.translate(str.maketrans({"-":  r"\-",
                                                           "]":  r"\]",
                                                           "\\": r"\\",
                                                           "^":  r"\^",
                                                           "$":  r"\$",
                                                           "*":  r"\*",
                                                           "(":  r"\(",
                                                           ")":  r"\)",
                                                           ".":  r"\."}))
    lignes_qui_contiennent_le_nom_du_produit = lignes_qui_contiennent_le_nom_du_produit[lignes_qui_contiennent_le_nom_du_produit['identifiant usage'].str.contains(utilisation_choisie_sans_caracteres_speciaux, na=False, case=False)]
    dose_autorisee=lignes_qui_contiennent_le_nom_du_produit['dose retenue'].iloc[0]
    unite=lignes_qui_contiennent_le_nom_du_produit['dose retenue unite'].iloc[0]
    applications=lignes_qui_contiennent_le_nom_du_produit["nombre max d'application"].iloc[0]
    produit_est_il_un_herbicide=str(lignes_qui_contiennent_le_nom_du_produit["(produit) fonctions"].iloc[0])
    if type(produit_est_il_un_herbicide) == str:
        a_trouver="Herbicide"
        if a_trouver in produit_est_il_un_herbicide :
            produit_est_il_un_herbicide=1
        else :
            produit_est_il_un_herbicide=0
    else :
        produit_est_il_un_herbicide=0

    return(dose_autorisee, unite, applications,produit_est_il_un_herbicide)

def recuperer_infos(nom_du_produit,utilisation_produit,dose_produit):
    resultat_biocontrole=0
    dose_produit=float(dose_produit)
    base=df[df['(produit) nom produit'].str.contains(nom_du_produit, na=False)]
    base=base[base['etat usage'].str.contains("Autorisé", na=False, case=False)]
    utilisation_produit_backslashee,utilisation_produit_originale=backslasher_les_caracteres_speciaux(utilisation_produit)
    #utilisation_produit_backslashee=str(utilisation_produit_backslashee)
    base=base[base['identifiant usage'].str.contains(utilisation_produit_backslashee, na=False)]
    base=base[base['dose retenue'].eq(float(dose_produit))]
    # Récupérer "biocontrôle"
    test_biocontrole=base['(produit) mentions autorisees'].iloc[0]
    if type(test_biocontrole) == str:
        a_trouver="Liste biocontr"
        if a_trouver in test_biocontrole :
            resultat_biocontrole=1
    # AMM
    amm=base['(produit) numero AMM'].iloc[0]
    # Substances actives
    substances=base['(produit) Substances actives'].iloc[0]
    # Fonction (herbicide, fongicide, etc.)
    fonction=base['(produit) fonctions'].iloc[0]
    return(resultat_biocontrole,amm,substances,fonction)




def recapitulatif(nom_parcelle,surface_exploitation,periode,debut,fin):
    # Si IFT vide : retourner les valeurs 0 pour tous les IFT
    tester_si_IFT_vide = pd.read_excel('IFT.xlsx')
    if tester_si_IFT_vide.empty :
        return(0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

    premiere_date_traitement=""
    if periode == 1 :
        fichier_IFT = pd.read_excel('IFT.xlsx')
        fichier_IFT['date_traitement'] = pd.to_datetime(fichier_IFT['date_traitement'], format = '%d/%m/%Y')
        debut_formate = pd.to_datetime(debut, format = "%d/%m/%Y")
        fin_formate = pd.to_datetime(fin, format = "%d/%m/%Y")
        fichier_IFT = fichier_IFT[(fichier_IFT['date_traitement'] >= debut_formate ) & (fichier_IFT['date_traitement'] <= fin_formate)]
        fichier_IFT['date_traitement'] = fichier_IFT['date_traitement'].dt.strftime('%d/%m/%Y')
    else :
        fichier_IFT = pd.read_excel('IFT.xlsx')
        if nom_parcelle == "Toute l'exploitation" :
            premiere_date_traitement = fichier_IFT['date_traitement'].iloc[0]
            premiere_date_traitement_formate = pd.to_datetime(premiere_date_traitement, format = "%d/%m/%Y")
            fichier_IFT['date_traitement'] = pd.to_datetime(fichier_IFT['date_traitement'], format = '%d/%m/%Y')
            for ligne in range(len(fichier_IFT)):
                if fichier_IFT['date_traitement'].iloc[ligne] <= premiere_date_traitement_formate :
                    premiere_date_traitement_formate = fichier_IFT['date_traitement'].iloc[ligne]
                    fichier_IFT['date_traitement'] = fichier_IFT['date_traitement'].dt.strftime('%d/%m/%Y')
                    premiere_date_traitement = fichier_IFT['date_traitement'].iloc[ligne]
                    fichier_IFT['date_traitement'] = pd.to_datetime(fichier_IFT['date_traitement'], format = '%d/%m/%Y')
            fichier_IFT['date_traitement'] = fichier_IFT['date_traitement'].dt.strftime('%d/%m/%Y')

        else :
            lignes_contenant_parcelle = fichier_IFT[fichier_IFT['nom_parcelle'].str.contains(nom_parcelle,na=False)]
            premiere_date_traitement=lignes_contenant_parcelle['date_traitement'].iloc[0]
            premiere_date_traitement_formate = pd.to_datetime(premiere_date_traitement, format = "%d/%m/%Y")
            lignes_contenant_parcelle['date_traitement'] = pd.to_datetime(lignes_contenant_parcelle['date_traitement'], format = '%d/%m/%Y')
            for ligne in range(len(lignes_contenant_parcelle)):
                if lignes_contenant_parcelle['date_traitement'].iloc[ligne] <= premiere_date_traitement_formate :
                    premiere_date_traitement_formate = lignes_contenant_parcelle['date_traitement'].iloc[ligne]
                    lignes_contenant_parcelle['date_traitement'] = lignes_contenant_parcelle['date_traitement'].dt.strftime('%d/%m/%Y')
                    premiere_date_traitement = lignes_contenant_parcelle['date_traitement'].iloc[ligne]
                    lignes_contenant_parcelle['date_traitement'] = pd.to_datetime(lignes_contenant_parcelle['date_traitement'], format = '%d/%m/%Y')
            lignes_contenant_parcelle['date_traitement'] = lignes_contenant_parcelle['date_traitement'].dt.strftime('%d/%m/%Y')

#    fichier_IFT = pd.read_excel('IFT.xlsx')
    # Si dans la combobox c'est "toute l'exploitation" qui est choisie alors on importe tout, sinon on le fait avec la parcelle en cours
    if nom_parcelle == "Toute l'exploitation" :
        base=fichier_IFT
    else :
        base=fichier_IFT[fichier_IFT['nom_parcelle'].str.contains(nom_parcelle,na=False)]
        surface_exploitation=base['surface_totale_parcelle'].iloc[0]

    # Surface en confusion sexuelle #TODO
    liste_parcelles= pd.read_excel('liste_parcelles.xlsx')
    surface_en_confusion_sexuelle=0 ##### TODO !!!!!!!
    if nom_parcelle == "Toute l'exploitation" :
        for i in range(len(liste_parcelles)):
            taille_confusion_en_cours = float(liste_parcelles['taille_en_confusion_sexuelle'].iloc[i])
            surface_en_confusion_sexuelle = float(surface_en_confusion_sexuelle + taille_confusion_en_cours)
    else :
        liste_parcelles=liste_parcelles[liste_parcelles['nom_parcelle'].str.contains(nom_parcelle,na=False)]
        surface_en_confusion_sexuelle=float(liste_parcelles['taille_en_confusion_sexuelle'].iloc[0])

    # IFT biocontrôle = (surface en confusion sexuelle / surface totale) + somme_si_bioncontrole_egale_1((dose appliquée*surfae traitée)/(dose référence * taille exploitation))
    lignes_avec_biocontrole = base[base['biocontrole'].eq(1)]
    IFT_en_cours=[]
    somme_IFT_biocontrole=0
    for i in range(len(lignes_avec_biocontrole)):
        dose=lignes_avec_biocontrole['dose_appliquee'].iloc[i]
        surface=lignes_avec_biocontrole['surface_traitee'].iloc[i]
        dose_reference=lignes_avec_biocontrole['dose_reglementaire'].iloc[i]
        IFT_en_cours.append(((dose*surface)/(dose_reference*surface_exploitation)))
    dose=0
    surface=0
    dose_reference=0
    for j in range(len(IFT_en_cours)):
        somme_IFT_biocontrole=somme_IFT_biocontrole + IFT_en_cours[j]
    IFT_en_cours=[]
    IFT_biocontrole = round(float((surface_en_confusion_sexuelle / surface_exploitation) + somme_IFT_biocontrole),2)

    # IFT classique = IFT total (calculé dans onglet "parcelles") - IFT biocontrôle
    lignes_sans_biocontrole = base[base['biocontrole'].eq(0)]
    IFT_en_cours=[]
    somme_IFT_classique=0
    for i in range(len(lignes_sans_biocontrole)):
        dose=lignes_sans_biocontrole['dose_appliquee'].iloc[i]
        surface=lignes_sans_biocontrole['surface_traitee'].iloc[i]
        dose_reference=lignes_sans_biocontrole['dose_reglementaire'].iloc[i]
        #IFT_en_cours.append((surface_en_confusion_sexuelle / surface_exploitation) + ((dose*surface)/(dose_reference*surface_exploitation)))
        IFT_en_cours.append(((dose*surface)/(dose_reference*surface_exploitation)))
    dose=0
    surface=0
    dose_reference=0
    for j in range(len(IFT_en_cours)):
        somme_IFT_classique=somme_IFT_classique + IFT_en_cours[j]
    IFT_en_cours=[]
    #IFT_classique = round(float((surface_en_confusion_sexuelle / surface_exploitation) + somme_IFT_classique),2)
    IFT_classique = round(float(somme_IFT_classique),2)

    # IFT Total (dans onglet "parcelles")
    #lignes_IFT = base
    #IFT_en_cours=[]
    #somme_IFT=0
    #for i in range(len(lignes_IFT)):
    #    dose=lignes_IFT['dose_appliquee'].iloc[i]
    #    surface=lignes_IFT['surface_traitee'].iloc[i]
    #    dose_reference=lignes_IFT['dose_reglementaire'].iloc[i]
    #    IFT_en_cours.append(((dose*surface)/(dose_reference*surface_exploitation)))
    #dose=0
    #surface=0
    #dose_reference=0
    #for j in range(len(IFT_en_cours)):
    #    #print(IFT_en_cours[j])
    #    somme_IFT=somme_IFT + float(IFT_en_cours[j])
    #IFT_total = round(float(somme_IFT),2)
    IFT_total = round(float(IFT_classique + IFT_biocontrole),2)

    # IFT mildiou = IFT si cible égale  "mildiou" (dans colonne "identifiant usage")
    lignes_mildiou = base[base['identifiant_usage'].str.contains("mildiou",case=False, na=False)]
    IFT_en_cours=[]
    somme_IFT_mildiou=0
    for i in range(len(lignes_mildiou)):
        dose=lignes_mildiou['dose_appliquee'].iloc[i]
        surface=lignes_mildiou['surface_traitee'].iloc[i]
        dose_reference=lignes_mildiou['dose_reglementaire'].iloc[i]
        IFT_en_cours.append(((dose*surface)/(dose_reference*surface_exploitation)))
    dose=0
    surface=0
    dose_reference=0
    for j in range(len(IFT_en_cours)):
        somme_IFT_mildiou=somme_IFT_mildiou + IFT_en_cours[j]
    IFT_en_cours=[]
    IFT_mildiou = round(float(somme_IFT_mildiou),2)



    # IFT oidium
    lignes_oidium = base[base['identifiant_usage'].str.contains("oïdium",case=False, na=False)]
    IFT_en_cours=[]
    somme_IFT_oidium=0
    for i in range(len(lignes_oidium)):
        dose=lignes_oidium['dose_appliquee'].iloc[i]
        surface=lignes_oidium['surface_traitee'].iloc[i]
        dose_reference=lignes_oidium['dose_reglementaire'].iloc[i]
        IFT_en_cours.append(((dose*surface)/(dose_reference*surface_exploitation)))
    dose=0
    surface=0
    dose_reference=0
    for j in range(len(IFT_en_cours)):
        somme_IFT_oidium=somme_IFT_oidium + IFT_en_cours[j]
    IFT_en_cours=[]
    IFT_oidium = round(float(somme_IFT_oidium),2)

    # IFT botrytis
    lignes_botrytis = base[base['identifiant_usage'].str.contains("pourriture grise",case=False, na=False)]
    IFT_en_cours=[]
    somme_IFT_botrytis=0
    for i in range(len(lignes_botrytis)):
        dose=lignes_botrytis['dose_appliquee'].iloc[i]
        surface=lignes_botrytis['surface_traitee'].iloc[i]
        dose_reference=lignes_botrytis['dose_reglementaire'].iloc[i]
        IFT_en_cours.append(((dose*surface)/(dose_reference*surface_exploitation)))
    dose=0
    surface=0
    dose_reference=0
    for j in range(len(IFT_en_cours)):
        somme_IFT_botrytis=somme_IFT_botrytis + IFT_en_cours[j]
    IFT_en_cours=[]
    IFT_botrytis = round(float(somme_IFT_botrytis),2)

    # IFT fongicide autres
    autres_fongicides = ['black rot', 'rougeot parasitaire']
    lignes_autres_fongicides = base[base['identifiant_usage'].str.contains('|'.join(autres_fongicides),case=False, na=False)]
    IFT_en_cours=[]
    somme_IFT_autres_fongicides=0
    for i in range(len(lignes_autres_fongicides)):
        dose=lignes_autres_fongicides['dose_appliquee'].iloc[i]
        surface=lignes_autres_fongicides['surface_traitee'].iloc[i]
        dose_reference=lignes_autres_fongicides['dose_reglementaire'].iloc[i]
        IFT_en_cours.append(((dose*surface)/(dose_reference*surface_exploitation)))
    dose=0
    surface=0
    dose_reference=0
    for j in range(len(IFT_en_cours)):
        somme_IFT_autres_fongicides=somme_IFT_autres_fongicides + IFT_en_cours[j]
    IFT_en_cours=[]
    IFT_autres_fongicides = round(float(somme_IFT_autres_fongicides),2)

    # IFT fongicide total
    IFT_fongicide_total = round(IFT_mildiou + IFT_oidium + IFT_botrytis + IFT_autres_fongicides,2)

    # IFT confusion sexuelle
    IFT_confusion_sexuelle = round((surface_en_confusion_sexuelle / surface_exploitation),2)

    # IFT acaricide
    lignes_acaricides = base[base['identifiant_usage'].str.contains(("acariens"),case=False, na=False)]
    IFT_en_cours=[]
    somme_IFT_acaricides=0
    for i in range(len(lignes_acaricides)):
        dose=lignes_acaricides['dose_appliquee'].iloc[i]
        surface=lignes_acaricides['surface_traitee'].iloc[i]
        dose_reference=lignes_acaricides['dose_reglementaire'].iloc[i]
        IFT_en_cours.append(((dose*surface)/(dose_reference*surface_exploitation)))
    dose=0
    surface=0
    dose_reference=0
    for j in range(len(IFT_en_cours)):
        somme_IFT_acaricides=somme_IFT_acaricides + IFT_en_cours[j]
    IFT_en_cours=[]
    IFT_acaricides = round(float(somme_IFT_acaricides),2)

    # IFT insecticide autre
    autres_acaricides = ['chenilles phytophages', 'cicadelles','cochenilles','coléoptères phytophages','erinose','mouches','thrips','tordeuses de la grappe']
    lignes_autres_acaricides = base[base['identifiant_usage'].str.contains('|'.join(autres_acaricides),case=False, na=False)]
    IFT_en_cours=[]
    somme_IFT_autres_acaricides=0
    for i in range(len(lignes_autres_acaricides)):
        dose=lignes_autres_acaricides['dose_appliquee'].iloc[i]
        surface=lignes_autres_acaricides['surface_traitee'].iloc[i]
        dose_reference=lignes_autres_acaricides['dose_reglementaire'].iloc[i]
        IFT_en_cours.append(((dose*surface)/(dose_reference*surface_exploitation)))
    dose=0
    surface=0
    dose_reference=0
    for j in range(len(IFT_en_cours)):
        somme_IFT_autres_acaricides=somme_IFT_autres_acaricides + IFT_en_cours[j]
    IFT_en_cours=[]
    IFT_autres_acaricides = round(float(somme_IFT_autres_acaricides),2)


    # IFT insecticide total
    IFT_insecticide_total = round(IFT_confusion_sexuelle + IFT_acaricides + IFT_autres_acaricides,2)

    # IFT hors herbicides
    IFT_hors_herbicides = round(IFT_fongicide_total + IFT_insecticide_total,2)

    # IFT hors herbicides biocontrôle
    #IFT_hors_herbicides_biocontrole = IFT_confusion_sexuelle + somme -


    # IFT hors herbicides hors biocontrôle
    # IFT prélevée
    lignes_herbicide_prelevee = base[base['si_herbicide'].str.contains("prélevée", na=False)]
    IFT_en_cours=[]
    somme_IFT_herbicide_prelevee=0
    for i in range(len(lignes_herbicide_prelevee)):
        dose=lignes_herbicide_prelevee['dose_appliquee'].iloc[i]
        surface=lignes_herbicide_prelevee['surface_traitee'].iloc[i]
        dose_reference=lignes_herbicide_prelevee['dose_reglementaire'].iloc[i]
        IFT_en_cours.append(((dose*surface)/(dose_reference*surface_exploitation)))
    dose=0
    surface=0
    dose_reference=0
    for j in range(len(IFT_en_cours)):
        somme_IFT_herbicide_prelevee=somme_IFT_herbicide_prelevee + IFT_en_cours[j]
    IFT_en_cours=[]
    IFT_herbicide_prelevee = round(float(somme_IFT_herbicide_prelevee),2)

    # IFT postlevée
    lignes_herbicide_postlevee = base[base['si_herbicide'].str.contains("postlevée", na=False)]
    IFT_en_cours=[]
    somme_IFT_herbicide_postlevee=0
    for i in range(len(lignes_herbicide_postlevee)):
        dose=lignes_herbicide_postlevee['dose_appliquee'].iloc[i]
        surface=lignes_herbicide_postlevee['surface_traitee'].iloc[i]
        dose_reference=lignes_herbicide_postlevee['dose_reglementaire'].iloc[i]
        IFT_en_cours.append(((dose*surface)/(dose_reference*surface_exploitation)))
    dose=0
    surface=0
    dose_reference=0
    for j in range(len(IFT_en_cours)):
        somme_IFT_herbicide_postlevee=somme_IFT_herbicide_postlevee + IFT_en_cours[j]
    IFT_en_cours=[]
    IFT_herbicide_postlevee = round(float(somme_IFT_herbicide_postlevee),2)


    #IFT herbicide total
    lignes_herbicide = base[base['fonction'].str.contains("herbicide",case=False, na=False)]
    IFT_en_cours=[]
    somme_IFT_herbicide=0
    for i in range(len(lignes_herbicide)):
        dose=lignes_herbicide['dose_appliquee'].iloc[i]
        surface=lignes_herbicide['surface_traitee'].iloc[i]
        dose_reference=lignes_herbicide['dose_reglementaire'].iloc[i]
        IFT_en_cours.append(((dose*surface)/(dose_reference*surface_exploitation)))
    dose=0
    surface=0
    dose_reference=0
    for j in range(len(IFT_en_cours)):
        somme_IFT_herbicide=somme_IFT_herbicide + IFT_en_cours[j]
    IFT_en_cours=[]
    IFT_herbicide = round(float(somme_IFT_herbicide),2)

    # IFT herbicide biocontrôle
    # IFT herbicide hors biocontrôle

    # Gestion des resistances :
    # Pourriture grise
    # phénylpyrroles
    lignes_phenylpyrroles=base[base['substances_actives'].str.contains("fludioxonil",case=False,na=False)]
    somme_produit_en_cours=0
    for i in range(len(lignes_phenylpyrroles)):
        somme_produit_en_cours=+1
    phenylpyrroles=somme_produit_en_cours
    # ANP
    produits_ANP=["pyriméthanil","mepanipyrim"]
    lignes_ANP=base[base['substances_actives'].str.contains('|'.join(produits_ANP),case=False,na=False)]
    somme_produit_en_cours=0
    for i in range(len(lignes_ANP)):
        somme_produit_en_cours=+1
    ANP=somme_produit_en_cours
    # IBS3
    produits_IBS3=["fenpyrazamine","fenhexamid"]
    lignes_IBS3=base[base['substances_actives'].str.contains('|'.join(produits_IBS3),case=False,na=False)]
    somme_produit_en_cours=0
    for i in range(len(lignes_IBS3)):
        somme_produit_en_cours=+1
    IBS3=somme_produit_en_cours
    # SDHI
    produits_SDHI=["isofetamid","boscalid"]
    lignes_SDHI=base[base['substances_actives'].str.contains('|'.join(produits_SDHI),case=False,na=False)]
    somme_produit_en_cours=0
    for i in range(len(lignes_SDHI)):
        somme_produit_en_cours=+1
    SDHI=somme_produit_en_cours
    # Mildiou
    # CAA
    produits_CAA=["mandipropamide","diméthomorphe","iprovalicarbe","benthiavalicarbe","valifénalate"]
    lignes_CAA=base[base['substances_actives'].str.contains('|'.join(produits_CAA),case=False,na=False)]
    somme_produit_en_cours=0
    for i in range(len(lignes_CAA)):
        somme_produit_en_cours=+1
    CAA=somme_produit_en_cours
    # Zoxamide
    lignes_zoxamide=base[base['substances_actives'].str.contains("zoxamide",case=False,na=False)]
    somme_produit_en_cours=0
    for i in range(len(lignes_zoxamide)):
        somme_produit_en_cours=+1
    zoxamide=somme_produit_en_cours
    # Qil
    produits_Qil=["cyazofamide","amisulbron"]
    lignes_Qil=base[base['substances_actives'].str.contains('|'.join(produits_Qil),case=False,na=False)]
    somme_produit_en_cours=0
    for i in range(len(lignes_Qil)):
        somme_produit_en_cours=+1
    Qil=somme_produit_en_cours
    # QosI/Qiol
    lignes_qosi=base[base['substances_actives'].str.contains("amétoctradine",case=False,na=False)]
    somme_produit_en_cours=0
    for i in range(len(lignes_qosi)):
        somme_produit_en_cours=+1
    qosi=somme_produit_en_cours
    # Fluopicolide
    lignes_fluopicolide=base[base['substances_actives'].str.contains("fluopicolide",case=False,na=False)]
    somme_produit_en_cours=0
    for i in range(len(lignes_fluopicolide)):
        somme_produit_en_cours=+1
    fluopicolide=somme_produit_en_cours
    # Oxathiapiproline
    lignes_oxathiapiproline=base[base['substances_actives'].str.contains("oxathiapiproline",case=False,na=False)]
    somme_produit_en_cours=0
    for i in range(len(lignes_oxathiapiproline)):
        somme_produit_en_cours=+1
    oxathiapiproline=somme_produit_en_cours
    # Anilides
    produits_anilides=["bénalaxyl","méfénoxam","bénélaxyl-M"]
    lignes_anilides=base[base['substances_actives'].str.contains('|'.join(produits_anilides),case=False,na=False)]
    somme_produit_en_cours=0
    for i in range(len(lignes_anilides)):
        somme_produit_en_cours=+1
    anilides=somme_produit_en_cours
    # Cymoxanil
    lignes_cymoxanil=base[base['substances_actives'].str.contains("cymoxanil",case=False,na=False)]
    somme_produit_en_cours=0
    for i in range(len(lignes_cymoxanil)):
        somme_produit_en_cours=+1
    cymoxanil=somme_produit_en_cours
    # QoI+contact
    lignes_qoicontact=base[base['substances_actives'].str.contains("pyraclostrobine",case=False,na=False)]
    somme_produit_en_cours=0
    for i in range(len(lignes_qoicontact)):
        somme_produit_en_cours=+1
    qoicontact=somme_produit_en_cours
    # Oïdium
    # Spiroxamine
    lignes_spiroxamine=base[base['substances_actives'].str.contains("spiroxamine",case=False,na=False)]
    somme_produit_en_cours=0
    for i in range(len(lignes_spiroxamine)):
        somme_produit_en_cours=+1
    spiroxamine=somme_produit_en_cours
    # APK
    produits_APK=["métrafénone","pyriofénone"]
    lignes_APK=base[base['substances_actives'].str.contains('|'.join(produits_APK),case=False,na=False)]
    somme_produit_en_cours=0
    for i in range(len(lignes_APK)):
        somme_produit_en_cours=+1
    APK=somme_produit_en_cours
    # SDHI (fluopyram)
    lignes_SDHI_fluopyram=base[base['substances_actives'].str.contains("fluopyram",case=False,na=False)]
    somme_produit_en_cours=0
    for i in range(len(lignes_SDHI_fluopyram)):
        somme_produit_en_cours=+1
    SDHI_fluopyram=somme_produit_en_cours
    # SDHI (boscalid)
    lignes_SDHI_boscalid=base[base['substances_actives'].str.contains("boscalid",case=False,na=False)]
    somme_produit_en_cours=0
    for i in range(len(lignes_SDHI_boscalid)):
        somme_produit_en_cours=+1
    SDHI_boscalid=somme_produit_en_cours
    # SDHI (fluxapyroxad)
    lignes_SDHI_fluxapyroxad=base[base['substances_actives'].str.contains("fluxapyroxad",case=False,na=False)]
    somme_produit_en_cours=0
    for i in range(len(lignes_SDHI_fluxapyroxad)):
        somme_produit_en_cours=+1
    SDHI_fluxapyroxad=somme_produit_en_cours
    # IBS1
    produits_IBS1=["tébuconazole","difénoconazole","tétraconazole","penconazole","myclobutanil","triadiménol"]
    lignes_IBS1=base[base['substances_actives'].str.contains('|'.join(produits_IBS1),case=False,na=False)]
    somme_produit_en_cours=0
    for i in range(len(lignes_IBS1)):
        somme_produit_en_cours=+1
    IBS1=somme_produit_en_cours
    # AZN
    produits_AZN=["quinoxyfen","proquinazid"]
    lignes_AZN=base[base['substances_actives'].str.contains('|'.join(produits_AZN),case=False,na=False)]
    somme_produit_en_cours=0
    for i in range(len(lignes_AZN)):
        somme_produit_en_cours=+1
    AZN=somme_produit_en_cours
    # Cyflufénamid
    lignes_cyflufenamid=base[base['substances_actives'].str.contains("cyflufénamid",case=False,na=False)]
    somme_produit_en_cours=0
    for i in range(len(lignes_cyflufenamid)):
        somme_produit_en_cours=+1
    cyflufenamid=somme_produit_en_cours




    # Retourner tous les calculs :
    #return(IFT_classique , IFT_biocontrole , IFT_total , IFT_mildiou , IFT_oidium , IFT_botrytis , IFT_autres_fongicides , IFT_fongicide_total , IFT_confusion_sexuelle , IFT_acaricides , IFT_autres_acaricides , IFT_insecticide_total , IFT_hors_herbicides , IFT_herbicide_prelevee, IFT_herbicide_postlevee, IFT_herbicide)
    return(IFT_classique , IFT_biocontrole , IFT_total , IFT_mildiou , IFT_oidium , IFT_botrytis , IFT_autres_fongicides , IFT_fongicide_total , IFT_confusion_sexuelle , IFT_acaricides , IFT_autres_acaricides , IFT_insecticide_total , IFT_hors_herbicides , IFT_herbicide_prelevee, IFT_herbicide_postlevee, IFT_herbicide, cyflufenamid, AZN, IBS1, SDHI_fluxapyroxad, SDHI_boscalid, SDHI_fluopyram, APK, spiroxamine, qoicontact, cymoxanil, anilides, oxathiapiproline, fluopicolide, qosi, Qil, zoxamide, CAA, SDHI, IBS3, ANP, phenylpyrroles, premiere_date_traitement)

#cyflufenamid, AZN, IBS1, SDHI_fluxapyroxad, SDHI_boscalid, SDHI_fluopyram, APK, spiroxamine, qoicontact, cymoxanil, anilides, oxathiapiproline, fluopicolide, qosi, Qil, zoxamide, CAA, SDHI, IBS3, ANP, phenylpyrroles


def enregistrer_en_pdf(ouvrir_ou_enregistrer,nom_parcelle,surface_exploitation,periode,debut,fin,cases_cochees):
    IFT_classique , IFT_biocontrole , IFT_total , IFT_mildiou , IFT_oidium , IFT_botrytis , IFT_autres_fongicides , IFT_fongicide_total , IFT_confusion_sexuelle , IFT_acaricides , IFT_autres_acaricides , IFT_insecticide_total , IFT_hors_herbicides , IFT_herbicide_prelevee, IFT_herbicide_postlevee, IFT_herbicide, cyflufenamid, AZN, IBS1, SDHI_fluxapyroxad, SDHI_boscalid, SDHI_fluopyram, APK, spiroxamine, qoicontact, cymoxanil, anilides, oxathiapiproline, fluopicolide, qosi, Qil, zoxamide, CAA, SDHI, IBS3, ANP, phenylpyrroles, premiere_date_traitement = recapitulatif(nom_parcelle,surface_exploitation,periode,debut,fin)

    table_IFT = [['IFT', 'Valeur'],
            ['IFT Total', str(IFT_total)],
            ['IFT Classique', str(IFT_classique)],
            ['IFT Biocontrôle', str(IFT_biocontrole)],
            ['IFT Mildiou', str(IFT_mildiou)],
            ['IFT Oïdium', str(IFT_oidium)],
            ['IFT Botrytis', str(IFT_botrytis)],
            ['IFT Autres fongicides', str(IFT_autres_fongicides)],
            ['IFT Fongicides total', str(IFT_fongicide_total)],
            ['IFT Confusion sexuelle', str(IFT_confusion_sexuelle)],
            ['IFT Acariens', str(IFT_acaricides)],
            ['IFT Autres insecticides', str(IFT_autres_acaricides)],
            ['IFT Insecticides total', str(IFT_insecticide_total)],
            ['IFT Hors herbicides', str(IFT_hors_herbicides)],
            ['IFT Herbicides pré-levée', str(IFT_herbicide_prelevee)],
            ['IFT Herbicides post-levée', str(IFT_herbicide_postlevee)],
            ['IFT Herbicides total', str(IFT_herbicide)]
            ]

    table_resistance = [['Substance active', 'Nombre de traitement', 'Indications'],
            ['Pourriture grise', "", "" ],
            ['Phénylpyrroles', str(phenylpyrroles), "1/an/parcelle" ],
            ['ANP', str(ANP), "1/an/parcelle (1 an sur 2)" ],
            ['IBS3', str(IBS3), "1/an/parcelle (1 an sur 2)" ],
            ['SDHI', str(SDHI), "1/an/parcelle (sauf boscalid, 1 an sur 2)"],
            ['Mildiou', "", "" ],
            ['CAA', str(CAA), "2/an/parcelle" ],
            ['Zoxamide', str(zoxamide), "3/an/parcelle" ],
            ['Qil', str(Qil), "1/an/parcelle" ],
            ['QoSI/Qiol', str(qosi), "1/an/parcelle"],
            ['Fluopicolide', str(fluopicolide), "1/an/parcelle"],
            ['Oxathiapiproline', str(oxathiapiproline), "1/an/parcelle"],
            ['Anilides', str(anilides), "2/an/parcelle"],
            ['Cymoxanil', str(cymoxanil), "2/an/parcelle"],
            ['Oïdium', "", "" ],
            ['Qol + contact', str(qoicontact), "1/an/parcelle"],
            ['Spiroxamine', str(spiroxamine), "2/an/parcelle"],
            ['APK', str(APK), "2/an/parcelle"],
            ['SDHI (fluopyram)', str(SDHI_fluopyram), "2 différentes/an/parcelle"],
            ['SDHI (boscalid)', str(SDHI_boscalid), "2 différentes/an/parcelle"],
            ['SDHI (fluxapyroxad)', str(SDHI_fluxapyroxad), "2 différentes/an/parcelle"],
            ['IBS1', str(IBS1), "1/an/parcelle"],
            ['AZN', str(AZN), "1/an/parcelle"],
            ['Cyflufénamid', str(cyflufenamid), "1/an/parcelle"]
            ]
            #['SDHI (fluopyram)', str(SDHI_fluopyram), "2 substances≠/an/parcelle"],
            #['SDHI (boscalid)', str(SDHI_boscalid), "2 substances≠/an/parcelle"],
            #['SDHI (fluxapyroxad)', str(SDHI_fluxapyroxad), "2 substances≠/an/parcelle"],


    # Crééer une liste des traitements en fonction des dates indiquées
    # Combien d'item par tranche de liste --> 'date_traitement', 'nom_produit', 'identifiant_usage', 'nom_parcelle', 'dose_appliquee'+'unite_dose_reglementaire', 'dose_reglementaire'+'unite_dose_reglementaire', 'surface_traitee'+"hectares" , 'IFT' (ift du traitement)
    # donc 8 colonnes

    debut_formate = pd.to_datetime(debut, format = "%d/%m/%Y")
    fin_formate = pd.to_datetime(fin, format = "%d/%m/%Y")
    if periode == 1 :
        traitements = pd.read_excel('IFT.xlsx')
        #traitements = traitements[(traitements['date_traitement'] >= debut ) & (traitements['date_traitement'] <= fin)]
        traitements['date_traitement'] = pd.to_datetime(traitements['date_traitement'], format = '%d/%m/%Y')
        traitements = traitements[(traitements['date_traitement'] >= debut_formate ) & (traitements['date_traitement'] <= fin_formate)]
        # Trier les dates
        traitements = traitements.sort_values(['date_traitement', 'nom_parcelle']) # trier par date (de l'ancienne à nouvelle) puis par parcelle TODO
        # Remettre les dates au bon format
        traitements['date_traitement'] = traitements['date_traitement'].dt.strftime('%d/%m/%Y')
    else :
        traitements = pd.read_excel('IFT.xlsx')
        traitements['date_traitement'] = pd.to_datetime(traitements['date_traitement'], format = '%d/%m/%Y')
        # Trier les dates
        traitements = traitements.sort_values(['date_traitement', 'nom_parcelle']) # trier par date (de l'ancienne à nouvelle) puis par parcelle TODO
        # Remettre les dates au bon format
        traitements['date_traitement'] = traitements['date_traitement'].dt.strftime('%d/%m/%Y')

    if nom_parcelle == "Toute l'exploitation" :
        table_traitements = [
            ['Date du traitement','Produit','Utilisation','Parcelle','Dose appliquée','Dose réglementaire','Superficie traitée','IFT du traitement']
                             ]
#        traitements = pd.read_excel('IFT.xlsx')
        nombre_de_traitements = 0
        for ligne in range(len(traitements)):
            date_traitement_trouve = traitements['date_traitement'].iloc[ligne]
            nom_produit_trouve = traitements['nom_produit'].iloc[ligne]
            utilisation_trouvee = traitements['identifiant_usage'].iloc[ligne]
            parcelle_trouvee = traitements['nom_parcelle'].iloc[ligne]
            unite_trouvee = traitements['unite_dose_reglementaire'].iloc[ligne]
            dose_app_trouvee = traitements['dose_appliquee'].iloc[ligne]
            dose_app_trouvee = str(dose_app_trouvee)+" "+str(unite_trouvee)
            dose_reg_trouvee = traitements['dose_reglementaire'].iloc[ligne]
            dose_reg_trouvee = str(dose_reg_trouvee)+" "+str(unite_trouvee)
            surface_traitee_trouvee = traitements['surface_traitee'].iloc[ligne]
            surface_traitee_trouvee = str(surface_traitee_trouvee)+" ha"
            IFT_trouve = traitements['IFT'].iloc[ligne]
            table_traitements.append([date_traitement_trouve , nom_produit_trouve , utilisation_trouvee, parcelle_trouvee , dose_app_trouvee , dose_reg_trouvee , surface_traitee_trouvee, IFT_trouve ])
            nombre_de_traitements = nombre_de_traitements + 1
    else :
        table_traitements = [
            ['Date du traitement','Produit','Utilisation','Dose appliquée','Dose réglementaire','Superficie traitée','IFT du traitement']
                             ]
#        traitements = pd.read_excel('IFT.xlsx')
        traitements = traitements[traitements['nom_parcelle'].str.contains(nom_parcelle, na=False)]
        nombre_de_traitements = 0
        for ligne in range(len(traitements)):
            date_traitement_trouve = traitements['date_traitement'].iloc[ligne]
            nom_produit_trouve = traitements['nom_produit'].iloc[ligne]
            utilisation_trouvee = traitements['identifiant_usage'].iloc[ligne]
            unite_trouvee = traitements['unite_dose_reglementaire'].iloc[ligne]
            dose_app_trouvee = traitements['dose_appliquee'].iloc[ligne]
            dose_app_trouvee = str(dose_app_trouvee)+" "+str(unite_trouvee)
            dose_reg_trouvee = traitements['dose_reglementaire'].iloc[ligne]
            dose_reg_trouvee = str(dose_reg_trouvee)+" "+str(unite_trouvee)
            surface_traitee_trouvee = traitements['surface_traitee'].iloc[ligne]
            surface_traitee_trouvee = str(surface_traitee_trouvee)+" ha"
            IFT_trouve = traitements['IFT'].iloc[ligne]
            table_traitements.append([date_traitement_trouve , nom_produit_trouve , utilisation_trouvee,  dose_app_trouvee , dose_reg_trouvee , surface_traitee_trouvee, IFT_trouve ])
            nombre_de_traitements = nombre_de_traitements + 1

    #print(table_traitements)


    class PDF(FPDF):
        def create_table(self, table_data, title='', data_size = 10, title_size=12, align_data='L', align_header='C', cell_width='even', x_start='x_default',emphasize_data=[], emphasize_style=None,emphasize_color=(0,0,0)):
            default_style = self.font_style
            if emphasize_style == None:
                emphasize_style = default_style
            def get_col_widths():
                col_width = cell_width
                if col_width == 'even':
                    col_width = self.epw / len(data[0]) - 1
                elif col_width == 'uneven':
                    col_widths = []
                    for col in range(len(table_data[0])):
                        longest = 0
                        for row in range(len(table_data)):
                            cell_value = str(table_data[row][col])
                            value_length = self.get_string_width(cell_value)
                            if value_length > longest:
                                longest = value_length
                        col_widths.append(longest + 4)
                    col_width = col_widths

                elif isinstance(cell_width, list):
                    col_width = cell_width
                else:

                    col_width = int(col_width)
                return col_width

            if isinstance(table_data, dict):
                header = [key for key in table_data]
                data = []
                for key in table_data:
                    value = table_data[key]
                    data.append(value)

                data = [list(a) for a in zip(*data)]

            else:
                header = table_data[0]
                data = table_data[1:]

            line_height = self.font_size * 2.5

            col_width = get_col_widths()
            self.set_font(size=title_size)

            if x_start == 'C':
                table_width = 0
                if isinstance(col_width, list):
                    for width in col_width:
                        table_width += width
                else:
                    table_width = col_width * len(table_data[0])
                margin_width = self.w - table_width

                center_table = margin_width / 2
                x_start = center_table
                self.set_x(x_start)
            elif isinstance(x_start, int):
                self.set_x(x_start)
            elif x_start == 'x_default':
                x_start = self.set_x(self.l_margin)





            if title != '':
                self.multi_cell(0, line_height, title, border=0, align='j', ln=3, max_line_height=self.font_size)
                self.ln(line_height)

            self.set_font(size=data_size)

            y1 = self.get_y()
            if x_start:
                x_left = x_start
            else:
                x_left = self.get_x()
            x_right = self.epw + x_left
            if  not isinstance(col_width, list):
                if x_start:
                    self.set_x(x_start)
                for datum in header:
                    self.multi_cell(col_width, line_height, datum, border=0, align=align_header, ln=3, max_line_height=self.font_size)
                    x_right = self.get_x()
                self.ln(line_height)
                y2 = self.get_y()
                self.line(x_left,y1,x_right,y1)
                self.line(x_left,y2,x_right,y2)

                for row in data:
                    if x_start:
                        self.set_x(x_start)
                    for datum in row:
                        if datum in emphasize_data:
                            self.set_text_color(*emphasize_color)
                            self.set_font(style=emphasize_style)
                            self.multi_cell(col_width, line_height, datum, border=0, align=align_data, ln=3, max_line_height=self.font_size)
                            self.set_text_color(0,0,0)
                            self.set_font(style=default_style)
                        else:
                            self.multi_cell(col_width, line_height, datum, border=0, align=align_data, ln=3, max_line_height=self.font_size)
                    self.ln(line_height)

            else:
                if x_start:
                    self.set_x(x_start)
                for i in range(len(header)):
                    datum = header[i]
                    self.multi_cell(col_width[i], line_height, datum, border=0, align=align_header, ln=3, max_line_height=self.font_size)
                    x_right = self.get_x()
                self.ln(line_height)
                y2 = self.get_y()
                self.line(x_left,y1,x_right,y1)
                self.line(x_left,y2,x_right,y2)


                for i in range(len(data)):
                    if x_start:
                        self.set_x(x_start)
                    row = data[i]
                    for i in range(len(row)):
                        datum = row[i]
                        if not isinstance(datum, str):
                            datum = str(datum)
                        adjusted_col_width = col_width[i]
                        if datum in emphasize_data:
                            self.set_text_color(*emphasize_color)
                            self.set_font(style=emphasize_style)
                            self.multi_cell(adjusted_col_width, line_height, datum, border=0, align=align_data, ln=3, max_line_height=self.font_size)
                            self.set_text_color(0,0,0)
                            self.set_font(style=default_style)
                        else:
                            self.multi_cell(adjusted_col_width, line_height, datum, border=0, align=align_data, ln=3, max_line_height=self.font_size)
                    self.ln(line_height)
            y3 = self.get_y()
            self.line(x_left,y3,x_right,y3)
    pdf = PDF()

    if cases_cochees[2] == 1 :
        if (cases_cochees[0] == 1) or (cases_cochees[1] == 1) :
            pdf.add_page()
            pdf.rect(5.0, 5.0, 200.0,282.0)
        else :
            pdf.add_page('L')
    else :
        pdf.add_page()
        pdf.rect(5.0, 5.0, 200.0,282.0)

# def create_table(self, table_data, title='', data_size = 10, title_size=12, align_data='L', align_header='C', cell_width='even', x_start='x_default',emphasize_data=[], emphasize_style=None,emphasize_color=(0,0,0)):

    pdf.set_font("Times", size = 15)
    pdf.cell(200, 10, txt = "Récapitulatif IFT",
             ln = 1, align = 'C')

    # changer police
    pdf.set_font("Times", size = 13)
    if nom_parcelle == "Toute l'exploitation" :
        extension_fichier = "exploitation"
        pdf.cell(200, 5, txt = "sur l'ensemble de l'exploitation ("+str(surface_exploitation)+" ha)", ln = 1, align = 'C')
    else :
        extension_fichier = str(nom_parcelle)
        pdf.cell(200, 5, txt = "Parcelle : "+str(nom_parcelle), ln = 1, align = 'C')
    if debut_formate >= fin_formate :
        debut = premiere_date_traitement
        fin = date.today()
        fin = fin.strftime("%d/%m/%Y")
        pdf.cell(200, 5, txt = "sur la période du "+str(debut)+" au "+str(fin), ln = 1, align = 'C')
    else :
        pdf.cell(200, 5, txt = "sur la période du "+str(debut)+" au "+str(fin), ln = 1, align = 'C')


    pdf.set_font("Times", size=10)

    # Si case IFT cochée : mettre IFT :
    if cases_cochees[0] == 1 :
        if cases_cochees[1] == 1 :
            # Tableau des IFT
            pdf.set_y(40)
            pdf.create_table(table_data = table_IFT, align_data='C',title="IFT",cell_width='uneven')
            pdf.ln()
        else :
            pdf.set_y(40)
            pdf.create_table(table_data = table_IFT, align_data='C',title="IFT",cell_width='uneven', x_start=75)
            pdf.ln()


    # Si case Resistances cochée :
    if cases_cochees[1] == 1 :
        if cases_cochees[0] == 1 :
            # Tableau de gestion des résistances
            pdf.set_y(40)
            pdf.create_table(table_data = table_resistance, align_data='C',title="Gestion des résistances",cell_width='uneven',x_start=70)
            pdf.ln()
        else :
            # Tableau de gestion des résistances
            pdf.set_y(40)
            pdf.create_table(table_data = table_resistance, align_data='C',title="Gestion des résistances",cell_width='uneven',x_start=40)
            pdf.ln()


    # Si case Traitements cochée :
    if cases_cochees[2] == 1 :
        if (cases_cochees[0] == 1) or (cases_cochees[1] == 1) :
            # Tableau récapitulatif des traitements
            pdf.add_page('L')
            pdf.create_table(table_data = table_traitements, align_data='C',title="Récapitulatif des traitements sur la période choisie ("+str(nombre_de_traitements)+" traitements)",cell_width='uneven')
            pdf.ln()
        else :
            pdf.create_table(table_data = table_traitements, align_data='C',title="Récapitulatif des traitements sur la période choisie ("+str(nombre_de_traitements)+" traitements)",cell_width='uneven')
            pdf.ln()


    pdf.set_font("Times", size = 9)
    pdf.set_y(-20)
    date_du_jour=date.today()
    date_du_jour=date_du_jour.strftime("%d/%m/%Y")
    pdf.cell(0, 0, txt = "Rapport généré par NOM_DU_LOGICIEL le "+str(date_du_jour),
             align = 'C')

    date_du_jour=date.today()
    date_du_jour=date_du_jour.strftime("%d-%m-%Y")

    if ouvrir_ou_enregistrer == 0 :
        # Choisir un nom associé à la date du jour
        nom_du_fichier="recapitulatif_"+str(date_du_jour)+"_"+str(extension_fichier)+".pdf"
        chemin = "./recapitulatifs/"+str(nom_du_fichier)
        pdf.output(chemin)

        return(nom_du_fichier)
    else :
        dir_name = filedialog.askdirectory()
        repertoire_courant = os.getcwd()
        os. chdir(dir_name)
        nom_du_fichier="recapitulatif_"+str(date_du_jour)+"_"+str(extension_fichier)+".pdf"
        chemin = str(dir_name)+"/"+str(nom_du_fichier)
        pdf.output(chemin)
        os.chdir(repertoire_courant)

        return(chemin)
