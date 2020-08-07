# Python project for comparing tables in a MySQL replication schema.
# Classification (U)

# Description:
  Used to compare tables between a master and slave database to ensure they are in sync.


###  This README file is broken down into the following sections:
  * Features
  * Prerequisites
  * Installation
  * Configuration
  * Program Help Function
  * Testing
    - Unit


# Features:
  * Compare tables between a master and slave database using checksum to ensure they are in sync.
  * Can check all tables in all databases, select databases, or select tables.

# Prerequisites:

  * List of Linux packages that need to be installed on the server.
    - git
    - python-pip

  * Local class/library dependencies within the program structure.
    - lib/cmds_gen
    - lib/arg_parser
    - lib/gen_libs
    - lib/gen_class
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

Create MySQL configuration file for Master database.
Make the appropriate change to the environment.
  * Change these entries in the MySQL setup:
    - user = "USER"
    - passwd = "PASSWORD"
    - host = "SERVER_IP"
    - name = "HOST_NAME"
    - sid = SERVER_ID
    - extra_def_file = "DIRECTORY_PATH/config/mysql.cfg"
    - cfg_file = "MYSQL_DIRECTORY/mysqld.cnf"
  * Change these entries only if required:
    - serv_os = Linux
    - port = 3306

```
cd config
cp mysql_cfg.py.TEMPLATE mysql_cfg.py
vim mysql_cfg.py
chmod 600 mysql_cfg.py
```

Create MySQL definition file for Master database.
Make the appropriate change to the environment.
  * Change these entries in the MySQL definition file:
    - password="PASSWORD"
    - socket=MYSQL_DIRECTORY/mysql.sock

```
cp mysql.cfg.TEMPLATE mysql.cfg
vim mysql.cfg
chmod 600 mysql.cfg
```

For the Slave database, create a seperate MySQL configuration and MySQL definition file.

Make the appropriate change to the Slave environment.  See above for the changes required in each file.  In addition, the "extra_def_file" entry will require "mysql.cfg" to be changed to "mysql\_SLAVENAME.cfg".
  * Replace **SLAVENAME** with the name of the slave being compared to.

```
cp mysql_cfg.py.TEMPLATE mysql_cfg_SLAVENAME.py
vim mysql_cfg_SLAVENAME.py
chmod 600 mysql_cfg_SLAVENAME.py
cp mysql.cfg.TEMPLATE mysql_SLAVENAME.cfg
vim mysql_SLAVENAME.cfg
chmod 600 mysql_SLAVENAME.cfg
```


# Program Help Function:

  The program has a -h (Help option) that will show display an usage message.  The help message will usually consist of a description, usage, arugments to the program, example, notes about the program, and any known bugs not yet fixed.  To run the help command:
  * Replace **{Python_Project}** with the baseline path of the python program.

```
{Python_Project}/mysql-cmp/mysql_rep_cmp.py -h
```


# Testing:

# Unit Testing:

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

### Testing:

```
cd {Python_Project}/mysql-cmp
test/unit/mysql_rep_cmp/unit_test_run.sh
```

### Code coverage:

```
cd {Python_Project}/mysql-cmp
test/unit/mysql_rep_cmp/code_coverage.sh
```

