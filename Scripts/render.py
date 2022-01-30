'''
DOCUMENTATION

 
09/29

before calling this script, 
the log file spreadsheet should be
saved in .csv format 
using Excel in Mac OS


flexible input arguments
Assets = 'a1,a2'
AssetCats = 'ac1,ac2'
Lamps = 'l1,l2'
Envs = 'e1,e2'
Cameras = 'int'/'c1,c2'

PLEASE DO NOT LEAVE SPACES BETWEEN ITEMS OF THE SAME TYPE

shell command examples:
i)
run the script on a certain category of assets under the Assets directory:
tian@ubuntu:~/Desktop/master$ python Scripts/test3.py AssetCats='chair' 

ii)
run the script on all the files:
tian@ubuntu:~/Desktop/master$ python Scripts/test3.py


iii)
run the script on a certain asset and a certain environment:
tian@ubuntu:~/Desktop/master$ python Scripts/test3.py Assets='deck.blend' Envs='ella.blend'
'''

import sys
import os
import re #regular expression to be used
from time import gmtime, strftime


#initialization of lists to be used
###################################
asset_list = []
assetcat_list = [] #the asset category list
#if the assetcat_list is defined by the user, 
#assest_list will become meaningless 
lamp_list = []
env_list = []
cam_list = '1' 
#a string to be passed to the renderScene script
#default value: 1, meaning 1 randomly chosen camera
###############

#open the file object of the error log file,
#which records all the error messages 
log_f = open('Meta/error_log.txt', 'a')

##########################################
#parsing the user inputs in shell commands
##########################################
shot = refresh = False
for arg in sys.argv:
	
	asset_match       = re.match('Assets=(.+)',    arg)
	assetcat_match    = re.match('AssetCats=(.+)', arg)
	lamp_match        = re.match('Lamps=(.+)',     arg) 
	env_match         = re.match('Envs=(.+)',      arg)
	camera_name_match = re.match('Cameras=(.+)',   arg)
	shot_match        = re.match('Shot',           arg)
	refresh_match     = re.match('Refresh',        arg)

	if asset_match:
		s_a = asset_match.groups()[0]
		asset_list = s_a.split(',')
		
	elif assetcat_match:
		s_ac = assetcat_match.groups()[0]
		assetcat_list = s_ac.split(',')
	
	elif lamp_match:
		s_l = lamp_match.groups()[0]
		lamp_list = s_l.split(',')
	
	elif env_match:
		s_e = env_match.groups()[0]
		env_list = s_e.split(',')
	
	elif camera_name_match:
		cam_list = camera_name_match.groups()[0]
		
	elif shot_match: shot = True	
	
	elif refresh_match: refresh = True

	else:
		#if this argument is not the script name itself,
		#an illegal argument is detected.
		if arg != sys.argv[0]: 
			#raise a fatal exception and quit
			log_f.write(strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' - FATAL - illegal user input\n')
			log_f.close()
			sys.exit('FATAL - illegal user input: please check the documentation for details')

###########################################
#end of the for loop parsing
############################
	
#compile asset_list
assets_final = []
asset_paths_final = []

#get list of available asset categories
available_assetcats = os.listdir('Assets')
try: available_assetcats.remove('.DS_Store')
except: pass

for asset in asset_list:
	for cat in available_assetcats:
		if asset in os.listdir('Assets/' + cat):
			assets_final.append(asset)
			asset_paths_final.append(cat + '/' + asset)
		else:
			log_f.write(strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' - WARNING - asset ' + asset + ' is not in the Assets/' + cat + ' dir\n')
			
	
for cat in assetcat_list: 
	if cat in available_assetcats: 
		assets_final += os.listdir('Assets/' + cat)
		asset_paths_final += [cat + '/' + asset for asset in os.listdir('Assets/' + cat)]
	else: log_f.write(strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' - WARNING - asset category ' + cat + ' is not in the Assets dir\n')

#if no assets were specified, use all of them
if asset_list == [] and assetcat_list == []: 
	for cat in available_assetcats:
		assets_final += os.listdir('Assets/' + cat)
		asset_paths_final += [cat + '/' + asset for asset in os.listdir('Assets/' + cat)]

#checking the lamp_list
if lamp_list == [] and shot: lamp_list = ['lamp1.blend']
elif lamp_list == [] and not shot: 
	lamp_list = os.listdir('Lamps')
	#lamp_list.remove('.DS_Store')
	lamp_list.remove('empty.blend')
else:
	#checking if the user-defined lamps are in the Lamps directory
	for l in lamp_list:
		if (not (l in os.listdir('Lamps'))):
			#if an invalid lamp is found in the user input
			#record a WARNING in the error log and remove this lamp
			log_f.write(strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' - WARNING - lamp ' + l + ' is not in the Lamps dir\n')
			lamp_list.remove(l) #this might leave the lamp list empty


#checking the env list
if env_list == [] and shot: env_list = ['env3.blend']
elif env_list == [] and not shot: env_list = os.listdir('Environments')
else:
	#checking if the user-defined environments are in the Environments directory
	for e in env_list:
		if (not (e in os.listdir('Environments'))):
			#if an invalid environment is found in the user input
			#record a WARNING in the error log and remove this environment
			log_f.write(strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' - WARNING - environment ' + e + ' is not in the Environments dir\n')
			env_list.remove(e) #this might leave the environment list empty


###########################################################################################
if  'darwin' in sys.platform: blenderPath = 'Blender_exec/blender.app/Contents/MacOS/blender'
elif 'linux' in sys.platform: blenderPath = 'Blender_exec/blender'
else: raise NameError('Unknown operating system, cant choose blenderPath')
for i,asset in enumerate(assets_final):
	os.system(blenderPath + ' -b Assets/' + asset_paths_final[i] + ' -P Scripts/getAssetPosition.py')
	for env in env_list:
		if env == 'env1.blend': my_lamp_list = ['empty.blend']*len(lamp_list)
		else: my_lamp_list = [lamp for lamp in lamp_list if lamp != 'empty.blend']
		for lamp in my_lamp_list:	
			a = asset[:-6]
			l = lamp[:-6]
			e = env[:-6]
			r = a + '_' + l + '_' + e + '.blend'
			
			if '.DS' not in r:
				if r not in os.listdir('Renderable') or refresh:
					os.system('python Scripts/renderSetup.py Assets/' + asset_paths_final[i] + ' Lamps/' + lamp + ' Environments/' + env + ' Renderable/')
					
				os.system(blenderPath + ' -b Renderable/' + r + ' -P Scripts/renderScene.py -- ' + cam_list)

log_f.close()
