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
            {-C [db_name [db_name2 ...]] [-t table_name [table_name2 ...]] |
                 [-m config_file -i db_name:table_name] |
                 [-e to_email [to_email2 ...] [-s subject_line] [-u]] |
                 [-z] [-p [-n N]]]
            [-y flavor_id]
            [-v | -h]

    Arguments:
        -c master_cfg => Master configuration file.  Required arg.
        -r slave_cfg => Slave configuration file.  Required arg.
        -d dir path => Directory path to config files.  Required arg.

        -C [database_names] => Check one or more databases
            -t table name(s) => Table names to check.  If this option is used
                only one database will be checked based on the -C option.
            -m file => Mongo config file.  Is loaded as a python, do not
                include the .py extension with the name.
                -i {database:collection} => Name of database and collection.
                    Default: sysmon:mysql_db_admin
            -o path/file => Directory path and file name for output.
                -w a|w => Append or write to output to output file. Default is
                    write.
            -e to_email_address(es) => Enables emailing and sends output to one
                    or more email addresses.  Email addresses are delimited by
                    a space.
                -s subject_line => Subject line of email.
                -u => Override the default mail command and use mailx.
            -z => Suppress standard out.
            -p => Expand the JSON format.
                -n N => Indentation for expanded JSON format.

        -y value => A flavor id for the program lock.  To create unique lock.
        -v => Display version of this program.
        -h => Help and usage message.

        NOTE 1:  -v or -h overrides the other options.

        NOTE 2:  -s option:  If not provided, then a default subject line will
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
            ign_db_tbl = {
                "mysql": ["innodb_index_stats", "innodb_table_stats",
                "slave_master_info", "slave_relay_log_info",
                "slave_worker_info"]}
            ign_dbs = ["performance_schema", "information_schema"]

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
import pprint

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


def get_all_dbs_tbls(server, db_list, dict_key, **kwargs):

    """Function:  get_all_dbs_tbls

    Description:  Return a dictionary of databases with table lists.

    Arguments:
        (input) server -> Server instance
        (input) db_list -> List of database names
        (input) dict_key -> Dictionary key that is tuned to the Mysql version
        (input) kwargs:
            ign_db_tbl -> Database dictionary with list of tables to ignore
        (output) db_dict -> Dictionary of databases and lists of tables

    """

    db_dict = dict()
    db_list = list(db_list)
    ign_db_tbl = dict(kwargs.get("ign_db_tbl", dict()))

    for dbs in db_list:
        tbl_list = gen_libs.dict_2_list(
            mysql_libs.fetch_tbl_dict(server, dbs), dict_key)
        ign_tbls = ign_db_tbl[dbs] if dbs in ign_db_tbl else list()
        tbl_list = gen_libs.del_not_and_list(tbl_list, ign_tbls)
        db_dict[dbs] = tbl_list

    return db_dict


def get_db_tbl(server, db_list, **kwargs):

    """Function:  get_db_tbl

    Description:  Determines which databases and tables will be checked.

    Arguments:
        (input) server -> Server instance
        (input) db_list -> List of database names
        (input) **kwargs:
            ign_dbs -> List of databases to skip
            tbls -> List of tables to compare
            ign_db_tbl -> Database dictionary with list of tables to ignore
        (output) db_dict -> Dictionary of databases and lists of tables

    """

    db_dict = dict()
    db_list = list(db_list)
    dict_key = "TABLE_NAME" if server.version >= (8, 0) else "table_name"
    ign_dbs = list(kwargs.get("ign_dbs", list()))
    tbls = kwargs.get("tbls", list())
    ign_db_tbl = dict(kwargs.get("ign_db_tbl", dict()))

    if db_list:
        db_list = gen_libs.del_not_and_list(db_list, ign_dbs)

        if len(db_list) == 1 and tbls:
            db_tables = gen_libs.dict_2_list(
                mysql_libs.fetch_tbl_dict(server, db_list[0]), dict_key)
            tbl_list = gen_libs.del_not_in_list(tbls, db_tables)
            db_dict[db_list[0]] = tbl_list

        elif db_list:
            db_dict = get_all_dbs_tbls(
                server, db_list, dict_key, ign_db_tbl=ign_db_tbl)

        else:
            print("get_db_tbl 1: Warning:  No databases to process")

    else:
        db_list = gen_libs.dict_2_list(
            mysql_libs.fetch_db_dict(server), "Database")
        db_list = gen_libs.del_not_and_list(db_list, ign_dbs)

        if db_list:
            db_dict = get_all_dbs_tbls(
                server, db_list, dict_key, ign_db_tbl=ign_db_tbl)

        else:
            print("get_db_tbl 2: Warning:  No databases to process")

    return db_dict


def get_json_template(server):

    """Function:  get_json_template

    Description:  Return a JSON template format.

    Arguments:
        (input) server -> Server instance
        (output) json_doc -> JSON filled-in template document

    """

    json_doc = dict()
    json_doc["Platform"] = "MySQL"
    json_doc["Server"] = server.name
    json_doc["AsOf"] = gen_libs.get_date() + "T" + gen_libs.get_time()

    return json_doc


def create_data_config(args):

    """Function:  create_data_config

    Description:  Create data_out config parameters.

    Arguments:
        (input) args -> ArgParser class instance
        (output) data_config -> Dictionary for data_out config parameters

    """

    data_config = dict()
    data_config["to_addr"] = args.get_val("-e")
    data_config["subj"] = args.get_val("-s")
    data_config["mailx"] = args.get_val("-u", def_val=False)
    data_config["outfile"] = args.get_val("-o")
    data_config["mode"] = args.get_val("-w", def_val="w")
    data_config["expand"] = args.get_val("-p", def_val=False)
    data_config["indent"] = args.get_val("-n")
    data_config["suppress"] = args.get_val("-z", def_val=False)
    data_config["mongo"] = args.get_val("-m")
    data_config["db_tbl"] = args.get_val("-i")

    return data_config


def data_out(data, **kwargs):

    """Function:  data_out

    Description:  Outputs the data in a variety of formats and media.

    Arguments:
        (input) data -> JSON data document
        (input) kwargs:
            to_addr -> To email address
            subj -> Email subject line
            mailx -> True|False - Use mailx command
            outfile -> Name of output file name
            mode -> w|a => Write or append mode for file
            expand -> True|False - Expand the JSON format
            indent -> Indentation of JSON document if expanded
            suppress -> True|False - Suppress standard out
            mongo -> Mongo config file - Insert into Mongo database
            db_tbl -> database:table - Database name:Table name
        (output) state -> True|False - Successful operation
        (output) msg -> None or error message

    """

    global SUBJ_LINE

    state = True
    msg = None

    if not isinstance(data, dict):
        return False, "Error: Is not a dictionary: %s" % (data)

    mail = None
    data = dict(data)
    cfg = {"indent": kwargs.get("indent", 4)} if kwargs.get("indent", False) \
        else dict()

    if kwargs.get("to_addr", False):
        subj = kwargs.get("subj", SUBJ_LINE)
        mail = gen_class.setup_mail(kwargs.get("to_addr"), subj=subj)
        mail.add_2_msg(json.dumps(data, **cfg))
        mail.send_mail(use_mailx=kwargs.get("mailx", False))

    if kwargs.get("outfile", False):
        outfile = open(kwargs.get("outfile"), kwargs.get("mode", "w"))
        pprint.pprint(data, stream=outfile, **cfg)

    if not kwargs.get("suppress", False):
        if kwargs.get("expand", False):
            pprint.pprint(data, **cfg)

        else:
            print(data)

    if kwargs.get("mongo", False):
        dbs, tbl = kwargs.get("db_tbl").split(":")
        state, msg = mongo_libs.ins_doc(kwargs.get("mongo"), dbs, tbl, data)

    return state, msg


#def fetch_db_list(server, ign_db_list=None, db_name=None):

    """Function:  fetch_db_list

    Description:  Return list of database(s) minus any in the ignore database
        list or return the databases in the do list.

    Arguments:
        (input) server -> Server instance
        (input) ign_db_list -> List of databases to be ignored
        (input) db_name -> List of specify database names to be checked
        (output) db_list | db_name -> List of databases

    """

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
    """


#def recur_tbl_cmp(master, slave, dbs, tbl, recur=0, **kwargs):
def recur_tbl_cmp(master, slave, dbs, tbl, recur=0):

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
        (output) data -> Status of the table comparsion
#        (input) **kwargs:
#            mail -> Mail class instance
#            no_std -> Suppress standard out

    """

#    mail = kwargs.get("mail", None)
#    no_std = kwargs.get("no_std", False)

    if recur < 4:

        if mysql_libs.checksum(master, dbs, tbl) == \
           mysql_libs.checksum(slave, dbs, tbl):
            data = "Synced"

#            data = "\tChecking: {0} {1}".format(tbl.ljust(40), "Synced")
#
#            if not no_std:
#                print(data)
#
#            if mail:
#                mail.add_2_msg(data)

        else:
            time.sleep(5)
            data = recur_tbl_cmp(master, slave, dbs, tbl, recur + 1)
#            recur_tbl_cmp(master, slave, dbs, tbl, recur + 1, mail=mail,
#                          no_std=no_std)

    else:
        data = "Checksums do not match"

    return data

#        data = "\tChecking: {0} {1}".format(tbl.ljust(40),
#                                            "Error:  Checksums do not match")
#
#        if not no_std:
#            print(data)
#
#        if mail:
#            mail.add_2_msg(data)


#def run_cmp(master, slave, dbs, tbl_list, **kwargs):

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
    """


#def setup_cmp(master, slave, sys_ign_db, db_name=None, tbl_name=None,
#              **kwargs):
def setup_cmp(args, master, slave):

    """Function:  setup_cmp

    Description:  Setup the comparsion check getting list of databases and
        tables then calling the compare function.

    Arguments:
        (input) args -> ArgParser class instance
        (input) master -> Master instance
        (input) slave -> Slave instance
#        (input) sys_ign_db -> List of system databases to ignore
#        (input) db_name -> List of database names
#        (input) tbl_name -> List of table names
#        (input) **kwargs:
#            ign_db_tbl -> Dictionary-List of dbs & tables to be ignored
#            mail -> Mail class instance
#            no_std -> Suppress standard out
#            use_mailx -> Use the mailx command for sending emails

    """

#    db_name = list() if db_name is None else list(db_name)
#    tbl_name = list() if tbl_name is None else list(tbl_name)
#    sys_ign_db = list(sys_ign_db)
#    ign_db_tbl = kwargs.get("ign_db_tbl", dict())
#    mail = kwargs.get("mail", None)
#    no_std = kwargs.get("no_std", False)

    db_list = args.get_val("-C", def_val=list())
    tbls = args.get_val("-t", def_val=list())
    cfg = gen_libs.load_module(args.get_val("-c"), args.get_val("-d"))
    mst_db_tbl = get_db_tbl(
        master, db_list=db_list, tbls=tbls, ign_dbs=cfg.ign_dbs,
        ign_db_tbl=cfg.ign_db_tbl)
    results = get_json_template(master)
    results["Master"] = master.name
    results["Slave"] = slave.name
    results["Checks"] = dict()
    data_config = dict(create_data_config(args))

    for dbs in mst_db_tbl:
        results["Checks"][dbs] = list()
        for tbl in mst_db_tbl[dbs]:
            # Recursion
            recur = 1
            data = recur_tbl_cmp(master, slave, dbs, tbl, recur)
            results["Checks"][dbs].append({"Table": tbl, "Status": data})

    state = data_out(results, **data_config)

    if not state[0]:
        print("setup_cmp: Error encountered: %s" % (state[1]))

#    mst_dbs = fetch_db_list(master)
#    slv_dbs = fetch_db_list(slave, sys_ign_db, db_name)
#    db_list = gen_libs.del_not_in_list(mst_dbs, slv_dbs)
#    slv_do_dict = slave.fetch_do_tbl()
#    slv_ign_dict = slave.fetch_ign_tbl()
#    dict_key = "table_name"
#    # Determine the MySQL version for dictionary key name
#    if mysql_class.fetch_sys_var(master, "version",
#                                 level="session")["version"] >= "8.0":
#        dict_key = "TABLE_NAME"
#
#    for dbs in db_list:
#        # Get master list of tables.
#        mst_tbl_list = gen_libs.dict_2_list(mysql_libs.fetch_tbl_dict(
#            master, dbs), dict_key)
#
#        # Database in "to do" list.
#        if dbs in slv_do_dict:
#            slv_tbl_list = slv_do_dict[dbs]
#
#        else:
#            # Get list of tables from slave.
#            slv_tbl_list = gen_libs.dict_2_list(
#                mysql_libs.fetch_tbl_dict(slave, dbs), dict_key)
#
#        slv_ign_tbl = []
#
#        # Database in slave "ignore" list
#        if dbs in slv_ign_dict:
#            slv_ign_tbl = slv_ign_dict[dbs]
#
#        if dbs in ign_db_tbl:
#            slv_ign_tbl = slv_ign_tbl + ign_db_tbl[dbs]
#
#        # Drop "ignore" tables.
#        slv_tbl_list = gen_libs.del_not_and_list(slv_tbl_list, slv_ign_tbl)
#
#        tbl_list = gen_libs.del_not_in_list(mst_tbl_list, slv_tbl_list)
#
#        if tbl_name:
#            tbl_list = gen_libs.del_not_in_list(tbl_list, tbl_name)
#
#        run_cmp(master, slave, dbs, tbl_list, mail=mail, no_std=no_std)
#
#    if mail:
#        mail.send_mail(use_mailx=kwargs.get("use_mailx", False))


#def run_program(args, sys_ign_db, **kwargs):
def run_program(args):

    """Function:  run_program

    Description:  Creates class instance(s) and controls flow of the program.

    Arguments:
        (input) args -> ArgParser class instance
#        (input) sys_ign_db -> List of system databases to ignore

    """

#    global SUBJ_LINE

#    sys_ign_db = list(sys_ign_db)
#    mail = None
#    use_mailx = False
#    no_std = args.get_val("-z", def_val=False)
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
#        if args.get_val("-e", def_val=None):
#            mail = gen_class.setup_mail(
#                args.get_val("-e"), subj=args.get_val("-s", def_val=SUBJ_LINE))
#            use_mailx = args.get_val("-u", def_val=False)

        # Determine datatype of server_id and convert appropriately.
        #   Required for mysql.connector v1.1.6 as this version assigns the
        #   id to a different datatype then later mysql.connector versions.

        sid = "Server_Id" if master.version >= (8, 0, 26) else "Server_id"
        slv_list = gen_libs.dict_2_list(master.show_slv_hosts(), sid)
        slv_id = str(slave.server_id) \
            if isinstance(slv_list[0], str) else slave.server_id

        # Is slave in replication with master
        if slv_id in slv_list:

            setup_cmp(args, master, slave)
            """
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
            """

            mysql_libs.disconnect(master, slave)

        else:
            mysql_libs.disconnect(master, slave)
            print("Error:  Slave is not in replication with Master.")


def main():

    """Function:  main

    Description:  Initializes program-wide used variables and processes command
        line arguments and values.

    Variables:
        dir_perms_chk -> contains directories and their octal permissions
#        ign_db_tbl -> contains list of databases and tables to be ignored
        multi_val -> contains the options that will have multiple values
        opt_con_req_list -> contains the options that require other options
        opt_req_list -> contains the options that are required for the program
        opt_req_xor_list -> contains a list of options that are required XOR
        opt_val_list -> contains options which require values
#        sys_ign_db -> contains a list of system databases to be ignored

    Arguments:
        (input) argv -> Arguments from the command line

    """

    dir_perms_chk = {"-d": 5}
# Move to config file.
#    ign_db_tbl = {
#        "mysql": [
#            "innodb_index_stats", "innodb_table_stats", "slave_master_info",
#            "slave_relay_log_info", "slave_worker_info"]}
#    multi_val = ["-B", "-e", "-s", "-t"]
    multi_val = ["-C", "-e", "-s", "-t"]
#    opt_con_req_list = {"-t": ["-C"], "-s": ["-e"], "-u": ["-e"]}
    opt_con_req_list = {"-t": ["-B"], "-s": ["-e"], "-u": ["-e"]}
    opt_req_list = ["-r", "-c", "-d"]
#    opt_req_xor_list = {"-A": "-B"}
    opt_val_list = ["-r", "-c", "-d", "-e", "-s", "-y"]
# Move to config file.
#    sys_ign_db = ["performance_schema", "information_schema"]

    # Process argument list from command line.
    args = gen_class.ArgParser(
        sys.argv, opt_val=opt_val_list, multi_val=multi_val, do_parse=True)

#       and args.arg_req_xor(opt_xor=opt_req_xor_list)           \
    if not gen_libs.help_func(args, __version__, help_message)  \
       and args.arg_require(opt_req=opt_req_list)               \
       and args.arg_cond_req(opt_con_req=opt_con_req_list)      \
       and args.arg_dir_chk(dir_perms_chk=dir_perms_chk):

        try:
            prog_lock = gen_class.ProgramLock(
                sys.argv, args.get_val("-y", def_val=""))
#            run_program(args, sys_ign_db, ign_db_tbl=ign_db_tbl)
            run_program(args)
            del prog_lock

        except gen_class.SingleInstanceException:
            print("WARNING:  lock in place for mysql_rep_cmp with id of: %s"
                  % (args.get_val("-y", def_val="")))


if __name__ == "__main__":
    sys.exit(main())
