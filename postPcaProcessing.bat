@echo off

set patch=5.11 5.14
rem set champ=131 134 25 27 28 161 4 8 127 269 55 50 115 117 112 82 84 85 3 7 245 103 101 105 38 31 30 34 60 61 63 68 69 99 90 96 10 13 17 45 43 1 9 143 76 74
set champ=1
set /a index=0

for %%b in (%champ%) do (
	for %%a in (%patch%) do (
		echo %%a
		echo %%b
		start python postPcaReadMatch.py %%b %%a
		ping 192.0.2.2 -n 1 -w 1000 > nul
	)
)

