#!/usr/bin/python3

from classcript.script import ScriptGenerique
from classcript.params import ParamString, ParamBool
from sys import argv

from re import findall, MULTILINE
import matplotlib.pyplot as plt
import numpy as np
from os.path import basename
import tikzplotlib as tikzplt


# Classe implémentant le script générique
class CourbeConvergence(ScriptGenerique):
    
    @staticmethod
    def lis_donnees(p_path : str):
        fichier = open(p_path, "r")
        tous_groupes = findall("^\s*(\d+) TAO,  Function value: (\d+\.?\d+)(e(\+?|-)\d+)?", fichier.read(), MULTILINE)
        fichier.close()
        donnees = np.array([[float(groupes[0]), float("".join(groupes[1:3]))] for groupes in tous_groupes])

        return donnees

    def corps(self):

        try:
        # Lecture des données 
            nuage = CourbeConvergence.lis_donnees(self.req_params()["-p"].req_valeur())

            # Création du graphique
            plt.plot(nuage[:,0],nuage[:,1],self.req_params()["-f"].req_valeur())
            plt.xlabel(self.req_params()["-x"].req_valeur())
            plt.ylabel(self.req_params()["-y"].req_valeur())
            if(self.req_params()["-lx"].req_valeur()):
                plt.xscale("log")
            if(self.req_params()["-ly"].req_valeur()):
                plt.yscale("log")

            nom_fichier = basename(self.req_params()["-p"].req_valeur())
            tikzplt.save("courbe_convergence_" + nom_fichier + ".tex")

            plt.show()
        except TypeError as e:
            print(f"Erreur d'ouverture du fichier {self.req_params()['-p'].req_valeur()}.")
        

if(__name__ == "__main__"):
    # On crée une instance de la classe de script
    scriptcc = CourbeConvergence()

    # Message par défaut quand on exécute le script sans paramètre
    scriptcc.asgn_message_sans_param("Usage: courbe_convergence.py -p chemin_du_fichier [-x x_label (str)] [-y y_label (str)] [-lx logscale_x (bool)] [-ly logscale_y (bool)] [-f format (str)]")

    # On ajoute les paramètres nécessaires au script avec leurs valeurs par défaut
    # Path (obligatoire)
    scriptcc.ajoute_param(ParamString("-p", ParamString.req_valeur_vide()), True)
    # xlabel
    scriptcc.ajoute_param(ParamString("-x", "Itérations"))
    # ylabel
    scriptcc.ajoute_param(ParamString("-y", "Objectif"))
    # log x
    scriptcc.ajoute_param(ParamBool("-lx"))
    # logscale y
    scriptcc.ajoute_param(ParamBool("-ly"))
    # format
    scriptcc.ajoute_param(ParamString("-f", "x-r"))

    # Exécuter le script
    scriptcc.execute(argv[1:])

