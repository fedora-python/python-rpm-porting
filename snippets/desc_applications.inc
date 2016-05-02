The section for applications is for software where the user doesn't care in which programming language it is written. For example, it doesn't matter if it is written in Python 2 or 3 because the application should run the same.

Applications have to have an executable, which you can check by running ``dnf repoquery -l your-package-name | grep /usr/bin/``.

If your package is not being imported by third-party projects (e.g. ``import some_module`` in a Python file), it is most likely an application.

Try running ``dnf repoquery --whatrequires your-package-name`` to see a list of packages that depend on yours. If there are none, your package is likely an application, because there would be little reason to package a module that nobody uses. However, if there are some packages that depend on yours, we cannot be sure if it's an application-only package or not, as some of these packages might be depending on your application itself, instead of importing modules from your package.
