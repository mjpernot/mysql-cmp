#!/usr/bin/python
# Classification (U)

"""Program:  run_cmp.py

    Description:  Unit testing of run_cmp in mysql_rep_cmp.py.

    Usage:
        test/unit/mysql_rep_cmp/run_cmp.py

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
        test_multiple_tables -> Test with multiple tables in list.
        test_empty_list -> Test with empty table list.
        test_default -> Test with default arguments only.

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.master = Server()
        self.slave = Server()
        self.tbllist = ["tbl1"]
        self.tbllist2 = ["tbl1", "tbl2"]

    @mock.patch("mysql_rep_cmp.recur_tbl_cmp", mock.Mock(return_value=True))
    def test_multiple_tables(self):

        """Function:  test_multiple_tables

        Description:  Test with multiple tables in list.

        Arguments:

        """

        with gen_libs.no_std_out():
            self.assertFalse(mysql_rep_cmp.run_cmp(
                self.master, self.slave, "db1", self.tbllist2))

    @mock.patch("mysql_rep_cmp.recur_tbl_cmp", mock.Mock(return_value=True))
    def test_empty_list(self):

        """Function:  test_empty_list

        Description:  Test with empty table list.

        Arguments:

        """

        with gen_libs.no_std_out():
            self.assertFalse(mysql_rep_cmp.run_cmp(
                self.master, self.slave, "db1", []))

    @mock.patch("mysql_rep_cmp.recur_tbl_cmp", mock.Mock(return_value=True))
    def test_default(self):

        """Function:  test_run_cmp

        Description:  Test with default arguments only.

        Arguments:

        """

        with gen_libs.no_std_out():
            self.assertFalse(mysql_rep_cmp.run_cmp(
                self.master, self.slave, "db1", self.tbllist))


if __name__ == "__main__":
    unittest.main()