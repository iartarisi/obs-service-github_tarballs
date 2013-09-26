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

from contextlib import contextmanager, nested
import imp
import io
import unittest

from mock import patch

GITHUB_API = "https://api.github.com"
ghb = imp.load_source('ghb', 'github_tarballs')


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
        with patch("urllib.urlretrieve") as urlretrieve:
            ghb.download_tarball('https://example.com/target.tar.gz',
                                 'filename')
            self.assertEqual(
                (("https://example.com/target.tar.gz",
                  "filename"),),
                urlretrieve.call_args)

    def test_get_changes(self):
        response = io.StringIO(u'{"commits": [1, 2, 3]}')
        response.code = 200
        with nested(patch("ghb.get_commit_from_spec", return_value="1234"),
                    patch("ghb.github_credentials", return_value=""),
                    patch("urllib.urlopen", return_value=response)
                    ) as (_, _, urlopen):
            self.assertEqual({'commits': [1, 2, 3]},
                             ghb.get_changes("package", "owner", "repo",
                                             "target"))
            self.assertEqual(
                ((GITHUB_API + "/repos/owner/repo/compare/1234...target",),),
                urlopen.call_args)

    def test_github_credentials_empty_file(self):
        with mock_open(u""):
            self.assertEqual("", ghb.github_credentials())

    def test_github_credentials_ioerror(self):
        with patch("__builtin__.open", side_effect=IOError):
            self.assertEqual("", ghb.github_credentials())

    def test_github_credentials_read_from_file(self):
        with mock_open(u"user:pass"):
            self.assertEqual("user:pass@", ghb.github_credentials())


@contextmanager
def mock_open(contents):
    with patch("__builtin__.open", return_value=io.StringIO(contents)):
        yield
