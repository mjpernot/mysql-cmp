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
import lib.gen_class as gen_class
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
        test_default_no_std
        test_check_once_no_std
        test_reached_max_no_std
        test_no_recur_no_std
        test_default_email
        test_check_once_email
        test_reached_max_mail
        test_no_recur_email
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
        self.mail = gen_class.setup_mail("email_addr", subj="subjectline")
        self.tbl = "tbl1"
        self.no_std = True
        self.results = "\tChecking: {0} {1}".format(self.tbl.ljust(40),
                                                    "Synced")
        self.results2 = "\tChecking: {0} {1}".format(
            self.tbl.ljust(40), "Error:  Checksums do not match")

    @mock.patch("mysql_rep_cmp.mysql_libs.checksum")
    def test_default_no_std(self, mock_checksum):

        """Function:  test_default_no_std

        Description:  Test with default arguments with no_std.

        Arguments:

        """

        mock_checksum.side_effect = [10, 10]

        self.assertFalse(mysql_rep_cmp.recur_tbl_cmp(
            self.master, self.slave, "db1", "tbl1", 1, mail=self.mail,
            no_std=self.no_std))

        self.assertEqual(self.mail.msg, self.results)

    @mock.patch("mysql_rep_cmp.time.sleep", mock.Mock(return_value=True))
    @mock.patch("mysql_rep_cmp.mysql_libs.checksum")
    def test_check_once_no_std(self, mock_checksum):

        """Function:  test_check_once_no_std

        Description:  Test with checksumming at once with no_std.

        Arguments:

        """

        mock_checksum.side_effect = [10, 11, 10, 10]

        self.assertFalse(mysql_rep_cmp.recur_tbl_cmp(
            self.master, self.slave, "db1", "tbl1", 1, mail=self.mail,
            no_std=self.no_std))

        self.assertEqual(self.mail.msg, self.results)

    @mock.patch("mysql_rep_cmp.time.sleep", mock.Mock(return_value=True))
    @mock.patch("mysql_rep_cmp.mysql_libs.checksum")
    def test_reached_max_no_std(self, mock_checksum):

        """Function:  test_reached_max_no_std

        Description:  Test with reaching max checks with no_std.

        Arguments:

        """

        mock_checksum.side_effect = [10, 11, 10, 11]

        self.assertFalse(mysql_rep_cmp.recur_tbl_cmp(
            self.master, self.slave, "db1", "tbl1", 3, mail=self.mail,
            no_std=self.no_std))

        self.assertEqual(self.mail.msg, self.results2)

    @mock.patch("mysql_rep_cmp.mysql_libs.checksum")
    def test_no_recur_no_std(self, mock_checksum):

        """Function:  test_no_recur_no_std

        Description:  Test with no recur parameter set with no_std.

        Arguments:

        """

        mock_checksum.side_effect = [10, 10]

        self.assertFalse(mysql_rep_cmp.recur_tbl_cmp(
            self.master, self.slave, "db1", "tbl1", mail=self.mail,
            no_std=self.no_std))

        self.assertEqual(self.mail.msg, self.results)

    @mock.patch("mysql_rep_cmp.mysql_libs.checksum")
    def test_default_email(self, mock_checksum):

        """Function:  test_default_email

        Description:  Test with default arguments with email.

        Arguments:

        """

        mock_checksum.side_effect = [10, 10]

        with gen_libs.no_std_out():
            self.assertFalse(mysql_rep_cmp.recur_tbl_cmp(
                self.master, self.slave, "db1", "tbl1", 1, mail=self.mail))

        self.assertEqual(self.mail.msg, self.results)

    @mock.patch("mysql_rep_cmp.time.sleep", mock.Mock(return_value=True))
    @mock.patch("mysql_rep_cmp.mysql_libs.checksum")
    def test_check_once_email(self, mock_checksum):

        """Function:  test_check_once_email

        Description:  Test with checksumming at once with email.

        Arguments:

        """

        mock_checksum.side_effect = [10, 11, 10, 10]

        with gen_libs.no_std_out():
            self.assertFalse(mysql_rep_cmp.recur_tbl_cmp(
                self.master, self.slave, "db1", "tbl1", 1, mail=self.mail))

        self.assertEqual(self.mail.msg, self.results)

    @mock.patch("mysql_rep_cmp.time.sleep", mock.Mock(return_value=True))
    @mock.patch("mysql_rep_cmp.mysql_libs.checksum")
    def test_reached_max_mail(self, mock_checksum):

        """Function:  test_reached_max_mail

        Description:  Test with reaching max checks with email.

        Arguments:

        """

        mock_checksum.side_effect = [10, 11, 10, 11]

        with gen_libs.no_std_out():
            self.assertFalse(mysql_rep_cmp.recur_tbl_cmp(
                self.master, self.slave, "db1", "tbl1", 3, mail=self.mail))

        self.assertEqual(self.mail.msg, self.results2)

    @mock.patch("mysql_rep_cmp.mysql_libs.checksum")
    def test_no_recur_email(self, mock_checksum):

        """Function:  test_no_recur_email

        Description:  Test with no recur parameter set with email.

        Arguments:

        """

        mock_checksum.side_effect = [10, 10]

        with gen_libs.no_std_out():
            self.assertFalse(mysql_rep_cmp.recur_tbl_cmp(
                self.master, self.slave, "db1", "tbl1", mail=self.mail))

        self.assertEqual(self.mail.msg, self.results)

    @mock.patch("mysql_rep_cmp.mysql_libs.checksum")
    def test_no_recur(self, mock_checksum):

        """Function:  test_no_recur

        Description:  Test with no recur parameter set.

        Arguments:

        """

        mock_checksum.side_effect = [10, 10]

        with gen_libs.no_std_out():
            self.assertFalse(mysql_rep_cmp.recur_tbl_cmp(
                self.master, self.slave, "db1", "tbl1"))

    @mock.patch("mysql_rep_cmp.time.sleep", mock.Mock(return_value=True))
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

    @mock.patch("mysql_rep_cmp.time.sleep", mock.Mock(return_value=True))
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

        """Function:  test_default

        Description:  Test with default arguments only.

        Arguments:

        """

        mock_checksum.side_effect = [10, 10]

        with gen_libs.no_std_out():
            self.assertFalse(mysql_rep_cmp.recur_tbl_cmp(
                self.master, self.slave, "db1", "tbl1", 1))


if __name__ == "__main__":
    unittest.main()
