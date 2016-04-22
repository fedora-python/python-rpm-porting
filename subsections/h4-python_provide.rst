:orphan:

%python_provide
***************

Now that we're splitting the package ``python-example`` into ``python2-example`` and ``python3-example``, we need to define what will happen when the user tries to install the unversioned name ``python-example``.

At the time of this writing, the `packaging guidelines`_ say that the *default* version should be the one for Python 2. However, it is expected to change to Python 3 some time in the future. To avoid having to adjust all Python packages in Fedora when that time comes, the ``%python_provide`` macro was devised:

.. _`packaging guidelines`: https://fedoraproject.org/wiki/Packaging:Python#Avoiding_collisions_between_the_python_2_and_python_3_stacks

.. code-block:: spec

    %{?python_provide:%python_provide python2-%{srcname}}
    and
    %{?python_provide:%python_provide python3-%{srcname}}

This is a line you should include in each of your subpackages and it works thus: First the part ``?python_provide:`` checks whether the macro exists and if not, the entire line is ignored. After that we actually use the ``%python_provide`` macro and give it one argument—the name of the given subpackage.

The macro will then check whether this Python version is default or not—if not, the line is again ignored. However, if indeed this is the currently default Python version, the macro is replaced with a *virtual provides* tag: ``Provides: python-%{srcname}``. This will tell the packaging system (dnf, yum, ...) to install this subpackage when user searches for ``python-example``.

