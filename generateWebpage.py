import sys
import urllib, json, os

fBaseHtml = open('main.html');
baseText = fBaseHtml.read();

mageList = json.loads(open('mages.json').read());

for key,value in mageList.iteritems():
	#writeText = baseText.replace('Katarina',value);
	champName = value.replace(" ","");
	champName = champName.replace("'","");
	champName = champName.lower();
	champName = champName[0].upper() + champName[1:];

	if champName == 'Fiddlesticks': champName = 'FiddleSticks';
	if champName == 'Kogmaw': champName = 'KogMaw';
	if champName == 'Twistedfate': champName = 'TwistedFate';
	print champName;

	writeText = baseText.replace('Katarina',champName);

	writeText = writeText.replace('/1/champStats.json','/'+key+'/champStats.json');

	fGenHtml = open('./html/'+champName+'.html','w');
	fGenHtml.write(writeText);
	fGenHtml.close();