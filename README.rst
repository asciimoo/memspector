Memspector
==========

Inspect memory usage of python functions


Features
~~~~~~~~

- Thread handling
- External tool, doesn't require code modification

Check ``memspector --help`` for command line options


Installation
~~~~~~~~~~~~

via pip: ``pip install memspector``


Example
~~~~~~~

``example.py``:

.. code-block:: python

    l = []


    def a():
        l.extend(range(100000))


    def b():
        global l
        l = []


    a()
    a()
    b()
    a()
    b()
    a()


Run ``memspector example.py`` to get the following output:

.. code-block::

    example.py:b()                                               thread: main_thread
    total memory       diff
        2,940,336     -1,799,976
        2,040,440       -900,048

    example.py:a()                                               thread: main_thread
    total memory       diff
        1,139,848        900,400
        2,040,280        900,000
        1,140,408        900,048
        1,140,408        900,048

    example.py                                                   thread: main_thread
    total memory       diff
        1,133,832        906,232



Bugs
~~~~

Bugs or suggestions? Visit the `issue tracker <https://github.com/asciimoo/memspector/issues>`__


License
~~~~~~~

.. code-block::

    Memspector
    Copyright (C) 2015 Adam Tauber <asciimoo@gmail.com>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    See <http://www.gnu.org/licenses/>.
