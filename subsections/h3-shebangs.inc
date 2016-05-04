Are shebangs dragging you down (to Python 2)?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A shebang is an indicator on the first line of an executable script that indicates in what interpreter is the script supposed to be launched, examples include *python, bash and perl*. When software gets ported to Python 3, the lone shebang often remains forgotten and keeps pointing to Python 2. In most cases this is handled automatically: the ``setup.py`` script (usually run through the ``%py3_build`` and ``%py3_install`` RPM macros) adjusts shebangs for you. However, sometimes it's up to you to handle the situation.

RPM has very good capabilities of automatically finding dependencies, and one of the ways it accomplishes that is by looking at the shebangs of all the files in the package. Therefore **it is important to check if the shebangs are not dragging in a runtime dependency on Python 2**.

As the porting of the spec file is nearly finished, build it and then run the following analysis on the resulting Python 3 RPM file:

.. code-block:: console

   $ # You can run this in mock as both rpm and grep are already installed.
   $ rpm -qp --requires path/to/an.rpm | grep -E '/usr/bin/(python|env python)'

This will list all the Python executables your RPM package depends on. If you find that an RPM package for Python 3 depends on Python 2 (either as ``/usr/bin/python`` or ``/usr/bin/env python``) you need to fix it.


Fixing shebangs
***************

First find out what shebangs are used in your package by unpacking the sources for the project, ``cd``-ing into the unpacked directory and trying the following command(s):

.. code-block:: console

   $ # Searches for all shebangs among the sources
   $ grep -r '^#!/' .

   $ # Searches only Python shebangs
   $ grep -rE '^#!/usr/bin/(python|env python)' .

You will usually find one of these two shebangs::

   #!/usr/bin/python
   #!/usr/bin/env python

It is advisable to change both of these to ``#!/usr/bin/python3``. ``/usr/bin/env`` can be useful for scripts, but applications should link to the system version of Python outright.

To change the shebangs in the files you can use one (or a combination) of the following commands, which you should place at the end of the ``%prep`` section.

.. code-block:: console

   $ # Change shebang in individual files
   $ sed -i '1s_^#!/usr/bin/\(python\|env python\)_#!/usr/bin/python3_' path/to/file1 file2 file3 ...

   $ # Change shebang in all relevant files in this directory and all subdirectories
   $ # See `man find` for how the `-exec command ;` syntax works
   $ find . -type f -exec sed -i '1s_^#!/usr/bin/\(python\|env python\)_#!/usr/bin/python3_' {} \;

   $ # Change shebang in all relevant executable files in this directory and all subdirectories
   $ find . -type f -executable -exec sed -i '1s_^#!/usr/bin/\(python\|env python\)_#!/usr/bin/python3_' {} \;

You don't have to worry about accidentally corrupting other files as these scripts will only change a file if the beginning of its first line exactly matches one of the two aforementioned shebangs.
