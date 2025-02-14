# Classification (U)

"""Program:  get_all_dbs_tbls.py

    Description:  Unit testing of get_all_dbs_tbls in mysql_rep_cmp.py.

    Usage:
        test/unit/mysql_rep_cmp/get_all_dbs_tbls.py

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
import mysql_rep_cmp                            # pylint:disable=E0401,C0413
import version                                  # pylint:disable=E0401,C0413

__version__ = version.__version__


class Server():                                         # pylint:disable=R0903

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


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_ignore_tbls_multiple_dbs4
        test_ignore_tbls_multiple_dbs3
        test_ignore_tbls_multiple_dbs2
        test_ignore_tbls_multiple_dbs
        test_ignore_tbls2
        test_ignore_tbls
        test_multiple_dbs
        test_one_db

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.server = Server()
        self.dict_key = "TABLE_NAME"
        self.db_list = ["db1"]
        self.db_list2 = ["db1", "db2"]
        self.tbl_dict = [{"TABLE_NAME": "t2"}]
        self.tbl_dict2 = [{"TABLE_NAME": "t1"}, {"TABLE_NAME": "t2"}]
        self.tbl_list = ["t2"]
        self.tbl_list2 = ["t1", "t2"]
        self.ign_db_tbl = {"db1": ["t1"]}
        self.ign_db_tbl2 = {"db1": ["t2"]}
        self.ign_db_tbl3 = {"db2": ["t2"]}
        self.ign_db_tbl4 = {"db1": ["t2"], "db2": ["t2"]}
        self.results = {"db1": ["t2"]}
        self.results2 = {"db1": ["t2"], "db2": ["t1", "t2"]}
        self.results3 = {"db1": []}
        self.results4 = {"db1": [], "db2": ["t1", "t2"]}
        self.results5 = {"db1": ["t2"], "db2": ["t1"]}
        self.results6 = {"db1": [], "db2": ["t1"]}

    @mock.patch("mysql_rep_cmp.mysql_libs.fetch_tbl_dict")
    def test_ignore_tbls_multiple_dbs4(self, mock_fetch):

        """Function:  test_ignore_tbls_multiple_dbs4

        Description:  Test with ignore tables in multiple databases.

        Arguments:

        """

        mock_fetch.side_effect = [self.tbl_dict, self.tbl_dict2]

        self.assertEqual(
            mysql_rep_cmp.get_all_dbs_tbls(
                self.server, self.db_list2, self.dict_key,
                ign_db_tbl=self.ign_db_tbl4), self.results6)

    @mock.patch("mysql_rep_cmp.mysql_libs.fetch_tbl_dict")
    def test_ignore_tbls_multiple_dbs3(self, mock_fetch):

        """Function:  test_ignore_tbls_multiple_dbs3

        Description:  Test with ignore tables in multiple databases.

        Arguments:

        """

        mock_fetch.side_effect = [self.tbl_dict, self.tbl_dict2]

        self.assertEqual(
            mysql_rep_cmp.get_all_dbs_tbls(
                self.server, self.db_list2, self.dict_key,
                ign_db_tbl=self.ign_db_tbl3), self.results5)

    @mock.patch("mysql_rep_cmp.mysql_libs.fetch_tbl_dict")
    def test_ignore_tbls_multiple_dbs2(self, mock_fetch):

        """Function:  test_ignore_tbls_multiple_dbs2

        Description:  Test with ignore tables in multiple databases.

        Arguments:

        """

        mock_fetch.side_effect = [self.tbl_dict, self.tbl_dict2]

        self.assertEqual(
            mysql_rep_cmp.get_all_dbs_tbls(
                self.server, self.db_list2, self.dict_key,
                ign_db_tbl=self.ign_db_tbl2), self.results4)

    @mock.patch("mysql_rep_cmp.mysql_libs.fetch_tbl_dict")
    def test_ignore_tbls_multiple_dbs(self, mock_fetch):

        """Function:  test_ignore_tbls_multiple_dbs

        Description:  Test with ignore tables in multiple databases.

        Arguments:

        """

        mock_fetch.side_effect = [self.tbl_dict, self.tbl_dict2]

        self.assertEqual(
            mysql_rep_cmp.get_all_dbs_tbls(
                self.server, self.db_list2, self.dict_key,
                ign_db_tbl=self.ign_db_tbl), self.results2)

    @mock.patch("mysql_rep_cmp.mysql_libs.fetch_tbl_dict")
    def test_ignore_tbls2(self, mock_fetch):

        """Function:  test_ignore_tbls2

        Description:  Test with ignoring tables in a database.

        Arguments:

        """

        mock_fetch.return_value = self.tbl_dict

        self.assertEqual(
            mysql_rep_cmp.get_all_dbs_tbls(
                self.server, self.db_list, self.dict_key,
                ign_db_tbl=self.ign_db_tbl2), self.results3)

    @mock.patch("mysql_rep_cmp.mysql_libs.fetch_tbl_dict")
    def test_ignore_tbls(self, mock_fetch):

        """Function:  test_ignore_tbls

        Description:  Test with ignoring tables in a database.

        Arguments:

        """

        mock_fetch.return_value = self.tbl_dict

        self.assertEqual(
            mysql_rep_cmp.get_all_dbs_tbls(
                self.server, self.db_list, self.dict_key,
                ign_db_tbl=self.ign_db_tbl), self.results)

    @mock.patch("mysql_rep_cmp.mysql_libs.fetch_tbl_dict")
    def test_multiple_dbs(self, mock_fetch):

        """Function:  test_multiple_dbs

        Description:  Test with multiple databases.

        Arguments:

        """

        mock_fetch.side_effect = [self.tbl_dict, self.tbl_dict2]

        self.assertEqual(
            mysql_rep_cmp.get_all_dbs_tbls(
                self.server, self.db_list2, self.dict_key), self.results2)

    @mock.patch("mysql_rep_cmp.mysql_libs.fetch_tbl_dict")
    def test_one_db(self, mock_fetch):

        """Function:  test_one_db

        Description:  Test with one database.

        Arguments:

        """

        mock_fetch.return_value = self.tbl_dict

        self.assertEqual(
            mysql_rep_cmp.get_all_dbs_tbls(
                self.server, self.db_list, self.dict_key), self.results)


if __name__ == "__main__":
    unittest.main()
