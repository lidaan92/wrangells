import json


testData = {
	'transName' : 'kennCL',
	'year' : 2015,
	'xDist': (0,10,20,30,40,50)
	}
	
aProfile = {
	'date': 2014.1231,
	'speed': (0.30,0.20,0.23)
	}
	
anotherProfile = {
	'date': 2014.88,
	'speed': (0.29,0.21,0.30)
	}


dates = [2014.18,2014.5,2014.98]
us = [(3, 2, 1),(1,1,1),(0,1,2)]

test = {
	'date':dates,
	'speed':us
	}

json_str = json.dumps(testData,separators=(',',':'))

test_json = json.loads(json_str)



### SCRIPT STARTING HERE

import json
import numpy as np
import matplotlib.pyplot as plt

testJsonFn = '/Users/wiar9509/Documents/CU2014-2015/wrangellStElias/corr/pycorr/vv_files/filtered/EPSG102006/L8SamplerOutput/kennCL_evenlySpace_100m_profiles_sampled_2015-12-04.json'

#testJsonFn = '/Users/wiar9509/defaultJsonFn.json'

with open(testJsonFn) as data_file: # open json data
	jsonData = json.load(data_file)

def separateYearsInJson(jsonData,outFilename='/Users/wiar9509/defaultJsonFn.json',plotToggle=1,writeToggle=1):
	'''
	Function that reads in Mark's L8 sampler formatted JSON data and outputs a new JSON file that has velocity profiles separated annually
	Inputs: jsonData = Mark L8 sampler formatted JSON data. outFilename = output JSON filename with full filepath. plotToggle = 1 to show plot, 0 to skip. writeToggle = 1 to write data, 0 to skip.
	Outputs: jsonDataOut = same as data in but now has keys for each year's velocity observations.
	
	William Armstrong
	23 February 2016
	'''
	
	print "Separating data by years using function 'separateYearsInJson()'"
	
	def test_separateYearsInJson():
		assert type(jsonData) == dict, 'Input data must be JSON format, which is a dict. Input data are not a dict'
		
	test_separateYearsInJson() # run tests

	yearStartDoy = 274 # doy 274 = oct 1. will put things from post oct 1 in with next year's observations.
	recordYears = [2013,2014,2015,2016] # years in which data exists

	numProfiles = len(jsonData["pts"]["mid_dec_year"]) # how many profiles are there?

	for yearNow in recordYears: # iterate over years of record
		#print "Record year: " + str(yearNow)
		x = jsonData["sample_pts_frontdist"] # x-coordinate
		jsonData[str(yearNow) + 'profiles'] = None # clear for each year
		uList = [] # clear for each year
		dateList = [] # clear for each year
		dataList = [] # clear for each year
		
		for i in range(0,numProfiles): # iterate over profiles
			midDoy = jsonData["pts"]["mid_dec_year"][i] # midpoint of correlation date
			if int(np.floor(midDoy)) == yearNow: # true if this profile in year of interest
				#print midDoy
				if jsonData["profiles"][i]["mid_dec_year"] == midDoy: # this should always be true, but just checking that referencing the right file
					uNow = jsonData["profiles"][i]["speed"]
				#	dateList.append(midDoy) # append current date to list
				#	uList.append(uNow)etst # append current velocity profile to list of other velocity profiles in this year
					dictNow = {'mid_dec_year':midDoy,'speed':uNow}
					dataList.append(dictNow)
				
			if i == numProfiles-1: # true if gone through all profiles
				#print {str(yearNow) + 'profiles':uList}
				#dataDict = { 'dates': dateList, 'speeds':uList }
				#jsonData.update({str(yearNow) + 'profiles':uList})
				jsonData.update({str(yearNow) + 'profiles':dataList})

			
		if yearNow == recordYears[-1] and i == numProfiles-1: # true if gone through all profiles and all years
			if plotToggle == 1:		
				for year in recordYears:
					samplesInYear = len(jsonData[str(year) + 'profiles']) # how many samples w/in year
					#print "Current year: " + str(year) + " has # samples: " + str(samplesInYear)
					for j in range(0,samplesInYear):
						if year == 2013:
							col = 'b'
							aVal = 0.75
						elif year == 2014:
							col = 'c'
							aVal = 0.4
						elif year == 2015:
							col = 'm'
							aVal = 0.3
						elif year == 2016:
							col = 'r'
							aVal = 0.2
				
						plt.plot(x,jsonData[str(year) + 'profiles'][j]['speed'],color=col,lw=0,marker='.',alpha=aVal)
	
				y1 = plt.plot(-1,-1,color='b',lw=0,marker='.',alpha=0.75,label='2013')
				y2 = plt.plot(-1,-1,color='c',lw=0,marker='.',alpha=0.75,label='2014')	
				y3 = plt.plot(-1,-1,color='m',lw=0,marker='.',alpha=0.75,label='2015')		
				y4 = plt.plot(-1,-1,color='m',lw=0,marker='.',alpha=0.75,label='2015')			
				plt.legend(numpoints=1)
				plt.xlim(0,np.max(x))
				plt.xlabel('Down-glacier distance [m]',fontsize=16)
				plt.ylabel('Horizontal velocity [m d$^{-1}$]',fontsize=16)
				#plt.ylim(0,2)
				plt.show()
				plt.close()

			jsonDataOut = jsonData	
										
			if writeToggle == 1:
				print "Saving data to: " + outFilename
				with open(outFilename, 'w') as f: 
					f.write(json.dumps(jsonDataOut))
		
			return jsonDataOut # output data when done

