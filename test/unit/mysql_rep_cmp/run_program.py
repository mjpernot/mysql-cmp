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
import mysql_rep_cmp                            # pylint:disable=E0401,C0413
import lib.gen_libs as gen_libs             # pylint:disable=E0401,C0413,R0402
import version                                  # pylint:disable=E0401,C0413

__version__ = version.__version__


class ArgParser():

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
        self.args_array = {}

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

        return  arg in self.args_array


class Mail():                                           # pylint:disable=R0903

    """Class:  Mail

    Description:  Class stub holder for gen_class.Mail class.

    Methods:
        __init__

    """

    def __init__(self):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:

        """

        self.data = None


class SlaveRep():                                       # pylint:disable=R0903

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


class MasterRep():

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
        test_non_slave_compare
        test_mysql_version3
        test_mysql_version2
        test_mysql_version
        test_both_conn_fail
        test_slave_conn_fail
        test_master_conn_fail
        test_conn_success
        test_str_server_id
        test_int_server_id
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
        self.args5 = ArgParser()
        self.args6 = ArgParser()
        self.args7 = ArgParser()

        self.args.args_array = {"-c": True, "-d": True, "-r": True}
        self.args2.args_array = {
            "-c": True, "-d": True, "-r": True, "-i": True}
        self.args5.args_array = {
            "-c": True, "-d": True, "-r": True, "-t": ["tbl1", "tbl2"],
            "-B": "db1"}
        self.args6.args_array = {
            "-c": True, "-d": True, "-r": True, "-B": "db1"}

    @mock.patch("mysql_rep_cmp.setup_cmp", mock.Mock(return_value=True))
    @mock.patch("mysql_rep_cmp.mysql_libs.disconnect",
                mock.Mock(return_value=True))
    @mock.patch("mysql_rep_cmp.mysql_libs.create_instance")
    def test_non_slave_compare(self, mock_server):

        """Function:  test_non_slave_compare

        Description:  Test with a non-slave database.

        Arguments:

        """

        self.slave.server_id = 12

        mock_server.side_effect = [self.master, self.slave]

        self.assertFalse(mysql_rep_cmp.run_program(self.args2))

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

        self.assertFalse(mysql_rep_cmp.run_program(self.args))

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

        self.assertFalse(mysql_rep_cmp.run_program(self.args))

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

        self.assertFalse(mysql_rep_cmp.run_program(self.args))

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
                mysql_rep_cmp.run_program(self.args))

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
                mysql_rep_cmp.run_program(self.args))

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
                mysql_rep_cmp.run_program(self.args))

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

        self.assertFalse(mysql_rep_cmp.run_program(self.args))

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

        self.assertFalse(mysql_rep_cmp.run_program(self.args))

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

        self.assertFalse(mysql_rep_cmp.run_program(self.args))

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
            self.assertFalse(mysql_rep_cmp.run_program(self.args))

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

        self.assertFalse(mysql_rep_cmp.run_program(self.args6))

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

        self.assertFalse(mysql_rep_cmp.run_program(self.args5))

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

        self.assertFalse(mysql_rep_cmp.run_program(self.args))


if __name__ == "__main__":
    unittest.main()
