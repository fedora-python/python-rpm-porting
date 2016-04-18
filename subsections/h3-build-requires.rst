BuildRequires and Requires
^^^^^^^^^^^^^^^^^^^^^^^^^^

Now that you're building subpackages for both Python 2 and Python 3, you need to adjust the ``BuildRequires:`` by adding Python 3 versions of all the existing build dependencies. Starting with ``python-devel``: Use its new version-specific name ``python2-devel`` and add it's Python 3 equivalent ``python3-devel``.

As described :ref:`above <requires_subsection>`, ``Requires:`` tags are a bit more complicated. You should move the current set of ``Requires:`` underneath the definition of the Python 2 subpackage, and for the Python 3 subpackage, you need to find Python 3 alternatives for all the current Python 2 runtime requirements that are specified with the ``Requires:`` tags.


