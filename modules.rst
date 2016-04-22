Porting Python modules
======================

This section is for Python **packages that do not have any executables**. Usually, these are normal Python modules that are being imported by third-party projects.

.. include:: snippets/section_header.inc


Porting the specfile to Python 3
--------------------------------

Because the software you're packaging is going to be imported by third-party projects, it is crucial to think about what Python versions your package will support.

If you switch your package to use only Python 3, suddenly projects running on Python 2 will no longer be able to import your modules. And of course, if you continue using Python 2 only, new Python 3 projects won't get to use your software either.

For these reasons, it is highly advised to **split your package into two subpackages**, one for each major Python version.

Let's take an example spec file and port it to illustrate the process. We start with a spec file for Python module packaged for Python 2.

.. literalinclude:: specs/module.spec.orig
   :language: spec


.. include:: subsections/h2-modifications.inc

.. include:: subsections/h3-subpackages.inc

.. include:: subsections/h4-python_provide.inc

.. include:: subsections/h4-description.inc

.. include:: subsections/h3-build-requires.inc

.. include:: subsections/h3-build.inc

.. include:: subsections/h3-install.inc

.. include:: subsections/h3-check.inc


%files
^^^^^^

.. include:: snippets/files_preamble.inc

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


.. include:: subsections/h2-ported-specfile.inc


.. literalinclude:: specs/module.spec
   :language: spec

.. include:: subsections/h2-diff.inc


.. literalinclude:: specs/module.spec
   :diff: specs/module.spec.orig
