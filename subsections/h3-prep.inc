%prep
^^^^^

The ``%prep`` section most likely already exists in your spec file and contains either the ``%setup`` macro, optionally followed by the ``%patchX`` macros (where ``X`` is a number) that apply patches, or it contains the ``%autesetup`` macro that applies any listed patches automatically. (Patches are listed with the ``Source0``, ``Source1``, ... tags).

If you find that some patches are being applied that are clearly only intended for Python 2 version of the application, you can try removing them. Otherwise, leave the macros as they are.
