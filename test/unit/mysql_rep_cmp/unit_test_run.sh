#!/bin/bash
# Unit testing program for the program module.
# This will run all the units tests for this program.
# Will need to run this from the base directory where the module file
#   is located at.

echo ""
echo "Unit testing..."
test/unit/mysql_rep_cmp/fetch_db_list.py
test/unit/mysql_rep_cmp/help_message.py
test/unit/mysql_rep_cmp/main.py
test/unit/mysql_rep_cmp/recur_tbl_cmp.py
test/unit/mysql_rep_cmp/run_cmp.py
test/unit/mysql_rep_cmp/run_program.py
test/unit/mysql_rep_cmp/setup_cmp.py
