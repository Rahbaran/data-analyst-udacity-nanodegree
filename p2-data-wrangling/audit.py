import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint
from num2words import num2words

# small sample from Duesseldorf
OSMFILE = "sample.osm" #

#use something like this: tag[phone] = re.sub(r'^00','+',tag['phone'])

def audit(osmfile):
	osm_file = open(osmfile, "r")
	phone_numbers = defaultdict(set)
	for event, elem in ET.iterparse(osm_file, events=("start",)):
		if elem.tag == "node" or elem.tag == "way":
			for tag in elem.iter("tag"):
				if tag.attrib['k'] == "phone":
					#print phone numbers as entered, then the cleaned version
					print tag.attrib['v']
					print clean_phone(tag.attrib['v'])
				# uncomment if you want to see the housenumers
				# 	if tag.attrib['k'] == "addr:housenumber":
				# 		print tag.attrib['v']
	osm_file.close()
	return phone_numbers

def clean_phone(phone_numbers):
	clean_number = re.sub(r'^00','+', phone_numbers)
	clean_number = re.sub(r'-',' ', clean_number)
	clean_number = re.sub(r'\/\s','', clean_number)
	clean_number = re.sub(r'\(0\)','', clean_number)
	clean_number = re.sub(r'^0211','+49 211', clean_number)
	return clean_number


def test():
	st_types = audit(OSMFILE)
	pprint.pprint(dict(st_types))


if __name__ == '__main__':
	test()
