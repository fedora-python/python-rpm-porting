%install
^^^^^^^^

First, in the same manner as in the preceding `build-section`_ section, it is advisable to upgrade the current Python 2 install command to use the new ``%py2_install`` macro, however, if that doesn't work for you, you can stick with the current install command, just make sure it's invoked by the ``%{__python2}`` macro.

After that, add the corresponding Python 3 install command, which will be either be the custom command prefixed by ``%{__python3}`` or the new ``%py3_install`` macro.

.. code-block:: spec

    %install
    %py2_install
    %py3_install

.. include:: /snippets/install_non-python-script.rst
