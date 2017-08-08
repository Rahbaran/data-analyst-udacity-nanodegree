# -*- coding: utf-8 -*-

import sqlite3
from pprint import pprint
import os
from hurry.filesize import size
import sys

## filesizes (somehow printed twice)
print "\n"
dirpath = '/Users/rahbaran/Documents/data_wrangling'

files_list = []

for path, dirs, files in os.walk(dirpath):
	os.walk(dirpath)
	files_list.extend([(filename, size(os.path.getsize(os.path.join(path, filename)))) for filename in files])

for filename, size in files_list:
	if filename.lower().endswith('.csv') or filename.lower().endswith('.db') \
	or filename.lower().endswith('.osm'):
		print '{:.<40s}: {:5s}'.format(filename,size)

###


def number_of_nodes():
	c.execute('SELECT COUNT(*) FROM nodes')
	return c.fetchone()[0]

def number_of_ways():
	c.execute('SELECT COUNT(*) FROM ways')
	return c.fetchone()[0]

def number_of_contributors():
	c.execute('SELECT COUNT(DISTINCT(uid)) FROM (SELECT uid FROM nodes UNION ALL SELECT uid FROM ways)')
	return c.fetchone()

def top_contributors():
	c.execute('SELECT user, COUNT(*) as num FROM (SELECT user FROM nodes UNION ALL SELECT user FROM ways) GROUP BY user ORDER BY num DESC LIMIT 10')
	for row in c.fetchall():
		print "  ", row
	return c.fetchall()

def top_amenities():
	c.execute('SELECT sub.value, COUNT(*) as num FROM (SELECT key, value FROM nodes_tags UNION ALL SELECT key, value FROM ways_tags) sub WHERE sub.key = "amenity" GROUP BY sub.value ORDER BY num DESC LIMIT 10')
	for row in c.fetchall():
		print "  ", row
	return c.fetchall()

def areas():
	c.execute('SELECT sub.value, COUNT(*) as num FROM (SELECT key, value FROM nodes_tags UNION ALL SELECT key, value FROM ways_tags) sub WHERE sub.key = "suburb" GROUP BY sub.value ORDER BY num DESC LIMIT 10')

	for row in c.fetchall():
		for values in row:
			print "  ", values,
			print "" 
	return c.fetchall()

if __name__ == '__main__':
	db = sqlite3.connect("/Users/rahbaran/Documents/data_wrangling/dussosm.db")
	c = db.cursor()
	print "\n"
	print "number of nodes", number_of_nodes()
	print "number of ways", number_of_ways()
	print "number of contributors", number_of_contributors()
	print "top contributors are:\n\n", top_contributors()
	print "top mentioned areas: \n\n", areas()
