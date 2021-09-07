Français
--------

Description:
~~~~~~~~~~~~

Classe abstraite de base pour les plugins. Tous les plugins doivent
hériter de cette classe.

Usage:
~~~~~~

-  La fonction ****init**** peut être surchargée au besoin, par exemple
   pour ajouter des paramètres supplémentaires. L’idéale serait
   d’appeler la fonction de la classe de base dans la fonction
   surchargée.
-  La fonction compute doit absolument être implémentée.

#. Exemple:

   .. code:: python

       python3
       import pandas as pd
       import spookipy.all as spooki
       class Exemple(spooki.Plugin):
           def __init__(self,df:pd.DataFrame,param) -> None:
               self.param = param
               super().__init__(df)

           def compute(self) -> pd.DataFrame:
               # my_df = ...
               # Manipulations quelconque sur le self.df 
               return my_df

Contacts:
~~~~~~~~~

Codé par : `Audrey
Germain <https://wiki.cmc.ec.gc.ca/wiki/User:Germaina>`__

Support :

-  `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__
-  `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

English
-------

Description:
~~~~~~~~~~~~

Abstract base class for plugins. Each plugin must inherit from this
class.

Usage:
~~~~~~

-  The ****init**** method can be overloaded if necessary, e.g. to add
   parameters. Ideally, the overloaded method should call the superclass
   method.
-  The compute method needs to be implemented.

#. Example:

   .. code:: python

       python3
       import pandas as pd
       import spookipy.all as spooki
       class Exemple(spooki.Plugin):
           def __init__(self,df:pd.DataFrame,param) -> None:
               self.param = param
               super().__init__(df)

           def compute(self) -> pd.DataFrame:
               # my_df = ...
               # Some manipulation on self.df 
               return my_df

Contacts:
~~~~~~~~~

Coded by : `Audrey
Germain <https://wiki.cmc.ec.gc.ca/wiki/User:Germaina>`__

Support :

-  `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__
-  `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__
