Porting an application and a module in one package
==================================================

.. include:: snippets/desc_application-modules.rst

.. include:: snippets/section_header.rst


Porting the specfile to Python 3
--------------------------------

Because the software you're packaging is going to be imported by third-party projects, it is crucial to think about what Python versions your package will support.

If you switch your package to use only Python 3, suddenly projects running on Python 2 will no longer be able to import your modules. And of course, if you continue using Python 2 only, new Python 3 projects won't get to use your software either.

For these reasons, the `Fedora Packaging Guidelines for Python`_ advise to **split your package into two subpackages**, one for each major Python version.

.. _`Fedora Packaging Guidelines for Python`: https://fedoraproject.org/wiki/Packaging:Python#Common_SRPM_vs_split_SRPMs

In contrast to the Python module, however, the bundled application does not interact with Python code, and is therefore Python version agnostic. For that reason, we need only to package it once, i.e. only in one of the subpackages.

Let's take an example spec file and port it to illustrate the process. We start with a spec file for a Python tool packaged for Python version 2:

.. literalinclude:: specs/tool.spec.orig
   :language: spec


.. include:: subsections/h2-modifications.rst

.. include:: subsections/h3-subpackages.rst

.. include:: subsections/h4-python_provide.rst

.. include:: subsections/h4-description.rst

.. include:: subsections/h3-build-requires.rst

.. include:: subsections/h3-build.rst

.. include:: subsections/h3-install.rst

.. include:: subsections/h3-check.rst


%files
^^^^^^

.. include:: snippets/files_python2_subpackage.rst

You can reuse the current ``%files`` section for the Python 2 submodule by giving it the appropriate package name. You can keep it almost the same as before, just make sure that, where appropriate, it uses the new macros ``%{python2_sitelib}``, ``%{python2_sitearch}``, ``%{python2_version}`` or perhaps ``%{python2_version_nodots}``.

However, be sure *not to* include the executable. The `Fedora Packaging Guidelines for Python`_ state that if you are packaging only one executable, it should be the one for Python 3.

.. code-block:: spec

    %files -n python2-%{srcname}
    %license COPYING
    %doc README
    %{python2_sitelib}/*

We'll also add a ``%files`` section for the Python 3 subpackage. You can copy the previous files section, but make sure you change all the Python 2 macros into Python 3 versions. And in this case, do not forget to *include* the executable as well.

.. code-block:: spec

    %files -n python3-%{srcname}
    %license COPYING
    %doc README
    %{python3_sitelib}/*
    %{_bindir}/sample-exec


.. include:: subsections/h2-ported-specfile.rst


.. literalinclude:: specs/application-module.spec
   :language: spec


.. include:: subsections/h2-diff.rst


.. literalinclude:: specs/application-module.spec
   :diff: specs/tool.spec.orig
