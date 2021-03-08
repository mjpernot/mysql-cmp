# Changelog
All notable changes to this project will be documented in this file.

The format is based on "Keep a Changelog".  This project adheres to Semantic Versioning.


## [3.2.0] - 2020-08-07
- Updated to use the mysql_libs v5.0.0 library.
- Updated to work with (much older) mysql.connector v1.1.6 library module.

### Added
- Added email capability for output of comparsion checks.
- Added standard out suppression option.
- Allow to override the default sendmail (postfix) and use mailx command.

### Fixed
- main:  Fixed handling command line arguments from SonarQube scan finding.
- config/mysql.cfg.TEMPLATE:  Point to correct socket file.

### Changed
- run_program:  Added silent option to the connect methods.
- run_program:  Replaced cmds_gen.disconnect with mysql_libs.connect.
- run_program:  Refactored part of the function to reduce complexity.
- run_program:  Check and process connection status for master and slave connections.
- run_program:  Determine if mail will use sendmail or mailx.
- fetch_db_list:  Remove \*\*kwargs from argument list.
- run_program:  Determine if server_id from the server is a string or integer and convert the slave's server_id to corresponding datatype.
- recur_tbl_cmp:  Removed unnecessary returns.
- config/mysql_cfg.py.TEMPLATE:  Changed configuration entry.
- setup_cmp, run_cmp, recur_tbl_cmp:  Changed variable name to standard naming convention.
- fetch_db_list:  Removed unnecessary else clause in if statement.
- recur_tbl_cmp:  Added checks for standard out prints for standard out suppression and passed no_std to recursive call.
- run_cmp:  Added check for standard out prints for standard out suppression and passed to recur_tbl_cmp function.
- setup_cmp:  Passed standard out suppression to function as keyword arg.
- run_program:  Determined if standard out suppression was selected and passed to setup_cmp.
- recur_tbl_cmp:  Added statements to email instance and passed email to recursive call.
- recur_tbl_cmp:  Added print check statement from run_cmp function.
- run_cmp:  Moved print check statement into recur_tbl_cmp function.
- run_cmp:  Added statements to email instance and passed email to relevant functions.
- setup_cmp:  Send email if email instance exists along with use_mailx option and passed email to relevant functions.
- run_program:  Created email instance, added default subject line, and passed to relevant functions.
- main:  Added -e, -s, and -u options to parsing for email capability.
- Documentation updates.

### Removed
- cmds_gen module


## [3.1.0] - 2020-01-06
### Fixed
- setup_cmp:  Set ign_db_tbl default value to empty dictionary.
- fetch_db_list, run_cmp, setup_cmp, run_program:  Fixed problem with mutable default arguments issue.

### Changed
- run_program:  Replaced sys.exit() call with print call.
- recur_tbl_cmp: Set recursion level to a default of 0.
- recur_tbl_cmp: Refactored recursion call to improve performance.
- main:  Added program lock functionality to program.
- main:  Added new option -y to the program.
- main:  Refactored if statements.
- fetch_db_list, recur_tbl_cmp, run_cmp, setup_cmp, run_program:  Changed variable name to standard convention.
- run_program:  Converted program to use mysql-lib v4.0.0.
- Added \*\*kwargs to those function parameter lists without the keyword argument capability.
- Documentation updates.


## [3.0.1] - 2018-12-06
### Fixed
- fetch_db_list:  Changed function parameter mutable argument default to immutable argument default.


## [3.0.0] - 2018-05-23
Breaking Change

### Changed
- mysql_class, mysql_libs, cmds_gen, gen_libs, arg_parser:  Changed calls to new naming schema.
- Changed function names from uppercase to lowercase.
- Setup single-source version control.


## [2.5.0] - 2018-05-04
### Changed
- Changed "server" to "mysql_class" module reference.
- Changed "commands" to "mysql_libs" module reference.

### Added
- Added single-source version control.


## [2.4.0] - 2017-08-18
### Changed
- Convert program to use local libraries from ./lib directory.
- Change single quotes to double quotes.
- Help_Message:  Replace docstring with printing the programs \_\_doc\_\_.


## [2.3.0] - 2016-11-22
### Changed
- Fetch_Db_List:  Replaced code to intersect specified database list with queried database list.
- Setup_Cmp:  Instead of checking for a single table name, replaced with with intersecting the table list with table name list.
- main:  Added new variable opt_multi_list to deal with multiple values for an option.
- Added capability to have multiple values listed for the -t (tables) and -B (databases) options.


## [2.2.0] - 2016-09-23
### Changed
- MySQL 5.6 has 5 new tables in the mysql database that are not replicated between master and slave.  These tables show up as out of synce when a comparsion is ran.  Ignore these tables for checking.  Tables are listed in ign_db_tbl.
- main:  Added variable: ign_db_tbl and passed as \*\*kwargs argument.
- Run_Program:  Added \*\*kwargs to functions argument list.  Added \*\*kwargs to function call to Setup_Cmp (3X).
- Setup_Cmp:  Added \*\*kwargs to functions argument list.  Add ignore tables to the slave ignore table list.
- Modifications work both for Mysql 5.5 and 5.6.


## [2.1.0] - 2016-09-21
### Changed
- main:  Changed -c to -r, -C to -c, -a to -A, and -b to -B.  Reorganized the 'if' statements to streamline the argument processing procedures.  Replaced Arg_Parse with Arg_Parse2 function call.
- Run_Program:  Changed -c to -r, -C to -c & -b to -B.  Changed commands.Disconnect to cmds_gen.Disconnect.


## [2.0.0] - 2015-12-11
### Changed
- Extension updates to the program to modularize and streamline the program and also replace the current database connection mechanism with a class based database connection mechanism.


## [1.0.0] - 2015-10-29
- Initial creation.

