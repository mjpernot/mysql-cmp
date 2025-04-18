# Classification (U)

"""Program:  get_db_tbl.py

    Description:  Unit testing of get_db_tbl in mysql_rep_cmp.py.

    Usage:
        test/unit/mysql_rep_cmp/get_db_tbl.py

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

        self.version = (8, 0)


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_remove_tbl
        test_ignore_db_tbl2
        test_ignore_db_tbl
        test_812
        test_81
        test_802
        test_80
        test_with_db_tbl2
        test_with_db_tbl
        test_with_system_db_only3
        test_with_empty_db_list
        test_with_multiple_dbs
        test_with_single_db

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.server = Server()
        self.fetch_db = [{"Database": "db1"}]
        self.fetch_db2 = [{"Database": "db1"}, {"Database": "db2"}]
        self.fetch_db3 = [{"Database": "systemdb"}]
        self.db_list = []
        self.db_list2 = ["db1"]
        self.db_list3 = ["systemdb"]
        self.db_list4 = ["systemdb", "db1"]
        self.db_list5 = ["db1", "db2"]
        self.tbl_list = ["t2"]
        self.tbl_list2 = ["t1", "t2"]
        self.tbl_dict = [{"TABLE_NAME": "t2"}]
        self.tbl_dict2 = [{"TABLE_NAME": "t1"}, {"TABLE_NAME": "t2"}]
        self.all_tbls = {"db1": ["t2"]}
        self.all_tbls2 = {"db1": ["t2"], "db2": ["t1"]}
        self.ign_dbs = ["systemdb"]

        self.tbl_dict6 = [
            {"TABLE_NAME": "tbl1"}, {"TABLE_NAME": "tbl2"},
            {"TABLE_NAME": "tbl3"}]
        self.tbl_dict8 = [
            {"TABLE_NAME": "tbl1"}, {"TABLE_NAME": "tbl2"}]
        self.ign_db_tbl6 = {"db1": ["tbl1", "tbl3"]}
        self.ign_db_tbl7 = {"db2": ["tbl1", "tbl3"]}
        self.tbl_list6 = ["tbl1", "tbl2", "tbl3"]
        self.results6 = {"db1": ["tbl2"]}
        self.results7 = {"db1": ["tbl1", "tbl2", "tbl3"]}
        self.results8 = {"db1": ["tbl1", "tbl2"]}

        self.results = {"db1": ["t2"]}
        self.results2 = {"db1": ["t2"], "db2": ["t1"]}
        self.results3 = {}
        self.results4 = {"db1": ["t1", "t2"]}

    @mock.patch("mysql_rep_cmp.mysql_libs.fetch_tbl_dict")
    def test_remove_tbl(self, mock_fetch):

        """Function:  test_remove_tbl

        Description:  Test with remove tables passed that are not in the
            database.

        Arguments:

        """

        mock_fetch.return_value = self.tbl_dict8

        self.assertEqual(
            mysql_rep_cmp.get_db_tbl(
                self.server, self.db_list2, ign_dbs=self.ign_dbs,
                tbls=self.tbl_list6, ign_db_tbl=self.ign_db_tbl7),
            self.results8)

    @mock.patch("mysql_rep_cmp.mysql_libs.fetch_tbl_dict")
    def test_ignore_db_tbl2(self, mock_fetch):

        """Function:  test_ignore_db_tbl2

        Description:  Test with ignoring some tables, but not in same database.

        Arguments:

        """

        mock_fetch.return_value = self.tbl_dict6

        self.assertEqual(
            mysql_rep_cmp.get_db_tbl(
                self.server, self.db_list2, ign_dbs=self.ign_dbs,
                tbls=self.tbl_list6, ign_db_tbl=self.ign_db_tbl7),
            self.results7)

    @mock.patch("mysql_rep_cmp.mysql_libs.fetch_tbl_dict")
    def test_ignore_db_tbl(self, mock_fetch):

        """Function:  test_ignore_db_tbl

        Description:  Test with ignoring some tables.

        Arguments:

        """

        mock_fetch.return_value = self.tbl_dict6

        self.assertEqual(
            mysql_rep_cmp.get_db_tbl(
                self.server, self.db_list2, ign_dbs=self.ign_dbs,
                tbls=self.tbl_list6, ign_db_tbl=self.ign_db_tbl6),
            self.results6)

    @mock.patch("mysql_rep_cmp.mysql_libs.fetch_tbl_dict")
    def test_812(self, mock_fetch):

        """Function:  test_812

        Description:  Test in 8.1 version.

        Arguments:

        """

        mock_fetch.return_value = self.tbl_dict2

        self.assertEqual(
            mysql_rep_cmp.get_db_tbl(
                self.server, self.db_list2, ign_dbs=self.ign_dbs,
                tbls=self.tbl_list2),
            self.results4)

    @mock.patch("mysql_rep_cmp.mysql_libs.fetch_tbl_dict")
    def test_81(self, mock_fetch):

        """Function:  test_81

        Description:  Test in 8.1 version.

        Arguments:

        """

        mock_fetch.return_value = self.tbl_dict2

        self.assertEqual(
            mysql_rep_cmp.get_db_tbl(
                self.server, self.db_list2, ign_dbs=self.ign_dbs,
                tbls=self.tbl_list),
            self.results)

    @mock.patch("mysql_rep_cmp.mysql_libs.fetch_tbl_dict")
    def test_802(self, mock_fetch):

        """Function:  test_802

        Description:  Test in 8.0 version.

        Arguments:

        """

        mock_fetch.return_value = self.tbl_dict2

        self.assertEqual(
            mysql_rep_cmp.get_db_tbl(
                self.server, self.db_list2, ign_dbs=self.ign_dbs,
                tbls=self.tbl_list2),
            self.results4)

    @mock.patch("mysql_rep_cmp.mysql_libs.fetch_tbl_dict")
    def test_80(self, mock_fetch):

        """Function:  test_80

        Description:  Test in 8.0 version.

        Arguments:

        """

        mock_fetch.return_value = self.tbl_dict2

        self.assertEqual(
            mysql_rep_cmp.get_db_tbl(
                self.server, self.db_list2, ign_dbs=self.ign_dbs,
                tbls=self.tbl_list),
            self.results)

    @mock.patch("mysql_rep_cmp.mysql_libs.fetch_tbl_dict")
    def test_with_db_tbl2(self, mock_fetch):

        """Function:  test_with_db_tbl2

        Description:  Test with database and tables.

        Arguments:

        """

        mock_fetch.return_value = self.tbl_dict2

        self.assertEqual(
            mysql_rep_cmp.get_db_tbl(
                self.server, self.db_list2, ign_dbs=self.ign_dbs,
                tbls=self.tbl_list2),
            self.results4)

    @mock.patch("mysql_rep_cmp.mysql_libs.fetch_tbl_dict")
    def test_with_db_tbl(self, mock_fetch):

        """Function:  test_with_db_tbl

        Description:  Test with database and table.

        Arguments:

        """

        mock_fetch.return_value = self.tbl_dict2

        self.assertEqual(
            mysql_rep_cmp.get_db_tbl(
                self.server, self.db_list2, ign_dbs=self.ign_dbs,
                tbls=self.tbl_list),
            self.results)

    @mock.patch("mysql_rep_cmp.get_all_dbs_tbls")
    @mock.patch("mysql_rep_cmp.mysql_libs.fetch_db_dict")
    def test_with_system_db_only3(self, mock_fetch, mock_all):

        """Function:  test_with_system_db_only3

        Description:  Test with system and user database list.

        Arguments:

        """

        mock_fetch.return_value = self.fetch_db3
        mock_all.return_value = self.all_tbls

        self.assertEqual(
            mysql_rep_cmp.get_db_tbl(
                self.server, self.db_list4, ign_dbs=self.ign_dbs),
            self.results)

    @mock.patch("mysql_rep_cmp.get_all_dbs_tbls")
    @mock.patch("mysql_rep_cmp.mysql_libs.fetch_db_dict")
    def test_with_empty_db_list(self, mock_fetch, mock_all):

        """Function:  test_with_empty_db_list

        Description:  Test with empty database list.

        Arguments:

        """

        mock_fetch.return_value = self.fetch_db
        mock_all.return_value = self.all_tbls2

        self.assertEqual(
            mysql_rep_cmp.get_db_tbl(
                self.server, self.db_list), self.results2)

    @mock.patch("mysql_rep_cmp.get_all_dbs_tbls")
    def test_with_multiple_dbs(self, mock_all):

        """Function:  test_with_multiple_dbs

        Description:  Test with multiple databases.

        Arguments:

        """

        mock_all.return_value = self.all_tbls2

        self.assertEqual(
            mysql_rep_cmp.get_db_tbl(
                self.server, self.db_list5), self.results2)

    @mock.patch("mysql_rep_cmp.get_all_dbs_tbls")
    def test_with_single_db(self, mock_all):

        """Function:  test_with_single_db

        Description:  Test with single database and get all tables in database.

        Arguments:

        """

        mock_all.return_value = self.all_tbls

        self.assertEqual(
            mysql_rep_cmp.get_db_tbl(self.server, self.db_list2), self.results)


if __name__ == "__main__":
    unittest.main()
