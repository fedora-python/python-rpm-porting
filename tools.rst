Porting tools for programming in Python
=======================================

.. include:: snippets/desc_tools.rst

.. include:: snippets/section_header.rst


Porting the specfile to Python 3
--------------------------------

Because your package has an executable that interacts with Python code, users will most likely want it to work both with code for Python 2 and code for Python 3, as both are very common today. And even in the future, there will be heaps of legacy Python 2 code that may still be useful.

When you want to package two different executables, the best practice (put forth by the `Fedora Packaging Guidelines for Python`_) is to **split your package into two subpackages.** One subpackage for Python 2 and one for Python 3. That will allow the user to install just one of them instead of having to install the other as well, for which they not have any need.

.. _`Fedora Packaging Guidelines for Python`: https://fedoraproject.org/wiki/Packaging:Python#Common_SRPM_vs_split_SRPMs

Let's take an example spec file and port it to illustrate the process. We start with a spec file for a Python tool packaged for Python version 2:

.. literalinclude:: specs/tool.spec.orig
   :language: spec


.. include:: subsections/h2-modifications.rst

.. include:: subsections/h3-subpackages.rst

.. include:: subsections/h4-python_provide.rst

.. include:: subsections/h4-description.rst

.. include:: subsections/h3-build-requires.rst

.. include:: subsections/h3-build.rst


%install
^^^^^^^^

The ``%install`` section is perhaps the most crucial one, because we have to be very mindful of which executable goes where and what symlinks should be created.

First, in the same manner as in the preceding `build-section`_ section, it is advisable to upgrade the current Python 2 install command to use the new ``%py2_install`` macro, however, if that doesn't work for you, you can stick with the current install command, just make sure it's invoked by the ``%{__python2}`` macro. The corresponding Python 3 install command will then either be the custom command prefixed by ``%{__python3}`` or the new ``%py3_install`` macro, which I'll be using in this example.

.. include:: snippets/install_non-python-script.rst

As the `packaging guidelines`_ specify, the Python 2 package is currently to be the default one, thus it is best if we first install the Python 3 version of our software and then the one for Python 2, because in case they are installing some files into the same directories (such as ``/usr/bin/``), one installation will overwrite the files of the other. So if we install the Python 2 version last, its files will be located in those shared directories.

.. code-block:: spec

    %install
    %py3_install

    # Now /usr/bin/sample-exec is Python 3, so we move it away
    mv %{buildroot}%{_bindir}/sample-exec %{buildroot}%{_bindir}/sample-exec-%{python3_version}

    %py2_install

    # Now /usr/bin/sample-exec is Python 2, and we move it away anyway
    mv %{buildroot}%{_bindir}/sample-exec %{buildroot}%{_bindir}/sample-exec-%{python2_version}

Moving the Executables and Making Symlinks
******************************************

Again in compliance with the `packaging guidelines`_, we should provide the executables in the format ``executable-name-X.Y``, where X and Y are the major and minor Python versions, e.g. ``2.7`` or ``3.5`` (instead of hardcoding these values, you can use the macros ``%{python2_version}`` and ``%{python3_version}``). Thus after each of the install scripts finishes, we move the resulting executable and rename it accordingly.

What remains is to provide symlinks for the executables in the format ``executable-name-2`` and ``executable-name-3``, pointing to their respective executables, and then finally a symlink for the general name, in this case ``sample-exec``, which shall point to the Python 2 version symlink—here ``sample-exec-2``.

.. code-block:: spec

    # The guidelines also specify we must provide symlinks with a '-X' suffix.
    ln -s ./sample-exec-%{python2_version} %{buildroot}%{_bindir}/sample-exec-2
    ln -s ./sample-exec-%{python3_version} %{buildroot}%{_bindir}/sample-exec-3

    # Finally, we provide /usr/bin/sample-exec as a link to /usr/bin/sample-exec-2
    ln -s ./sample-exec-2 %{buildroot}%{_bindir}/sample-exec

Note that these symlinks use a relative path in relation to their location, i.e. they are pointing to a file that is at any given moment in the same directory as they are.


.. include:: subsections/h3-check.rst


%files
^^^^^^

.. include:: snippets/files_preamble.rst

You can reuse the current ``%files`` section for the Python 2 submodule by giving it the appropriate package name. You can keep it almost the same as before, just make sure that, where appropriate, it uses the new macros ``%{python2_sitelib}``, ``%{python2_sitearch}``, ``%{python2_version}`` or perhaps ``%{python2_version_nodots}``. Finally, don't forget to add the two new locations of the executable we've made available through the symlinks.

.. code-block:: spec

    %files -n python2-%{srcname}
    %license COPYING
    %doc README
    %{python2_sitelib}/*
    %{_bindir}/sample-exec
    %{_bindir}/sample-exec-2
    %{_bindir}/sample-exec-%{python2_version}

Accordingly we'll also add a ``%files`` section for the Python 3 subpackage. You can copy the previous files section, but make sure you change all the Python 2 macros into Python 3 versions. And unlike the former, the Python 3 ``%files`` section shall not contain the unversioned executable (``sample-exec`` in our example) as that executable is for Python 2, not 3.

.. code-block:: spec

    %files -n python3-%{srcname}
    %license COPYING
    %doc README
    %{python3_sitelib}/*
    %{_bindir}/sample-exec-3
    %{_bindir}/sample-exec-%{python3_version}


.. include:: subsections/h2-ported-specfile.rst


.. literalinclude:: specs/tool.spec
   :language: spec


.. include:: subsections/h2-diff.rst


.. literalinclude:: specs/tool.spec
   :diff: specs/tool.spec.orig
