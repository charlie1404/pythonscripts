#!/usr/bin/python

import sys
import urllib2
import csv
import MySQLdb
import json
from bs4 import BeautifulSoup
from difflib import SequenceMatcher

result = urllib2.urlopen("http://www.igiworldwide.com/searchreport_postreq.php?r=" + str(234625698)).read()
soup = BeautifulSoup(result, "html.parser")
table = soup.find('table')
rows = table.findAll('tr')
values = []
for row in rows[1:] :
	val = []
	val.append( row.findAll('td')[0].getText().encode("utf-8").strip() )
	val.append( row.findAll('td')[1].getText().encode("utf-8").strip() )
	values.append( val )

print json.dumps(values)
file_obj = open("test.output","w")
for item in values:
	file_obj.write("%s\n" % item)

print SequenceMatcher(None, "shailendra".lower(), "Shailendra".lower()).ratio()






# if ( len(sys.argv) != 3 ) :
# 	print "Only 2 arguments are allowed"
# 	quit()

# if ( sys.argv[1] > sys.argv[2] ) :
# 	print "Invalid Arguments"
# 	quit()


# paramList = list(range( int(sys.argv[1]), int(sys.argv[2])+1 ))


# for reportNo in paramList :
# 	#result = urllib2.urlopen("http://www.igiworldwide.com/searchreport_postreq.php?r=" + str(reportNo)).read()
# 	result = urllib2.urlopen("http://www.igiworldwide.com/searchreport_postreq.php?r=" + str(234625698)).read()
# 	soup = BeautifulSoup(result, "html.parser")
# 	table = soup.find('table')
# 	if table is None:
# 		continue
# 	else:
# 		rows = table.findAll('tr')
# 		values = []
# 		for row in rows[1:] :
# 			values.append( row.findAll('td')[1].getText().strip() )

# 		file.writerow(values)
