#!/usr/bin/python
# Classification (U)

"""Program:  fetch_db_list.py

    Description:  Unit testing of fetch_db_list in mysql_rep_cmp.py.

    Usage:
        test/unit/mysql_rep_cmp/fetch_db_list.py

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
import version

__version__ = version.__version__


class Server(object):

    """Class:  Server

    Description:  Class stub holder for mysql_class.Server class.

    Methods:
        __init__
        fetch_do_db
        fetch_ign_db

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

    def fetch_do_db(self):

        """Method:  fetch_do_db

        Description:  Stub holder for mysql_class.Server.fetch_do_db method.

        Arguments:

        """

        return self.do_db

    def fetch_ign_db(self):

        """Method:  fetch_ign_db

        Description:  Stub holder for mysql_class.Server.fetch_ign_db method.

        Arguments:

        """

        return self.ign_db


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_db_name_ign_db_list2
        test_db_name_ign_db_list
        test_db_name_pass
        test_ign_db_list_pass
        test_ign_db_exist
        test_do_db_exist
        test_default

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.server = Server()
        self.databases = [{"Database": "db1"}, {"Database": "db2"}]
        self.dblist = ["db1", "db2"]
        self.dblist2 = ["db1"]
        self.dblist3 = ["db1", "db2", "db4"]
        self.dblist4 = ["db2"]
        self.ignlist = ["db2", "db3"]
        self.dolist = ["db4", "db5"]
        self.dolist2 = ["db2", "db5"]
        self.dolist3 = ["db1", "db2", "db4"]

    def test_db_name_ign_db_list2(self):

        """Function:  test_db_name_ign_db_list2

        Description:  Test with db_name and ign_db_list args.

        Arguments:

        """

        self.server.do_db = self.dblist

        self.assertEqual(
            mysql_rep_cmp.fetch_db_list(
                self.server, db_name=self.dolist3, ign_db_list=self.ignlist),
            self.dblist2)

    def test_db_name_ign_db_list(self):

        """Function:  test_db_name_ign_db_list

        Description:  Test with db_name and ign_db_list args.

        Arguments:

        """

        self.server.do_db = self.dblist

        self.assertEqual(mysql_rep_cmp.fetch_db_list(
            self.server, db_name=self.dolist2, ign_db_list=self.ignlist), [])

    def test_db_name_pass2(self):

        """Function:  test_db_name_pass2

        Description:  Test with db_name passed to function - match.

        Arguments:

        """

        self.server.do_db = self.dblist

        self.assertEqual(mysql_rep_cmp.fetch_db_list(
            self.server, db_name=self.dolist2), self.dblist4)

    def test_db_name_pass(self):

        """Function:  test_db_name_pass

        Description:  Test with db_name passed to function - no matches.

        Arguments:

        """

        self.server.do_db = self.dblist

        self.assertEqual(mysql_rep_cmp.fetch_db_list(
            self.server, db_name=self.dolist), [])

    def test_ign_db_list_pass(self):

        """Function:  test_ign_db_list_pass

        Description:  Test with ign_db_list passed to function.

        Arguments:

        """

        self.server.do_db = self.dblist

        self.assertEqual(mysql_rep_cmp.fetch_db_list(
            self.server, ign_db_list=self.ignlist), self.dblist2)

    def test_ign_db_exist(self):

        """Function:  test_ign_db_exist

        Description:  Test with ign_db attribute exists in class.

        Arguments:

        """

        self.server.do_db = self.dblist
        self.server.ign_db = self.ignlist

        self.assertEqual(mysql_rep_cmp.fetch_db_list(self.server),
                         self.dblist2)

    def test_do_db_exist(self):

        """Function:  test_do_db_exist

        Description:  Test with do_db attribute exists in class.

        Arguments:

        """

        self.server.do_db = self.dblist

        self.assertEqual(mysql_rep_cmp.fetch_db_list(self.server), self.dblist)

    @mock.patch("mysql_rep_cmp.mysql_libs.fetch_db_dict")
    def test_default(self, mock_fetch):

        """Function:  test_fetch_db_list

        Description:  Test with default arguments only.

        Arguments:

        """

        mock_fetch.return_value = self.databases

        self.assertEqual(mysql_rep_cmp.fetch_db_list(self.server), self.dblist)


if __name__ == "__main__":
    unittest.main()
