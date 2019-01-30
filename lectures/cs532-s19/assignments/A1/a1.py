#!/usr/bin/python3

import sys
from parseLink import scrapePdfContentLength
from bs4 import BeautifulSoup
from threading import Thread
import urllib.request
import re as regex
import queue

baseurl = str(sys.argv[1])

q = queue.Queue(maxsize=0)
results = []

'''
grab our urls from the base page. we perform a regex match to ensure that href = a valid url and 
    not something like href= '#todo' or href='javascript.void(0)' 
    '''
with urllib.request.urlopen(baseurl) as res:
    baseHTML = res.read()
    soup = BeautifulSoup(baseHTML, features="html.parser")
    for links in soup.find_all('a'):
        matchObj = regex.match(r'http(.*)', str(links.get('href')))
        if matchObj:
            q.put(str(links.get('href')))
        else:
            pass
# http://www.learn4master.com/programming-language/python/python-multi-thread-example
print("Number of Links: {}".format(q.qsize()))
thread_pool_size = q.qsize()
for i in range(thread_pool_size):
    t = Thread(name='Thread-' + str(i), target=scrapePdfContentLength, args=(q, results))
    t.daemon = True
    t.start()
q.join()

for i in results:
    print(i)