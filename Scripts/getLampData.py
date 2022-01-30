import bpy
import sys

lampList = ''
for lamp in bpy.data.objects:
	if lamp.type == 'LAMP':
		lampList = lampList + lamp.name + ','


f = open('Meta/lampData.txt', 'w')
for lamp in lampList:
	f.write(lamp)
f.close()
