#!/usr/bin/python
# Classification (U)

"""Program:  run_program.py

    Description:  Unit testing of run_program in mysql_rep_cmp.py.

    Usage:
        test/unit/mysql_rep_cmp/run_program.py

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


class Mail(object):

    """Class:  Mail

    Description:  Class stub holder for gen_class.Mail class.

    Methods:
        __init__
        add_2_msg
        send_mail

    """

    def __init__(self):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:

        """

        self.data = None


class SlaveRep(object):

    """Class:  Server

    Description:  Class stub holder for mysql_class.SlaveRep class.

    Methods:
        __init__
        connect

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
        self.server_id = 11
        self.conn_msg = None

    def connect(self, silent=False):

        """Method:  connect

        Description:  Method stub holder for mysql_class.SlaveRep.connect.

        Arguments:

        """

        status = True

        if silent:
            status = True

        return status


class MasterRep(object):

    """Class:  Server

    Description:  Class stub holder for mysql_class.MasterRep class.

    Methods:
        __init__
        connect
        show_slv_hosts

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
        self.server_id = 10
        self.slv_lists = [{"Server_id": 11}]
        self.conn_msg = None

    def connect(self, silent=False):

        """Method:  connect

        Description:  Method stub holder for mysql_class.MasterRep.connect.

        Arguments:

        """

        status = True

        if silent:
            status = True

        return status

    def show_slv_hosts(self):

        """Method:  show_slv_hosts

        Description:  Stub holder for mysql_class.MasterRep.show_slv_hosts.

        Arguments:

        """

        return self.slv_lists


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_both_conn_fail
        test_slave_conn_fail
        test_master_conn_fail
        test_conn_success
        test_str_server_id
        test_int_server_id
        test_no_std_out
        test_email_no_subj_mailx
        test_email_no_subj
        test_email_mailx
        test_email
        test_slave_not_present
        test_database_option
        test_table_option
        test_run_program

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.err_msg = "Failed Conection Message"
        self.mail = Mail()
        self.master = MasterRep()
        self.slave = SlaveRep()
        self.sys_ign_db = ["performance_schema", "information_schema"]
        self.args_array = {"-c": True, "-d": True, "-r": True}
        self.args_array2 = {"-c": True, "-d": True, "-r": True,
                            "-e": "email_address", "-s": "subject_line"}
        self.args_array2a = {"-c": True, "-d": True, "-r": True,
                             "-e": "email_address", "-s": "subject_line",
                             "-u": True}
        self.args_array3 = {"-c": True, "-d": True, "-r": True,
                            "-e": "email_address"}
        self.args_array3a = {"-c": True, "-d": True, "-r": True,
                             "-e": "email_address", "-u": True}
        self.args_array4 = {"-c": True, "-d": True, "-r": True, "-z": True}

    @mock.patch("mysql_rep_cmp.setup_cmp", mock.Mock(return_value=True))
    @mock.patch("mysql_rep_cmp.mysql_libs.disconnect",
                mock.Mock(return_value=True))
    @mock.patch("mysql_rep_cmp.mysql_libs.create_instance")
    def test_both_conn_fail(self, mock_server):

        """Function:  test_both_conn_fail

        Description:  Test with failed connection on master and slave.

        Arguments:

        """

        self.master.conn_msg = self.err_msg
        self.slave.conn_msg = self.err_msg

        mock_server.side_effect = [self.master, self.slave]

        with gen_libs.no_std_out():
            self.assertFalse(mysql_rep_cmp.run_program(self.args_array,
                                                       self.sys_ign_db))

    @mock.patch("mysql_rep_cmp.setup_cmp", mock.Mock(return_value=True))
    @mock.patch("mysql_rep_cmp.mysql_libs.disconnect",
                mock.Mock(return_value=True))
    @mock.patch("mysql_rep_cmp.mysql_libs.create_instance")
    def test_slave_conn_fail(self, mock_server):

        """Function:  test_slave_conn_fail

        Description:  Test with failed connection on slave.

        Arguments:

        """

        self.slave.conn_msg = self.err_msg

        mock_server.side_effect = [self.master, self.slave]

        with gen_libs.no_std_out():
            self.assertFalse(mysql_rep_cmp.run_program(self.args_array,
                                                       self.sys_ign_db))

    @mock.patch("mysql_rep_cmp.setup_cmp", mock.Mock(return_value=True))
    @mock.patch("mysql_rep_cmp.mysql_libs.disconnect",
                mock.Mock(return_value=True))
    @mock.patch("mysql_rep_cmp.mysql_libs.create_instance")
    def test_master_conn_fail(self, mock_server):

        """Function:  test_master_conn_fail

        Description:  Test with failed connection on master.

        Arguments:

        """

        self.master.conn_msg = self.err_msg

        mock_server.side_effect = [self.master, self.slave]

        with gen_libs.no_std_out():
            self.assertFalse(mysql_rep_cmp.run_program(self.args_array,
                                                       self.sys_ign_db))

    @mock.patch("mysql_rep_cmp.setup_cmp", mock.Mock(return_value=True))
    @mock.patch("mysql_rep_cmp.mysql_libs.disconnect",
                mock.Mock(return_value=True))
    @mock.patch("mysql_rep_cmp.mysql_libs.create_instance")
    def test_conn_success(self, mock_server):

        """Function:  test_conn_success

        Description:  Test with successful connection to master and slave.

        Arguments:

        """

        mock_server.side_effect = [self.master, self.slave]

        self.assertFalse(mysql_rep_cmp.run_program(self.args_array,
                                                   self.sys_ign_db))

    @mock.patch("mysql_rep_cmp.setup_cmp", mock.Mock(return_value=True))
    @mock.patch("mysql_rep_cmp.mysql_libs.disconnect",
                mock.Mock(return_value=True))
    @mock.patch("mysql_rep_cmp.mysql_libs.create_instance")
    def test_str_server_id(self, mock_server):

        """Function:  test_str_server_id

        Description:  Test with string server_id.

        Arguments:

        """

        self.master.slv_lists = [{"Server_id": "11"}]

        mock_server.side_effect = [self.master, self.slave]

        self.assertFalse(mysql_rep_cmp.run_program(self.args_array,
                                                   self.sys_ign_db))

    @mock.patch("mysql_rep_cmp.setup_cmp", mock.Mock(return_value=True))
    @mock.patch("mysql_rep_cmp.mysql_libs.disconnect",
                mock.Mock(return_value=True))
    @mock.patch("mysql_rep_cmp.mysql_libs.create_instance")
    def test_int_server_id(self, mock_server):

        """Function:  test_int_server_id

        Description:  Test with integer server_id.

        Arguments:

        """

        mock_server.side_effect = [self.master, self.slave]

        self.assertFalse(mysql_rep_cmp.run_program(self.args_array,
                                                   self.sys_ign_db))

    @mock.patch("mysql_rep_cmp.setup_cmp", mock.Mock(return_value=True))
    @mock.patch("mysql_rep_cmp.mysql_libs.disconnect",
                mock.Mock(return_value=True))
    @mock.patch("mysql_rep_cmp.mysql_libs.create_instance")
    def test_no_std_out(self, mock_server):

        """Function:  test_no_std_out

        Description:  Test with no standard out suppression selected.

        Arguments:

        """

        mock_server.side_effect = [self.master, self.slave]

        self.assertFalse(mysql_rep_cmp.run_program(self.args_array4,
                                                   self.sys_ign_db))

    @mock.patch("mysql_rep_cmp.setup_cmp", mock.Mock(return_value=True))
    @mock.patch("mysql_rep_cmp.mysql_libs.disconnect",
                mock.Mock(return_value=True))
    @mock.patch("mysql_rep_cmp.mysql_libs.create_instance")
    @mock.patch("mysql_rep_cmp.gen_class.setup_mail")
    def test_email_no_subj_mailx(self, mock_mail, mock_server):

        """Function:  test_email_no_subj_mailx

        Description:  Test with email using mailx and no subject line.

        Arguments:

        """

        mock_mail.return_value = self.mail
        mock_server.side_effect = [self.master, self.slave]

        self.assertFalse(mysql_rep_cmp.run_program(self.args_array3a,
                                                   self.sys_ign_db))

    @mock.patch("mysql_rep_cmp.setup_cmp", mock.Mock(return_value=True))
    @mock.patch("mysql_rep_cmp.mysql_libs.disconnect",
                mock.Mock(return_value=True))
    @mock.patch("mysql_rep_cmp.mysql_libs.create_instance")
    @mock.patch("mysql_rep_cmp.gen_class.setup_mail")
    def test_email_no_subj(self, mock_mail, mock_server):

        """Function:  test_email_no_subj

        Description:  Test with email, but no subject line.

        Arguments:

        """

        mock_mail.return_value = self.mail
        mock_server.side_effect = [self.master, self.slave]

        self.assertFalse(mysql_rep_cmp.run_program(self.args_array3,
                                                   self.sys_ign_db))

    @mock.patch("mysql_rep_cmp.setup_cmp", mock.Mock(return_value=True))
    @mock.patch("mysql_rep_cmp.mysql_libs.disconnect",
                mock.Mock(return_value=True))
    @mock.patch("mysql_rep_cmp.mysql_libs.create_instance")
    @mock.patch("mysql_rep_cmp.gen_class.setup_mail")
    def test_email_mailx(self, mock_mail, mock_server):

        """Function:  test_email_mailx

        Description:  Test with using mailx command.

        Arguments:

        """

        mock_mail.return_value = self.mail
        mock_server.side_effect = [self.master, self.slave]

        self.assertFalse(mysql_rep_cmp.run_program(self.args_array2a,
                                                   self.sys_ign_db))

    @mock.patch("mysql_rep_cmp.setup_cmp", mock.Mock(return_value=True))
    @mock.patch("mysql_rep_cmp.mysql_libs.disconnect",
                mock.Mock(return_value=True))
    @mock.patch("mysql_rep_cmp.mysql_libs.create_instance")
    @mock.patch("mysql_rep_cmp.gen_class.setup_mail")
    def test_email(self, mock_mail, mock_server):

        """Function:  test_email

        Description:  Test with email setup.

        Arguments:

        """

        mock_mail.return_value = self.mail
        mock_server.side_effect = [self.master, self.slave]

        self.assertFalse(mysql_rep_cmp.run_program(self.args_array2,
                                                   self.sys_ign_db))

    @mock.patch("mysql_rep_cmp.mysql_libs.disconnect",
                mock.Mock(return_value=True))
    @mock.patch("mysql_rep_cmp.mysql_libs.create_instance")
    def test_slave_not_present(self, mock_server):

        """Function:  test_slave_not_present

        Description:  Test with slave not in replic set.

        Arguments:

        """

        self.slave.server_id = 12

        mock_server.side_effect = [self.master, self.slave]

        with gen_libs.no_std_out():
            self.assertFalse(mysql_rep_cmp.run_program(self.args_array,
                                                       self.sys_ign_db))

    @mock.patch("mysql_rep_cmp.setup_cmp", mock.Mock(return_value=True))
    @mock.patch("mysql_rep_cmp.mysql_libs.disconnect",
                mock.Mock(return_value=True))
    @mock.patch("mysql_rep_cmp.mysql_libs.create_instance")
    def test_database_option(self, mock_server):

        """Function:  test_database_option

        Description:  Test with database option in args_array.

        Arguments:

        """

        mock_server.side_effect = [self.master, self.slave]

        self.args_array["-B"] = "db1"

        self.assertFalse(mysql_rep_cmp.run_program(self.args_array,
                                                   self.sys_ign_db))

    @mock.patch("mysql_rep_cmp.setup_cmp", mock.Mock(return_value=True))
    @mock.patch("mysql_rep_cmp.mysql_libs.disconnect",
                mock.Mock(return_value=True))
    @mock.patch("mysql_rep_cmp.mysql_libs.create_instance")
    def test_table_option(self, mock_server):

        """Function:  test_table_option

        Description:  Test with table option in args_array.

        Arguments:

        """

        mock_server.side_effect = [self.master, self.slave]

        self.args_array["-t"] = ["tbl1", "tbl2"]
        self.args_array["-B"] = "db1"

        self.assertFalse(mysql_rep_cmp.run_program(self.args_array,
                                                   self.sys_ign_db))

    @mock.patch("mysql_rep_cmp.setup_cmp", mock.Mock(return_value=True))
    @mock.patch("mysql_rep_cmp.mysql_libs.disconnect",
                mock.Mock(return_value=True))
    @mock.patch("mysql_rep_cmp.mysql_libs.create_instance")
    def test_run_program(self, mock_server):

        """Function:  test_run_program

        Description:  Test with only default arguments passed.

        Arguments:

        """

        mock_server.side_effect = [self.master, self.slave]

        self.assertFalse(mysql_rep_cmp.run_program(self.args_array,
                                                   self.sys_ign_db))


if __name__ == "__main__":
    unittest.main()
