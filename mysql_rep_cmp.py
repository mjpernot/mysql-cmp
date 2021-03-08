#!/usr/bin/python
# Classification (U)

"""Program:  mysql_rep_cmp.py

    Description:  Does a table checksum comparsion between a master database
        and a replica database.  This should determine whether the tables
        in both databases are in sync with each other.  This is not a
        100% guarntee check as the comparsion process only uses a
        time-delay recursion check.  If a table is listed as being out
        of sync, then further investigation will be required.

    Usage:
        mysql_rep_cmp.py -c master_cfg -r slave_cfg -d path
            {-A [-e addr [addr2 ...] [-s subject_line] [-u]] [-z] |
             -B name [-t name [name2 name3 ...]
                 [-e addr [addr2 ...] [-s subject_line] [-u]] [-z]}
            [-y flavor_id]
            [-v | -h]

    Arguments:
        -c master_cfg => Master configuration file.  Required arg.
        -r slave_cfg => Slave configuration file.  Required arg.
        -d dir path => Directory path to config files.  Required arg.

        -A => Check all databases and tables.
            -e addr [addr2 ...] => Sends output to one or more email addresses.
                -s subject_line => Subject line of email.
                -u => Override the default mail command and use mailx.
            -z => Suppress standard out.

        -B Database name => Name of database.
            -t Table name(s) => Name of tables, space delimited.
            -e addr [addr2 ...] => Sends output to one or more email addresses.
                -s subject_line => Subject line of email.
                -u => Override the default mail command and use mailx.
            -z => Suppress standard out.

        -y value => A flavor id for the program lock.  To create unique lock.
        -v => Display version of this program.
        -h => Help and usage message.

        NOTE 1:  -v or -h overrides the other options.

        NOTE 2:  -A and -B are required XOR arguments.

        NOTE 3:  -A option:  Some system tables may not be in sync in mysql and
             sys databases.

        NOTE 4:  -s option:  If not provided, then a default subject line will
            be created.

    Notes:
        Database configuration file format (config/mysql_cfg.py.TEMPLATE):
            # Configuration file for each Master/Slave Database
            user = "USER"
            japd = "PSWORD"
            host = "HOST_IP"
            name = "HOST_NAME"
            sid = SERVER_ID
            extra_def_file = "PYTHON_PROJECT/config/mysql.cfg"
            serv_os = "Linux"
            port = 3306
            cfg_file = "MYSQL_DIRECTORY/mysqld.cnf"

        NOTE 1:  Include the cfg_file even if running remotely as the file will
            be used in future releases.

        NOTE 2:  In MySQL 5.6 - it now gives warning if password is passed on
            the command line.  To suppress this warning, will require the use
            of the --defaults-extra-file option (i.e. extra_def_file) in the
            database configuration file.  See below for the defaults-extra-file
            format.

        configuration modules -> name is runtime dependent as it can be
            used to connect to different databases with different names.

        Defaults Extra File format (config/mysql.cfg.TEMPLATE):
            [client]
            password="PASSWORD"
            socket=DIRECTORY_PATH/mysql.sock

        NOTE:  The socket information can be obtained from the my.cnf
            file under ~/mysql directory.

    Example:
        mysql_rep_cmp.py -c master -r slave -d config -A

"""

# Libraries and Global Variables

# Standard
# For Python 2.6/2.7: Redirection of stdout in a print command.
from __future__ import print_function
import sys
import time

# Local
import lib.arg_parser as arg_parser
import lib.gen_libs as gen_libs
import lib.gen_class as gen_class
import mysql_lib.mysql_libs as mysql_libs
import mysql_lib.mysql_class as mysql_class
import version

__version__ = version.__version__

# Global
SUBJ_LINE = "MySQL_Replication_Comparsion"


def help_message():

    """Function:  help_message

    Description:  Displays the program's docstring which is the help and usage
        message when -h option is selected.

    Arguments:

    """

    print(__doc__)


def fetch_db_list(server, ign_db_list=None, db_name=None):

    """Function:  fetch_db_list

    Description:  Return list of database(s) minus any in the ignore database
        list or return the databases in the do list.

    Arguments:
        (input) server -> Server instance.
        (input) ign_db_list -> List of databases to be ignored.
        (input) db_name -> List of specify database names to be checked.
        (output) db_list | db_name -> List of databases.

    """

    if ign_db_list is None:
        ign_db_list = list()

    else:
        ign_db_list = list(ign_db_list)

    if db_name is None:
        db_name = list()

    else:
        db_name = list(db_name)

    if server.do_db:
        db_list = server.fetch_do_db()

    else:
        db_list = gen_libs.dict_2_list(mysql_libs.fetch_db_dict(server),
                                       "Database")

    if server.ign_db:
        ign_db_list = server.fetch_ign_db() + ign_db_list

    # Remove "ignore" databases from database list.
    db_list = gen_libs.del_not_and_list(db_list, ign_db_list)

    if db_name:
        return gen_libs.del_not_in_list(db_name, db_list)

    return db_list


def recur_tbl_cmp(master, slave, dbs, tbl, recur=0, **kwargs):

    """Function:  recur_tbl_cmp

    Description:  Recursive call to check a table between the master and
        replica databases.  Will compare the table's checksums and if not same,
        then recursively call itself to N levels with a specific time period
        between calls.

    Arguments:
        (input) master -> Master instance.
        (input) slave -> Slave instance.
        (input) dbs -> Database name.
        (input) tbl -> Table name.
        (input) recur -> Current level of recursion.
        (input) **kwargs:
            mail -> Mail class instance.
            no_std -> Suppress standard out.

    """

    mail = kwargs.get("mail", None)
    no_std = kwargs.get("no_std", False)

    if recur < 4:

        if mysql_libs.checksum(master, dbs, tbl) == \
           mysql_libs.checksum(slave, dbs, tbl):

            data = "\tChecking: {0} {1}".format(tbl.ljust(40), "Synced")

            if not no_std:
                print(data)

            if mail:
                mail.add_2_msg(data)

        else:
            time.sleep(5)
            recur_tbl_cmp(master, slave, dbs, tbl, recur + 1, mail=mail,
                          no_std=no_std)

    else:
        data = "\tChecking: {0} {1}".format(tbl.ljust(40),
                                            "Error:  Checksums do not match")

        if not no_std:
            print(data)

        if mail:
            mail.add_2_msg(data)


def run_cmp(master, slave, dbs, tbl_list, **kwargs):

    """Function:  run_cmp

    Description:  Run the table checksum comparsion between the master and
        replica databases.

    Arguments:
        (input) master -> Master instance.
        (input) slave -> Slave instance.
        (input) dbs -> Database name.
        (input) tbl_list -> List of tables to be compared.
        (input) **kwargs:
            mail -> Mail class instance.
            no_std -> Suppress standard out.

    """

    tbl_list = list(tbl_list)
    mail = kwargs.get("mail", None)
    no_std = kwargs.get("no_std", False)
    data = "\nDatabase: {0}".format(dbs)

    if not no_std:
        print(data)

    if mail:
        mail.add_2_msg(data)

    for tbl in tbl_list:
        # Recursive compare.
        recur = 1
        recur_tbl_cmp(master, slave, dbs, tbl, recur, mail=mail, no_std=no_std)


def setup_cmp(master, slave, sys_ign_db, db_name=None, tbl_name=None,
              **kwargs):

    """Function:  setup_cmp

    Description:  Setup the comparsion check getting list of databases and
        tables then calling the compare function.

    Arguments:
        (input) master -> Master instance.
        (input) slave -> Slave instance.
        (input) sys_ign_db -> List of system databases to ignore.
        (input) db_name -> List of database names.
        (input) tbl_name -> List of table names.
        (input) **kwargs:
            ign_db_tbl -> Dictionary-List of dbs & tables to be ignored.
            mail -> Mail class instance.
            no_std -> Suppress standard out.
            use_mailx -> Use the mailx command for sending emails.

    """

    if db_name is None:
        db_name = list()

    else:
        db_name = list(db_name)

    if tbl_name is None:
        tbl_name = list()

    else:
        tbl_name = list(tbl_name)

    sys_ign_db = list(sys_ign_db)
    ign_db_tbl = kwargs.get("ign_db_tbl", {})
    mail = kwargs.get("mail", None)
    no_std = kwargs.get("no_std", False)
    mst_dbs = fetch_db_list(master)
    slv_dbs = fetch_db_list(slave, sys_ign_db, db_name)
    db_list = gen_libs.del_not_in_list(mst_dbs, slv_dbs)
    slv_do_dict = slave.fetch_do_tbl()
    slv_ign_dict = slave.fetch_ign_tbl()

    for dbs in db_list:
        # Get master list of tables.
        mst_tbl_list = gen_libs.dict_2_list(mysql_libs.fetch_tbl_dict(
            master, dbs), "table_name")

        # Database in "to do" list.
        if dbs in slv_do_dict:
            slv_tbl_list = slv_do_dict[dbs]

        else:
            # Get list of tables from slave.
            slv_tbl_list = gen_libs.dict_2_list(
                mysql_libs.fetch_tbl_dict(slave, dbs), "table_name")

        slv_ign_tbl = []

        # Database in slave "ignore" list
        if dbs in slv_ign_dict:
            slv_ign_tbl = slv_ign_dict[dbs]

        if dbs in ign_db_tbl:
            slv_ign_tbl = slv_ign_tbl + ign_db_tbl[dbs]

        # Drop "ignore" tables.
        slv_tbl_list = gen_libs.del_not_and_list(slv_tbl_list, slv_ign_tbl)

        tbl_list = gen_libs.del_not_in_list(mst_tbl_list, slv_tbl_list)

        if tbl_name:
            tbl_list = gen_libs.del_not_in_list(tbl_list, tbl_name)

        run_cmp(master, slave, dbs, tbl_list, mail=mail, no_std=no_std)

    if mail:
        mail.send_mail(use_mailx=kwargs.get("use_mailx", False))


def run_program(args_array, sys_ign_db, **kwargs):

    """Function:  run_program

    Description:  Creates class instance(s) and controls flow of the program.

    Arguments:
        (input) args_array -> Array of command line options and values.
        (input) sys_ign_db -> List of system databases to ignore.

    """

    global SUBJ_LINE

    args_array = dict(args_array)
    sys_ign_db = list(sys_ign_db)
    mail = None
    use_mailx = False
    no_std = args_array.get("-z", False)
    master = mysql_libs.create_instance(args_array["-c"], args_array["-d"],
                                        mysql_class.MasterRep)
    master.connect(silent=True)
    slave = mysql_libs.create_instance(args_array["-r"], args_array["-d"],
                                       mysql_class.SlaveRep)
    slave.connect(silent=True)

    if master.conn_msg or slave.conn_msg:
        print("run_program: Error encountered with connection of master/slave")
        print("\tMaster:  %s" % (master.conn_msg))
        print("\tSlave:  %s" % (slave.conn_msg))

    else:
        if args_array.get("-e", None):
            mail = gen_class.setup_mail(args_array.get("-e"),
                                        subj=args_array.get("-s", SUBJ_LINE))
            use_mailx = args_array.get("-u", False)

        # Determine datatype of server_id and convert appropriately.
        #   Required for mysql.connector v1.1.6 as this version assigns the
        #   id to a different datatype then later mysql.connector versions.
        slv_list = gen_libs.dict_2_list(master.show_slv_hosts(), "Server_id")
        slv_id = str(slave.server_id) \
            if isinstance(slv_list[0], str) else slave.server_id

        # Is slave in replication with master
        if slv_id in slv_list:

            # Check specified tables in database
            if "-t" in args_array:
                setup_cmp(
                    master, slave, sys_ign_db, args_array["-B"],
                    args_array["-t"], mail=mail, no_std=no_std,
                    use_mailx=use_mailx, **kwargs)

            # Check single database
            elif "-B" in args_array:
                setup_cmp(
                    master, slave, sys_ign_db, args_array["-B"], "", mail=mail,
                    no_std=no_std, use_mailx=use_mailx, **kwargs)

            # Check all tables in all databases
            else:
                setup_cmp(
                    master, slave, sys_ign_db, "", "", mail=mail,
                    no_std=no_std, use_mailx=use_mailx, **kwargs)

            mysql_libs.disconnect(master, slave)

        else:
            mysql_libs.disconnect(master, slave)
            print("Error:  Replica is not in replication with Master.")


def main():

    """Function:  main

    Description:  Initializes program-wide used variables and processes command
        line arguments and values.

    Variables:
        dir_chk_list -> contains options which will be directories.
        ign_db_tbl -> contains list of databases and tables to be ignored.
        opt_con_req_list -> contains the options that require other options.
        opt_multi_list -> contains the options that will have multiple values.
        opt_req_list -> contains the options that are required for the program.
        opt_req_xor_list -> contains a list of options that are required XOR.
        opt_val_list -> contains options which require values.
        sys_ign_db -> contains a list of system databases to be ignored.

    Arguments:
        (input) argv -> Arguments from the command line.

    """

    cmdline = gen_libs.get_inst(sys)
    dir_chk_list = ["-d"]
    ign_db_tbl = {"mysql": ["innodb_index_stats", "innodb_table_stats",
                            "slave_master_info", "slave_relay_log_info",
                            "slave_worker_info"]}
    opt_con_req_list = {"-t": ["-B"], "-s": ["-e"], "-u": ["-e"]}
    opt_multi_list = ["-B", "-e", "-s", "-t"]
    opt_req_list = ["-r", "-c", "-d"]
    opt_req_xor_list = {"-A": "-B"}
    opt_val_list = ["-r", "-c", "-d", "-e", "-s", "-y"]
    sys_ign_db = ["performance_schema", "information_schema"]

    # Process argument list from command line.
    args_array = arg_parser.arg_parse2(cmdline.argv, opt_val_list,
                                       multi_val=opt_multi_list)

    if not gen_libs.help_func(args_array, __version__, help_message) \
       and arg_parser.arg_req_xor(args_array, opt_req_xor_list) \
       and not arg_parser.arg_require(args_array, opt_req_list) \
       and arg_parser.arg_cond_req(args_array, opt_con_req_list) \
       and not arg_parser.arg_dir_chk_crt(args_array, dir_chk_list):

        try:
            prog_lock = gen_class.ProgramLock(cmdline.argv,
                                              args_array.get("-y", ""))
            run_program(args_array, sys_ign_db, ign_db_tbl=ign_db_tbl)
            del prog_lock

        except gen_class.SingleInstanceException:
            print("WARNING:  lock in place for mysql_rep_cmp with id of: %s"
                  % (args_array.get("-y", "")))


if __name__ == "__main__":
    sys.exit(main())
