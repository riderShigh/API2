import sys
import urllib, json, os, numpy, math
from numpy import linalg, ndarray
import plotly.plotly as py
from plotly.graph_objs import *
from classes import *
from processing import *
py.sign_in('pa1087','5lnuuhu8xi');



thisChamp = sys.argv[1];
thisPatch = sys.argv[2];
statsFileName = 'champGoodMainsStats_' + str(thisPatch) + '_' + str(thisChamp) + '.json';
extractChampStats('champGoodMains.json',statsFileName,thisPatch,thisChamp);

fStats = open(statsFileName,'r');
#fStats = open('vladStats2.json','r');
data = json.loads(fStats.read());
vecRawStats = [];
vecDim = 6;
vecMean = [0 for col in range(vecDim)];
vecVar = [0 for col in range(vecDim)];
scatMatrix = [[0 for col in range(vecDim)] for row in range(vecDim)];
tempVec = [0 for col in range(vecDim)];

goodPlayers = [];
highestKDA = 0;
highestKDAIndex = 0;
lowestKDA = 10;
lowestKDAIndex = 0;
mostPlayed = 0;
mostPlayedIndex = 0;
regionKeys = [];

for i in xrange(0,len(data)):
	#if data[str(i)]['win'] == True:
	#	wl = 20;
	#else:
	#	wl = -20;

	vecRawStats.append([
		data[str(i)]['totalSessionsPlayed'],
		data[str(i)]['totalSessionsWon']/float(data[str(i)]['totalSessionsPlayed']),
		data[str(i)]['championPlayRate'],
		data[str(i)]['totalChampionKills'],
		data[str(i)]['totalAssists'],
		data[str(i)]['totalKDA']
		]);
	#print vecRawStats[i];
	regionKeys.append(data[str(i)]['region']);
	#vecRawStats.append([
	#	data[str(i)]['GPM'],
	#	data[str(i)]['DPS'],
	#	data[str(i)]['KDA'],
	#	data[str(i)]['percentDamage']
		#wl,
	#	]);

for k in xrange(0,vecDim):
	for i in xrange(0,len(vecRawStats)):
		if vecRawStats[i][vecDim-1] > highestKDA: 
			highestKDA = vecRawStats[i][vecDim-1];
			highestKDAIndex = i;
		if vecRawStats[i][vecDim-1] < lowestKDA: 
			lowestKDA = vecRawStats[i][vecDim-1];
			lowestKDAIndex = i;
		if vecRawStats[i][0] > mostPlayed: 
			mostPlayed = vecRawStats[i][0];
			mostPlayedIndex = i;
		vecMean[k] += vecRawStats[i][k];
	vecMean[k] /= float(len(vecRawStats));

for i in xrange(0,len(vecRawStats)):
	for j in xrange(0,vecDim):
		vecRawStats[i][j] = vecRawStats[i][j] - vecMean[j];
		#tempVec[j] = vecRawStats[i][j]/vecMean[j] - 1;

for k in xrange(0,vecDim):
	for i in xrange(0,len(vecRawStats)):
		vecVar[k] += vecRawStats[i][k]*vecRawStats[i][k];
	vecVar[k] /= float(len(vecRawStats));
	vecVar[k] = math.sqrt(vecVar[k]);

for i in xrange(0,len(vecRawStats)):
	for j in xrange(0,vecDim):
		vecRawStats[i][j] = vecRawStats[i][j]/vecVar[j];

for i in xrange(0,len(vecRawStats)):
	for j in xrange(0,vecDim):
		for k in xrange(0,vecDim):
			scatMatrix[j][k] += vecRawStats[i][j] * vecRawStats[i][j];

w,v = linalg.eigh(scatMatrix);
wArgSorted = ndarray.argsort(w);

transMatrix = [v[:,wArgSorted[vecDim-1]],v[:,wArgSorted[vecDim-2]]]
print transMatrix

analyzedData = [[0 for col in range(2)] for row in range(len(vecRawStats))]
xi = [];
yi = [];
xj = [];
yj = [];
xk = [];
yk = [];
xa = [];
ya = [];

for i in xrange(0,len(vecRawStats)):
	for j in xrange(0,2):
		for k in xrange(0,vecDim):
			analyzedData[i][j] += transMatrix[j][k] * vecRawStats[i][k]; #/vecMean[k];
	#if  data[str(i)]['win'] == True:
	xi.append(analyzedData[i][0]);
	yi.append(analyzedData[i][1]);
	if i == highestKDAIndex:
		xj.append(analyzedData[i][0]);
		yj.append(analyzedData[i][1]);
	if i == lowestKDAIndex:
		xk.append(analyzedData[i][0]);
		yk.append(analyzedData[i][1]);
	if i == mostPlayedIndex:
		xa.append(analyzedData[i][0]);
		ya.append(analyzedData[i][1]);

	#else:
	#	xj.append(analyzedData[i][0]);
	#	yj.append(analyzedData[i][1]);

analyzedData = tuple(analyzedData);
trace0 = Scatter(x=xi,y=yi,mode='markers',name='Data');
trace1 = Scatter(x=xj,y=yj,mode='markers',name='Highest KDA');
trace2 = Scatter(x=xk,y=yk,mode='markers',name='Lowest KDA');
trace3 = Scatter(x=xa,y=ya,mode='markers',name='Most Number of Plays');
traceData = Data([trace0,trace1,trace2,trace3]);

layout = Layout(
	title='Champion ' + str(thisChamp) + '   Patch ' + str(thisPatch),
	xaxis = XAxis(title='PC1'),
	yaxis = YAxis(title='PC2')
	);
fig = Figure(data=traceData,layout=layout);

plot_url = py.plot(fig);

fGoodMainsId = open(statsFileName);
goodMainsId = json.loads(fGoodMainsId.read());
pcaSide = 1;
#if xj[0] < 0: pcaSide = -1;
for i in xrange(0,len(vecRawStats)):
	if analyzedData[i][0] * pcaSide > 0:
		goodPlayer = {};
		goodPlayer['id'] = goodMainsId[str(i)]['summonerId'];
		goodPlayer['region'] = goodMainsId[str(i)]['region'];
		goodPlayers.append(goodPlayer);

fGoodPlayers = open('champGoodHighMainStats_' + thisPatch + '_' + thisChamp + '.json','w');
json.dump(goodPlayers,fGoodPlayers);
fGoodPlayers.close();
print len(goodPlayers);