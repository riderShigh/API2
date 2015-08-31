import sys
import urllib, json, os, numpy, math
from numpy import linalg, ndarray
import operator
import errno
from plotly.graph_objs import *
from classes import *
from processing import *
from download import *

fGoodPlayerList = open('./champGoodMains.json');
goodPlayerList = json.loads(fGoodPlayerList.read());

#patch = ['5.11','5.14'];
patch = ['5.11','5.14'];

region = ['BR','EUNE','EUW','KR','LAN','LAS','NA','OCE','RU','TR'];
#region = [sys.argv[2]];
#region=['KR'];

#region = ['NA'];

#championId = [1,3,4,7,8,9,10,13,17,25,27,28,30,31,34,38,43,45,50,55,60,61,63,68,69,74,76,82,84,85,90,96,99,101,103,105,112,115,117,127,131,134,143,161,245,268];
champChoice = sys.argv[1];
championId = [champChoice];
numberPlayedTally = {'beforePatch':[],'afterPatch':[]};
#storeRepeated = {};

print "---------------------------";
print 'Champion ' + str(champChoice);
print "---------------------------";

for thisPatch in patch:
	print "---------------------------";
	print 'Players Found in Patch ' + str(thisPatch);
	print "---------------------------";
	
	for thisRegion in region:
		print "~~~~~~~~~~~~~~~";
		print "Region " + thisRegion;
		print "~~~~~~~~~~~~~~~";

		#storeRepeated[thisRegion] = [];

		for thisChamp in championId:
			numberPlayedTally = {'beforePatch':[],'afterPatch':[]};
			idList = goodPlayerList[thisPatch][thisRegion][str(thisChamp)];
			summonerIter = 0;
			listLength = len(idList);

			while summonerIter < listLength:
				thisSummoner = idList[summonerIter];
				#if str(thisSummoner) in storeRepeated[thisRegion]:
				#	summonerIter += 1;
				#	print "Visited this summoner before.";
				#	continue;
				#storeRepeated[thisRegion].append(str(thisSummoner));
				#print '+++++++';
				print 'Summoner: ' + str(thisSummoner) + ' (' + str(summonerIter) + '/' + str(listLength) + ')';
				#print '+++++++';
				try:
					fMatchList = dlURLData_matchList(thisRegion.lower(),str(thisSummoner),str(thisChamp),'RANKED_SOLO_5x5');
					matchList = json.loads(fMatchList);
				except:
					continue;
				thisGame = 0;
				playCounts = [0,0];
				#exitCount = 0;
				isBeforePatch = -1;
				while thisGame < matchList['totalGames']:
					try:
						#if exitCount > 9:
						#	exitCount = 0;
						#	thisGame += 1;
						#	continue;
						thisMatchId = matchList['matches'][thisGame]['matchId'];
						fMatch = dlURLData_match(thisRegion.lower(),str(thisMatchId),0);
						try:
							match = json.loads(fMatch);
						except:
							#exitCount += 1;
							print "Error loading match " + str(thisMatchId) + " (" + str(exitCount) + "/1)";
							if isBeforePatch == 1: playCounts[0] += 1;
							if isBeforePatch == 0: playCounts[1] += 1;
							thisGame += 1;
							continue;
						patchNum = checkPatch(str(match['matchVersion']));
						#print checkPatch(str(match['matchVersion']));

						if patchNum == '5.13' or patchNum == '5.14' or patchNum == '5.15':
							isBeforePatch = 0;
							playCounts[1] += 1;
						elif patchNum == '5.12' or patchNum == '5.11' or patchNum == '5.10':
							isBeforePatch = 1;
							playCounts[0] += 1;
						elif patchNum == '5.16':
							thisGame += 1;
							continue;
						else:
							if isBeforePatch == 1: thisGame += 1;
							break;
						thisGame += 1;
						#exitCount += 1;
						#print patchNum;
					except:
						print 'Exit by failure';
						thisGame += 1;
						continue;
					if thisGame%10==0: print 'number of games by this summoner > ' + str(thisGame);
				numberPlayedTally['beforePatch'].append(playCounts[0]);
				numberPlayedTally['afterPatch'].append(playCounts[1]);
				summonerIter += 1;

			print numberPlayedTally;
			try:
				os.makedirs('./pickDropStats/'+ str(champChoice) + '/');
			except OSError as exception:
				if exception.errno != errno.EEXIST:
					raise

			fWriteStats = open('./pickDropStats/' + str(champChoice) + '/' + thisRegion + '.json','w');
			json.dump(numberPlayedTally,fWriteStats);
			fWriteStats.close();