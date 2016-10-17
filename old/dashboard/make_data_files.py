#! /usr/bin/python2.7

# Copyright 2014 Jtmorgan

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import grantsbot_settings
import output_settings
import profiles
import queries

#grab queries from the args
#run the queries
#for each query, create a datafile with a standard name
#deposit the datafile in my public html directory

#for arg in args where arg is greater than 1
#if there is a matching query in queries, run that query and dump the data in /data/project/grantsbot/public_html/metrics/

#metrics = [a for a in sys.args if .index(a) > 0]
#for m in metrics:
#try:
#q=queries.getQuery(m)
#except: print "fail to find query"
#try:
#run query in mysql
#rows = cursor.fetchall()
#try:
#create output file with name from arg and write header row
#except: failed to create output file with name from arg and write header
#for row in rows
#try:
#write the row
#except: print "failed to write a row"
#try:
#save output file to the directory
#except: failed to save [argname] output file
#close all my cursors, readers, and writers
#prepend which metrics were created and the date to the log file /data/project/grantsbot/public_html/metrics/log
