#!/usr/bin/env python

import os 
import sys
import zipfile
import subprocess
import glob
import pandas as pd

#read in each of the lines.
velocityOut = 'velocity'
qualityOut = 'quality'
for root, dirNames, fileNames in os.walk(os.path.join(os.getcwd(),'dataIn')):
	for fileName in fileNames :
		print(fileName)
		latNum = ''
		longNum =''
		f = open(os.path.join(os.getcwd(),'dataIn',fileName))
		fname,fExt = os.path.splitext(fileName)
		f1 = open(os.path.join(os.getcwd(),'dataOut',fname+velocityOut+fExt), 'a')
		f2 = open(os.path.join(os.getcwd(),'dataOut',fname+qualityOut+fExt), 'a')
		outString = ('owner, idNum , latitude, longitude, yr, mo, dy, hr, mn, binCount, binCountGood, binCountTotal, depthStart, depthEnd, average ')
		f2.write(outString + '\n')
		binCount = 0
		binCountGood = 0
		binCountTotal = 0
		depthStart=0
		depthEnd=0
		metaData = fname.split('_')
		owner	 = metaData[0]
		idNum 	=	metaData[1]
		yr = ''
		mo =''
		dy = ''
		hr = ''
		mn = ''
		x = 12 if owner == 'Shell' else 13
		print(x)
		for line in f.readlines():`
			if 'PROFILE_STATUS' in line:
				data = line.split()

				if len(data) > 12 and len(yr) > 2 :
					latNum = data[8]
					longNum	= data[10]
					outString = owner + '1, ' + idNum + ', ' + yr + ', '+mo+', '+dy+', '+hr+', '+ mn +', '+ str(binCount) +', '+ str(binCountGood) +', '+ str(binCountTotal) +', '+ str(depthStart)+ ', '+str(depthEnd) + ',' +str(binCountGood/binCount)
					f2.write(outString + '\n')
					outString = owner + '2, ' + idNum + ', ' + yr + ', '+mo+', '+dy+', '+hr+', '+ mn +', '+ str(binCount) +', '+ str(binCountGood) +', '+ str(binCountTotal) +', '+ str(depthEnd)+ ', '+str(depthStart) + ',' +str(binCountGood/binCount)
					f2.write(outString + '\n')
				binCount = 0
				binCountGood = 0
				binCountTotal = 0
				depthStart=0
				depthEnd=0
				depthFlag =0

			if not 'PROFILE_STATUS' in line:
				#split the line to array.
				numbers = line.split()
				checkDepth = numbers[7]
				if len(numbers)>13 and checkDepth != 'Depth' and checkDepth != 'm':
					#try:
					depthNew = float(checkDepth)
					binCount += 1
					if binCount == 1 : 
						depthStart = depthNew

					binCountTotal += int(numbers[x])
					if int(numbers[x]) > 90 : 
						binCountGood += 1
						if depthNew > depthEnd:
							depthEnd = depthNew
						if float(depthNew) < depthStart:
							depthStart = float(depthNew)

					#except:
					#	print('oops' + line)

					if not 'MM' in numbers[9]:
						
						outString 	= owner +', ' + idNum +', '+ latNum +', '+ longNum +', '+','.join(numbers[0:10])
						#print('Output to velocity '+ outString + '\n')
						yr = numbers[0]
						mo = numbers[1]
						dy = numbers[2]
						hr = numbers[3]
						mn = numbers[4]
						f1.write(outString +','+numbers[x]+'\n')
		f1.close()
		f2.close()
		f.close()

