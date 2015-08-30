import sys
import urllib, json, os, numpy, math
from numpy import linalg, ndarray
import plotly.plotly as py
import operator
import errno
from plotly.graph_objs import *
from classes import *
from processing import *
py.sign_in('pa1087','5lnuuhu8xi');

thisPatch = sys.argv[2];
thisChamp = sys.argv[1];

region = ['BR','EUNE','EUW','KR','LAN','LAS','NA','OCE','RU','TR'];

fGoodHighPlayerIds = open('./champGoodHighStats/champGoodHighMainStats_' + thisPatch + '_' + thisChamp + '.json');
goodHighPlayerIds = json.loads(fGoodHighPlayerIds.read());

fGoodPlayerList = open('./champGoodMains.json');
goodPlayerList = json.loads(fGoodPlayerList.read());

fMatchList = open('./champGoodMainMatches.json');
matchList = json.loads(fMatchList.read());

fAvgMatchList = open('./champMatches.json');
avgMatchList = json.loads(fAvgMatchList.read());

gamesRecorded = {'avg':0,'mains':0};
gamesWon = {'avg':0,'mains':0};
kda = {'win':{'avg':0,'mains':0},'lose':{'avg':0,'mains':0}};
totalDamage = {'win':{'avg':0,'mains':0},'lose':{'avg':0,'mains':0}};
champDamage = {'win':{'avg':0,'mains':0},'lose':{'avg':0,'mains':0}};
ccTime = {'win':{'avg':0,'mains':0},'lose':{'avg':0,'mains':0}};
itemTally = {'avg':{},'mains':{}};

kdaWinCount = {'avg':0,'mains':0};
kdaLoseCount = {'avg':0,'mains':0};

ghpInd = 0;
maxI = len(goodHighPlayerIds);

for reg in xrange(0,len(region)):
	print str(region[reg]);
	length = len(avgMatchList[thisPatch][region[reg]][thisChamp]);

	for i in xrange(0,length):
		if i%50==0: print str(i) + ' out of ' + str(length);
		fMatch = open('./' + thisPatch + '/RANKED_SOLO/' + region[reg] + '/' + str(avgMatchList[thisPatch][region[reg]][thisChamp][i]) + '.json');
		match = json.loads(fMatch.read());
		gamesRecorded['avg'] += 1;
		isPartLoopDone = 0;

		for j in xrange(0,10):
			if isPartLoopDone == 1: continue;
			if match['participants'][j]['championId'] == int(thisChamp):
				thisMatchStats = match['participants'][j]['stats'];
				thisKDA = 1;

				try:
					thisKDA = (thisMatchStats['kills']+thisMatchStats['assists'])/float(thisMatchStats['deaths']);
				except:
					thisKDA = (thisMatchStats['kills']+thisMatchStats['assists'])/0.5;
				
				thisTotalDamage = thisMatchStats['totalDamageDealt']/float(match['matchDuration']);
				thisChampDamage = thisMatchStats['totalDamageDealtToChampions']/float(match['matchDuration']);
				try:
					thisCcTime = thisMatchStats['totalTimeCrowdControlDealt']/float(match['matchDuration']);
				except:
					thisCcTime = 0;

				if thisMatchStats['winner']:
					gamesWon['avg'] += 1;
					kda['win']['avg'] += thisKDA;
					totalDamage['win']['avg'] += thisTotalDamage;
					champDamage['win']['avg'] += thisChampDamage;
					ccTime['win']['avg'] += thisCcTime;
					kdaWinCount['avg'] += 1;
				else:

					kda['lose']['avg'] += thisKDA;
					totalDamage['lose']['avg'] += thisTotalDamage;
					champDamage['lose']['avg'] += thisChampDamage;
					ccTime['lose']['avg'] += thisCcTime;
					kdaLoseCount['avg'] += 1;
				for itemSlot in xrange(0,7):
					itemStr = 'item' + str(itemSlot);
					if thisMatchStats[itemStr]==3716 or thisMatchStats[itemStr]==3720 or thisMatchStats[itemStr]==3724: thisMatchStats[itemStr] = 3708;
					if str(thisMatchStats[itemStr]) in itemTally['avg']:
						itemTally['avg'][str(thisMatchStats[itemStr])] += 1;
					else:
						itemTally['avg'][str(thisMatchStats[itemStr])] = 1;

				#int(match['participantIdentities'][j]['participantId'])-1
				if ghpInd < maxI:
					if goodHighPlayerIds[ghpInd]['id'] == match['participantIdentities'][j]['player']['summonerId']:
						#goodHighPlayerIds[ghpInd]['region'] == region[reg]:
						ghpInd += 1;
						gamesRecorded['mains'] += 1;
						if thisMatchStats['winner']:
							gamesWon['mains'] += 1;
							kda['win']['mains'] += thisKDA;
							totalDamage['win']['mains'] += thisTotalDamage;
							champDamage['win']['mains'] += thisChampDamage;
							ccTime['win']['mains'] += thisCcTime;
							kdaWinCount['mains'] += 1;
						else:
							kda['lose']['mains'] += thisKDA;
							totalDamage['lose']['mains'] += thisTotalDamage;
							champDamage['lose']['mains'] += thisChampDamage;
							ccTime['lose']['mains'] += thisCcTime;
							kdaLoseCount['mains'] += 1;
						for itemSlot in xrange(0,7):
							itemStr = 'item' + str(itemSlot);
							if str(thisMatchStats[itemStr]) in itemTally['mains']:
								itemTally['mains'][str(thisMatchStats[itemStr])] += 1;
							else:
								itemTally['mains'][str(thisMatchStats[itemStr])] = 1;
						isPartLoopDone = 1;


#length = len(goodHighPlayerIds);
#for i in xrange(0,length):
#	if i%100==0: print 'On ' + str(i+1) + ' out of ' + str(length);
#	thisRegion = goodHighPlayerIds[i]['region'];
#	thisId = goodHighPlayerIds[i]['id'];
#	thisIndex = goodPlayerList[thisPatch][thisRegion][thisChamp].index(thisId);
#	
#	matchId= matchList[thisPatch][thisRegion][thisChamp][thisIndex];
#	fMatch = open('./' + thisPatch + '/RANKED_SOLO/' + thisRegion + '/' + str(matchId) + '.json');
	#print thisPatch + ' ' + thisRegion + ' ' + str(matchId);
#	match = json.loads(fMatch.read());
#	gamesRecorded += 1;
#	for j in xrange(0,10):
#		if match['participants'][j]['championId'] == int(thisChamp) and match['participants'][j]['stats']['winner']:
#			gamesWon += 1;

winRateAvg = gamesWon['avg']/float(gamesRecorded['avg']);
winRateGood = gamesWon['mains']/float(gamesRecorded['mains']);
kda['win']['avg'] /= float(kdaWinCount['avg']);
kda['lose']['avg'] /= float(kdaLoseCount['avg']);
kda['win']['mains'] /= float(kdaWinCount['mains']);
kda['lose']['mains'] /= float(kdaLoseCount['mains']);
totalDamage['win']['avg'] /= float(kdaWinCount['avg']);
totalDamage['lose']['avg'] /= float(kdaLoseCount['avg']);
totalDamage['win']['mains'] /= float(kdaWinCount['mains']);
totalDamage['lose']['mains'] /= float(kdaLoseCount['mains']);
champDamage['win']['avg'] /= float(kdaWinCount['avg']);
champDamage['lose']['avg'] /= float(kdaLoseCount['avg']);
champDamage['win']['mains'] /= float(kdaWinCount['mains']);
champDamage['lose']['mains'] /= float(kdaLoseCount['mains']);
ccTime['win']['avg'] /= float(kdaWinCount['avg']);
ccTime['lose']['avg'] /= float(kdaLoseCount['avg']);
ccTime['win']['mains'] /= float(kdaWinCount['mains']);
ccTime['lose']['mains'] /= float(kdaLoseCount['mains']);

#print itemTally;

fBigItemNameIds = open('./bigItemNameIds.json');
bigItemNameIds = json.loads(fBigItemNameIds.read());
itemTallyTrimmed = {'avg':{},'mains':{}};
#itemTallyTrimmed = {'avg':itemTally['avg'],'mains':itemTally['mains']};
unusedItem = {'avg':[],'mains':[]};
for key in bigItemNameIds['na'][str(thisPatch)]:
	try:
		itemTallyTrimmed['mains'][str(key)] = itemTally['mains'][str(key)];
	except:
		unusedItem['mains'].append(str(key));
	try:
		itemTallyTrimmed['avg'][str(key)] = itemTally['avg'][str(key)];
	except:
		unusedItem['avg'].append(str(key));

itemTallySorted = {'avg':(),'mains':()};
itemTallySorted['mains'] = sorted(itemTallyTrimmed['mains'].items(),key=operator.itemgetter(1),reverse=True);
itemTallySorted['avg'] = sorted(itemTallyTrimmed['avg'].items(),key=operator.itemgetter(1),reverse=True);
l = len(itemTallySorted['mains'])
if l > 10:
	for p in xrange(10,l):
		itemTallySorted['mains'].pop(8);
l = len(itemTallySorted['avg'])
if l > 10:
	for p in xrange(10,l):
		itemTallySorted['avg'].pop(8);

itemTallySortedDict = {'avg':{},'mains':{}};
itemTallySortedDict['mains'] = dict(itemTallySorted['mains']);
itemTallySortedDict['avg'] = dict(itemTallySorted['avg']);
fItemNames = open('./itemNameIdsPatch'+thisPatch+'.json');
#fItemNames = open('./bigItemNameIds.json');
itemNames = json.loads(fItemNames.read());
itemTallySortedTrimmed = {'avg':{},'mains':{}};
for key,value in itemTallySortedDict['mains'].iteritems():
	if key in itemNames:
		itemTallySortedTrimmed['mains'][itemNames[str(key)]] = value/float(gamesRecorded['mains']);
for key,value in itemTallySortedDict['avg'].iteritems():
	if key in itemNames:
		itemTallySortedTrimmed['avg'][itemNames[str(key)]] = value/float(gamesRecorded['avg']);
		

print 'Games Recorded (Mains/Avg) = ' + str(gamesRecorded['mains']) + '/' + str(gamesRecorded['avg']);
print 'Win Rate = ' + str(float("{0:.5f}".format(winRateAvg)));
print 'Win Rate Mains = ' + str(float("{0:.5f}".format(winRateGood)));
print 'KDA = ' + str(kda['win']['avg']) + '/' + str(kda['lose']['avg']);
print 'KDA Mains = ' + str(kda['win']['mains']) + '/' + str(kda['lose']['mains']);
print 'DPS = ' + str(totalDamage['win']['avg']) + '/' + str(totalDamage['lose']['avg']);
print 'DPS Mains = ' + str(totalDamage['win']['mains']) + '/' + str(totalDamage['lose']['mains']);
print 'DPS to Champions = ' + str(champDamage['win']['avg']) + '/' + str(champDamage['lose']['avg']);
print 'DPS to Champions Mains = ' + str(champDamage['win']['mains']) + '/' + str(champDamage['lose']['mains']);
print 'CCPS = ' + str(ccTime['win']['avg']) + '/' + str(ccTime['lose']['avg']);
print 'CCPS Mains = ' + str(ccTime['win']['mains']) + '/' + str(ccTime['lose']['mains']);
print 'Mains items:';
print itemTallySorted['mains'];
print itemTallySortedTrimmed['mains'];
print unusedItem['mains'];
print 'Avg items:';
print itemTallySorted['avg'];
print itemTallySortedTrimmed['avg'];
print unusedItem['avg'];

try:
	os.makedirs('./statsCompare/' + thisPatch + '/' + thisChamp + '/')
except OSError as exception:
	if exception.errno != errno.EEXIST:
		raise

fWriteStats = open('./statsCompare/' + thisPatch + '/' + thisChamp + '/champStats.json','w');
combinedObj = {'gamesRecorded':gamesRecorded,
				'gamesWon':gamesWon,
				'KDA':kda,
				'totalDamageDealt':totalDamage,
				'totalDamageToChampions':champDamage,
				'totalTimeCrowdControlDealt':ccTime,
				'itemUsage':itemTallySortedTrimmed,
				'unusedItems':unusedItem};

json.dump(combinedObj,fWriteStats);

fGoodHighPlayerIds.close();
fGoodPlayerList.close();
fMatchList.close();