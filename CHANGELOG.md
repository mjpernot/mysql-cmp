# Changelog
All notable changes to this project will be documented in this file.

The format is based on "Keep a Changelog".  This project adheres to Semantic Versioning.


## [3.1.0] - 2020-01-06
### Fixed
- fetch_db_list:  Fixed problem with mutable default arguments issue.
- run_cmp:  Fixed problem with mutable default arguments issue.
- setup_cmp:  Fixed problem with mutable default arguments issue.
- run_program:  Fixed problem with mutable default arguments issue.

### Changed
- run_program:  Converted program to use mysql-lib v4.0.0.
- Added \*\*kwargs to those function parameter lists without the keyword argument capability.
- Documentation updates.


## [3.0.1] - 2018-12-06
### Fixed
- fetch_db_list:  Changed function parameter mutable argument default to immutable argument default.


## [3.0.0] - 2018-05-23
Breaking Change

### Changed
- Changed "mysql_class" calls to new naming schema.
- Changed "mysql_libs" calls to new naming schema.
- Changed "cmds_gen" calls to new naming schema.
- Changed "gen_libs" calls to new naming schema.
- Changed "arg_parser" calls to new naming schema.
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

