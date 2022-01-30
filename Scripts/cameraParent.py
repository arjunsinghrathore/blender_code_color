import bpy
import os

'''
for obj in bpy.data.objects:
	if obj.type == 'CAMERA': 
		obj.location = (obj.location[0],obj.location[1],obj.location[2] + .5)
'''		
bpy.data.objects['Plane'].location = (0,0,-0.2)
bpy.data.objects['Plane'].parent = bpy.data.objects['Camera_transform']
		
		
bpy.ops.wm.save_as_mainfile(filepath = bpy.data.filepath)