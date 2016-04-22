:orphan:

.. _description-subsection:

%description
************

Each subpackage also needs to contain its own description. However, unlike the ``Summary:`` and ``Requires:`` tags, which are automatically applied to the subpackage declared above them, the ``%description`` macro needs to be told to which subpackage it belongs. You can do that by appending the same name as you did with the ``%package`` macro itself.

.. code-block:: spec

    %description -n python3-%{srcname}
    A Python tool which provides a convenient example.

