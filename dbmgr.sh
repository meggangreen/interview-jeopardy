################################################################################
# Manages the cliijeopardy database in the shell.
#
# Source and excellent explanation:
# https://stackoverflow.com/a/16783253
#

if psql -lqt | cut -d \| -f 1 | grep -wq cliijeopardy; then
    echo 'wheee!';
else
    echo 'booooo';
fi;


################################################################################
### What it does ###
#
# psql -l outputs something like the following:
#
#                                         List of databases
#      Name  |   Owner   | Encoding |  Collate   |   Ctype    |   Access privileges
# -----------+-----------+----------+------------+------------+-----------------------
#  my_db     | my_user   | UTF8     | en_US.UTF8 | en_US.UTF8 |
#  postgres  | postgres  | LATIN1   | en_US      | en_US      |
#  template0 | postgres  | LATIN1   | en_US      | en_US      | =c/postgres          +
#            |           |          |            |            | postgres=CTc/postgres
#  template1 | postgres  | LATIN1   | en_US      | en_US      | =c/postgres          +
#            |           |          |            |            | postgres=CTc/postgres
# (4 rows)
#
# Using the naive approach means that searching for a database called "List",
# "Access", or "rows" will succeed. So we pipe this output through a bunch of
# built-in command line tools to only search in the first column.
#
# The -t flag removes headers and footers:
#
#  my_db     | my_user   | UTF8     | en_US.UTF8 | en_US.UTF8 |
#  postgres  | postgres  | LATIN1   | en_US      | en_US      |
#  template0 | postgres  | LATIN1   | en_US      | en_US      | =c/postgres          +
#            |           |          |            |            | postgres=CTc/postgres
#  template1 | postgres  | LATIN1   | en_US      | en_US      | =c/postgres          +
#            |           |          |            |            | postgres=CTc/postgres
#
# The next bit, cut -d \| -f 1 splits the output by the vertical pipe | character
# (escaped from the shell with a backslash), and selects field 1. This leaves:
#
#  my_db
#  postgres
#  template0
#
#  template1
#
# grep -w matches whole words, and so won't match if you are searching for temp in
# this scenario.
#
# Note that grep -w matches alphanumeric, digits and the underscore, which is
# exactly the set of characters allowed in unquoted database names in postgresql
# (hyphens are not legal in unquoted identifiers). If you are using other
# characters, grep -w won't work for you.
#
# The -q option suppresses any output written to the screen, so if
# you want to run this interactively at a command prompt you may with to exclude
# the -q so something gets displayed immediately.
#
# The exit status of this whole pipeline will be 0 (success) if the database
# exists or 1 (failure) if it doesn't. Your shell will set the special variable $?
# to the exit status of the last command. You can also test the status directly in
# a conditional:
#
# if psql -lqt | cut -d \| -f 1 | grep -qw <db_name>; then
#     # database exists
#     # $? is 0
# else
#     # ruh-roh
#     # $? is 1
# fi
#
# You can also add ... | grep 0 to make the shell return value be 0 if the DB does
# not exist and 1 if it does; or ... | grep 1 for the opposite behavior
#
# If you want to reverse the exit status, Bash supports a bang operator:
# "! psql ..."
#