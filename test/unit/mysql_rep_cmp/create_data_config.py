# Classification (U)

"""Program:  create_data_config.py

    Description:  Unit testing of create_data_config in mysql_rep_cmp.py.

    Usage:
        test/unit/mysql_rep_cmp/create_data_config.py

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


class ArgParser():                                      # pylint:disable=R0903

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

        self.args_array = {
            "-c": "mysql_cfg", "-d": "config", "-e": "to_addr",
            "-o": "outfile", "-n": "indentation",
            "-i": "database:table", "-w": "a", "-p": False}

    def get_val(self, skey, def_val=None):

        """Method:  get_val

        Description:  Method stub holder for gen_class.ArgParser.get_val.

        Arguments:

        """

        return self.args_array.get(skey, def_val)


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_with_no_mongo
        test_with_mongo
        test_mode_with_data
        test_mailx_with_no_data
        test_subj_with_no_data
        test_to_addr_with_data

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.args = ArgParser()
        self.args.args_array["-m"] = "mongo"
        self.args2 = ArgParser()
        self.results = None
        self.results2 = "to_addr"
        self.results3 = False
        self.results4 = "a"

    def test_with_no_mongo(self):

        """Function:  test_with_no_mongo

        Description:  Test with mongo being passed.

        Arguments:

        """

        data_config = mysql_rep_cmp.create_data_config(self.args2)

        self.assertNotIn("mongo", data_config)

    @mock.patch("mysql_rep_cmp.gen_libs.load_module")
    def test_with_mongo(self, mock_load):

        """Function:  test_with_mongo

        Description:  Test with mongo being passed.

        Arguments:

        """

        mock_load.return_value = "Mongo_Config"

        self.assertEqual(
            mysql_rep_cmp.create_data_config(self.args)["mode"],
            self.results4)

    @mock.patch("mysql_rep_cmp.gen_libs.load_module")
    def test_mode_with_data(self, mock_load):

        """Function:  test_mode_with_data

        Description:  Test with mode with data.

        Arguments:

        """

        mock_load.return_value = "Mongo_Config"

        self.assertEqual(
            mysql_rep_cmp.create_data_config(self.args)["mode"],
            self.results4)

    @mock.patch("mysql_rep_cmp.gen_libs.load_module")
    def test_mailx_with_no_data(self, mock_load):

        """Function:  test_mailx_with_no_data

        Description:  Test with mailx with no data.

        Arguments:

        """

        mock_load.return_value = "Mongo_Config"

        self.assertEqual(
            mysql_rep_cmp.create_data_config(self.args)["mailx"],
            self.results3)

    @mock.patch("mysql_rep_cmp.gen_libs.load_module")
    def test_subj_with_no_data(self, mock_load):

        """Function:  test_subj_with_no_data

        Description:  Test with to_address with data.

        Arguments:

        """

        mock_load.return_value = "Mongo_Config"

        self.assertEqual(
            mysql_rep_cmp.create_data_config(self.args)["subj"],
            self.results)

    @mock.patch("mysql_rep_cmp.gen_libs.load_module")
    def test_to_addr_with_data(self, mock_load):

        """Function:  test_to_addr_with_data

        Description:  Test with to_address with data.

        Arguments:

        """

        mock_load.return_value = "Mongo_Config"

        self.assertEqual(
            mysql_rep_cmp.create_data_config(self.args)["to_addr"],
            self.results2)


if __name__ == "__main__":
    unittest.main()
