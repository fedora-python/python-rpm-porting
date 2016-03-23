Applications written in Python
==============================

This section is for packages that are not being imported by third-party projects (e.g. ``import some-module`` in a python file). If your package *is* being imported, look into :doc:`other sections <index>`.

Porting specfile to Python 3
----------------------------

Applications behave the same when run under python 2 and python 3, therefore all you need to do is change the specfile to use python 3 instead of python 2.

So let's take an example spec file and port it to illustrate the process. We start with a specfile for an application using python 2::

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

Modifying
^^^^^^^^^
::

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

Test
^^^^^^^^^^^^^^^^^^^

.. literalinclude:: diffs/application-diff-1
   :diff: diffs/application-diff-2

Diff of the changes
^^^^^^^^^^^^^^^^^^^
.. .. role:: red

.. :red:`-Release:        1%{?dist}`

::

     %global srcname example

     Name:           %{srcname}
     Version:        1.2.3
    -Release:        1%{?dist}
    +Release:        2%{?dist}
     Summary:        An example python application

     License:        MIT
     URL:            http://pypi.python.org/pypi/%{srcname}
     Source0:        http://pypi.python.org/packages/source/e/%{srcname}/%{srcname}-%{version}.tar.gz

     BuildArch:      noarch
    -BuildRequires:  python2-devel
    +BuildRequires:  python3-devel

     %description
     An python application which provides a convenient example.

     %prep
     %autosetup -n %{srcname}-%{version}

     %build
    -%py2_build
    +%py3_build

     %install
    -%py2_install
    +%py3_install

     %check
    -%{__python2} setup.py test
    +%{__python3} setup.py test

     %files
     %license COPYING
     %doc README.rst
    -%{python2_sitelib}/*
    +%{python3_sitelib}/*
     %{_bindir}/sample-exec
    -%{_bindir}/sample-exec-2.7
    +%{_bindir}/sample-exec-3.4

     %changelog
     ...
