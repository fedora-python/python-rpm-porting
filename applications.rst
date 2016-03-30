Applications written in Python
==============================

This section is for packages that are not being imported by third-party projects (e.g. ``import some_module`` in a Python file) and that do not interact with user code (such as plugins). Otherwise, look into :doc:`other sections <index>`.


Porting the specfile to Python 3
--------------------------------

Applications behave the same when run under Python 2 and Python 3, therefore all you need to do is change the specfile to use Python 3 instead of Python 2.

**In essense, porting of an application RPM mostly consists of going through the spec file and adding number 3 or substituting number 3 for number 2 where appropriate. Occasionally also substituting old macros for new ones that are more versatile.**

So let's take an example spec file and port it to illustrate the process. We start with a spec file for an application using Python 2:

.. literalinclude:: diffs/application.spec.orig
   :language: spec
   :caption: Example spec file for an application running on Python 2.


Modifications
-------------

First it is recommended to update the software to the newest upstream version. If it already is at the latest version, increment the release number.


BuildRequires and Requires
^^^^^^^^^^^^^^^^^^^^^^^^^^

Change ``BuildRequires`` from ``python2-devel`` to ``python3-devel`` and adjust all other ``Requires`` and ``BuildRequires`` entries to point only to python3 packages.

**It is very important that you don't use any Python 2 dependencies, because that would mean your package would depend on Python version 2 and version 3, which would render your porting efforts useless.**


%build
^^^^^^

In the build section you can find a variety of macros, for example ``%py_build`` and its newer version ``%py2_build``. You can freely substitute these by the new Python 3 macro ``%py3_build``.

Occasionally you will find a custom build command prefixed by the ``%{__python}`` or ``%{__python2}`` macros, or in some cases just prefixed by the python interpreter invoked without a macro at all, e.g.::

    %{__python} setup.py build
        or
    python setup.py build

In these cases first try substituting the whole build command by the new smart macro ``%py3_build`` which should in many cases correctly figure out what ought to be done automatically. Otherwise change the invocation of the python interpreter to the ``%{__python3}`` macro.


%install and %check
^^^^^^^^^^^^^^^^^^^

Install sections can vary a lot, but the above-mentioned general rule applies: substitute number 2 by number 3 where appropriate.

For example, if you find the ``%py2_install`` macro, substitute it with ``%py3_install``, if you find the ``%{__python2}`` macro, substitute it with ``%{__python3}``, etc.
    TODO same as %build section


%files
^^^^^^

In the files section you usually find the ``%{python2_sitelib}`` macro, which you should substitute with ``%{python3_sitelib}``.

The files section may also contain the versioned executable, usually ``%{_bindir}/sample-exec-2.7`` in which case it should be substituted by ``%{_bindir}/sample-exec-%{python3_version}``.


Diff of the changes
-------------------

.. literalinclude:: diffs/application.spec
   :diff: diffs/application.spec.orig
   :caption: Diff between the original example Python 2 spec file and the converted Python 3 spec file.


Ported RPM spec file
--------------------

.. literalinclude:: diffs/application.spec
   :language: spec
   :caption: Example RPM spec file converted to Python 3

