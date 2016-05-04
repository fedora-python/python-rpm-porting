%build
^^^^^^

Currently your package is building the software for Python 2, what we need to do is also add building for Python 3. While we're modifying the spec file, however, it's a good idea to also update it to new standards—in this case a new macro.

In the ideal case, you'll find the build done with either the ``%py2_build`` macro or its older version ``%py_build``, which you then should exchange for the former. In either case, you can just add the macro ``%py3_build`` afterwards, and this part is done.

.. code-block:: spec

    %build
    %py2_build
    %py3_build

In many cases, however, you will find a custom build command prefixed by the ``%{__python}`` or ``%{__python2}`` macros, or in some cases just prefixed by the python interpreter invoked without a macro at all, e.g.::

    %{__python} custombuild.py --many-flags
        or
    python custombuild.py --many-flags

In these cases first try substituting the whole build command by the new pair of smart macros ``%py2_build`` and ``%py3_build``, which should in many cases correctly figure out what ought to be done automatically. Otherwise, duplicate the entire command and change the invocation of the python interpreter to the ``%{__python2}`` macro in one of them and to the ``%{__python3}`` in the other.

.. code-block:: spec

    %build
    %{__python2} custombuild.py --many-flags
    %{__python3} custombuild.py --many-flags

Rarely, you might encounter some non-Python build script such as a Makefile. In these instances you have to adjust the script on your own, consult the documentation for the specific build method.
