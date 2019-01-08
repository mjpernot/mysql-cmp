# Python project for comparing tables in a MySQL replication schema.
# Classification (U)

# Description:
  This program is used to compare tables between a master and slave database to ensure they are in sync.


###  This README file is broken down into the following sections:
  * Features
  * Prerequisites
  * Installation
  * Configuration
  * Program Description
  * Program Help Function
  * Help Message
  * Testing
    - Unit
    - Integration
    - Blackbox


# Features:
  * Compare tables between a master and slave database using checksum to ensure they are in sync.
  * Can check all tables in all databases, select databases, or select tables.

# Prerequisites:

  * List of Linux packages that need to be installed on the server.
    - python-libs
    - python-devel
    - git
    - python-pip

  * Local class/library dependencies within the program structure.
    - lib/cmds_gen
    - lib/arg_parser
    - lib/gen_libs
    - mysql_lib/mysql_libs
    - mysql_lib/mysql_class



# Installation:

Install this project using git.
  * Replace **{Python_Project}** with the baseline path of the python program.

```
umask 022
cd {Python_Project}
git clone git@sc.appdev.proj.coe.ic.gov:JAC-DSXD/mysql-cmp.git
```

Install/upgrade system modules.

```
cd mysql-cmp
umask 022
pip install -r requirements.txt --upgrade --trusted-host pypi.appdev.proj.coe.ic.gov
exit
```

Install supporting classes and libraries.

```
pip install -r requirements-python-lib.txt --target lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-mysql-lib.txt --target mysql_lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-python-lib.txt --target mysql_lib/lib --trusted-host pypi.appdev.proj.coe.ic.gov
```

# Configuration:

Create MySQL configuration file.
  * Replace **{Python_Project}** with the baseline path of the python program.

```
cd config
cp mysql_cfg.py.TEMPLATE mysql_cfg.py
```

Make the appropriate change to the environment.
  * Change these entries in the MySQL setup:
    - passwd = "ROOT_PASSWORD"
    - host = "SERVER_IP"
    - name = "HOST_NAME"
    - sid = SERVER_ID
    - extra_def_file = "{Python_Project}/config/mysql.cfg"

```
vim mysql_cfg.py
chmod 600 mysql_cfg.py
```

Create MySQL definition file.

```
cp mysql.cfg.TEMPLATE mysql.cfg
```

Make the appropriate change to the environment.
  * Change these entries in the MySQL definition file:
    - password="ROOT_PASSWORD"
    - socket={BASE_DIR}/mysql/tmp/mysql.sock

```
vim mysql.cfg
chmod 600 mysql.cfg
```

Create a MySQL slave configuration file.

```
cp slave.txt.TEMPLATE slave.txt
```

Make the appropriate change to the environment.
  * Change these entries in the MySQL slave setup:
    * NOTE:  Create a new set of entries for each slave in the MySQL replica set.
    - passwd = ROOT_PASSWORD
    - host = HOST_IP
    - name = HOSTNAME
    - sid = SERVER_ID

```
vim slave.txt
chmod 600 slave.txt
```


# Program Descriptions:
### Program: mysql_rep_cmp.py
##### Description: Administration program for the MySQL binary log system.


# Program Help Function:

  The program has a -h (Help option) that will show display an usage message.  The help message will usually consist of a description, usage, arugments to the program, example, notes about the program, and any known bugs not yet fixed.  To run the help command:
  * Replace **{Python_Project}** with the baseline path of the python program.

```
{Python_Project}/mysql-cmp/mysql_rep_cmp.py -h
```


# Help Message:
  Below is the help message for the program the program.  Run the program with the -h option get the latest help message for the program.

    Program:  mysql_rep_cmp.py

    Description:  Does a table checksum comparsion between a master database and
        a replica database.  This should determine whether the tables
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
        -t Table name(s) => Name of tables, space delimited.  Requires -B option
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



# Testing:


# Unit Testing:

### Description: Testing consists of unit testing for the functions in the mysql_rep_cmp.py program.

### Installation:

Install this project using git.
  * Replace **{Python_Project}** with the baseline path of the python program.
  * Replace **{Branch_Name}** with the name of the Git branch being tested.  See Git Merge Request.

```
umask 022
cd {Python_Project}
git clone --branch {Branch_Name} git@sc.appdev.proj.coe.ic.gov:JAC-DSXD/mysql-cmp.git
```

Install/upgrade system modules.

```
cd mysql-cmp
sudo bash
umask 022
pip install -r requirements.txt --upgrade --trusted-host pypi.appdev.proj.coe.ic.gov
exit
```

Install supporting classes and libraries.

```
pip install -r requirements-python-lib.txt --target lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-mysql-lib.txt --target mysql_lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-python-lib.txt --target mysql_lib/lib --trusted-host pypi.appdev.proj.coe.ic.gov
```


# Unit test runs for mysql_rep_cmp.py:
  * Replace **{Python_Project}** with the baseline path of the python program.

```
cd {Python_Project}/mysql-cmp
```

### Unit:  help_message
```
test/unit/mysql_rep_cmp/help_message.py
```

### Unit:  
```
test/unit/mysql_rep_cmp/
```

### Unit:  
```
test/unit/mysql_rep_cmp/
```

### Unit:  run_program
```
test/unit/mysql_rep_cmp/run_program.py
```

### Unit:  main
```
test/unit/mysql_rep_cmp/main.py
```

### All unit testing
```
test/unit/mysql_rep_cmp/unit_test_run.sh
```

### Code coverage program
```
test/unit/mysql_rep_cmp/code_coverage.sh
```


# Integration Testing:

### Description: Testing consists of integration testing of functions in the mysql_rep_cmp.py program.

### Installation:

Install this project using git.
  * Replace **{Python_Project}** with the baseline path of the python program.
  * Replace **{Branch_Name}** with the name of the Git branch being tested.  See Git Merge Request.

```
umask 022
cd {Python_Project}
git clone --branch {Branch_Name} git@sc.appdev.proj.coe.ic.gov:JAC-DSXD/mysql-cmp.git
```

Install/upgrade system modules.

```
cd mysql-cmp
sudo bash
umask 022
pip install -r requirements.txt --upgrade --trusted-host pypi.appdev.proj.coe.ic.gov
exit
```

Install supporting classes and libraries.

```
pip install -r requirements-python-lib.txt --target lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-mysql-lib.txt --target mysql_lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-python-lib.txt --target mysql_lib/lib --trusted-host pypi.appdev.proj.coe.ic.gov
```

### Configuration:

Create MySQL configuration file.
  * Replace **{Python_Project}** with the baseline path of the python program.

```
cd test/integration/mysql_rep_cmp/config
cp ../../../../config/mysql_cfg.py.TEMPLATE mysql_cfg.py
```

Make the appropriate change to the environment.
  * Change these entries in the MySQL setup.
    - passwd = "ROOT_PASSWORD"
    - host = "HOST_IP"
    - name = "HOSTNAME"
    - sid = SERVER_ID
    - extra_def_file = '{Python_Project}/config/mysql.cfg'

```
vim mysql_cfg.py
chmod 600 mysql_cfg.py
```

Create MySQL definition file.

```
cp ../../../../config/mysql.cfg.TEMPLATE mysql.cfg
```

Make the appropriate change to the MySQL definition setup.
  * Change these entries in the MySQL configuration file:
    - password="ROOT_PASSWORD"
    - socket={BASE_DIR}/mysql/tmp/mysql.sock

```
vim mysql.cfg
chmod 600 mysql.cfg
```

Create a MySQL slave configuration file.
```
cp ../../../../config/slave.txt.TEMPLATE slave.txt
```

Make the appropriate change to the environment.
  * Change these entries in the MySQL slave setup:
    * NOTE:  Create a new set of entries for each slave in the MySQL replica set.
    - passwd = ROOT_PASSWORD
    - host = HOST_IP
    - name = HOSTNAME
    - sid = SERVER_ID

```
vim slave.txt
chmod 600 slave.txt
```


# Integration test runs for mysql_rep_cmp.py:
  * Replace **{Python_Project}** with the baseline path of the python program.

```
cd {Python_Project}/mysql-cmp
```


### Integration:  
```
test/integration/mysql_rep_cmp/
```

### All integration testing
```
test/integration/mysql_rep_cmp/integration_test_run.sh
```

### Code coverage program
```
test/integration/mysql_rep_cmp/code_coverage.sh
```


# Blackbox Testing:

### Description: Testing consists of blackbox testing of the mysql_rep_cmp.py program.

### Installation:

Install this project using git.
  * Replace **{Python_Project}** with the baseline path of the python program.
  * Replace **{Branch_Name}** with the name of the Git branch being tested.  See Git Merge Request.

```
umask 022
cd {Python_Project}
git clone --branch {Branch_Name} git@sc.appdev.proj.coe.ic.gov:JAC-DSXD/mysql-cmp.git
```

Install/upgrade system modules.

```
cd mysql-cmp
sudo bash
umask 022
pip install -r requirements.txt --upgrade --trusted-host pypi.appdev.proj.coe.ic.gov
exit
```

Install supporting classes and libraries.

```
pip install -r requirements-python-lib.txt --target lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-mysql-lib.txt --target mysql_lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-python-lib.txt --target mysql_lib/lib --trusted-host pypi.appdev.proj.coe.ic.gov
```

### Configuration:

Create MySQL configuration file.
  * Replace **{Python_Project}** with the baseline path of the python program.

```
cd test/blackbox/mysql_rep_cmp/config
cp ../../../../config/mysql_cfg.py.TEMPLATE mysql_cfg.py
```

Make the appropriate change to the environment.
  * Change these entries in the MySQL setup:
    - passwd = "ROOT_PASSWORD"
    - host = "HOST_IP"
    - name = "HOSTNAME"
    - sid = SERVER_ID
    - extra_def_file = '{Python_Project}/config/mysql.cfg'

```
vim mysql_cfg.py
chmod 600 mysql_cfg.py
```

Create MySQL definition file.

```
cp ../../../../config/mysql.cfg.TEMPLATE mysql.cfg
```

Make the appropriate change to the MySQL definition setup.
  * Change these entries in the MySQL configuration file:
    - password="ROOT_PASSWORD"
    - socket={BASE_DIR}/mysql/tmp/mysql.sock

```
vim mysql.cfg
chmod 600 mysql.cfg
```

Create a MySQL slave configuration file.

```
cp ../../../../config/slave.txt.TEMPLATE slave.txt
```

Make the appropriate change to the environment.
  * Change these entries in the MySQL slave setup:
    * NOTE:  Create a new set of entries for each slave in the MySQL replica set.
    - passwd = ROOT_PASSWORD
    - host = HOST_IP
    - name = HOSTNAME
    - sid = SERVER_ID

```
vim slave.txt
chmod 600 slave.txt
```


# Blackbox test run for mysql_rep_cmp.py:
  * Replace **{Python_Project}** with the baseline path of the python program.

```
cd {Python_Project}/mysql-cmp
```


### Blackbox:  
```
test/blackbox/mysql_rep_cmp/blackbox_test.sh
```

