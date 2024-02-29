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
    - Centos 7 (Running Python 2.7):
      -> python-pip
    - Redhat 8 (Running Python 3.6):
      -> python3-pip


# Installation:

Install this project using git.
  * From here on out, any reference to **{Python_Project}** or **PYTHON_PROJECT** replace with the baseline path of the python program.

```
git clone git@sc.appdev.proj.coe.ic.gov:JAC-DSXD/mysql-cmp.git
cd mysql-cmp
```

Install/upgrade system modules.

Centos 7 (Running Python 2.7):
```
sudo pip install -r requirements.txt --upgrade --trusted-host pypi.appdev.proj.coe.ic.gov
```

Redhat 8 (Running Python 3.6):
NOTE: Install as the user that will run the program.

```
python -m pip install --user -r requirements3.txt --upgrade --trusted-host pypi.appdev.proj.coe.ic.gov
```


Install supporting classes and libraries.

Centos 7 (Running Python 2.7):
```
pip install -r requirements-python-lib.txt --target lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-mysql-lib.txt --target mysql_lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-python-lib.txt --target mysql_lib/lib --trusted-host pypi.appdev.proj.coe.ic.gov
```

Redhat 8 (Running Python 3.6):
```
python -m pip install -r requirements-python-lib.txt --target lib --trusted-host pypi.appdev.proj.coe.ic.gov
python -m pip install -r requirements-mysql-lib.txt --target mysql_lib --trusted-host pypi.appdev.proj.coe.ic.gov
python -m pip install -r requirements-mysql-python-lib.txt --target mysql_lib/lib --trusted-host pypi.appdev.proj.coe.ic.gov
```


# Configuration:

Create MySQL configuration file for Master database.
Make the appropriate change to the environment.
  * Change these entries in the MySQL setup:
    - user = "USER"
    - passwd = "PASSWORD"
    - host = "HOST_IP"
    - name = "HOST_NAME"
    - sid = SERVER_ID
    - extra_def_file = "DIRECTORY_PATH/config/mysql.cfg"
    - cfg_file = "MYSQL_DIRECTORY/mysqld.cnf"

  * Change these entries only if required:
    - serv_os = Linux
    - port = 3306

  * If SSL connections are being used, configure one or more of these entries:
    - ssl_client_ca = None
    - ssl_client_key = None
    - ssl_client_cert = None

  * Only changes these if necessary and have knowledge in MySQL SSL configuration setup:
    - ssl_client_flag = None
    - ssl_disabled = False
    - ssl_verify_id = False
    - ssl_verify_cert = False

```
cd config
cp mysql_cfg.py.TEMPLATE mysql_cfg.py
vim mysql_cfg.py
chmod 600 mysql_cfg.py
```

Create MySQL definition file for Master database.
Make the appropriate change to the environment.
  * Change these entries in the MySQL definition file:
  * Note:  socket use is only required to be set in certain conditions when connecting using localhost.
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

```
{Python_Project}/mysql-cmp/mysql_rep_cmp.py -h
```


# Testing:

# Unit Testing:

### Installation:

Install the project using the procedures in the Installation section.

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

