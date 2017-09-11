#!/usr/bin/python

import sys
import urllib2
import csv
import re
import time
from bs4 import BeautifulSoup
from difflib import SequenceMatcher

#################### Importing Liraries ########################

if ( len(sys.argv) != 3 ) :
    print "Only 2 arguments are allowed"
    quit()

if ( sys.argv[1] > sys.argv[2] ) :
    print "Invalid Arguments"
    quit()

#################### Checking Arguments ########################

MEASUREMENT_REGEX = r"[0-9\.]{4}"
REQUEST_URL = "http://www.igiworldwide.com/searchreport_postreq.php?r="
PARAM_1 = int(sys.argv[1])
PARAM_2 = int(sys.argv[2])
REPORT_NO_LIST = list(range(PARAM_1 , PARAM_2 + 1))
REQ_FEILDS = ["report_no","shape_cut","carat_weight","color_grade","clarity_grade","polish","symmetry","table_size","total_depth","fluorescence", "width", "length", "depth", "measurement", "shape", "cut", "cut_grade"]
#CSV_FILENAME = "csv_" + time.strftime("%d-%m-%Y_%H-%M-%S") + ".csv"
CSV_FILENAME = "test.csv"  ## development only

##################### Global Constants #########################

def getValueFromDict(dict_param, str):
    if str in dict_param:
        return dict_param[str]
    else:
        return None

def populateRowsList(raw_rows):
    rows_list = []
    for row in raw_rows[1:] :
        tmp = []
        key = row.findAll('td')[0].getText().encode("utf-8").strip().lower()
        value = row.findAll('td')[1].getText().encode("utf-8").strip().lower().replace('\xc2\xb0', '')
        tmp.append( key )
        tmp.append( value )
        rows_list.append(tmp)
    return rows_list

################### User Defined Functions ######################

csv_file_handler = csv.writer(open(CSV_FILENAME, "w"))
csv_file_handler.writerow(REQ_FEILDS)

for report_no in REPORT_NO_LIST :
    raw_data = urllib2.urlopen(REQUEST_URL + str(report_no)).read()
    html_soup = BeautifulSoup(raw_data, "html.parser")
    table_data_soup = html_soup.find('table')

    if table_data_soup is None:
        print str(report_no) + " Failure"
        continue
        
    try:
        rows_soup = table_data_soup.findAll('tr')
        rows_list = populateRowsList(rows_soup)
        rows_dict = dict(rows_list)
        measurements_list = re.findall(MEASUREMENT_REGEX, rows_dict['measurements'])
        shape_cut_list = rows_dict['shape and cut'].split()

        req_rows_list = []
        req_rows_dict = {
            'report_no': getValueFromDict( rows_dict ,'report number' ),
            'shape_cut': getValueFromDict( rows_dict , 'shape and cut' ),
            'carat_weight': getValueFromDict( rows_dict , 'carat weight' ).replace('carat','').strip(),
            'color_grade': getValueFromDict( rows_dict , 'color grade' ),
            'clarity_grade': getValueFromDict( rows_dict , 'clarity grade' ),
            'polish': getValueFromDict( rows_dict , 'polish' ),
            'symmetry': getValueFromDict( rows_dict , 'symmetry' ),
            'table_size': getValueFromDict( rows_dict , 'table size' ).replace('%','').strip(),
            'total_depth': getValueFromDict( rows_dict , 'total depth' ).replace('%','').strip(),
            'fluorescence': getValueFromDict( rows_dict , 'fluorescence' ),
            'width': measurements_list[0],
            'length': measurements_list[1],
            'depth': measurements_list[2],
            'shape': shape_cut_list[0],
            'cut': shape_cut_list[1],
            'cut_grade': getValueFromDict( rows_dict , 'cut grade' ),
            'measurement': getValueFromDict( rows_dict , 'measurements' )
        }

        for req in REQ_FEILDS :
            req_rows_list.append(req_rows_dict[req])

        csv_file_handler.writerow(req_rows_list)
        print str(report_no) + " Success"
    except:
        print str(report_no) + " Failure"
        EX_FILE = str(replaceeport_no) + ".txt"
        file_handler = open(EX_FILE,"w")
        file_handler.write(table_data_soup)
        file_handler.close()


#################################################################

# print SequenceMatcher(None, "shailendra".lower(), "Shailendra".lower()).ratio()
