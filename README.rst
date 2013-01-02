=========================================
 OBS service for downloading git tarballs
=========================================

This is an `Open Build Service`_ source service. It downloads a tarball from a remote URL and updates the ``.spec`` and ``.changes`` files with git commit information from the `github API`_.

The ``github_tarballs`` service will also change the specfile's
``Source:`` to the ``filename`` argument of the service and the ``%setup
-q`` line to match the parent folder name in the tarball.

On the first run, ``github_tarballs`` will just set the spec file's ``Version`` field to the latest git commit. The .changes file will only be updated with commit message information when newer commits (compared to the one now set in ``Version``) are found.

Requires argparse which is part of python2.7, but available as a third-party dependency in python2.6.


TODO:

* use current user's email address in .changes file
* tests


.. _Open Build Service: http://openbuildservice.org/
.. _github API: http://api.github.com/
