Applications written in Python
==============================

This section is for packages that are not being imported by third-party projects (e.g. ``import some-module`` in a Python file). If your package *is* being imported, look into :doc:`other sections <index>`.

Porting the specfile to Python 3
--------------------------------

Applications behave the same when run under Python 2 and Python 3, therefore all you need to do is change the specfile to use Python 3 instead of Python 2.

**In essense the porting of an application RPM consists of simply going through the spec file and substituting the number 2 with number 3 where appropriate.**

So let's take an example spec file and port it to illustrate the process. We start with a spec file for an application using Python 2:

.. code-block:: spec
   :caption: Original spec file for an application running on Python 2.

    %global srcname example

    Name:           %{srcname}
    Version:        1.2.3
    Release:        1%{?dist}
    Summary:        An example python application

    License:        MIT
    URL:            http://pypi.python.org/pypi/%{srcname}
    Source0:        http://pypi.python.org/packages/source/e/%{srcname}/%{srcname}-%{version}.tar.gz

    BuildArch:      noarch
    BuildRequires:  python2-devel

    %description
    An python application which provides a convenient example.

    %prep
    %autosetup -n %{srcname}-%{version}

    %build
    %py2_build

    %install
    %py2_install

    %check
    %{__python2} setup.py test

    %files
    %license COPYING
    %doc README.rst
    %{python2_sitelib}/*
    %{_bindir}/sample-exec
    %{_bindir}/sample-exec-2.7

    %changelog
    ...

Modifications
-------------

First it's recommended to update the software to the newest version, otherwise bump the release number.

BuildRequires and Requires
^^^^^^^^^^^^^^^^^^^^^^^^^^

First change ``BuildRequires`` from ``python2-devel`` to ``python3-devel``. Next adjust all other ``Requires`` and ``BuildRequires`` entries to point only to python3 packages.

It is very important that you don't use any Python 2 dependencies, because that would mean your package would depend both on Python version 2 and 3, the worst of possible options.

Build
^^^^^

In the build section you'll usually find either the ``py2_build`` macro or some custom build script prefixed by the ``%{__python2}`` macro. In both cases just substitute number 2 by number 3.

# Install

Install sections can vary a lot, but the rule from the general rule

.. code-block:: spec
   :caption: RPM spec file converted to Python 3

    %global srcname example

    Name:           %{srcname}
    Version:        1.2.3
    Release:        2%{?dist}
    Summary:        An example python application

    License:        MIT
    URL:            http://pypi.python.org/pypi/%{srcname}
    Source0:        http://pypi.python.org/packages/source/e/%{srcname}/%{srcname}-%{version}.tar.gz

    BuildArch:      noarch
    BuildRequires:  python3-devel

    %description
    An python application which provides a convenient example.

    %prep
    %autosetup -n %{srcname}-%{version}

    %build
    %py3_build

    %install
    %py3_install

    %check
    %{__python3} setup.py test

    %files
    %license COPYING
    %doc README.rst
    %{python3_sitelib}/*
    %{_bindir}/sample-exec
    %{_bindir}/sample-exec-3.4

    %changelog
    ...

Diff of the changes
^^^^^^^^^^^^^^^^^^^

.. literalinclude:: diffs/application.spec
   :diff: diffs/application.spec.orig
   :caption: Diff between the origina Python 2 spec file and the converted Python 3 spec file.

