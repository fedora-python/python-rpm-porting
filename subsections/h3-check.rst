%check
^^^^^^

Unlike in previous sections, there's no special macro for the ``%check`` section, and so here just make sure that the tests are invoked once using the ``%{__python2}`` macro and a second time using the ``%{__python3}`` macro.

.. code-block:: spec

    %check
    %{__python2} setup.py test
    %{__python3} setup.py test
