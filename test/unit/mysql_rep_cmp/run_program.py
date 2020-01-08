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


class Server2(object):

    """Class:  Server

    Description:  Class stub holder for mysql_class.Server class.

    Methods:
        __init__ -> Class initialization.
        connect -> Method stub holder for mysql_class.Server.connect.
        set_srv_binlog_crc -> Stub for mysql_class.Server.set_srv_binlog_crc.

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

    def connect(self):

        """Method:  connect

        Description:  Method stub holder for mysql_class.Server.connect.

        Arguments:

        """

        return True

    def show_slv_hosts(self):

        """Method:  show_slv_hosts

        Description:  Stub holder for mysql_class.MasterRep.show_slv_hosts.

        Arguments:

        """

        return [{"Server_id": 10}]


class Server(object):

    """Class:  Server

    Description:  Class stub holder for mysql_class.Server class.

    Methods:
        __init__ -> Class initialization.
        connect -> Method stub holder for mysql_class.Server.connect.
        set_srv_binlog_crc -> Stub for mysql_class.Server.set_srv_binlog_crc.

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

    def connect(self):

        """Method:  connect

        Description:  Method stub holder for mysql_class.Server.connect.

        Arguments:

        """

        return True

    def show_slv_hosts(self):

        """Method:  show_slv_hosts

        Description:  Stub holder for mysql_class.MasterRep.show_slv_hosts.

        Arguments:

        """

        return [{"Server_id": 10}]


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp -> Initialize testing environment.
        test_slave_not_present -> Test with slave not in replic set.
        test_database_option -> Test with database option in args_array.
        test_table_option -> Test with table option in args_array.
        test_run_program -> Test with only default arguments passed.

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.sys_ign_db = ["performance_schema", "information_schema"]
        self.args_array = {"-c": True, "-d": True, "-r": True}

    @mock.patch("mysql_rep_cmp.sys.exit", mock.Mock(return_value=True))
    @mock.patch("mysql_rep_cmp.cmds_gen.disconnect",
                mock.Mock(return_value=True))
    @mock.patch("mysql_rep_cmp.mysql_libs.create_instance",
                mock.Mock(return_value=Server2()))
    def test_slave_not_present(self):

        """Function:  test_slave_not_present

        Description:  Test with slave not in replic set.

        Arguments:

        """

        self.assertFalse(mysql_rep_cmp.run_program(self.args_array,
                                                   self.sys_ign_db))

    @mock.patch("mysql_rep_cmp.setup_cmp", mock.Mock(return_value=True))
    @mock.patch("mysql_rep_cmp.cmds_gen.disconnect",
                mock.Mock(return_value=True))
    @mock.patch("mysql_rep_cmp.mysql_libs.create_instance",
                mock.Mock(return_value=Server()))
    def test_database_option(self):

        """Function:  test_database_option

        Description:  Test with database option in args_array.

        Arguments:

        """

        self.args_array["-B"] = "db1"

        self.assertFalse(mysql_rep_cmp.run_program(self.args_array,
                                                   self.sys_ign_db))

    @mock.patch("mysql_rep_cmp.setup_cmp", mock.Mock(return_value=True))
    @mock.patch("mysql_rep_cmp.cmds_gen.disconnect",
                mock.Mock(return_value=True))
    @mock.patch("mysql_rep_cmp.mysql_libs.create_instance",
                mock.Mock(return_value=Server()))
    def test_table_option(self):

        """Function:  test_table_option

        Description:  Test with table option in args_array.

        Arguments:

        """

        self.args_array["-t"] = ["tbl1", "tbl2"]
        self.args_array["-B"] = "db1"

        self.assertFalse(mysql_rep_cmp.run_program(self.args_array,
                                                   self.sys_ign_db))

    @mock.patch("mysql_rep_cmp.setup_cmp", mock.Mock(return_value=True))
    @mock.patch("mysql_rep_cmp.cmds_gen.disconnect",
                mock.Mock(return_value=True))
    @mock.patch("mysql_rep_cmp.mysql_libs.create_instance",
                mock.Mock(return_value=Server()))
    def test_run_program(self):

        """Function:  test_run_program

        Description:  Test with only default arguments passed.

        Arguments:

        """

        self.assertFalse(mysql_rep_cmp.run_program(self.args_array,
                                                   self.sys_ign_db))


if __name__ == "__main__":
    unittest.main()
