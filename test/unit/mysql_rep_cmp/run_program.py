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
import unittest
import mock

# Local
sys.path.append(os.getcwd())
import mysql_rep_cmp
import lib.gen_libs as gen_libs
import version

__version__ = version.__version__


class ArgParser(object):

    """Class:  ArgParser

    Description:  Class stub holder for gen_class.ArgParser class.

    Methods:
        __init__
        get_val
        arg_exist

    """

    def __init__(self):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:

        """

        self.cmdline = None
        self.args_array = dict()

    def get_val(self, skey, def_val=None):

        """Method:  get_val

        Description:  Method stub holder for gen_class.ArgParser.get_val.

        Arguments:

        """

        return self.args_array.get(skey, def_val)

    def arg_exist(self, arg):

        """Method:  arg_exist

        Description:  Method stub holder for gen_class.ArgParser.arg_exist.

        Arguments:

        """

        return True if arg in self.args_array else False


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
        self.slv_lists = [{"Server_Id": 11}]
        self.conn_msg = None
        self.version = (8, 0, 30)

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
        test_mysql_version3
        test_mysql_version2
        test_mysql_version
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
        self.args = ArgParser()
        self.args2 = ArgParser()
        self.args2a = ArgParser()
        self.args3 = ArgParser()
        self.args3a = ArgParser()
        self.args4 = ArgParser()
        self.args5 = ArgParser()
        self.args6 = ArgParser()
        self.args.args_array = {"-c": True, "-d": True, "-r": True}
        self.args2.args_array = {
            "-c": True, "-d": True, "-r": True, "-e": "email_address",
            "-s": "subject_line"}
        self.args2a.args_array = {
            "-c": True, "-d": True, "-r": True, "-e": "email_address",
            "-s": "subject_line", "-u": True}
        self.args3.args_array = {
            "-c": True, "-d": True, "-r": True, "-e": "email_address"}
        self.args3a.args_array = {
            "-c": True, "-d": True, "-r": True, "-e": "email_address",
            "-u": True}
        self.args4.args_array = {
            "-c": True, "-d": True, "-r": True, "-z": True}
        self.args5.args_array = {
            "-c": True, "-d": True, "-r": True, "-t": ["tbl1", "tbl2"],
            "-B": "db1"}
        self.args6.args_array = {
            "-c": True, "-d": True, "-r": True, "-B": "db1"}

    @mock.patch("mysql_rep_cmp.setup_cmp", mock.Mock(return_value=True))
    @mock.patch("mysql_rep_cmp.mysql_libs.disconnect",
                mock.Mock(return_value=True))
    @mock.patch("mysql_rep_cmp.mysql_libs.create_instance")
    def test_mysql_version3(self, mock_server):

        """Function:  test_mysql_version3

        Description:  Test with MySQL version 8.0.6.

        Arguments:

        """

        self.master.version = (8, 0, 6)
        self.master.slv_lists = [{"Server_id": 11}]

        mock_server.side_effect = [self.master, self.slave]

        self.assertFalse(mysql_rep_cmp.run_program(self.args, self.sys_ign_db))

    @mock.patch("mysql_rep_cmp.setup_cmp", mock.Mock(return_value=True))
    @mock.patch("mysql_rep_cmp.mysql_libs.disconnect",
                mock.Mock(return_value=True))
    @mock.patch("mysql_rep_cmp.mysql_libs.create_instance")
    def test_mysql_version2(self, mock_server):

        """Function:  test_mysql_version2

        Description:  Test with MySQL version 8.0.26.

        Arguments:

        """

        self.master.version = (8, 0, 26)

        mock_server.side_effect = [self.master, self.slave]

        self.assertFalse(mysql_rep_cmp.run_program(self.args, self.sys_ign_db))

    @mock.patch("mysql_rep_cmp.setup_cmp", mock.Mock(return_value=True))
    @mock.patch("mysql_rep_cmp.mysql_libs.disconnect",
                mock.Mock(return_value=True))
    @mock.patch("mysql_rep_cmp.mysql_libs.create_instance")
    def test_mysql_version(self, mock_server):

        """Function:  test_mysql_version

        Description:  Test with MySQL version 8.0.30.

        Arguments:

        """

        mock_server.side_effect = [self.master, self.slave]

        self.assertFalse(mysql_rep_cmp.run_program(self.args, self.sys_ign_db))

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
            self.assertFalse(
                mysql_rep_cmp.run_program(self.args, self.sys_ign_db))

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
            self.assertFalse(
                mysql_rep_cmp.run_program(self.args, self.sys_ign_db))

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
            self.assertFalse(
                mysql_rep_cmp.run_program(self.args, self.sys_ign_db))

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

        self.assertFalse(mysql_rep_cmp.run_program(self.args, self.sys_ign_db))

    @mock.patch("mysql_rep_cmp.setup_cmp", mock.Mock(return_value=True))
    @mock.patch("mysql_rep_cmp.mysql_libs.disconnect",
                mock.Mock(return_value=True))
    @mock.patch("mysql_rep_cmp.mysql_libs.create_instance")
    def test_str_server_id(self, mock_server):

        """Function:  test_str_server_id

        Description:  Test with string server_id.

        Arguments:

        """

        self.master.slv_lists = [{"Server_Id": "11"}]

        mock_server.side_effect = [self.master, self.slave]

        self.assertFalse(mysql_rep_cmp.run_program(self.args, self.sys_ign_db))

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

        self.assertFalse(mysql_rep_cmp.run_program(self.args, self.sys_ign_db))

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

        self.assertFalse(
            mysql_rep_cmp.run_program(self.args4, self.sys_ign_db))

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

        self.assertFalse(
            mysql_rep_cmp.run_program(self.args3a, self.sys_ign_db))

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

        self.assertFalse(
            mysql_rep_cmp.run_program(self.args3, self.sys_ign_db))

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

        self.assertFalse(
            mysql_rep_cmp.run_program(self.args2a, self.sys_ign_db))

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

        self.assertFalse(
            mysql_rep_cmp.run_program(self.args2, self.sys_ign_db))

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
            self.assertFalse(
                mysql_rep_cmp.run_program(self.args, self.sys_ign_db))

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

        self.assertFalse(
            mysql_rep_cmp.run_program(self.args6, self.sys_ign_db))

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

        self.assertFalse(
            mysql_rep_cmp.run_program(self.args5, self.sys_ign_db))

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

        self.assertFalse(mysql_rep_cmp.run_program(self.args, self.sys_ign_db))


if __name__ == "__main__":
    unittest.main()
