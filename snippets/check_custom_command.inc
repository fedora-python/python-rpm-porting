As you can see on the example of the ``nosetests``, not all packages follow the proper naming conventions for executables. To list what executables a package contains, you can use:

.. code-block:: console

    $ dnf repoquery -l python3-nose | grep /usr/bin/
    /usr/bin/nosetests-3.4
