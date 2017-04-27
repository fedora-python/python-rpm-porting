New Python package naming scheme
================================

.. include:: snippets/naming_scheme.inc

.. note::
   This section is related to the renaming of Python **binary RPM** packages to avoid using the ``python-`` prefix without a version. Changing the main package/SRPM name is not required.

Why is this important?
----------------------

When the time comes and ``python`` means Python 3 in Fedora, installing a ``python-<srcname>`` package will imply a Python 3 version of this package. This is planned for 2020, when upstream support for Python 2 ends. To achieve this, all Python binary RPM packages have to follow the new naming scheme and use the ``%python_provide`` macro, devised to make the switch easier. However, we are still far away from achieving this goal.

Using the outdated naming scheme in your subpackage names or run-time/build-time requirements might cause a range of issues when the switch happens.

What needs to be changed?
-------------------------

Check the names of binary RPM packages you are building from your SRPM, and if you use one of the following naming schemes, you'll find instructions on how to fix it in the `section below <required_changes_>`_.

.. _common_naming_scheme_violations:

Common naming scheme violations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

See the following naming schemes which violate the current naming guidelines:

.. list-table:: 
   :header-rows: 1
   :stub-columns: 1

   *  -  SRPM
      -  Binary RPMs built
      -  Violation
   *  -  python-<srcname>
      -  | python-<srcname>
      -  unversioned `python-` prefix in the binary package
   *  -  python-<srcname>
      -  | python-<srcname>
         | python3-<srcname>
      -  unversioned `python-` prefix in the binary package
   *  -  <srcname>
      -  | <srcname>
         | python3-<srcname>
      -  missing `python2-` prefix in the binary package

.. _required_changes:

Required changes
^^^^^^^^^^^^^^^^

Add a ``%package`` section for the Python 2 subpackage
""""""""""""""""""""""""""""""""""""""""""""""""""""""

To rename the binary RPM package to ``python2-<srcname>``, you should build it as a subpackage with an appropriate name. Make sure to move all related runtime requirements from the main package to the new subpackage and use the `%python_provide`_ macro, which will provide both ``python-<srcname>`` and ``python2-<srcname>`` until the switch to Python 3 happens.

The change should look like this:

.. literalinclude:: specs/module.spec
   :diff: specs/module.spec.orig
   :lines: 15-19,21-32,43

Note, that in case of the last naming scheme example in the `table above <common_naming_scheme_violations_>`_, when you rename the binary RPM from ``<srcname>`` to ``python2-<srcname>``, the `%python_provide`_ macro will not provide the old name ``<srcname>``. To keep the upgrade path clean you will have to provide it and obsolete the old verision manually. You may place the tags right after the `%python_provide`_ macro:

.. code-block:: spec
   :emphasize-lines: 2,3

   %{?python_provide:%python_provide python2-%{srcname}}
   Provides:   %{srcname} = %{version}-%{release}
   Obsoletes:  %{srcname} < current_version-current_release

In the Obsoletes tag, ``current_version`` and ``current_release`` are the hardcoded version and release that were current when you did the change.

.. _%python_provide: modules.html#python-provide

Use the ``%python_provide`` macro in the Python 3 subpackage
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

Check your Python 3 subpackage (if you build any), and make sure you are using the `%python_provide`_ macro to handle provides:

.. literalinclude:: specs/module.spec
   :language: spec
   :emphasize-lines: 5
   :lines: 30-37

Rename the ``%files`` section
"""""""""""""""""""""""""""""

To assign the ``%files`` section to the Python 2 subpackage, add the subpackage name with the versioned prefix after the ``%files`` macro. Make sure to use the new versioned macros ``%{python2_sitelib}``, ``%{python2_sitearch}``, and ``%{python2_version}`` as well:

.. literalinclude:: specs/module.spec
   :diff: specs/module.spec.orig
   :lines: 67-68,70-74

At this point you should be done. Don't forget to bump the release tag and add a changelog entry indicating you've updated the package to use the new naming scheme.
