#!/usr/bin/python
# Classification (U)

"""Program:  recur_tbl_cmp.py

    Description:  Unit testing of recur_tbl_cmp in mysql_rep_cmp.py.

    Usage:
        test/unit/mysql_rep_cmp/recur_tbl_cmp.py

    Arguments:

"""

# Libraries and Global Variables

# Standard
import sys
import os

if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest

# Third-party
import mock

# Local
sys.path.append(os.getcwd())
import mysql_rep_cmp
import lib.gen_libs as gen_libs
import version

__version__ = version.__version__


class Server(object):

    """Class:  Server

    Description:  Class stub holder for mysql_class.Server class.

    Methods:
        __init__ -> Class initialization.

    """

    def __init__(self):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:

        """

        self.extra_def_file = None
        self.sql_user = "mysql"
        self.host = "hostname"
        self.port = 3306
        self.do_db = None
        self.ign_db = None


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp -> Initialize testing environment.
        test_reached_max -> Test with reaching max checks.
        test_check_once -> Test with checksumming at once.
        test_default -> Test with default arguments only.

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.master = Server()
        self.slave = Server()

    @mock.patch("mysql_rep_cmp.mysql_libs.checksum")
    def test_reached_max(self, mock_checksum):

        """Function:  test_reached_max

        Description:  Test with reaching max checks.

        Arguments:

        """

        mock_checksum.side_effect = [10, 11, 10, 11]

        with gen_libs.no_std_out():
            self.assertFalse(mysql_rep_cmp.recur_tbl_cmp(
                self.master, self.slave, "db1", "tbl1", 3))

    @mock.patch("mysql_rep_cmp.mysql_libs.checksum")
    def test_check_once(self, mock_checksum):

        """Function:  test_check_once

        Description:  Test with checksumming at once.

        Arguments:

        """

        mock_checksum.side_effect = [10, 11, 10, 10]

        with gen_libs.no_std_out():
            self.assertFalse(mysql_rep_cmp.recur_tbl_cmp(
                self.master, self.slave, "db1", "tbl1", 1))

    @mock.patch("mysql_rep_cmp.mysql_libs.checksum")
    def test_default(self, mock_checksum):

        """Function:  test_recur_tbl_cmp

        Description:  Test with default arguments only.

        Arguments:

        """

        mock_checksum.side_effect = [10, 10]

        with gen_libs.no_std_out():
            self.assertFalse(mysql_rep_cmp.recur_tbl_cmp(
                self.master, self.slave, "db1", "tbl1", 1))


if __name__ == "__main__":
    unittest.main()
