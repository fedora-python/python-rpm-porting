.. toctree::
   :hidden:

   self
   applications
   modules
   application-modules
   tools


=======================================
Welcome to the Python RPM Porting Guide
=======================================

This document aims to guide you through the process of porting your Python 2 RPM package to Python 3.

.. note::
    If you struggle with the porting of your package and would like help or more information, please contact us at the `python-devel mailing list`_ (also accessible through a `web interface`_) and we will try to help you and/or improve the guide accordingly.

    If you've spotted any errors, have any suggestions or think some section(s) could be expanded, please create an Issue or a Pull request on our `GitHub`_.

.. _python-devel mailing list: https://lists.fedoraproject.org/admin/lists/python-devel.lists.fedoraproject.org/
.. _web interface: https://lists.fedoraproject.org/archives/list/python-devel@lists.fedoraproject.org/
.. _GitHub: https://github.com/fedora-python/python-rpm-porting

.. contents:: Table of Contents
   :local:


Is your package ready to be ported?
-----------------------------------

First thing you need to figure out is if the software you're packaging is ready to be packaged for Python 3.

Does upstream support Python 3?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Look  upstream and try to find out if the software is released with Python 3 support. First look at the front page of the project, Python compatibility is oftentimes listed there. There is also a good chance the project will have this information listed on `PyPI`_. If not, look at release notes or the changelog history. You can also look at issues and pull requests.

.. _PyPI: https://pypi.python.org/pypi

However, the important thing to note is that the Python 3 support needs to be *released*, not just committed in the version control system (git, mercurial,...).

Are the dependencies of your package ported to Python 3 for your distribution?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Before you start porting, it's imperative that you check that all the dependencies of your package are also ported to Python 3 in the distribution you are packaging for (Fedora, CentOS, RHEL or any other RPM-based distribution).

You may encounter a situation where your software is Python 3 ready upstream, but it uses some dependencies that are packaged only for Python 2 in your distribution. In that case try to communicate with the maintainer of the needed package and try to motivate and/or help them with porting of the package.


.. _chosing-type-section:

What type of software are you packaging?
----------------------------------------

There are four distinct types of Python packages, each with different instructions for porting, so be mindful of which you chose.

In rare cases your package might not nicely fall into either of these categories. In that case use the relevant parts from multiple sections or contact us on the mailing list.

1. Applications that happen to be written in Python
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. include:: snippets/desc_applications.inc

*See:* :doc:`applications`

2. Python modules
^^^^^^^^^^^^^^^^^

If your package is being imported by third-party projects, but does not have any executables, you're dealing with a Python module.

*See:* :doc:`modules`

3. An application and a module in one package
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. include:: snippets/desc_application-modules.inc

*See:* :doc:`application-modules`

4. Tools for programming in Python
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. include:: snippets/desc_tools.inc

*See:* :doc:`tools`
