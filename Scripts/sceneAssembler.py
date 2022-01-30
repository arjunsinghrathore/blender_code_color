import sys
import bpy

assetPath   = sys.argv[6]
lampPath    = sys.argv[7]
outPath     = sys.argv[8]


#import assets specified in fileData from assetPath (a .blend file)
#then do the same using lampData and lampPath

f = open('Meta/assetData.txt','r')
assetData = f.read()
f.close()

f = open('Meta/lampData.txt','r')
lampData = f.read()
f.close()

f = open('Meta/assetPosition.txt','r')
assetPosition = f.read()
f.close()

meshList = assetData.split('..')[0].split(',')[:-1]
texList  = assetData.split('..')[1].split(',')[:-1]
matList  = assetData.split('..')[2].split(',')[:-1]

for lamp in lampData.split(',')[:-1]:
	bpy.ops.wm.append(filename = lamp,link = False, directory = lampPath + '/Object/' )

for mesh in meshList:
	bpy.ops.wm.append(filename = mesh,link = False, directory = assetPath + '/Object/' )


if False and bpy.data.filepath.split('/')[-1] == 'env2.blend':
	mat=bpy.data.materials.new('grayShader')
	mat.diffuse_color = (1,1,1,1)
	mat.diffuse_intensity = .7
	mat.specular_intensity = 0
	
	for mesh in meshList:
		if mesh != 'Plane':
			while len(bpy.data.objects[mesh].data.materials) > 0:
				bpy.data.objects[mesh].data.materials.pop(0, update_data=True)
			bpy.data.objects[mesh].data.materials.append(mat)
else:			
	for tex  in texList:
		bpy.ops.wm.append(filename = tex, link = False, directory = assetPath + '/Texture/' )

	for mat in matList:
		bpy.ops.wm.append(filename = mat, link = False, directory = assetPath + '/Material/' )
	


scaleFactor = float(assetPosition.split(',')[0]) * 1.2
Xcenter     = float(assetPosition.split(',')[1])
Ycenter     = float(assetPosition.split(',')[2])
Zmin        = float(assetPosition.split(',')[3])

camera_transform = bpy.data.objects['Camera_transform']

bpy.ops.object.add()
lamp_transform = bpy.context.view_layer.objects.active
for obj in bpy.data.objects:
	if obj.type == 'LAMP': obj.parent = lamp_transform

camera_transform.location = (Xcenter, Ycenter, Zmin + 0.2 * scaleFactor)
camera_transform.scale = (scaleFactor,scaleFactor,scaleFactor)

lamp_transform.scale = (scaleFactor,scaleFactor,scaleFactor)
lamp_transform.location = (Xcenter, Ycenter, Zmin)

#save the scene to outPath with filename envName_assetName.blend

envPath = bpy.data.filepath
envName     = (envPath.split('/')[-1]).split('.')[0]
assetName = (assetPath.split('/')[-1]).split('.')[0]
lampName = (lampPath.split('/')[-1]).split('.')[0]
outName = assetName + '_' + lampName + '_' +envName + '.blend'

bpy.ops.wm.save_as_mainfile(filepath = outPath + '/' + outName)



