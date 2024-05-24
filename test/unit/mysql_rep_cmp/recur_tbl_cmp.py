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
import unittest
import mock

# Local
sys.path.append(os.getcwd())
import mysql_rep_cmp
import version

__version__ = version.__version__


class Server(object):

    """Class:  Server

    Description:  Class stub holder for mysql_class.Server class.

    Methods:
        __init__

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
        setUp
        test_no_recur
        test_reached_max
        test_check_once
        test_default

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.master = Server()
        self.slave = Server()
        self.tbl = "tbl1"
        self.status = "Synced"
        self.status2 = "Checksums do not match"

    @mock.patch("mysql_rep_cmp.mysql_libs.checksum")
    def test_no_recur(self, mock_checksum):

        """Function:  test_no_recur

        Description:  Test with no recur parameter set.

        Arguments:

        """

        mock_checksum.side_effect = [10, 10]

        self.assertEqual(
            mysql_rep_cmp.recur_tbl_cmp(
                self.master, self.slave, "db1", "tbl1"), self.status)

    @mock.patch("mysql_rep_cmp.time.sleep", mock.Mock(return_value=True))
    @mock.patch("mysql_rep_cmp.mysql_libs.checksum")
    def test_reached_max(self, mock_checksum):

        """Function:  test_reached_max

        Description:  Test with reaching max checks.

        Arguments:

        """

        mock_checksum.side_effect = [10, 11, 10, 11]

        self.assertEqual(
            mysql_rep_cmp.recur_tbl_cmp(
                self.master, self.slave, "db1", "tbl1", 3), self.status2)

    @mock.patch("mysql_rep_cmp.time.sleep", mock.Mock(return_value=True))
    @mock.patch("mysql_rep_cmp.mysql_libs.checksum")
    def test_check_once(self, mock_checksum):

        """Function:  test_check_once

        Description:  Test with checksumming at once.

        Arguments:

        """

        mock_checksum.side_effect = [10, 11, 10, 10]

        self.assertEqual(
            mysql_rep_cmp.recur_tbl_cmp(
                self.master, self.slave, "db1", "tbl1", 1), self.status)

    @mock.patch("mysql_rep_cmp.mysql_libs.checksum")
    def test_default(self, mock_checksum):

        """Function:  test_default

        Description:  Test with default arguments only.

        Arguments:

        """

        mock_checksum.side_effect = [10, 10]

        self.assertEqual(
            mysql_rep_cmp.recur_tbl_cmp(
                self.master, self.slave, "db1", "tbl1", 1), self.status)


if __name__ == "__main__":
    unittest.main()
