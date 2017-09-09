#!/usr/bin/python

import sys
import urllib2
import csv
import re
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

##################### Global Constants #########################

def getDictValue(dict_param, str):
    if str in dict_param:
        return dict_param[str]
    else:
        return None

################### User Defined Functions ######################

for report_no in REPORT_NO_LIST :
    raw_data = urllib2.urlopen(REQUEST_URL + str(report_no)).read()
    html_soup = BeautifulSoup(raw_data, "html.parser")
    table_data_soup = html_soup.find('table')

    if table_data_soup is None:
        continue
    
    rows_soup = table_data_soup.findAll('tr')
    rows_list = []

    for row in rows_soup[1:] :
        tmp = []
        key = row.findAll('td')[0].getText().encode("utf-8").strip().lower()
        value = row.findAll('td')[1].getText().encode("utf-8").strip().lower().replace('\xc2\xb0', '')
        tmp.append( key )
        tmp.append( value )
        rows_list.append(tmp)

    rows_dict = dict(rows_list)
    measurements_list = re.findall(MEASUREMENT_REGEX, rows_dict['measurements'])
    print measurements_list

    req_rows_dict = {
        'report_no': getValueFromDict( rows_dict ,'report number' ),
        'shape_cut': getValueFromDict( rows_dict , 'shape and cut' ),
        'carat_weight': getValueFromDict( rows_dict , 'carat weight' ),
        'color_grade': getValueFromDict( rows_dict , 'color grade' ),
        'clarity_grade': getValueFromDict( rows_dict , 'clarity grade' ),
        'polish': getValueFromDict( rows_dict , 'polish' ),
        'symmetry': getValueFromDict( rows_dict , 'symmetry' ),
        'table_size': getValueFromDict( rows_dict , 'table size' ),
        'total_depth': getValueFromDict( rows_dict , 'total depth' ),
        'fluorescence': getValueFromDict( rows_dict , 'fluorescence' ),
        'width': measurements_list[0],
        'length': measurements_list[1],
        'depth': measurements_list[2],
        'shape': 'shape',
        'cut': 'cut',
        'cut_grade': getValueFromDict( rows_dict , 'cut grade' ),
        'measurement': getValueFromDict( rows_dict , 'measurements' )
    }
