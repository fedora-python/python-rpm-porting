Porting Python modules
======================

This section is for Python **packages that do not have any executables**. Usually normal Python modules that are being imported by third-party projects.

If this is not the case for your software, look into :ref:`other sections <chosing-type-section>`.

Porting the specfile to Python 3
--------------------------------

Because the software you're packaging is going to be imported by third-party projects, it is crucial to think about what Python versions your package will support.

If you switch your package to use only Python 3, suddenly projects running on Python 2 will no longer be able to import your modules. And of course, if you continue using Python 2 only, new Python 3 projects won't get to use your software either.

For these reasons, it is highly advised to **provide two subpackages**, one for each major Python version.

Let's take an example spec file and port it to illustrate the process. We start with a spec file for Python module packaged for Python 2.

.. literalinclude:: specs/module.spec.orig
   :language: spec
   :caption: Example spec file of a Python module packaged for Python 2.


Diff of the changes
-------------------

Here is a visualization of the changes to the spec file we have made according to the section :ref:`modifications`.

.. literalinclude:: specs/tool.spec
   :diff: specs/tool.spec.orig
   :caption: Diff between the original example Python 2 spec file and the converted Python 3 spec file.


Ported RPM spec file
--------------------

Finally, here is a fully ported RPM spec file you can peruse at your own pleasure.

.. literalinclude:: specs/module.spec
   :language: spec
   :caption: Example RPM spec file converted to use both Python 2 and Python 3

