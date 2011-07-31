Building translation and documentation
======================================

We have some documentation and localizations to build, if wanted. So let's do so. Feel free to skip this section if you only want to hack on your code.

Compiling translations
----------------------

To get a localized version, compile shipped translations by running::

    # On Mac/Linux
    $ scripts/compile-translations

    # On Win
    C:\pyfire> python scripts\compile-translations

Adding a new translation or updating a current one always requires this step after modifications of the raw file.

Building inline documentation
-----------------------------

We use sphinx to build our documentation so you want to have it installed

     # On Mac/Linux
     $ pip install sphinx

