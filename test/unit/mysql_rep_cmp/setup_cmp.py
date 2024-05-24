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

    """

    def __init__(self):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:

        """

        self.cmdline = None
        self.args_array = {"-C": list(), "-c": "mysql_cfg", "-d": "config"}

    def get_val(self, skey, def_val=None):

        """Method:  get_val

        Description:  Method stub holder for gen_class.ArgParser.get_val.

        Arguments:

        """

        return self.args_array.get(skey, def_val)


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
        self.name = "MasterName"

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


class Cfg(object):

    """Class:  Cfg

    Description:  Emulate a configuration file.

    Methods:
        __init__

    """

    def __init__(self):

        """Method:  __init__

        Description:  Initialization.

        Arguments:

        """

        self.ign_dbs = [
            "performance_schema", "information_schema", "mysql", "sys"]
        self.ign_db_tbl = {"mysql": ["systems"]}


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_status_failed
        test_two_dbs
        test_one_db2
        test_one_db
        test_no_dbs

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.args = ArgParser()
        self.master = Server()
        self.slave = Server()
        self.slave.name = "SlaveName"
        self.cfg = Cfg()
        self.json_template = {"Platform": "MySQL"}
        self.mst_db_tbl = dict()
        self.mst_db_tbl2 = {"dbs": ["tbl1"]}
        self.mst_db_tbl3 = {"dbs": ["tbl1", "tbl2"]}
        self.mst_db_tbl4 = {"dbs": ["tbl1", "tbl2"], "dbs2": ["tbl3", "tbl4"]}
        self.data_config = {"mongo": "mongo"}
        self.status = (True, None)
        self.status2 = (False, "Error Message")

    @mock.patch("mysql_rep_cmp.recur_tbl_cmp", mock.Mock(return_value="OK"))
    @mock.patch("mysql_rep_cmp.gen_libs.load_module")
    @mock.patch("mysql_rep_cmp.data_out")
    @mock.patch("mysql_rep_cmp.create_data_config")
    @mock.patch("mysql_rep_cmp.get_db_tbl")
    @mock.patch("mysql_rep_cmp.get_json_template")
    def test_status_failed(self, mock_template, mock_dbstbls, mock_config,
                           mock_out, mock_load):

        """Function:  test_status_failed

        Description:  Test with status failure from data_out call.

        Arguments:

        """

        mock_dbstbls.return_value = self.mst_db_tbl4
        mock_template.return_value = self.json_template
        mock_config.return_value = self.data_config
        mock_out.return_value = self.status2
        mock_load.return_value = self.cfg

        with gen_libs.no_std_out():
            self.assertFalse(
                mysql_rep_cmp.setup_cmp(self.args, self.master, self.slave))

    @mock.patch("mysql_rep_cmp.recur_tbl_cmp", mock.Mock(return_value="OK"))
    @mock.patch("mysql_rep_cmp.gen_libs.load_module")
    @mock.patch("mysql_rep_cmp.data_out")
    @mock.patch("mysql_rep_cmp.create_data_config")
    @mock.patch("mysql_rep_cmp.get_db_tbl")
    @mock.patch("mysql_rep_cmp.get_json_template")
    def test_two_dbs(self, mock_template, mock_dbstbls, mock_config, mock_out,
                     mock_load):

        """Function:  test_two_dbs

        Description:  Test with two databases to check.

        Arguments:

        """

        mock_dbstbls.return_value = self.mst_db_tbl4
        mock_template.return_value = self.json_template
        mock_config.return_value = self.data_config
        mock_out.return_value = self.status
        mock_load.return_value = self.cfg

        self.assertFalse(
            mysql_rep_cmp.setup_cmp(self.args, self.master, self.slave))

    @mock.patch("mysql_rep_cmp.recur_tbl_cmp", mock.Mock(return_value="OK"))
    @mock.patch("mysql_rep_cmp.gen_libs.load_module")
    @mock.patch("mysql_rep_cmp.data_out")
    @mock.patch("mysql_rep_cmp.create_data_config")
    @mock.patch("mysql_rep_cmp.get_db_tbl")
    @mock.patch("mysql_rep_cmp.get_json_template")
    def test_one_db2(self, mock_template, mock_dbstbls, mock_config, mock_out,
                     mock_load):

        """Function:  test_one_db2

        Description:  Test with one database to check.

        Arguments:

        """

        mock_dbstbls.return_value = self.mst_db_tbl3
        mock_template.return_value = self.json_template
        mock_config.return_value = self.data_config
        mock_out.return_value = self.status
        mock_load.return_value = self.cfg

        self.assertFalse(
            mysql_rep_cmp.setup_cmp(self.args, self.master, self.slave))

    @mock.patch("mysql_rep_cmp.recur_tbl_cmp", mock.Mock(return_value="OK"))
    @mock.patch("mysql_rep_cmp.gen_libs.load_module")
    @mock.patch("mysql_rep_cmp.data_out")
    @mock.patch("mysql_rep_cmp.create_data_config")
    @mock.patch("mysql_rep_cmp.get_db_tbl")
    @mock.patch("mysql_rep_cmp.get_json_template")
    def test_one_db(self, mock_template, mock_dbstbls, mock_config, mock_out,
                    mock_load):

        """Function:  test_one_db

        Description:  Test with one database to check.

        Arguments:

        """

        mock_dbstbls.return_value = self.mst_db_tbl2
        mock_template.return_value = self.json_template
        mock_config.return_value = self.data_config
        mock_out.return_value = self.status
        mock_load.return_value = self.cfg

        self.assertFalse(
            mysql_rep_cmp.setup_cmp(self.args, self.master, self.slave))

    @mock.patch("mysql_rep_cmp.gen_libs.load_module")
    @mock.patch("mysql_rep_cmp.data_out")
    @mock.patch("mysql_rep_cmp.create_data_config")
    @mock.patch("mysql_rep_cmp.get_db_tbl")
    @mock.patch("mysql_rep_cmp.get_json_template")
    def test_no_dbs(self, mock_template, mock_dbstbls, mock_config, mock_out,
                    mock_load):

        """Function:  test_no_dbs

        Description:  Test with no databases from master.

        Arguments:

        """

        mock_dbstbls.return_value = self.mst_db_tbl
        mock_template.return_value = self.json_template
        mock_config.return_value = self.data_config
        mock_out.return_value = self.status
        mock_load.return_value = self.cfg

        self.assertFalse(
            mysql_rep_cmp.setup_cmp(self.args, self.master, self.slave))


if __name__ == "__main__":
    unittest.main()
