Porting an application and a module in one package
==================================================

.. include:: snippets/desc_application-modules.inc

.. include:: snippets/section_header.inc


Porting the specfile to Python 3
--------------------------------

Because the software you're packaging is going to be imported by third-party projects, it is crucial to think about what Python versions your package will support.

If you switch your package to use only Python 3, suddenly projects running on Python 2 will no longer be able to import your modules. And of course, if you continue using Python 2 only, new Python 3 projects won't get to use your software either.

For these reasons, the `Fedora Packaging Guidelines for Python`_ advise to **split your package into two subpackages**, one for each major Python version.

.. _`Fedora Packaging Guidelines for Python`: https://fedoraproject.org/wiki/Packaging:Python#Common_SRPM_vs_split_SRPMs

In contrast to the Python module, however, the bundled application does not interact with Python code, and is therefore Python version agnostic. For that reason, we need only to include it in one of the subpackages, not both. And when the version does not matter, the guidelines compel us to install the version for Python 3, therefore we will include it in the Python 3 subpackage.

Let's take an example spec file and port it to illustrate the process. We start with a spec file for a Python tool packaged for Python version 2:

.. literalinclude:: specs/tool.spec.orig
   :language: spec


.. include:: subsections/h2-modifications.inc

.. include:: subsections/h3-subpackages.inc

.. include:: subsections/h4-python_provide.inc

.. include:: subsections/h4-description.inc


.. include:: subsections/h3-build-requires.inc

As we will be including the executable (application) only in the Python 3 subpackage, you may be also able to get rid of some runtime dependencies (listed using the ``Requires:`` tags) in the Python 2 subpackage that were previously used only by the executable and are therefore no longer needed in that subpackage. However, figuring out what runtime dependencies are no longer needed is a problematic task, therefore if you are unsure of which dependencies can be omitted, you can skip this task.

.. include:: subsections/h3-build.inc


%install
^^^^^^^^

First, in the same manner as in the preceding `%build`_ section, it is advisable to upgrade the current Python 2 install command to use the new ``%py2_install`` macro, however, if that doesn't work for you, you can stick with the current install command, just make sure it's invoked by the ``%{__python2}`` macro.

After the Python 2 install macro is run, it is likely going to install the Python 2 version of the application. As we want to package only the Python 3 version of the application, we have to remove the Python 2 executable(s) that were installed into ``/usr/bin/`` so that the Python 3 version(s) can take their place afterwards.

.. code-block:: spec

    %install
    %py2_install
    rm %{buildroot}%{_bindir}/*

After that, add the corresponding Python 3 install command, which will be either the custom command prefixed by ``%{__python3}`` or the new ``%py3_install`` macro.

.. code-block:: spec

    %py3_install

.. include:: /snippets/install_non-python-script.inc


.. include:: subsections/h3-check.inc


%files
^^^^^^

.. include:: snippets/files_preamble.inc

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


.. include:: subsections/h3-shebangs.inc


Have you broken third-party packages?
-------------------------------------

Congratulations, you have now successfully ported your package to be available for both Python 2 and Python 3! However, in doing so, many of the third-party packages that depend on the application bundled in this package may have just been broken.

The best practice when depending on executables is to depend on them explicitly, i.e. use ``Requires: /usr/bin/sample-exec``. That way no matter to which package the executable moves, your dependency gets loaded fine. However, many (if not most) packages are written with dependencies on the package itself (``Requires: python-example``) in which case they will now be depending on the ``python2-example`` subpackage, because it has the currently active ``%python_provide`` macro (see `%python_provide`_). However, the executable has moved to the ``python3-example`` subpackage, and thus the dependency has been broken.

First, see what (if any) packages depend on this package itself:

.. code-block:: console

   $ dnf repoquery --whatrequires python-example

Now you ought to go through these packages one by one and try to figure out if they need to depend on the application from your package, or on the Python module, or possibly, both.

If you do think they want to depend on your application, and therefore the dependency may have just been broken, you are advised to open a BugZilla report and request that they change (or add) the dependency to the executable itself (``Requires: /usr/bin/sample-exec``). If you can provide a patch as well, your requests will be all the faster resolved.

If you are unsure whether the package needs to depend on your application, open a BugZilla report for the package and ask the maintainer(s) to answer the question themselves.


.. include:: subsections/h2-ported-specfile.inc


.. literalinclude:: specs/application-module.spec
   :language: spec


.. include:: subsections/h2-diff.inc


.. literalinclude:: specs/application-module.spec
   :diff: specs/tool.spec.orig
