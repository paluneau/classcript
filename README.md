# classcript
A package to write Python scripts without having to deal with the cumbersome task of parsing command line parameters.

## Create a subclass

Create a class that inherits from `ScriptGenerique`, and implement the abstract `corps()` method: this will be the _body_ of your script. You can interact with the dictionary of parameters via the `req_params()` method (see the class `CourbeConvergence` in `courbe_convergence.py`).

## Set the parameters

In the `if(__name__ == "__main__"):` clause, create an instance of your class, and set the parameters (children of `Param` class) with the `ajoute_param()` method (you can set a default value and if the parameter is optional). You can also set a default message for when no parameter is passed to the script (`asgn_message_sans_param()`).

## Run the script

Top it off with the `execute()` method, which receives the command line arguments.
