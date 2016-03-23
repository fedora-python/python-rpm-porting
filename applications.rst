Applications written in Python
==============================

This section is for packages that are not being imported by third-party projects (e.g. ``import some-module`` in a Python file). If your package *is* being imported, look into :doc:`other sections <index>`.

Porting the specfile to Python 3
--------------------------------

Applications behave the same when run under Python 2 and Python 3, therefore all you need to do is change the specfile to use Python 3 instead of Python 2.

**In essense the porting of an application RPM consists of simply going through the spec file and substituting the number 2 with number 3 where appropriate.**

So let's take an example spec file and port it to illustrate the process. We start with a spec file for an application using Python 2:

.. literalinclude:: diffs/application.spec.orig
   :language: spec
   :caption: Example spec file for an application running on Python 2.

Modifications
-------------

First it's recommended to update the software to the newest upstream version, or if not, increase the release number.

BuildRequires and Requires
^^^^^^^^^^^^^^^^^^^^^^^^^^

Change ``BuildRequires`` from ``python2-devel`` to ``python3-devel`` and adjust all other ``Requires`` and ``BuildRequires`` entries to point only to python3 packages.

**It is very important that you don't use any Python 2 dependencies, because that would mean your package would depend both on Python version 2 and version 3, which is even worse than relying only on Python 2.**

%build
^^^^^^

In the build section you'll usually find either the ``%py2_build`` macro or some custom build script prefixed by the ``%{__python2}`` macro. In both cases just substitute number 2 by number 3.

%install and %check
^^^^^^^^^^^^^^^^^^^

Install sections can vary a lot, but the above-mentioned general rule applies: substitute number 2 by number 3 where appropriate.

For example, if you find the ``%py2_install`` macro, substitute ``%py3_install``, if you find the ``%{__python2}`` macro, substitute ``%{__python3}``, etc.

%files
^^^^^^

In the files section you should usually find the ``%{python2_sitelib}`` macro, which you should substitute with ``%{python3_sitelib}``.

Files section also may contain the versioned executable, usually ``%{_bindir}/sample-exec-2.7`` in which case substitute ``%{_bindir}/sample-exec-3.?``.

Diff of the changes
-------------------

.. literalinclude:: diffs/application.spec
   :diff: diffs/application.spec.orig
   :caption: Diff between the original example Python 2 spec file and the converted Python 3 spec file.

Ported RPM spec file
--------------------

.. literalinclude:: diffs/application.spec
   :language: spec
   :caption: Example RPM spec file converted to Python 3

