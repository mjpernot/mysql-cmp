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
            -i => Override the master/slave check and compare the databases.

        -y value => A flavor id for the program lock.  To create unique lock.
        -v => Display version of this program.
        -h => Help and usage message.

        NOTE 1:  -v or -h overrides the other options.

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

# Standard
import sys
import time
import pprint

try:
    import simplejson as json
except ImportError:
    import json

# Local
try:
    from .lib import gen_libs
    from .lib import gen_class
    from .mysql_lib import mysql_libs
    from .mysql_lib import mysql_class
    from . import version

except (ValueError, ImportError) as err:
    import lib.gen_libs as gen_libs                     # pylint:disable=R0402
    import lib.gen_class as gen_class                   # pylint:disable=R0402
    import mysql_lib.mysql_libs as mysql_libs           # pylint:disable=R0402
    import mysql_lib.mysql_class as mysql_class         # pylint:disable=R0402
    import version

__version__ = version.__version__

# Global


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

    db_dict = {}
    db_list = list(db_list)
    ign_db_tbl = dict(kwargs.get("ign_db_tbl", {}))

    for dbs in db_list:
        tbl_list = gen_libs.dict_2_list(
            mysql_libs.fetch_tbl_dict(server, dbs), dict_key)
        ign_tbls = ign_db_tbl[dbs] if dbs in ign_db_tbl else []
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

    db_dict = {}
    db_list = list(db_list)
    dict_key = "TABLE_NAME"
    ign_dbs = list(kwargs.get("ign_dbs", []))
    tbls = kwargs.get("tbls", [])
    ign_db_tbl = dict(kwargs.get("ign_db_tbl", {}))

    if db_list:
        db_list = gen_libs.del_not_and_list(db_list, ign_dbs)

        if len(db_list) == 1 and tbls:
            db_tables = gen_libs.dict_2_list(
                mysql_libs.fetch_tbl_dict(server, db_list[0]), dict_key)
            tbl_list = gen_libs.del_not_in_list(tbls, db_tables)
            ign_tbls = \
                ign_db_tbl[db_list[0]] if db_list[0] in ign_db_tbl else list()
            tbl_list = gen_libs.del_not_and_list(tbl_list, ign_tbls)
            db_dict[db_list[0]] = tbl_list

        elif db_list:
            db_dict = get_all_dbs_tbls(
                server, db_list, dict_key, ign_db_tbl=ign_db_tbl)

    else:
        db_list = gen_libs.dict_2_list(
            mysql_libs.fetch_db_dict(server), "Database")
        db_list = gen_libs.del_not_and_list(db_list, ign_dbs)

        if db_list:
            db_dict = get_all_dbs_tbls(
                server, db_list, dict_key, ign_db_tbl=ign_db_tbl)

    return db_dict


def get_json_template(server):

    """Function:  get_json_template

    Description:  Return a JSON template format.

    Arguments:
        (input) server -> Server instance
        (output) json_doc -> JSON filled-in template document

    """

    json_doc = {}
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

    data_config = {}
    data_config["to_addr"] = args.get_val("-e")
    data_config["subj"] = args.get_val("-s")
    data_config["mailx"] = args.get_val("-u", def_val=False)
    data_config["outfile"] = args.get_val("-o")
    data_config["mode"] = args.get_val("-w", def_val="w")
    data_config["expand"] = args.get_val("-p", def_val=False)
    data_config["indent"] = args.get_val("-n")
    data_config["suppress"] = args.get_val("-z", def_val=False)

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
        (output) state -> True|False - Successful operation
        (output) msg -> None or error message

    """

    state = True
    msg = None

    if not isinstance(data, dict):
        return False, f"Error: Is not a dictionary: {data}"

    mail = None
    data = dict(data)
    cfg = {"indent": kwargs.get("indent", 4)} if kwargs.get("indent", False) \
        else {}

    if kwargs.get("to_addr", False):
        subj = kwargs.get("subj", "MySQLRepCompare")
        mail = gen_class.setup_mail(kwargs.get("to_addr"), subj=subj)
        mail.add_2_msg(json.dumps(data, **cfg))
        mail.send_mail(use_mailx=kwargs.get("mailx", False))

    if kwargs.get("outfile", False):
        if kwargs.get("expand", False):
            with open(kwargs.get("outfile"), kwargs.get("mode", "w"),
                      encoding="UTF-8") as outfile:
                pprint.pprint(data, stream=outfile, **cfg)

        else:
            gen_libs.write_file(
                kwargs.get("outfile"), kwargs.get("mode", "w"),
                json.dumps(data, indent=kwargs.get("indent")))

    if not kwargs.get("suppress", False):
        if kwargs.get("expand", False):
            pprint.pprint(data, **cfg)

        else:
            print(data)

    return state, msg


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

    """

    if recur < 4:

        if mysql_libs.checksum(master, dbs, tbl) == \
           mysql_libs.checksum(slave, dbs, tbl):
            data = "Synced"

        else:
            time.sleep(5)
            data = recur_tbl_cmp(master, slave, dbs, tbl, recur + 1)

    else:
        data = "Checksums do not match"

    return data


def setup_cmp(args, master, slave):

    """Function:  setup_cmp

    Description:  Setup the comparsion check getting list of databases and
        tables then calling the compare function.

    Arguments:
        (input) args -> ArgParser class instance
        (input) master -> Master instance
        (input) slave -> Slave instance

    """

    db_list = args.get_val("-C", def_val=[])
    tbls = args.get_val("-t", def_val=[])
    cfg = gen_libs.load_module(args.get_val("-c"), args.get_val("-d"))
    mst_db_tbl = get_db_tbl(
        master, db_list=db_list, tbls=tbls, ign_dbs=cfg.ign_dbs,
        ign_db_tbl=cfg.ign_db_tbl)
    results = get_json_template(master)
    results["Master"] = master.name
    results["Slave"] = slave.name
    results["Checks"] = {}
    data_config = dict(create_data_config(args))

    for dbs in mst_db_tbl:                              # pylint:disable=C0206
        results["Checks"][dbs] = []
        for tbl in mst_db_tbl[dbs]:
            # Recursion
            recur = 1
            data = recur_tbl_cmp(master, slave, dbs, tbl, recur)
            results["Checks"][dbs].append({"Table": tbl, "Status": data})

    state = data_out(results, **data_config)

    if not state[0]:
        print(f"setup_cmp: Error encountered: {state[1]}")


def run_program(args):

    """Function:  run_program

    Description:  Creates class instance(s) and controls flow of the program.

    Arguments:
        (input) args -> ArgParser class instance

    """

    master = mysql_libs.create_instance(
        args.get_val("-c"), args.get_val("-d"), mysql_class.MasterRep)
    master.connect(silent=True)

    server_type = mysql_class.SlaveRep

    if args.arg_exist("-i"):
        server_type = mysql_class.Server

    slave = mysql_libs.create_instance(
        args.get_val("-r"), args.get_val("-d"), server_type)
    slave.connect(silent=True)

    if master.conn_msg or slave.conn_msg:
        print("run_program: Error encountered with connection of master/slave")
        print(f"\tMaster:  {master.conn_msg}")
        print(f"\tSlave:  {slave.conn_msg}")

    else:
        if args.arg_exist("-i"):
            setup_cmp(args, master, slave)
            mysql_libs.disconnect(master, slave)

        else:
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
        file_perms -> file check options with their perms in octal
        file_crt_list -> contains options which require files to be created
        multi_val -> contains the options that will have multiple values
        opt_con_req_list -> contains the options that require other options
        opt_def_dict -> contains options with their default values
        opt_req_list -> contains the options that are required for the program
        opt_req_xor_list -> contains a list of options that are required XOR
        opt_val_list -> contains options which require values

    Arguments:
        (input) argv -> Arguments from the command line

    """

    dir_perms_chk = {"-d": 5}
    file_perms = {"-o": 6}
    file_crt_list = ["-o"]
    multi_val = ["-C", "-e", "-s", "-t"]
    opt_con_req_list = {"-t": ["-C"], "-s": ["-e"], "-u": ["-e"], "-w": ["-o"]}
    opt_def_dict = {"-C": [], "-t": None, "-n": 4}
    opt_req_list = ["-r", "-c", "-d"]
    opt_val_list = ["-r", "-c", "-d", "-e", "-s", "-y", "-C", "-n", "-t"]

    # Process argument list from command line.
    args = gen_class.ArgParser(
        sys.argv, opt_val=opt_val_list, multi_val=multi_val,
        opt_def=opt_def_dict)

    if args.arg_parse2()                                                    \
       and not gen_libs.help_func(args, __version__, help_message)          \
       and args.arg_require(opt_req=opt_req_list)                           \
       and args.arg_cond_req(opt_con_req=opt_con_req_list)                  \
       and args.arg_dir_chk(dir_perms_chk=dir_perms_chk)                    \
       and args.arg_file_chk(file_perm_chk=file_perms, file_crt=file_crt_list):

        try:
            prog_lock = gen_class.ProgramLock(
                sys.argv, args.get_val("-y", def_val=""))
            run_program(args)
            del prog_lock

        except gen_class.SingleInstanceException:
            print(f'WARNING:  lock in place for mysql_rep_cmp with id of:'
                  f' {args.get_val("-y", def_val="")}')


if __name__ == "__main__":
    sys.exit(main())
