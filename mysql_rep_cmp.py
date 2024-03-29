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

            # If SSL connections are being used, configure one or more of these
                entries:
            ssl_client_ca = None
            ssl_client_key = None
            ssl_client_cert = None

            # Only changes these if necessary and have knowledge in MySQL
                SSL configuration setup:
            ssl_client_flag = None
            ssl_disabled = False
            ssl_verify_id = False
            ssl_verify_cert = False

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

        NOTE 1:  The socket information can be obtained from the my.cnf
            file under ~/mysql directory.
        NOTE 2:  Socket use is only required to be set in certain conditions
            when connecting using localhost.

    Example:
        mysql_rep_cmp.py -c master -r slave -d config -A

"""

# Libraries and Global Variables
from __future__ import print_function
from __future__ import absolute_import

# Standard
import sys
import time

# Local
try:
    from .lib import gen_libs
    from .lib import gen_class
    from .mysql_lib import mysql_libs
    from .mysql_lib import mysql_class
    from . import version

except (ValueError, ImportError) as err:
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
        (input) server -> Server instance
        (input) ign_db_list -> List of databases to be ignored
        (input) db_name -> List of specify database names to be checked
        (output) db_list | db_name -> List of databases

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
        (input) master -> Master instance
        (input) slave -> Slave instance
        (input) dbs -> Database name
        (input) tbl -> Table name
        (input) recur -> Current level of recursion
        (input) **kwargs:
            mail -> Mail class instance
            no_std -> Suppress standard out

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
        (input) master -> Master instance
        (input) slave -> Slave instance
        (input) dbs -> Database name
        (input) tbl_list -> List of tables to be compared
        (input) **kwargs:
            mail -> Mail class instance
            no_std -> Suppress standard out

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
        (input) master -> Master instance
        (input) slave -> Slave instance
        (input) sys_ign_db -> List of system databases to ignore
        (input) db_name -> List of database names
        (input) tbl_name -> List of table names
        (input) **kwargs:
            ign_db_tbl -> Dictionary-List of dbs & tables to be ignored
            mail -> Mail class instance
            no_std -> Suppress standard out
            use_mailx -> Use the mailx command for sending emails

    """

    db_name = list() if db_name is None else list(db_name)
    tbl_name = list() if tbl_name is None else list(tbl_name)
    sys_ign_db = list(sys_ign_db)
    ign_db_tbl = kwargs.get("ign_db_tbl", dict())
    mail = kwargs.get("mail", None)
    no_std = kwargs.get("no_std", False)
    mst_dbs = fetch_db_list(master)
    slv_dbs = fetch_db_list(slave, sys_ign_db, db_name)
    db_list = gen_libs.del_not_in_list(mst_dbs, slv_dbs)
    slv_do_dict = slave.fetch_do_tbl()
    slv_ign_dict = slave.fetch_ign_tbl()
    dict_key = "table_name"

    # Determine the MySQL version for dictionary key name
    if mysql_class.fetch_sys_var(master, "version",
                                 level="session")["version"] >= "8.0":
        dict_key = "TABLE_NAME"

    for dbs in db_list:
        # Get master list of tables.
        mst_tbl_list = gen_libs.dict_2_list(mysql_libs.fetch_tbl_dict(
            master, dbs), dict_key)

        # Database in "to do" list.
        if dbs in slv_do_dict:
            slv_tbl_list = slv_do_dict[dbs]

        else:
            # Get list of tables from slave.
            slv_tbl_list = gen_libs.dict_2_list(
                mysql_libs.fetch_tbl_dict(slave, dbs), dict_key)

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


def run_program(args, sys_ign_db, **kwargs):

    """Function:  run_program

    Description:  Creates class instance(s) and controls flow of the program.

    Arguments:
        (input) args -> ArgParser class instance
        (input) sys_ign_db -> List of system databases to ignore

    """

    global SUBJ_LINE

    sys_ign_db = list(sys_ign_db)
    mail = None
    use_mailx = False
    no_std = args.get_val("-z", def_val=False)
    master = mysql_libs.create_instance(
        args.get_val("-c"), args.get_val("-d"), mysql_class.MasterRep)
    master.connect(silent=True)
    slave = mysql_libs.create_instance(
        args.get_val("-r"), args.get_val("-d"), mysql_class.SlaveRep)
    slave.connect(silent=True)

    if master.conn_msg or slave.conn_msg:
        print("run_program: Error encountered with connection of master/slave")
        print("\tMaster:  %s" % (master.conn_msg))
        print("\tSlave:  %s" % (slave.conn_msg))

    else:
        if args.get_val("-e", def_val=None):
            mail = gen_class.setup_mail(
                args.get_val("-e"), subj=args.get_val("-s", def_val=SUBJ_LINE))
            use_mailx = args.get_val("-u", def_val=False)

        # Determine datatype of server_id and convert appropriately.
        #   Required for mysql.connector v1.1.6 as this version assigns the
        #   id to a different datatype then later mysql.connector versions.

        sid = "Server_Id" if master.version >= (8, 0, 26) else "Server_id"
        slv_list = gen_libs.dict_2_list(master.show_slv_hosts(), sid)
        slv_id = str(slave.server_id) \
            if isinstance(slv_list[0], str) else slave.server_id

        # Is slave in replication with master
        if slv_id in slv_list:

            # Check specified tables in database
            if args.arg_exist("-t"):
                setup_cmp(
                    master, slave, sys_ign_db, args.get_val("-B"),
                    args.get_val("-t"), mail=mail, no_std=no_std,
                    use_mailx=use_mailx, **kwargs)

            # Check single database
            elif args.arg_exist("-B"):
                setup_cmp(
                    master, slave, sys_ign_db, args.get_val("-B"), "",
                    mail=mail, no_std=no_std, use_mailx=use_mailx, **kwargs)

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
        dir_perms_chk -> contains directories and their octal permissions
        ign_db_tbl -> contains list of databases and tables to be ignored
        multi_val -> contains the options that will have multiple values
        opt_con_req_list -> contains the options that require other options
        opt_req_list -> contains the options that are required for the program
        opt_req_xor_list -> contains a list of options that are required XOR
        opt_val_list -> contains options which require values
        sys_ign_db -> contains a list of system databases to be ignored

    Arguments:
        (input) argv -> Arguments from the command line

    """

    dir_perms_chk = {"-d": 5}
    ign_db_tbl = {
        "mysql": [
            "innodb_index_stats", "innodb_table_stats", "slave_master_info",
            "slave_relay_log_info", "slave_worker_info"]}
    multi_val = ["-B", "-e", "-s", "-t"]
    opt_con_req_list = {"-t": ["-B"], "-s": ["-e"], "-u": ["-e"]}
    opt_req_list = ["-r", "-c", "-d"]
    opt_req_xor_list = {"-A": "-B"}
    opt_val_list = ["-r", "-c", "-d", "-e", "-s", "-y"]
    sys_ign_db = ["performance_schema", "information_schema"]

    # Process argument list from command line.
    args = gen_class.ArgParser(
        sys.argv, opt_val=opt_val_list, multi_val=multi_val, do_parse=True)

    if not gen_libs.help_func(args, __version__, help_message)  \
       and args.arg_req_xor(opt_xor=opt_req_xor_list)           \
       and args.arg_require(opt_req=opt_req_list)               \
       and args.arg_cond_req(opt_con_req=opt_con_req_list)      \
       and args.arg_dir_chk(dir_perms_chk=dir_perms_chk):

        try:
            prog_lock = gen_class.ProgramLock(
                sys.argv, args.get_val("-y", def_val=""))
            run_program(args, sys_ign_db, ign_db_tbl=ign_db_tbl)
            del prog_lock

        except gen_class.SingleInstanceException:
            print("WARNING:  lock in place for mysql_rep_cmp with id of: %s"
                  % (args.get_val("-y", def_val="")))


if __name__ == "__main__":
    sys.exit(main())
