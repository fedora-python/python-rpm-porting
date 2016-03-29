.. Python RPM Porting documentation master file, created by
   sphinx-quickstart on Tue Mar 22 13:14:36 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

=======================================
Welcome to the Python RPM Porting Guide
=======================================

This is a guide for porting Python 2 Fedora packages to Python 3.

There are three disctinct types of Python packages, each with its corresponding section of this guide:


Is your package ready to be ported?

* Is upstream ported to python 3?
* Are the dependencies of your package ported to python 3 in fedora?


1. :doc:`Applications written in Python <applications>`
-------------------------------------------------------

If your package is not being imported by third-party projects (e.g. ``import some_module`` in a python file), your package is most likely an application.

However, if your application has a plugin system or interacts with user code, look into :doc:`section 3 <modules-with-executables>`.

TODO move links here to the end of the explain text, because clicking on the headings isn't very obvious

2. :doc:`Modules for Python <modules>`
--------------------------------------

If your package is being imported by third-party projects, but does not have any executables, you're dealing with a standard Python module.

3. :doc:`Modules with their own executables <modules-with-executables>`
-----------------------------------------------------------------------
TODO Python tools??

This section is useful in three cases:

* If your application has a plugin system or in any way interacts with user code.
* If your package is being imported by third-party projects and also has an executable.
* If your package needs to ship both Python 2 and Python 3 executable.

