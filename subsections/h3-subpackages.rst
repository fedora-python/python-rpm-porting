Creating subpackages
^^^^^^^^^^^^^^^^^^^^

Each subpackage you create will need to have its own name, summary and description. If you haven't already, it is thus advised to declare macros for common values at the top of the specfile:

.. code-block:: spec

    %global srcname example
    %global sum An example Python tool

Now we can use these to create the subpackages. The following should be placed beneath the ``%description`` section of the base package:

.. code-block:: spec

    %package -n python2-%{srcname}
    Summary:  %{sum}
    Requires: python-some-module
    Requires: python2-other-module
    %{?python_provide:%python_provide python2-%{srcname}}

    %description -n python2-%{srcname}
    A Python tool which provides a convenient example.


    %package -n python3-%{srcname}
    Summary:  %{sum}
    Requires: python3-some-module
    Requires: python3-other-module
    %{?python_provide:%python_provide python3-%{srcname}}

    %description -n python3-%{srcname}
    A Python tool which provides a convenient example.

First, using the ``%package`` macro you start defining a new *subpackage*, specifying its full name as ``python2-%{srcname}``, which in this case will become ``python2-example``. Next we provide the summary through the macro we defined earlier.

.. _requires_subsection:

``BuildRequires:`` tags from the original spec file will remain where they are—declared in the definition of the base package at the top of the spec file. However, the runtime requirements—the ones listed using the ``Requires:`` tag—will be different for the two subpackages, so they have to be moved here to the definition of each subpackage.

While you can *cut and paste* all the ``Requires:`` tags directly from the base package to the ``python2-`` subpackage, remember that for the ``python3-`` subpackage you need to find Python 3 versions of each of the runtime dependencies.

.. note::

    You can see that the naming of Python 2 packages isn't uniform: some follow the current convention of using the ``python2-`` prefix, older ones use only the ``python-`` prefix, and the oldest might be without a prefix at all.

    In many cases the Python 2 package can be found under both the ``python2-`` and ``python-`` prefixes, one of them being *virtually provided* by the ``Provides:`` tag. Whenever possible, use the version with the ``python2-`` prefix.
