#!/usr/bin/python
# Classification (U)

"""Program:  setup_cmp.py

    Description:  Unit testing of setup_cmp in mysql_rep_cmp.py.

    Usage:
        test/unit/mysql_rep_cmp/setup_cmp.py

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
        fetch_do_tbl -> Stub holder for mysql_class.Server.fetch_do_tbl method.
        fetch_ign_tbl -> Stub for mysql_class.Server.fetch_ign_tbl method.

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
        self.do_tbl = {}
        self.ign_tbl = {}

    def fetch_do_tbl(self):

        """Method:  fetch_do_tbl

        Description:  Stub holder for mysql_class.Server.fetch_do_tbl method.

        Arguments:

        """

        return self.do_tbl

    def fetch_ign_tbl(self):

        """Method:  fetch_ign_tbl

        Description:  Stub holder for mysql_class.Server.fetch_ign_tbl method.

        Arguments:

        """

        return self.ign_tbl


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp -> Initialize testing environment.
        test_two_dbs -> Test with two databases to check.
        test_one_db -> Test with one database to check.
        test_no_dbs -> Test with no databases from master or slave.

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.master = Server()
        self.slave = Server()
        self.databases = [{"table_name": "tbl1"}, {"table_name": "tbl2"}]
        self.databases2 = [{"table_name": "tbl3"}, {"table_name": "tbl4"}]
        self.dblist = ["db1"]
        self.dblist2 = ["db1", "db2"]

    # Remove "ign_db_tbl={}" when ign_db_tbl default value bug has been fixed.
    @mock.patch("mysql_rep_cmp.run_cmp", mock.Mock(return_value=True))
    @mock.patch("mysql_rep_cmp.mysql_libs.fetch_tbl_dict")
    @mock.patch("mysql_rep_cmp.fetch_db_list")
    def test_two_dbs(self, mock_fetch, mock_tbl):

        """Function:  test_two_dbs

        Description:  Test with two databases to check.

        Arguments:

        """

        mock_fetch.side_effect = [self.dblist2, self.dblist2]
        mock_tbl.side_effect = [self.databases, self.databases,
                                self.databases2, self.databases2]

        self.assertFalse(mysql_rep_cmp.setup_cmp(self.master, self.slave, [],
                                                 ign_db_tbl={}))

    # Remove "ign_db_tbl={}" when ign_db_tbl default value bug has been fixed.
    @mock.patch("mysql_rep_cmp.run_cmp", mock.Mock(return_value=True))
    @mock.patch("mysql_rep_cmp.mysql_libs.fetch_tbl_dict")
    @mock.patch("mysql_rep_cmp.fetch_db_list")
    def test_one_db(self, mock_fetch, mock_tbl):

        """Function:  test_master_db

        Description:  Test with one database to check.

        Arguments:

        """

        mock_fetch.side_effect = [self.dblist, self.dblist]
        mock_tbl.side_effect = [self.databases, self.databases]

        self.assertFalse(mysql_rep_cmp.setup_cmp(self.master, self.slave, [],
                                                 ign_db_tbl={}))

    @mock.patch("mysql_rep_cmp.fetch_db_list")
    def test_no_dbs(self, mock_fetch):

        """Function:  test_no_dbs

        Description:  Test with no databases from master or slave.

        Arguments:

        """

        mock_fetch.side_effect = [[], []]

        self.assertFalse(mysql_rep_cmp.setup_cmp(self.master, self.slave, []))


if __name__ == "__main__":
    unittest.main()
