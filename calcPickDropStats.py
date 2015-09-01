import sys
import urllib, json, os, math
import operator
import errno
from classes import *
from processing import *
from download import *

thisChamp = sys.argv[1];

fData = open('./pickDropStats/filtered/' + str(thisChamp) + '.json');
data = json.loads();