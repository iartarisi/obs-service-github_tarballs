========================================================================
 OBS service for downloading tarballs and commit information from github
========================================================================

This is an `Open Build Service`_ source service. It downloads a tarball
from a remote URL and updates the ``.spec`` and ``.changes`` files with
git commit information from the `github API`_.

How It Works
------------

The ``Version`` field will be set to ``%(tarball_version)s+git.%(timestamp)s.%(commit_sha)s``. Where ``tarball_version`` is the version as read from the parent directory inside the downloaded tarball - everything after the last dash (``-``) in the directory's name. ``timestamp`` is the current seconds from the UNIX epoch when the source service was run. ``commit_sha`` is the latest commit sha hash from the git repository.

On the first run, ``github_tarballs`` will just set the spec file's
``Version`` field to the latest git commit. The .changes file will only
be updated with commit message information when newer commits (compared
to the one now set in ``Version``) are found.

The ``github_tarballs`` service will also change the specfile's
``Source:`` to the ``filename`` argument of the service and the ``%setup
-q`` line to match the parent folder name in the tarball.

Rate Limiting
-------------

The github API rate limits requests. The limit can be extended by using github credentials to access the API. ``obs-service-github_tarballs`` will read and use these credentials from the ``.github_tarballs_credentials`` file in the current user's home directory if it can. The file should contain one line with the standard in standard HTTP BasicAuth format ``username:password``.

Dependencies
------------

Requires argparse which is part of python2.7, but available as a
third-party dependency in python2.6.

The tests require `python-mock`_. To run them, just use ``nosetests`` or ``python -m unittest discover`` (on python2.7).


.. _Open Build Service: http://openbuildservice.org/
.. _github API: http://api.github.com/
.. _python-mock: http://www.voidspace.org.uk/python/mock/mock.html
