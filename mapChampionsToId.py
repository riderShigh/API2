import sys
import urllib, json, os, numpy, math
from classes import *

region = ['br','eune','euw','kr','lan','las','na','oce','ru','tr'];

regionMap = {};
mapItemIds = {};
patchItems = {};
fItemIds = open('championNameIds.json','w');

for reg in region:
	print 'current region = ' + reg;
	url = 'https://global.api.pvp.net/api/lol/static-data/' + reg + '/v1.2/versions?api_key=ac3b3bf8-1aa6-4570-8a84-8163ba9e0a89';

	urlData = urllib.urlopen(url);
	versions = json.loads(urlData.read());
	i = 0;
	season = '5';
	skipOldVersion = 0;
	
	while season == '5':
		if skipOldVersion > 0:
			i += 1;
			skipOldVersion -= 1;
			continue;
		url1 = 'http://ddragon.leagueoflegends.com/cdn/' + versions[i] + '/data/en_US/champion.json';
		fItems = urllib.urlopen(url1);
		items = json.loads(fItems.read());
		for key in items['data']:
		#print url
			mapItemIds[items['data'][key]['key']] = items['data'][key]['name'];
		versionStr = versions[i];
		versionStr = versionStr[:-2];

		patchItems[versionStr] = mapItemIds;
		skipOldVersion = int(versions[i][-1]) - 1;
		print versions[i];
		i += 1;
		season = versions[i][0];
	regionMap[reg] = patchItems;


json.dump(regionMap,fItemIds);
fItemIds.close();