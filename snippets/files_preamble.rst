:orphan:

The presence or absence of a ``%files`` section is the deciding factor in whether a given package or subpackage gets built or not. Therefore, to assure that our base package doesn't get built (as all the content has been moved to the two subpackages), make sure there is no ``%files`` section without a subpackage name.
