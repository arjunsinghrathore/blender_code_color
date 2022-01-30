import sys
import bpy
from random import randint

numCams = 1

for i in range(numCams):
	# this is a hack for now -- snag the first of the 1000 cameras caleb set up
	cam = 'Camera.' + repr(1).zfill(3)	
	bpy.context.scene.camera = bpy.data.objects[cam]
	# this is where the camera settings go
	'''
	# translation	
	bpy.context.scene.camera.location.x = 
	bpy.context.scene.camera.location.y = 
	bpy.context.scene.camera.location.z = 
	# rotation (in degrees)
	bpy.context.scene.camera.rotation_mode = 'XYZ'
	bpy.context.scene.camera.rotation_euler[0] = 
	bpy.context.scene.camera.rotation_euler[1] = 
	bpy.context.scene.camera.rotation_euler[2] = 
	# or you could manipulate the camera transform directly instead if you want to
	#camera_transform = bpy.data.objects['Camera_transform']
	'''
	imName = bpy.data.filepath.split('/')[-1][:-6] + '_' + repr(i).zfill(3) + '.png'
	bpy.context.scene.render.filepath = 'Images/' + imName
	bpy.ops.render.render( write_still=True )

'''
# caleb's original camera picking code
camList = []
if sys.argv[6].isdigit():
	while len(camList) < int(sys.argv[6]):
		newCam = 'Camera.' + repr(randint(1,500)).zfill(3)
		if bpy.data.objects.get(newCam): camList.append(newCam)
else: 
	camList = sys.argv[6].split(',')
	for cam in camList:
		if not bpy.data.objects.get(cam): camList.remove(cam)

for cam in camList:
	bpy.context.scene.camera = bpy.data.objects[cam]
	imName = bpy.data.filepath.split('/')[-1][:-6] + '_' + cam.split('.')[-1] + '.png'
	bpy.context.scene.render.filepath = 'Images/' + imName
	print(imName)
	bpy.ops.render.render( write_still=True )
'''
