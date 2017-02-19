#coding=utf-8

from HTMLParser import  HTMLParser
from xml.dom import  minidom,Node


class html_parers(HTMLParser):
    def __init__(self):
        self.readline=0
        self.title=''
        self.raw=[]
        HTMLParser.__init__(self)


    def handel_entityref(self,name):
        pass

    def handle_starttag(self, tag, attrs):
        if tag=='a':

            for x in attrs:
                if x[1].startswith('http'):
                    self.readline = 1
                    self.raw.append(x[1])
        return self.raw



    def handle_endtag(self, tag):
        if tag=="a":
            self.readline=0

    def handle_data(self, data):
        if self.readline:

            self.title+=data

    def gettitle(self):
        return self.title


html_file='./2.html'
html=html_parers()
fd=open(html_file,'rb')
html.feed(fd.read())
print html
print  html.gettitle()
print html_parers.__class__