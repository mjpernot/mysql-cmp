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

# Local
sys.path.append(os.getcwd())
import mysql_rep_cmp
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

        self.args_array = {
            "-c": "mysql_cfg", "-d": "config", "-e": "to_addr",
            "-o": "outfile", "-n": "indentation", "-m": "mongo",
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
        self.results = None
        self.results2 = "to_addr"
        self.results3 = False
        self.results4 = "a"

    def test_mode_with_data(self):

        """Function:  test_mode_with_data

        Description:  Test with mode with data.

        Arguments:

        """

        self.assertEqual(
            mysql_rep_cmp.create_data_config(self.args)["mode"],
            self.results4)

    def test_mailx_with_no_data(self):

        """Function:  test_mailx_with_no_data

        Description:  Test with mailx with no data.

        Arguments:

        """

        self.assertEqual(
            mysql_rep_cmp.create_data_config(self.args)["mailx"],
            self.results3)

    def test_subj_with_no_data(self):

        """Function:  test_subj_with_no_data

        Description:  Test with to_address with data.

        Arguments:

        """

        self.assertEqual(
            mysql_rep_cmp.create_data_config(self.args)["subj"],
            self.results)

    def test_to_addr_with_data(self):

        """Function:  test_to_addr_with_data

        Description:  Test with to_address with data.

        Arguments:

        """

        self.assertEqual(
            mysql_rep_cmp.create_data_config(self.args)["to_addr"],
            self.results2)


if __name__ == "__main__":
    unittest.main()
