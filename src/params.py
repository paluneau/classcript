from abc import ABC, abstractmethod
from numpy import nan


# Classe abstraite représentant un paramètre du script
class Param(ABC):
    """
    Classe qui représente un paramètre à passer au script

    ...

    Attributes
    ----------
    __cle : str
        Nom du paramètre.

    __val : str
        Valeur du paramètre.

    Methods
    -------
    accepte(p_visiteur)
        Se fait visiter par l'objet visiteur
    req_cle()
        Retourne la clé du paramètre
    asgn_valeur(p_val)
        Assigne une valeur au paramètre
    req_valeur(n=1.0)
        Change the photo's gamma exposure.
    req_valeur_vide

    """
    
    def __init__(self, p_cle : str, p_val):
        self.__cle = p_cle
        self.__val = p_val

    @abstractmethod
    def accepte(self, p_visiteur):
        pass

    def req_cle(self):
        return self.__cle

    def asgn_valeur(self, p_val):
        self.__val = p_val

    def req_valeur(self):
        return self.__val
    
    @staticmethod
    @abstractmethod
    def req_valeur_vide():
        pass


# Classe abstraite pour appliquer des opérations à tous les paramètres
class ParamVisiteur(ABC):
    
    @abstractmethod
    def visite_bool(self, p_param : Param):
        pass

    @abstractmethod
    def visite_numeric(self, p_param : Param):
        pass

    @abstractmethod
    def visite_string(self, p_param : Param):
        pass

# Classe pour faire une conversion d'une string en la valeur d'un paramètre
class Str2ParamVisiteur(ParamVisiteur):

    def __init__(self):
        self.__chaine = ""

    def asgn_chaine_car(self, p_chaine : str):
        self.__chaine = p_chaine
    
    def visite_bool(self, p_param : Param):
        p_param.asgn_valeur(True)

    def visite_numeric(self, p_param : Param):
        try:
            p_param.asgn_valeur(float(self.__chaine))
        except(ValueError):
            print(f"La chaine {self.__chaine} n'est pas un nombre à virgule flottante valide. La valeur par défaut sera préservée.")

    def visite_string(self, p_param : Param):
        p_param.asgn_valeur(self.__chaine)

# Wrapper pour un paramètre booléen
class ParamBool(Param):

    def __init__(self, p_cle : str):
        super().__init__(p_cle, False)

    def accepte(self, p_visiteur: ParamVisiteur):
        return p_visiteur.visite_bool(self)

    @staticmethod
    def req_valeur_vide():
        return False

# Wrapper pour un paramètre booléen
class ParamNumeric(Param):

    def __init__(self, p_cle : str, p_val : float):
        super().__init__(p_cle, p_val)

    def accepte(self, p_visiteur: ParamVisiteur):
        return p_visiteur.visite_numeric(self)

    @staticmethod
    def req_valeur_vide():
        return nan

# Wrapper pour un paramètre string
class ParamString(Param):

    def __init__(self, p_cle : str, p_val : str):
        super().__init__(p_cle, p_val)

    def accepte(self, p_visiteur: ParamVisiteur):
        return p_visiteur.visite_string(self)

    @staticmethod
    def req_valeur_vide():
        return ""