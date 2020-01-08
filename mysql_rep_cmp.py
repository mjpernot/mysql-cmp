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
        mysql_rep_cmp.py -c file -r file -d path
            {-A | -B name [-t name1 [name2 name3 ...]} [-v | -h]

    Arguments:
        -c file => Master configuration file.  Required arg.
        -r file => Replica configuration file.  Required arg.
        -d dir path => Directory path to config files.  Required arg.
        -A => Check of all databases and tables.  Required XOR arg.
        -B Database name => Name of database.  Required XOR arg.
        -t Table name(s) => Name of tables, space delimited.
            Requires -B option.
        -v => Display version of this program.
        -h => Help and usage message.

        NOTE 1:  -v or -h overrides the other options.

        NOTE 2:  -A and -B are required XOR arguments.

    Notes:
        Database configuration file format (mysql_{host}.py):
            # Configuration file for {Database Name/Server}
            user = "root"
            passwd = "ROOT_PASSWORD"
            host = "IP_ADDRESS"
            serv_os = "Linux" or "Solaris"
            name = "HOSTNAME"
            port = PORT_NUMBER (default of mysql is 3306)
            cfg_file = "DIRECTORY_PATH/my.cfg"
            sid = "SERVER_ID"
            extra_def_file = "DIRECTORY_PATH/myextra.cfg"

        Slave configuration file is the same format as the Master.

        NOTE:  Include the cfg_file even if running remotely as the file will
            be used in future releases.

        configuration modules -> name is runtime dependent as it can be
            used to connect to different databases with different names.

        Defaults Extra File format (filename.cfg):
            [client]
            password="ROOT_PASSWORD"
            socket="DIRECTORY_PATH/mysql.sock"

        NOTE:  The socket information can be obtained from the my.cnf
            file under ~/mysql directory.

    Example:
        mysql_rep_cmp.py -r slave -c master -d config -A

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
import lib.cmds_gen as cmds_gen
import mysql_lib.mysql_libs as mysql_libs
import mysql_lib.mysql_class as mysql_class
import version

__version__ = version.__version__


def help_message():

    """Function:  help_message

    Description:  Displays the program's docstring which is the help and usage
        message when -h option is selected.

    Arguments:

    """

    print(__doc__)


def fetch_db_list(server, ign_db_list=None, db_name=None, **kwargs):

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

    else:
        return db_list


def recur_tbl_cmp(master, slave, db, tbl, recur, **kwargs):

    """Function:  recur_tbl_cmp

    Description:  Recursive call to check a table between the master and
        replica databases.  Will compare the table's checksums and if not same,
        then recursively call itself to N levels with a specific time period
        between calls.

    Arguments:
        (input) master -> Master instance.
        (input) slave -> Slave instance.
        (input) db -> Database name.
        (input) tbl -> Table name.
        (input) recur -> Current level of recursion.

    """

    if recur < 4:

        if mysql_libs.checksum(master, db, tbl) == \
           mysql_libs.checksum(slave, db, tbl):
            print("Synced")
            return

        else:
            recur += 1
            time.sleep(5)

            recur_tbl_cmp(master, slave, db, tbl, recur)

    else:
        print("Error:  Checksums do not match.")
        return


def run_cmp(master, slave, db, tbl_list, **kwargs):

    """Function:  run_cmp

    Description:  Run the table checksum comparsion between the master and
        replica databases.

    Arguments:
        (input) master -> Master instance.
        (input) slave -> Slave instance.
        (input) db -> Database name.
        (input) tbl_list -> List of tables to be compared.

    """

    tbl_list = list(tbl_list)
    print("\nDatabase: {0}".format(db))

    for tbl in tbl_list:
        print("\tChecking: {0}".format(tbl.ljust(40)), end="")
        recur = 1

        # Recursive compare.
        recur_tbl_cmp(master, slave, db, tbl, recur)


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
    ign_db_tbl = kwargs.get("ign_db_tbl", None)
    mst_dbs = fetch_db_list(master)
    slv_dbs = fetch_db_list(slave, sys_ign_db, db_name)
    db_list = gen_libs.del_not_in_list(mst_dbs, slv_dbs)
    slv_do_dict = slave.fetch_do_tbl()
    slv_ign_dict = slave.fetch_ign_tbl()

    for db in db_list:
        # Get master list of tables.
        mst_tbl_list = gen_libs.dict_2_list(mysql_libs.fetch_tbl_dict(
            master, db), "table_name")

        # Database in "to do" list.
        if db in slv_do_dict:
            slv_tbl_list = slv_do_dict[db]

        else:
            # Get list of tables from slave.
            slv_tbl_list = gen_libs.dict_2_list(
                mysql_libs.fetch_tbl_dict(slave, db), "table_name")

        slv_ign_tbl = []

        # Database in slave "ignore" list
        if db in slv_ign_dict:
            slv_ign_tbl = slv_ign_dict[db]

        if db in ign_db_tbl:
            slv_ign_tbl = slv_ign_tbl + ign_db_tbl[db]

        # Drop "ignore" tables.
        slv_tbl_list = gen_libs.del_not_and_list(slv_tbl_list, slv_ign_tbl)

        tbl_list = gen_libs.del_not_in_list(mst_tbl_list, slv_tbl_list)

        if tbl_name:
            tbl_list = gen_libs.del_not_in_list(tbl_list, tbl_name)

        run_cmp(master, slave, db, tbl_list)


def run_program(args_array, sys_ign_db, **kwargs):

    """Function:  run_program

    Description:  Creates class instance(s) and controls flow of the program.

    Arguments:
        (input) args_array -> Array of command line options and values.
        (input) sys_ign_db -> List of system databases to ignore.

    """

    args_array = dict(args_array)
    sys_ign_db = list(sys_ign_db)
    master = mysql_libs.create_instance(args_array["-c"], args_array["-d"],
                                        mysql_class.MasterRep)
    master.connect()
    slave = mysql_libs.create_instance(args_array["-r"], args_array["-d"],
                                       mysql_class.SlaveRep)
    slave.connect()

    # Is slave in replication with master
    if slave.server_id in gen_libs.dict_2_list(master.show_slv_hosts(),
                                               "Server_id"):

        # Check specified tables in database
        if "-t" in args_array:
            setup_cmp(master, slave, sys_ign_db, args_array["-B"],
                      args_array["-t"], **kwargs)

        # Check single database
        elif "-B" in args_array:
            setup_cmp(master, slave, sys_ign_db, args_array["-B"], "",
                      **kwargs)

        # Check all tables in all databases
        else:
            setup_cmp(master, slave, sys_ign_db, "", "", **kwargs)

        cmds_gen.disconnect(master, slave)

    else:
        cmds_gen.disconnect(master, slave)
        sys.exit("Error:  Replica is not in replication with Master.")


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

    dir_chk_list = ["-d"]
    ign_db_tbl = {"mysql": ["innodb_index_stats", "innodb_table_stats",
                            "slave_master_info", "slave_relay_log_info",
                            "slave_worker_info"]}
    opt_con_req_list = {"-t": ["-B"]}
    opt_multi_list = ["-B", "-t"]
    opt_req_list = ["-r", "-c", "-d"]
    opt_req_xor_list = {"-A": "-B"}
    opt_val_list = ["-r", "-c", "-d"]
    sys_ign_db = ["performance_schema", "information_schema"]

    # Process argument list from command line.
    args_array = arg_parser.arg_parse2(sys.argv, opt_val_list,
                                       multi_val=opt_multi_list)

    if not gen_libs.help_func(args_array, __version__, help_message) \
       and arg_parser.arg_req_xor(args_array, opt_req_xor_list) \
       and not arg_parser.arg_require(args_array, opt_req_list) \
       and arg_parser.arg_cond_req(args_array, opt_con_req_list) \
       and not arg_parser.arg_dir_chk_crt(args_array, dir_chk_list):
        run_program(args_array, sys_ign_db, ign_db_tbl=ign_db_tbl)


if __name__ == "__main__":
    sys.exit(main())
