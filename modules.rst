Porting Python modules
======================

This section is for Python **packages that do not have any executables**. Usually, these are normal Python modules that are being imported by third-party projects.

.. include:: snippets/section_header.rst


Porting the specfile to Python 3
--------------------------------

Because the software you're packaging is going to be imported by third-party projects, it is crucial to think about what Python versions your package will support.

If you switch your package to use only Python 3, suddenly projects running on Python 2 will no longer be able to import your modules. And of course, if you continue using Python 2 only, new Python 3 projects won't get to use your software either.

For these reasons, it is highly advised to **split your package into two subpackages**, one for each major Python version.

Let's take an example spec file and port it to illustrate the process. We start with a spec file for Python module packaged for Python 2.

.. literalinclude:: specs/module.spec.orig
   :language: spec


.. include:: subsections/h2-modifications.rst

.. include:: subsections/h3-subpackages.rst

.. include:: subsections/h4-python_provide.rst

.. include:: subsections/h4-description.rst

.. include:: subsections/h3-build-requires.rst

.. include:: subsections/h3-build.rst


%install
^^^^^^^^

First, in the same manner as in the preceding :ref:`build-section` section, it is advisable to upgrade the current Python 2 install command to use the new ``%py2_install`` macro, however, if that doesn't work for you, you can stick with the current install command, just make sure it's invoked by the ``%{__python2}`` macro.

After that, add the corresponding Python 3 install command, which will be either be the custom command prefixed by ``%{__python3}`` or the new ``%py3_install`` macro.

.. code-block:: spec

    %install
    %py2_install
    %py3_install

.. include:: snippets/install_non-python-script.rst


.. include:: subsections/h3-check.rst


%files
^^^^^^

The presence or absence of a ``%files`` section is the deciding factor in whether a given package or subpackage gets built or not. Therefore, to assure that our base package doesn't get built (as all the content has been moved to the two subpackages), make sure there is no ``%files`` section without a subpackage name.

You can reuse the current ``%files`` section for the Python 2 submodule by giving it the appropriate package name. You can keep it almost the same as before, just make sure that, where appropriate, it uses the new macros ``%{python2_sitelib}``, ``%{python2_sitearch}``, ``%{python2_version}`` or perhaps ``%{python2_version_nodots}``.

.. code-block:: spec

    %files -n python2-%{srcname}
    %license COPYING
    %doc README
    %{python2_sitelib}/*

Accordingly we'll also add a ``%files`` section for the Python 3 subpackage. You can copy the previous files section, but make sure you change all the Python 2 macros into Python 3 versions.

.. code-block:: spec

    %files -n python3-%{srcname}
    %license COPYING
    %doc README
    %{python3_sitelib}/*


.. include:: subsections/h2-ported-specfile.rst


.. literalinclude:: specs/module.spec
   :language: spec

.. include:: subsections/h2-diff.rst


.. literalinclude:: specs/module.spec
   :diff: specs/module.spec.orig
