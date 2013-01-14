# Copyright 2012 SUSE Linux
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from contextlib import contextmanager
import imp
import io
import unittest

import mock

ghb = imp.load_source('github_tarballs', 'github_tarballs')


class TestGitHubTarballs(unittest.TestCase):

    def test_version_parse(self):
        with mock_open(u"\nVersion: 2012.2.3+git.1355917214.0c8c2a3\n"):
            self.assertEqual('0c8c2a3',
                             ghb.get_commit_from_spec('example_pkg'))

    def test_version_parse_comment(self):
        with mock_open(
                u"\nVersion: 2012.2.3+git.1355917214.0c8c2a3 # oi comment\n"):
            self.assertEqual('0c8c2a3',
                             ghb.get_commit_from_spec('example_pkg'))

    def test_download_tarball(self):
        with mock.patch("urllib.urlretrieve") as urlretrieve:
            ghb.download_tarball('owner', 'repo', 'target', 'filename')
            self.assertEqual(
                (("https://github.com/owner/repo/archive/target.tar.gz",
                  "filename"),),
                urlretrieve.call_args)


@contextmanager
def mock_open(contents):
    with mock.patch("__builtin__.open", return_value=io.StringIO(contents)):
        yield
