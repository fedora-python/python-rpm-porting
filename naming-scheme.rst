Following the new naming scheme
===============================

.. include:: snippets/naming_scheme.inc

.. note::
	This is mostly related to renaming Python **binary** packages to avoid using ``python-`` prefix without a version and does not require changing the SRPM name.

Why is this so important?
-------------------------

When the time comes and ``python`` means Python 3 in Fedora, installing a ``python-<srcname>`` package will imply a Python 3 version of this package. This is planned for 2020, when upstream support for Python 2 ends. To achieve this all Python binary packages have to follow the new naming scheme and use ``%python_provide`` macro, devised to make the switch easier. However, currently we are far away from achieving this goal.

Using outdated naming scheme in your subpackage names or runtime/builtime requirements might cause a range of issues when the switch happens.

What needs to be changed?
-------------------------

Check the names of binary packages you are building from your SRPM, and if you use one of the following naming schemes, fix it with the instructions provided in `Required changes`_.

Common naming scheme violations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

See the following naming schemes which violate the current naming guidelines:

.. list-table:: 
   :header-rows: 1
   :stub-columns: 1

   *  -  SRPM
      -  RPMs built
      -  Violaion
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

Required changes
^^^^^^^^^^^^^^^^

Add ``%package`` section for the Python 2 subpackage
""""""""""""""""""""""""""""""""""""""""""""""""""""

To rename the binary package to ``python2-<srcname>``, you should build it as a subpackage with an appropriate name. Make sure to move all related runtime requirements and use `%python_provide`_ macro, which will provide both ``python-<srcname>`` and ``python2-<srcname>`` until the switch to Python 3 happens.

The change you are about to do should look like this:

.. literalinclude:: specs/module.spec
	:diff: specs/module.spec.orig
	:lines: 15-19,21-34

.. _%python_provide: modules.html#python-provide
	
Use ``%python_provide`` macro in the Python 3 subpackage
""""""""""""""""""""""""""""""""""""""""""""""""""""""""

Check your Python 3 subpackage (if you build any), and make sure you are using the `%python_provide`_ macro to handle provides:

.. literalinclude:: specs/module.spec
	:language: spec
	:emphasize-lines: 5
	:lines: 30-37

Rename ``%files`` section
"""""""""""""""""""""""""

Give a name with a versioned prefix to the current ``%files`` section, and make sure to use new versioned macros ``%{python2_sitelib}``, ``%{python2_sitearch}``, ``%{python2_version}``:

.. literalinclude:: specs/module.spec
	:diff: specs/module.spec.orig
	:lines: 67-68,70-74

At this point you should be done. Just bump the release tag and add a changelog that you've updated the package to use the new naming scheme.
