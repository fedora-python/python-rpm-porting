.. Python RPM Porting documentation master file, created by
   sphinx-quickstart on Tue Mar 22 13:14:36 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

===================================
Welcome to Python RPM Porting Guide
===================================

This is a guide to for porting Fedora packages for Python 2 to Python 3.

There are three disctinct types of Python packages, each with its corresponding section of this guide:

1. :doc:`Applications written in Python <applications>`
----------------------

If your package is not being imported by third-party projects (e.g. ``import some-module`` in a python file), your package is most likely an application.

2. :doc:`Modules for Python <modules>`
--------------------------------------

If your package is being imported by third-party projects, but does not have any executables, you're dealing with a standard Python module.

3. :doc:`Modules with their own executables <modules-with-executables>`
-----------------------------------------------------------------------

This section is useful in two cases:

* If your package is being imported by third-party projects and also has an executable.
* If your package needs to ship both Python 2 and Python 3 executable.

