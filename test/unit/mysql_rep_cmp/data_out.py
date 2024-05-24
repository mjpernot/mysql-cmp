# Classification (U)

"""Program:  data_out.py

    Description:  Unit testing of data_out in mysql_rep_cmp.py.

    Usage:
        test/unit/mysql_rep_cmp/data_out.py

    Arguments:

"""

# Libraries and Global Variables

# Standard
import sys
import os
import json
import unittest
import mock

# Local
sys.path.append(os.getcwd())
import lib.gen_libs as gen_libs
import mysql_rep_cmp

import version

__version__ = version.__version__


class MailTest(object):

    """Class:  MailTest

    Description:  Class which is a representation of an email.

    Methods:
        __init__
        add_2_msg
        send_mail

    """

    def __init__(self, toline, subj=None, frm=None, msg_type=None):

        """Method:  __init__

        Description:  Initialization of an instance of the Mail class.

        Arguments:

        """

        if isinstance(subj, list):
            subj = list(subj)

        if isinstance(toline, list):
            self.toline = list(toline)

        else:
            self.toline = toline

        self.subj = subj
        self.frm = frm
        self.msg_type = msg_type
        self.msg = ""

    def add_2_msg(self, txt_ln=None):

        """Method:  add_2_msg

        Description:  Add text to text string if data is present.

        Arguments:

        """

        if txt_ln:

            if isinstance(txt_ln, str):
                self.msg = self.msg + txt_ln

            else:
                self.msg = self.msg + json.dumps(txt_ln)

    def send_mail(self, use_mailx=False):

        """Method:  send_mail

        Description:  Send email.

        Arguments:

        """

        status = True

        if use_mailx:
            status = True

        return status


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_mongo_error
        test_mongo
        test_outfile_mode2
        test_outfile_mode
        test_outfile
        test_email_subj
        test_email_no_subj
        test_email_mailx2
        test_email_mailx
        test_email_indent
        test_email
        test_indent_true
        test_indent_false
        test_suppress_true
        test_suppress_false_expand2
        test_suppress_false_expand
        test_suppress_false
        test_not_dictionary

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.mail = MailTest("toaddr")
        self.data = {"key": "value", "key2": ["list1", "list2"]}
        self.data2 = ["key", "value"]
        self.to_addr = "To_Address"
        self.subj = "EmailSubject"
        self.mailx = True
        self.mailx2 = False
        self.outfile = "/path/file"
        self.mode = "a"
        self.mode2 = "w"
        self.expand = True
        self.expand2 = False
        self.indent = 4
        self.suppress = True
        self.suppress2 = False
        self.mongo = "mongo"
        self.db_tbl = "db1:tbl1"
        self.results = (True, None)
        self.results2 = (
            False, "Error: Is not a dictionary: %s" % (self.data2))
        self.results3 = (False, "Error Message")

    @mock.patch("mysql_rep_cmp.mongo_libs.ins_doc",
                mock.Mock(return_value=(False, "Error Message")))
    def test_mongo_error(self):

        """Function:  test_mongo_error

        Description:  Test with mongo option with an error status.

        Arguments:

        """

        self.assertEqual(
            mysql_rep_cmp.data_out(
                self.data, suppress=self.suppress, mongo=self.mongo,
                db_tbl=self.db_tbl), self.results3)

    @mock.patch("mysql_rep_cmp.mongo_libs.ins_doc",
                mock.Mock(return_value=(True, None)))
    def test_mongo(self):

        """Function:  test_mongo

        Description:  Test with mongo option.

        Arguments:

        """

        self.assertEqual(
            mysql_rep_cmp.data_out(
                self.data, suppress=self.suppress, mongo=self.mongo,
                db_tbl=self.db_tbl), self.results)

    @mock.patch("mysql_rep_cmp.pprint.pprint", mock.Mock(return_value=True))
    @mock.patch("mysql_rep_cmp.open", mock.Mock(return_value=True))
    def test_outfile_mode2(self):

        """Function:  test_outfile_mode2

        Description:  Test with outfile and mode option.

        Arguments:

        """

        self.assertEqual(
            mysql_rep_cmp.data_out(
                self.data, suppress=self.suppress, outfile=self.outfile,
                mode=self.mode2), self.results)

    @mock.patch("mysql_rep_cmp.pprint.pprint", mock.Mock(return_value=True))
    @mock.patch("mysql_rep_cmp.open", mock.Mock(return_value=True))
    def test_outfile_mode(self):

        """Function:  test_outfile_mode

        Description:  Test with outfile and mode option.

        Arguments:

        """

        self.assertEqual(
            mysql_rep_cmp.data_out(
                self.data, suppress=self.suppress, outfile=self.outfile,
                mode=self.mode), self.results)

    @mock.patch("mysql_rep_cmp.pprint.pprint", mock.Mock(return_value=True))
    @mock.patch("mysql_rep_cmp.open", mock.Mock(return_value=True))
    def test_outfile(self):

        """Function:  test_outfile

        Description:  Test with outfile option.

        Arguments:

        """

        self.assertEqual(
            mysql_rep_cmp.data_out(
                self.data, suppress=self.suppress, outfile=self.outfile),
            self.results)

    @mock.patch("mysql_rep_cmp.gen_class.setup_mail")
    def test_email_subj(self, mock_mail):

        """Function:  test_email_subj

        Description:  Test with email option with subject option.

        Arguments:

        """

        mock_mail.return_value = self.mail

        self.assertEqual(
            mysql_rep_cmp.data_out(
                self.data, suppress=self.suppress, to_addr=self.to_addr,
                subj=self.subj), self.results)

    @mock.patch("mysql_rep_cmp.gen_class.setup_mail")
    def test_email_no_subj(self, mock_mail):

        """Function:  test_email_no_subj

        Description:  Test with email option with no subject option.

        Arguments:

        """

        mock_mail.return_value = self.mail

        self.assertEqual(
            mysql_rep_cmp.data_out(
                self.data, suppress=self.suppress, to_addr=self.to_addr),
            self.results)

    @mock.patch("mysql_rep_cmp.gen_class.setup_mail")
    def test_email_mailx2(self, mock_mail):

        """Function:  test_email_mailx2

        Description:  Test with email option with mailx option.

        Arguments:

        """

        mock_mail.return_value = self.mail

        self.assertEqual(
            mysql_rep_cmp.data_out(
                self.data, suppress=self.suppress, to_addr=self.to_addr,
                mailx=self.mailx2), self.results)

    @mock.patch("mysql_rep_cmp.gen_class.setup_mail")
    def test_email_mailx(self, mock_mail):

        """Function:  test_email_mailx

        Description:  Test with email option with mailx option.

        Arguments:

        """

        mock_mail.return_value = self.mail

        self.assertEqual(
            mysql_rep_cmp.data_out(
                self.data, suppress=self.suppress, to_addr=self.to_addr,
                mailx=self.mailx), self.results)

    @mock.patch("mysql_rep_cmp.gen_class.setup_mail")
    def test_email_indent(self, mock_mail):

        """Function:  test_email_indent

        Description:  Test with email option with indent.

        Arguments:

        """

        mock_mail.return_value = self.mail

        self.assertEqual(
            mysql_rep_cmp.data_out(
                self.data, suppress=self.suppress, to_addr=self.to_addr,
                indent=self.indent), self.results)

    @mock.patch("mysql_rep_cmp.gen_class.setup_mail")
    def test_email(self, mock_mail):

        """Function:  test_email

        Description:  Test with email option.

        Arguments:

        """

        mock_mail.return_value = self.mail

        self.assertEqual(
            mysql_rep_cmp.data_out(
                self.data, suppress=self.suppress, to_addr=self.to_addr),
            self.results)

    def test_indent_true(self):

        """Function:  test_indent_true

        Description:  Test pass in indent arg.

        Arguments:

        """

        self.assertEqual(
            mysql_rep_cmp.data_out(
                self.data, suppress=self.suppress, indent=self.indent),
            self.results)

    def test_indent_false(self):

        """Function:  test_indent_false

        Description:  Test with no indent arg passed in.

        Arguments:

        """

        self.assertEqual(
            mysql_rep_cmp.data_out(
                self.data, suppress=self.suppress), self.results)

    def test_suppress_true(self):

        """Function:  test_suppress_true

        Description:  Test with suppression is true.

        Arguments:

        """

        self.assertEqual(
            mysql_rep_cmp.data_out(
                self.data, suppress=self.suppress), self.results)

    def test_suppress_false_expand2(self):

        """Function:  test_suppress_false_expand2

        Description:  Test with suppression is false and expand option.

        Arguments:

        """

        with gen_libs.no_std_out():
            self.assertEqual(
                mysql_rep_cmp.data_out(
                    self.data, suppress=self.suppress2, expand=self.expand2,
                    indent=self.indent), self.results)

    def test_suppress_false_expand(self):

        """Function:  test_suppress_false_expand

        Description:  Test with suppression is false and expand option.

        Arguments:

        """

        with gen_libs.no_std_out():
            self.assertEqual(
                mysql_rep_cmp.data_out(
                    self.data, suppress=self.suppress2, expand=self.expand,
                    indent=self.indent), self.results)

    def test_suppress_false(self):

        """Function:  test_suppress_false

        Description:  Test with suppression is false.

        Arguments:

        """

        with gen_libs.no_std_out():
            self.assertEqual(
                mysql_rep_cmp.data_out(
                    self.data, suppress=self.suppress2), self.results)

    def test_not_dictionary(self):

        """Function:  test_not_dictionary

        Description:  Test data is not a dictionary.

        Arguments:

        """

        self.assertEqual(mysql_rep_cmp.data_out(self.data2), self.results2)


if __name__ == "__main__":
    unittest.main()
