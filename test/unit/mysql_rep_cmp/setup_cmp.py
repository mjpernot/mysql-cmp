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
import version

__version__ = version.__version__


class Mail(object):

    """Class:  Mail

    Description:  Class stub holder for gen_class.Mail class.

    Methods:
        __init__
        send_mail

    """

    def __init__(self):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:

        """

        self.data = None

    def send_mail(self, use_mailx=False):

        """Method:  send_mail

        Description:  Stub method holder for Mail.send_mail.

        Arguments:
            (input) use_mailx

        """

        status = True

        if use_mailx:
            status = True

        return status


class Server(object):

    """Class:  Server

    Description:  Class stub holder for mysql_class.Server class.

    Methods:
        __init__
        fetch_do_tbl
        fetch_ign_tbl

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
        setUp
        test_mysql_80
        test_pre_mysql_80
        test_no_std_out
        test_email_mailx2
        test_email_mailx
        test_email
        test_tbl_name
        test_db_name
        test_sys_ign_db
        test_ign_db_tbls
        test_ign_tbls
        test_do_tbls2
        test_do_tbls
        test_no_matches
        test_two_dbs
        test_one_db
        test_no_dbs

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.master = Server()
        self.slave = Server()
        self.mail = Mail()
        self.databases = [{"table_name": "tbl1"}, {"table_name": "tbl2"}]
        self.databases2 = [{"table_name": "tbl3"}, {"table_name": "tbl4"}]
        self.databases3 = [{"TABLE_NAME": "tbl1"}, {"TABLE_NAME": "tbl2"}]
        self.databases4 = [{"TABLE_NAME": "tbl3"}, {"TABLE_NAME": "tbl4"}]
        self.dblist = ["db1"]
        self.dblist2 = ["db1", "db2"]
        self.dblist3 = ["db3", "db4"]
        self.ign_db_tbl = {"db1": ["tbl1"]}
        self.sys_ign_db = ["performance_schema", "information_schema"]
        self.tbllist = ["tbl1"]
        self.no_std = True
        self.version = {"version": "5.7"}
        self.version2 = {"version": "8.0"}

    @mock.patch("mysql_rep_cmp.run_cmp", mock.Mock(return_value=True))
    @mock.patch("mysql_rep_cmp.mysql_class.fetch_sys_var")
    @mock.patch("mysql_rep_cmp.mysql_libs.fetch_tbl_dict")
    @mock.patch("mysql_rep_cmp.fetch_db_list")
    def test_mysql_80(self, mock_fetch, mock_tbl, mock_version):

        """Function:  test_mysql_80

        Description:  Test with MySQL 8.0 version database.

        Arguments:

        """

        self.slave.ign_tbl = {"db1": ["tbl1", "tbl2"]}

        mock_version.return_value = self.version2
        mock_fetch.side_effect = [self.dblist2, self.dblist2]
        mock_tbl.side_effect = [self.databases3, self.databases3,
                                self.databases4, self.databases4]

        self.assertFalse(mysql_rep_cmp.setup_cmp(
            self.master, self.slave, self.sys_ign_db, db_name=self.dblist,
            no_std=self.no_std))

    @mock.patch("mysql_rep_cmp.run_cmp", mock.Mock(return_value=True))
    @mock.patch("mysql_rep_cmp.mysql_class.fetch_sys_var")
    @mock.patch("mysql_rep_cmp.mysql_libs.fetch_tbl_dict")
    @mock.patch("mysql_rep_cmp.fetch_db_list")
    def test_pre_mysql_80(self, mock_fetch, mock_tbl, mock_version):

        """Function:  test_pre_mysql_80

        Description:  Test with pre MySQL 8.0 version database.

        Arguments:

        """

        self.slave.ign_tbl = {"db1": ["tbl1", "tbl2"]}

        mock_version.return_value = self.version
        mock_fetch.side_effect = [self.dblist2, self.dblist2]
        mock_tbl.side_effect = [self.databases, self.databases,
                                self.databases2, self.databases2]

        self.assertFalse(mysql_rep_cmp.setup_cmp(
            self.master, self.slave, self.sys_ign_db, db_name=self.dblist,
            no_std=self.no_std))

    @mock.patch("mysql_rep_cmp.run_cmp", mock.Mock(return_value=True))
    @mock.patch("mysql_rep_cmp.mysql_class.fetch_sys_var")
    @mock.patch("mysql_rep_cmp.mysql_libs.fetch_tbl_dict")
    @mock.patch("mysql_rep_cmp.fetch_db_list")
    def test_no_std_out(self, mock_fetch, mock_tbl, mock_version):

        """Function:  test_no_std_out

        Description:  Test with passing no standard out suppression.

        Arguments:

        """

        self.slave.ign_tbl = {"db1": ["tbl1", "tbl2"]}

        mock_version.return_value = self.version
        mock_fetch.side_effect = [self.dblist2, self.dblist2]
        mock_tbl.side_effect = [self.databases, self.databases,
                                self.databases2, self.databases2]

        self.assertFalse(mysql_rep_cmp.setup_cmp(
            self.master, self.slave, self.sys_ign_db, db_name=self.dblist,
            no_std=self.no_std))

    @mock.patch("mysql_rep_cmp.run_cmp", mock.Mock(return_value=True))
    @mock.patch("mysql_rep_cmp.mysql_class.fetch_sys_var")
    @mock.patch("mysql_rep_cmp.mysql_libs.fetch_tbl_dict")
    @mock.patch("mysql_rep_cmp.fetch_db_list")
    def test_email_mailx2(self, mock_fetch, mock_tbl, mock_version):

        """Function:  test_email_mailx2

        Description:  Test with email using use_mailx option.

        Arguments:

        """

        self.slave.ign_tbl = {"db1": ["tbl1", "tbl2"]}

        mock_version.return_value = self.version
        mock_fetch.side_effect = [self.dblist2, self.dblist2]
        mock_tbl.side_effect = [self.databases, self.databases,
                                self.databases2, self.databases2]

        self.assertFalse(mysql_rep_cmp.setup_cmp(
            self.master, self.slave, self.sys_ign_db, db_name=self.dblist,
            mail=self.mail, use_mailx=True))

    @mock.patch("mysql_rep_cmp.run_cmp", mock.Mock(return_value=True))
    @mock.patch("mysql_rep_cmp.mysql_class.fetch_sys_var")
    @mock.patch("mysql_rep_cmp.mysql_libs.fetch_tbl_dict")
    @mock.patch("mysql_rep_cmp.fetch_db_list")
    def test_email_mailx(self, mock_fetch, mock_tbl, mock_version):

        """Function:  test_email_mailx

        Description:  Test with email using use_mailx option.

        Arguments:

        """

        self.slave.ign_tbl = {"db1": ["tbl1", "tbl2"]}

        mock_version.return_value = self.version
        mock_fetch.side_effect = [self.dblist2, self.dblist2]
        mock_tbl.side_effect = [self.databases, self.databases,
                                self.databases2, self.databases2]

        self.assertFalse(mysql_rep_cmp.setup_cmp(
            self.master, self.slave, self.sys_ign_db, db_name=self.dblist,
            mail=self.mail, use_mailx=False))

    @mock.patch("mysql_rep_cmp.run_cmp", mock.Mock(return_value=True))
    @mock.patch("mysql_rep_cmp.mysql_class.fetch_sys_var")
    @mock.patch("mysql_rep_cmp.mysql_libs.fetch_tbl_dict")
    @mock.patch("mysql_rep_cmp.fetch_db_list")
    def test_email(self, mock_fetch, mock_tbl, mock_version):

        """Function:  test_email

        Description:  Test with email is passed.

        Arguments:

        """

        self.slave.ign_tbl = {"db1": ["tbl1", "tbl2"]}

        mock_version.return_value = self.version
        mock_fetch.side_effect = [self.dblist2, self.dblist2]
        mock_tbl.side_effect = [self.databases, self.databases,
                                self.databases2, self.databases2]

        self.assertFalse(mysql_rep_cmp.setup_cmp(
            self.master, self.slave, self.sys_ign_db, db_name=self.dblist,
            mail=self.mail))

    @mock.patch("mysql_rep_cmp.run_cmp", mock.Mock(return_value=True))
    @mock.patch("mysql_rep_cmp.mysql_class.fetch_sys_var")
    @mock.patch("mysql_rep_cmp.mysql_libs.fetch_tbl_dict")
    @mock.patch("mysql_rep_cmp.fetch_db_list")
    def test_tbl_name(self, mock_fetch, mock_tbl, mock_version):

        """Function:  test_tbl_name

        Description:  Test with tbl_name is passed.

        Arguments:

        """

        self.slave.ign_tbl = {"db1": ["tbl1", "tbl2"]}

        mock_version.return_value = self.version
        mock_fetch.side_effect = [self.dblist2, self.dblist2]
        mock_tbl.side_effect = [self.databases, self.databases,
                                self.databases2, self.databases2]

        self.assertFalse(mysql_rep_cmp.setup_cmp(
            self.master, self.slave, self.sys_ign_db, tbl_name=self.tbllist))

    @mock.patch("mysql_rep_cmp.run_cmp", mock.Mock(return_value=True))
    @mock.patch("mysql_rep_cmp.mysql_class.fetch_sys_var")
    @mock.patch("mysql_rep_cmp.mysql_libs.fetch_tbl_dict")
    @mock.patch("mysql_rep_cmp.fetch_db_list")
    def test_db_name(self, mock_fetch, mock_tbl, mock_version):

        """Function:  test_db_name

        Description:  Test with db_name is passed.

        Arguments:

        """

        self.slave.ign_tbl = {"db1": ["tbl1", "tbl2"]}

        mock_version.return_value = self.version
        mock_fetch.side_effect = [self.dblist2, self.dblist2]
        mock_tbl.side_effect = [self.databases, self.databases,
                                self.databases2, self.databases2]

        self.assertFalse(mysql_rep_cmp.setup_cmp(
            self.master, self.slave, self.sys_ign_db, db_name=self.dblist))

    @mock.patch("mysql_rep_cmp.run_cmp", mock.Mock(return_value=True))
    @mock.patch("mysql_rep_cmp.mysql_class.fetch_sys_var")
    @mock.patch("mysql_rep_cmp.mysql_libs.fetch_tbl_dict")
    @mock.patch("mysql_rep_cmp.fetch_db_list")
    def test_sys_ign_db(self, mock_fetch, mock_tbl, mock_version):

        """Function:  test_sys_ign_db

        Description:  Test with sys_ign_db is passed.

        Arguments:

        """

        self.slave.ign_tbl = {"db1": ["tbl1", "tbl2"]}

        mock_version.return_value = self.version
        mock_fetch.side_effect = [self.dblist2, self.dblist2]
        mock_tbl.side_effect = [self.databases, self.databases,
                                self.databases2, self.databases2]

        self.assertFalse(mysql_rep_cmp.setup_cmp(self.master, self.slave,
                                                 self.sys_ign_db))

    @mock.patch("mysql_rep_cmp.run_cmp", mock.Mock(return_value=True))
    @mock.patch("mysql_rep_cmp.mysql_class.fetch_sys_var")
    @mock.patch("mysql_rep_cmp.mysql_libs.fetch_tbl_dict")
    @mock.patch("mysql_rep_cmp.fetch_db_list")
    def test_ign_db_tbls(self, mock_fetch, mock_tbl, mock_version):

        """Function:  test_ign_db_tbls

        Description:  Test with ign_db_tbl parameter passed.

        Arguments:

        """

        self.slave.ign_tbl = {"db1": ["tbl1", "tbl2"]}

        mock_version.return_value = self.version
        mock_fetch.side_effect = [self.dblist2, self.dblist2]
        mock_tbl.side_effect = [self.databases, self.databases,
                                self.databases2, self.databases2]

        self.assertFalse(mysql_rep_cmp.setup_cmp(self.master, self.slave, [],
                                                 ign_db_tbl=self.ign_db_tbl))

    @mock.patch("mysql_rep_cmp.run_cmp", mock.Mock(return_value=True))
    @mock.patch("mysql_rep_cmp.mysql_class.fetch_sys_var")
    @mock.patch("mysql_rep_cmp.mysql_libs.fetch_tbl_dict")
    @mock.patch("mysql_rep_cmp.fetch_db_list")
    def test_ign_tbls(self, mock_fetch, mock_tbl, mock_version):

        """Function:  test_ign_tbls

        Description:  Test with slave ignore tables found.

        Arguments:

        """

        self.slave.ign_tbl = {"db1": ["tbl1", "tbl2"]}

        mock_version.return_value = self.version
        mock_fetch.side_effect = [self.dblist2, self.dblist2]
        mock_tbl.side_effect = [self.databases, self.databases,
                                self.databases2, self.databases2]

        self.assertFalse(mysql_rep_cmp.setup_cmp(self.master, self.slave, []))

    @mock.patch("mysql_rep_cmp.run_cmp", mock.Mock(return_value=True))
    @mock.patch("mysql_rep_cmp.mysql_class.fetch_sys_var")
    @mock.patch("mysql_rep_cmp.mysql_libs.fetch_tbl_dict")
    @mock.patch("mysql_rep_cmp.fetch_db_list")
    def test_do_tbls2(self, mock_fetch, mock_tbl, mock_version):

        """Function:  test_do_tbls2

        Description:  Test with slave do tables found.

        Arguments:

        """

        self.slave.do_tbl = {"db1": ["tbl1", "tbl2"]}

        mock_version.return_value = self.version
        mock_fetch.side_effect = [self.dblist2, self.dblist2]
        mock_tbl.side_effect = [self.databases,
                                self.databases2, self.databases2]

        self.assertFalse(mysql_rep_cmp.setup_cmp(self.master, self.slave, []))

    @mock.patch("mysql_rep_cmp.run_cmp", mock.Mock(return_value=True))
    @mock.patch("mysql_rep_cmp.mysql_class.fetch_sys_var")
    @mock.patch("mysql_rep_cmp.mysql_libs.fetch_tbl_dict")
    @mock.patch("mysql_rep_cmp.fetch_db_list")
    def test_do_tbls(self, mock_fetch, mock_tbl, mock_version):

        """Function:  test_do_tbls

        Description:  Test with slave do tables found.

        Arguments:

        """

        self.slave.do_tbl = {"db1": ["tbl1", "tbl2"], "db2": ["tbl3"]}

        mock_version.return_value = self.version
        mock_fetch.side_effect = [self.dblist2, self.dblist2]
        mock_tbl.side_effect = [self.databases, self.databases2]

        self.assertFalse(mysql_rep_cmp.setup_cmp(self.master, self.slave, []))

    @mock.patch("mysql_rep_cmp.mysql_class.fetch_sys_var")
    @mock.patch("mysql_rep_cmp.fetch_db_list")
    def test_no_matches(self, mock_fetch, mock_version):

        """Function:  test_no_matches

        Description:  Test with no matches between master and slave.

        Arguments:

        """

        mock_version.return_value = self.version
        mock_fetch.side_effect = [self.dblist2, self.dblist3]

        self.assertFalse(mysql_rep_cmp.setup_cmp(self.master, self.slave, []))

    @mock.patch("mysql_rep_cmp.run_cmp", mock.Mock(return_value=True))
    @mock.patch("mysql_rep_cmp.mysql_class.fetch_sys_var")
    @mock.patch("mysql_rep_cmp.mysql_libs.fetch_tbl_dict")
    @mock.patch("mysql_rep_cmp.fetch_db_list")
    def test_two_dbs(self, mock_fetch, mock_tbl, mock_version):

        """Function:  test_two_dbs

        Description:  Test with two databases to check.

        Arguments:

        """

        mock_version.return_value = self.version
        mock_fetch.side_effect = [self.dblist2, self.dblist2]
        mock_tbl.side_effect = [self.databases, self.databases,
                                self.databases2, self.databases2]

        self.assertFalse(mysql_rep_cmp.setup_cmp(self.master, self.slave, []))

    @mock.patch("mysql_rep_cmp.run_cmp", mock.Mock(return_value=True))
    @mock.patch("mysql_rep_cmp.mysql_class.fetch_sys_var")
    @mock.patch("mysql_rep_cmp.mysql_libs.fetch_tbl_dict")
    @mock.patch("mysql_rep_cmp.fetch_db_list")
    def test_one_db(self, mock_fetch, mock_tbl, mock_version):

        """Function:  test_master_db

        Description:  Test with one database to check.

        Arguments:

        """

        mock_version.return_value = self.version
        mock_fetch.side_effect = [self.dblist, self.dblist]
        mock_tbl.side_effect = [self.databases, self.databases]

        self.assertFalse(mysql_rep_cmp.setup_cmp(self.master, self.slave, []))

    @mock.patch("mysql_rep_cmp.mysql_class.fetch_sys_var")
    @mock.patch("mysql_rep_cmp.fetch_db_list")
    def test_no_dbs(self, mock_fetch, mock_version):

        """Function:  test_no_dbs

        Description:  Test with no databases from master or slave.

        Arguments:

        """

        mock_version.return_value = self.version
        mock_fetch.side_effect = [[], []]

        self.assertFalse(mysql_rep_cmp.setup_cmp(self.master, self.slave, []))


if __name__ == "__main__":
    unittest.main()
