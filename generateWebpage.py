import sys
import urllib, json, os, numpy, math
from numpy import linalg, ndarray
from classes import *
from processing import *

fBaseHtml = open('main.html');
baseText = fBaseHtml.read();

mageList = json.loads(open('mages.json').read());

for key,value in mageList.iteritems():
	writeText = baseText.replace('Katarina',value);
	writeText = writeText.replace('/1/champStats.json','/'+key+'/champStats.json');

	fGenHtml = open('./html/'+value+'.html','w');
	fGenHtml.write(writeText);
	fGenHtml.close();