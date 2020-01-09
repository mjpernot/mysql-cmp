#!/bin/bash
# Unit test code coverage for SonarQube to cover all modules.
# This will run the Python code coverage module against all unit test modules.
# This will show the amount of code that was tested and which lines of code
#       that was skipped during the test.

coverage erase

echo ""
echo "Running unit test modules in conjunction with coverage"
coverage run -a --source=mysql_rep_cmp test/unit/mysql_rep_cmp/fetch_db_list.py
coverage run -a --source=mysql_rep_cmp test/unit/mysql_rep_cmp/help_message.py
coverage run -a --source=mysql_rep_cmp test/unit/mysql_rep_cmp/main.py
coverage run -a --source=mysql_rep_cmp test/unit/mysql_rep_cmp/recur_tbl_cmp.py
coverage run -a --source=mysql_rep_cmp test/unit/mysql_rep_cmp/run_cmp.py
coverage run -a --source=mysql_rep_cmp test/unit/mysql_rep_cmp/run_program.py
coverage run -a --source=mysql_rep_cmp test/unit/mysql_rep_cmp/setup_cmp.py

echo ""
echo "Producing code coverage report"
coverage combine
coverage report -m
coverage xml -i
