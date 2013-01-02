=========================================
 OBS service for downloading git tarballs
=========================================

This is an `Open Build Service`_ source service. It downloads a tarball from a remote URL and updates the ``.spec`` and ``.changes`` files with git commit information from the `github API`_.

The ``github_tarballs`` service will also change the specfile's
``Source:`` to the ``filename`` argument of the service and the ``%setup
-q`` line to match the parent folder name in the tarball.

Requires argparse which is part of python2.7, but available as a third-party dependency in python2.6.


TODO:

* use current user's email address in .changes file
* tests


.. _Open Build Service: http://openbuildservice.org/
.. _github API: http://api.github.com/
