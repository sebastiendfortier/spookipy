Description:
============

-  Calculate probability of exceedance of a threshold using ensemble percentiles.

Iteration method:
~~~~~~~~~~~~~~~~~

-  Point-by-Point

Dependencies:
~~~~~~~~~~~~~

-  At least 2 fields 

Result(s):
~~~~~~~~~~

-  A field with the result of the operation

Algorithm:
~~~~~~~~~~

.. code-block:: text

        Each percentile field y has a corresponding field of values x.

        At each point of the grid, a linear piece-wise function f is built such that f(x) = y.

        Then a threshold T is applied:

        For values lesser than the threshold (option le), the probability of exceeding the threshold is f(T).
        For values greater than the threshold (option ge), the probability of exceeding the threshold is 1 - f(T).

Reference:
~~~~~~~~~~

-  Does not apply

Keywords:
~~~~~~~~~

-  MÉTÉO/WEATHER, température/temperature, potentielle/potential

Usage:
~~~~~~

.. code:: python

   python3
   
   import os
   import fstpy.all as fstpy
   import spookipy.all as spooki
