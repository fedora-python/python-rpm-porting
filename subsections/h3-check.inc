%check
^^^^^^

Unlike in previous sections, there's no special macro for the ``%check`` section, and so here if the original spec file uses any sort of a python script for testing, just make sure that the tests are invoked once using the ``%{__python2}`` macro and a second time using the ``%{__python3}`` macro.

.. code-block:: spec

    %check
    %{__python2} setup.py test
    %{__python3} setup.py test

Chances are that you will encounter a custom Python command that runs the tests, such as ``nosetests`` or ``py.test``. In that case find out what is the name of the executable for Python 3 and run it after the Python 2 command.

If the command for Python 2 can be invoked explicitly for Python 2, e.g. as ``py.test-2`` instead of just ``py.test``, use it.

.. code-block:: spec

    %check
    py.test-2
    py.test-3

    or

    nosetests-%{python2_version}
    nosetests-%{python3_version}

.. include:: /snippets/check_custom_command.inc
