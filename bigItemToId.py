import sys
import urllib, json, os, numpy, math
from numpy import linalg, ndarray
import plotly.plotly as py
import operator
from plotly.graph_objs import *
from classes import *
from processing import *
py.sign_in('pa1087','5lnuuhu8xi');

fBigItems = open('./bigItems.json');
#readBigItems = '"""'+fBigItems.read()+'"""';
#print readBigItems
bigItems = json.loads(fBigItems.read());

fItems = open('./itemNameIds.json');
items = json.loads(fItems.read());

itemStore = {};

fBigItemIds = open('./bigItemNameIds.json','w');

for region in items:
	thisRegion = items[region];
	itemStore[region] = {};
	for patch in thisRegion:
		itemStore[region][str(patch)] = {};
		thisPatch = thisRegion[str(patch)];
		for item in thisPatch:
			if item in bigItems: 
				itemStore[region][str(patch)][thisPatch[str(item)]] = item;
				if item=='Enchantment: Magus': print str(region)+str(patch)+thisPatch[str(item)];

json.dump(itemStore,fBigItemIds);
fBigItems.close();
fItems.close();
fBigItemIds.close()