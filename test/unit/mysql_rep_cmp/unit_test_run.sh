#!/bin/bash
# Unit testing program for the program module.
# This will run all the units tests for this program.
# Will need to run this from the base directory where the module file
#   is located at.

echo ""
echo "Unit testing..."
/usr/bin/python test/unit/mysql_rep_cmp/help_message.py
/usr/bin/python test/unit/mysql_rep_cmp/main.py
/usr/bin/python test/unit/mysql_rep_cmp/recur_tbl_cmp.py
/usr/bin/python test/unit/mysql_rep_cmp/run_program.py
/usr/bin/python test/unit/mysql_rep_cmp/setup_cmp.py
/usr/bin/python test/unit/mysql_rep_cmp/create_data_config.py
/usr/bin/python test/unit/mysql_rep_cmp/get_json_template.py
/usr/bin/python test/unit/mysql_rep_cmp/data_out.py
