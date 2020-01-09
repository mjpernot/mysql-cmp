# Python project for comparing tables in a MySQL replication schema.
# Classification (U)

# Description:
  This program is used to compare tables between a master and slave database to ensure they are in sync.


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
    - python-libs
    - python-devel
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

Create MySQL definition file for Master database.

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

For the Slave database, create a seperate MySQL configuration and MySQL definition file.

Make the appropriate change to the Slave environment.  See above for the changes required in each file.  In addition, the "extra_def_file" entry will require "mysql.cfg" to be changed to "mysql\_{SlaveName}.cfg".

```
cp mysql_cfg.py.TEMPLATE mysql_cfg_{SlaveName}.py
vim mysql_cfg_{SlaveName}.py
chmod 600 mysql_cfg_{SlaveName}.py
cp mysql.cfg.TEMPLATE mysql_{SlaveName}.cfg
vim mysql_{SlaveName}.cfg
chmod 600 mysql_{SlaveName}.cfg
```


# Program Help Function:

  The program has a -h (Help option) that will show display an usage message.  The help message will usually consist of a description, usage, arugments to the program, example, notes about the program, and any known bugs not yet fixed.  To run the help command:
  * Replace **{Python_Project}** with the baseline path of the python program.

```
{Python_Project}/mysql-cmp/mysql_rep_cmp.py -h
```


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

### Unit testing:
```
cd {Python_Project}/mysql-cmp
test/unit/mysql_rep_cmp/fetch_db_list.py
test/unit/mysql_rep_cmp/help_message.py
test/unit/mysql_rep_cmp/main.py
test/unit/mysql_rep_cmp/recur_tbl_cmp.py
test/unit/mysql_rep_cmp/run_cmp.py
test/unit/mysql_rep_cmp/run_program.py
test/unit/mysql_rep_cmp/setup_cmp.py
```

### All unit testing
```
test/unit/mysql_rep_cmp/unit_test_run.sh
```

### Code coverage program
```
test/unit/mysql_rep_cmp/code_coverage.sh
```

