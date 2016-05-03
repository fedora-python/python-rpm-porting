%prep
^^^^^

The ``%prep`` section most likely already exists in your spec file and contains either the ``%setup`` macro, optionally followed by the ``%patchX`` macros (where ``X`` is a number) that apply patches, or it contains the ``%autesetup`` macro that applies any listed patches automatically. (Patches are listed with the ``Source0``, ``Source1``, ... tags).

If you find that some patches are being applied that are clearly only intended for Python 2 version of the application, you can try removing them. Otherwise, leave the macros as they are.

Shebangs
********

A shebang is an indicator on the first line of an executable script that indicates in what interpreter is the script supposed to be launched, examples include *python, bash and perl*. **If the shebang of the executable(s) in our package is pointing to Python 2 it needs to be updated to Python 3.**

First find out if and what shebangs are used in your package by unpacking the sources for the project, ``cd``-ing into the unpacked directory and trying the following command(s):

.. code-block:: console

   # Searches for all shebangs among the sources
   $ grep -r '^#!/' .

   # Searches only Python shebangs
   $ grep -rE '^#!/usr/bin/(python|env python)' .

You will usually find one of these two shebangs::

   #!/usr/bin/python
   #!/usr/bin/env python

It is advisable to change both of these to ``#!/usr/bin/python3``. ``/usr/bin/env`` can be useful for scripts, but applications should link to the system version of Python outright.

To change the shebangs in the files you can use one (or a combination) of the following commands, which you should place at the end of the ``%prep`` section.

.. code-block:: console

   # Change shebang in individual files
   sed -i '1s_^#!/usr/bin/\(python\|env python\)_#!/usr/bin/python3_' path/to/file1 file2 file3 ...

   # Change shebang in all files in this directory and all subdirectories
   # See `man find` for how the `-exec command ;` syntax works
   find . -type f -exec sed -i '1s_^#!/usr/bin/\(python\|env python\)_#!/usr/bin/python3_' {} \;

   # Change shebang in all executable files in this directory and all subdirectories
   find . -type f -executable -exec sed -i '1s_^#!/usr/bin/\(python\|env python\)_#!/usr/bin/python3_' {} \;

You don't have to worry about accidentally corrupting other files as these scripts will only change a file if the beginning of its first line exactly matches one of the two aforementioned shebangs.

Autodetection of Runtime Dependencies
+++++++++++++++++++++++++++++++++++++

RPM has very good capabilities of automatically finding dependencies, and one of the ways it accomplishes that is by looking at the shebangs of all the files in the package. Therefore it is doubly important to update the shebangs of all the executables to Python 3 so as not to drag in a runtime dependency on Python 2.

All executable scripts should be located either in ``/usr/bin``, ``/usr/sbin`` or ``/usr/libexec``. If you find shebangs in scripts that are not intended to be executed, you should remove them as they have no place to be there. However, one exception would be *sample scripts* in documentation.
