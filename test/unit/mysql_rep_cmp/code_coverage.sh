#!/bin/bash
# Unit test code coverage for program module.
# This will run the Python code coverage module against all unit test modules.
# This will show the amount of code that was tested and which lines of code
#   that was skipped during the test.

coverage erase

echo ""
echo "Running unit test modules in conjunction with coverage"
coverage run -a --source=mysql_rep_cmp test/unit/mysql_rep_cmp/help_message.py
coverage run -a --source=mysql_rep_cmp test/unit/mysql_rep_cmp/main.py
coverage run -a --source=mysql_rep_cmp test/unit/mysql_rep_cmp/recur_tbl_cmp.py
coverage run -a --source=mysql_rep_cmp test/unit/mysql_rep_cmp/run_program.py
coverage run -a --source=mysql_rep_cmp test/unit/mysql_rep_cmp/setup_cmp.py
coverage run -a --source=mysql_rep_cmp test/unit/mysql_rep_cmp/create_data_config.py
coverage run -a --source=mysql_rep_cmp test/unit/mysql_rep_cmp/get_all_dbs_tbls.py
coverage run -a --source=mysql_rep_cmp test/unit/mysql_rep_cmp/get_db_tbl.py
coverage run -a --source=mysql_rep_cmp test/unit/mysql_rep_cmp/get_json_template.py
coverage run -a --source=mysql_rep_cmp test/unit/mysql_rep_cmp/data_out.py

echo ""
echo "Producing code coverage report"
coverage combine
coverage report -m
