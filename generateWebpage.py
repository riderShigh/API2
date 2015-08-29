import sys
import urllib, json, os

fBaseHtml = open('main.html');
baseText = fBaseHtml.read();

mageList = json.loads(open('mages.json').read());

for key,value in mageList.iteritems():
	writeText = baseText.replace('Katarina',value);
	champName = value.replace(" ","");
	champName = champName.replace("'","");
	if champName == 'Fiddlesticks': champName == 'FiddleSticks';
	if champName == 'ChoGath': champName == 'Chogath';
	if champName == 'LeBlanc': champName == 'Leblanc';

	writeText = writeText.replace('/1/champStats.json','/'+key+'/champStats.json');

	fGenHtml = open('./html/'+champName+'.html','w');
	fGenHtml.write(writeText);
	fGenHtml.close();