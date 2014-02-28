#######################################################################
# BMW Soup v1.0
#
#   This program shows how to use BeautifulSoup4 library to grab data
#   from the BMW website.
#
# Author: Davide Valeriani
#         University of Essex
# 
#######################################################################

import requests
from bs4 import BeautifulSoup

# Print a pretty label of the section
def print_label(label):
    num_stars = 80
    print '*'*num_stars
    l = len(label)
    num_spaces = (num_stars - l - 2)/2
    print '|'+' '*num_spaces+label.upper()+' '*num_spaces+'|'
    print '*'*num_stars

#extract the html_content from the BMW website
url = 'https://www.bmw.co.uk/en_GB/new-vehicles/z4/roadster/2012/technical-data.html'
r = requests.get(url)
html_content = r.text

#apply beautiful soup to the html_content
soup = BeautifulSoup(html_content)

#select the div with class specContainerTables
spec = soup.find('div', class_ = 'specContainerTables')

# select the first of this div
tables = spec.findAll('div', class_ = 'table copyText clearfix')
for table in tables:
    # find the label of the section
    label = table.find('div', class_ = 'caption').text
    # remove unused characters
    label = label.replace(" ","")
    label = label.replace("\n","")
    label = label.replace("\r","")
    # print the prettify label
    print_label(label)
    # find the value of the table (div.td)
    tds = table.findAll('div', class_ = 'td')
    # the first value will be the name of the field
    key = True
    element = ""
    for td in tds:
        if key:
            # the next value will be the value of this field
            key = False
            # store the name of the field
            element = td.p.text
        else:
            # the next value will be the name of the next field
            key = True
            # print key-value in a pretty way
            print '{0:40s} {1:40s}'.format(element.encode('utf8'),td.p.text.encode('utf8'))
            element = ""
    # print a final element
    print '*'*80
    print
