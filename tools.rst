Porting Python tools
====================

This section is for Python **packages with executables that in some-way or another interact with Python code**. For example:

* If your application has a plugin system or in any way interacts with user code.
* If your package is being imported by third-party projects and also has an executable.
* If your package needs to ship both Python 2 and Python 3 executables.

If this is not the case for your software, look into :ref:`other sections <chosing-type-section>`.

.. contents:: Table of Contents
   :local:

Porting the specfile to Python 3
--------------------------------

Because your package has an executable that interacts with Python code, users will most likely want it to work both with code for Python 2 and code for Python 3, as both are very common today. And even in the future, there will be heaps of legacy Python 2 code that may still be useful.

When you want to package two different executables, the best practice (put forth by the `Fedora Packaging Guidelines for Python`_) is to **split your package into two subpackages.** One subpackage for Python 2 and one for Python 3. That will allow the user to install just one of them instead of having to install the other as well, for which they not have any need.

.. _`Fedora Packaging Guidelines for Python`: https://fedoraproject.org/wiki/Packaging:Python#Common_SRPM_vs_split_SRPMs

Let's take an example spec file and port it to illustrate the process. We start with a spec file for a Python tool packaged for Python version 2.

.. literalinclude:: specs/tool.spec.orig
   :language: spec
   :caption: Example spec file of a Python tool packaged for Python 2.


Modifications
-------------

First it is recommended to update the software you are packaging to its newest upstream version. If it already is at the latest version, increment the release number. Don't forget to add a ``%changelog`` entry as well.


Creating subpackages
^^^^^^^^^^^^^^^^^^^^

Each subpackage you create will need to have it's own name, summary and description. If you haven't already, it is thus advised to declare some macros for your package at the top of the specfile:

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

%python_provide
***************

Now that we're splitting the package ``python-example`` into ``python2-example`` and ``python3-example``, we need to define what will happen when the user tries to install the unversioned name ``python-example``.

At the time of this writing, the `packaging guidelines`_ say that the *default* version should be the one for Python 2. However, it is expected to change to Python 3 some time in the future. To avoid having to adjust all Python packages in Fedora when that time comes, the ``%python_provide`` macro was devised:

.. _`packaging guidelines`: https://fedoraproject.org/wiki/Packaging:Python#Avoiding_collisions_between_the_python_2_and_python_3_stacks

.. code-block:: spec

    %{?python_provide:%python_provide python2-%{srcname}}
    and
    %{?python_provide:%python_provide python3-%{srcname}}

This is a line you should include in each of your subpackages and it works thus: First the part ``?python_provide:`` checks whether the macro exists and if not, the entire line is ignored. After that we actually use the ``%python_provide`` macro and give it one argument—the name of the given subpackage.

The macro will then check whether this Python version is default or not—if not, the line is again ignored. However, if indeed this is the currently default Python version, the macro is replaced with a *virtual provides* tag: ``Provides: python-%{srcname}``. This will tell the packaging system (dnf, yum, ...) to install this subpackage when user searches for ``python-example``.

.. _description-subsection:

%description
************

Each subpackage also needs to contain its own description. However, unlike the ``Summary:`` and ``Requires:`` tags, which are automatically applied to the subpackage declared above them, the ``%description`` macro needs to be told to which subpackage it belongs. You can do that by appending the same name as you did with the ``%package`` macro itself.

.. code-block:: spec

    %description -n python3-%{srcname}
    A Python tool which provides a convenient example.


BuildRequires and Requires
^^^^^^^^^^^^^^^^^^^^^^^^^^

Now that you're building subpackages for both Python 2 and Python 3, you need to adjust the ``BuildRequires:`` by adding Python 3 versions of all the existing build dependencies. Starting with ``python-devel``: Use it's new version-specific name ``python2-devel`` and add it's Python 3 equivalent ``python3-devel``.

As described :ref:`above <requires_subsection>`, ``Requires:`` tags are a bit more complicated. You should move the current set of ``Requires:`` underneath the definition of the Python 2 subpackage, and for the Python 3 subpackage, you need to find Python 3 alternatives for all the current Python 2 runtime requirements that are specified with the ``Requires:`` tags.


.. _build-section:

%build
^^^^^^

Currently your package is building the software for Python 2, what we need to do is also add building for Python 3. While we're modifying the spec file, however, it's a good idea to also update it to new standards—in this case a new macro.

In the ideal case, you'll find the build done with either the ``%py2_build`` macro or its older version ``%py_build``, which you then should exchange for the former. In either case, you can just add the macro ``%py3_build`` afterwards, and this part is done.

.. code-block:: spec

    %build
    %py2_build
    %py3_build

In many cases, however, you will find a custom build command prefixed by the ``%{__python}`` or ``%{__python2}`` macros, or in some cases just prefixed by the python interpreter invoked without a macro at all, e.g.::

    %{__python} custombuild.py --many-flags
        or
    python custombuild.py --many-flags

In these cases first try substituting the whole build command by the new pair of smart macros ``%py2_build`` and ``%py3_build``, which should in many cases correctly figure out what ought to be done automatically. Otherwise, duplicate the entire command and change the invocation of the python interpreter to the ``%{__python2}`` macro in one of them and to the ``%{__python3}`` in the other.

.. code-block:: spec

    %build
    %{__python2} custombuild.py --many-flags
    %{__python3} custombuild.py --many-flags


%install
^^^^^^^^

The ``%install`` section is perhaps the most crucial one, because we have to be very mindful of which executable goes where and what symlinks should be created.

First, in the same manner as in the preceding :ref:`build-section` section, it is advisable to upgrade the current Python 2 install command to use the new ``%py2_install`` macro, however, if that doesn't work for you, you can stick to the current install command, just make sure it's invoked by the ``%{__python2}`` macro. The corresponding Python 3 install command will then either be the custom command prefixed by ``%{__python3}`` or the new ``%py3_install`` macro, which I'll be using in this example.

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


%check
^^^^^^

Unlike in previous sections, there's no special macro for the ``%check`` section, and so here just make sure that the tests are invoked once using the ``%{__python2}`` macro and a second time using the ``%{__python3}`` macro.

.. code-block:: spec

    %check
    %{__python2} setup.py test
    %{__python3} setup.py test

%files
^^^^^^

The presence or absence of a ``%files`` section is the deciding factor in whether a given package or subpackage gets built or not. Therefore, to assure that our base package doesn't get built (as all the content has been moved to the two subpackages), make sure there is no ``%files`` section without a subpackage name.

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

Ported RPM spec file
--------------------

Here you can peruse the entire ported spec file:

.. literalinclude:: specs/tool.spec
   :language: spec


Diff of the changes
-------------------

And here you can see the diff of the original and the ported spec files to fully observe all the changes that were made:

.. literalinclude:: specs/tool.spec
   :diff: specs/tool.spec.orig


