# run this script to create a sqlite database of terms and glosses in Think
# Python 2e, indexed by chapter and order in chapter
# place .sqlite file in folder with main application

import urllib
from bs4 import BeautifulSoup
import sqlite3

conn = sqlite3.connect('GlossThinkPython-db.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Glosses')
cur.execute('CREATE TABLE Glosses (term TEXT, chapter_index INTEGER, order_in_chapter INTEGER, gloss TEXT)')

# create strings for URLs to scrape

full_page_url = list()
page_url1 = 'http://greenteapress.com/thinkpython2/html/thinkpython2'
page_url3 = '.html'

i = 2
while i < 23:
    if i < 10:
        page_url2 = '00' + str(i)
    else:
        page_url2 = '0' + str(i)
    full_page_url.append(page_url1 + page_url2 + page_url3)
    i += 1

# variables to write to database file

term = str()
chapter_index = int()
order_in_chapter = int()
gloss = str()

# outer loop moves through html files for chapter

j = 0

while j < 21:
    
    page = urllib.urlopen(full_page_url[j])
    soup = BeautifulSoup(page, 'lxml')

    # assign index for chapter

    chapter_index = j

    # find h2 tag with content 'Glossary,' then go to second nextSibling, 
    # which is a div tagged 'dl' with children tagged 'dt' for terms and 'dd' for glosses

    tags_h2 = soup('h2') 
    h2_num = len(tags_h2)
    d = 0
    while d < h2_num:
        for child in tags_h2[d].children:
            if 'Glossary' in unicode(child.string):
                glossary_div = tags_h2[d].nextSibling.nextSibling
                break
        d += 1

    # k records order in chapter 

    k = 0
    for child in glossary_div.children:
        if child.name == 'dt':
            term = unicode(child.string)
            if term[-1] == ':':
                term = term[:-1]
                order_in_chapter = k
                k += 1
                continue
        elif child.name == 'dd':
            gloss = ''
            for string in child.strings:
                gloss += string
            gloss = gloss.strip().replace('\n', ' ').replace('  ', ' ')
    
        # write values to database file before moving to next term

        cur.execute('INSERT INTO Glosses (term, chapter_index, order_in_chapter, gloss) VALUES ( ?, ?, ?, ? )',
            (term, chapter_index, order_in_chapter, gloss) )
    
    j += 1

conn.commit()

cur.close()
