from .params import Param, Str2ParamVisiteur
from abc import ABC, abstractmethod
from sys import stderr


class ScriptGenerique(ABC):

    __params = {};
    __message = "";


    def ajoute_param(self, p_param : Param, p_est_oblig : bool = False):
        if p_est_oblig & (type(p_param).req_valeur_vide() != p_param.req_valeur()):
            raise ValueError(f"Paramètre obligatoire {p_param.req_cle()} a une valeur non-vide.")
        else:
            self.__params[p_param.req_cle()] = (p_param, p_est_oblig)

    def asgn_message_sans_param(self, p_message : str):
        self.__message = p_message

    def req_params(self):
        return { param : self.__params[param][0] for param in self.__params }

    @abstractmethod
    def corps(self):
        pass

    def execute(self, p_args : list):
        str2param = Str2ParamVisiteur()

        if len(p_args) < 1:
            print(self.__message, file=stderr)
            return 2
        
        try:
            it = iter(p_args)

            # On "mange" un argument qui représente un paramètre, puis on "mange" son suivant qui doit être la valeur du paramètre
            it_val = next(it, None)
            while(it_val is not None):
                param_key = it_val
                param_tuple = self.__params.get(param_key)
                if(param_tuple is not None):
                    param = param_tuple[0]
                    it_val = next(it, None)
                    est_un_param = it_val in self.__params
                    val = ""
                    if((not est_un_param) & (it_val is not None)):
                        val = it_val
                    str2param.asgn_chaine_car(val)
                    param.accepte(str2param)
                    if(not(est_un_param)):
                        it_val = next(it, None)
                else:
                    raise KeyError(f"Le paramètre {param_key} n'existe pas.")

            # Lecture des données
            for param in self.__params:
                if self.__params[param][1] & (self.__params[param][0].req_valeur() == type(self.__params[param][0]).req_valeur_vide()):
                    raise ValueError(f"Spécifier l'argument obligatoire {self.__params[param][0].req_cle()}.")

            self.corps()

        except KeyError as err:
            print(f"ERREUR (clé du paramètre) : {err}")
            return 1
        except ValueError as err:
            print(f"ERREUR (valeur du paramètre) : {err}")
            return 1
        else:
            return 0

        



