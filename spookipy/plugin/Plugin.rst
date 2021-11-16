Description:
============

Abstract base class for plugins. Each plugin must inherit from this class.

Use:
~~~~~~

- The `__init__` method can be overloaded if necessary, e.g. to add parameters. Ideally, the overloaded method should call the superclass method.
- The compute method needs to be implemented.



.. code:: python

    python3

    import pandas as pd
    import spookipy.all as spooki
    
    class Example (spooki.Plugin):
        def __init __ (self, df: pd.DataFrame, param) -> None:
            self.param = param
            super ().__ init __ (df)

        def compute (self) -> pd.DataFrame:
            # my_df = ...
            # Some manipulation on self.df
            return my_df

Contacts:
~~~~~~~~~

- Author : `Audrey Germain <https://wiki.cmc.ec.gc.ca/wiki/User:Germaina>`__
- Coded by : `Audrey Germain <https://wiki.cmc.ec.gc.ca/wiki/User:Germaina>`__
- Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ / `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__
