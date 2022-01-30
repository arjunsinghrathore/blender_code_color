import bpy
import sys

meshList = ''
for obj in bpy.data.objects:
	if obj.type == 'MESH':
		meshList = meshList + obj.name + ','

textureList = ''
for texture in bpy.data.textures:
		textureList = textureList + texture.name + ','

materialList = ''
for mat in bpy.data.materials:
	materialList = materialList + mat.name + ','

f = open('Meta/assetData.txt', 'w')
for mesh in meshList:
	f.write(mesh)
f.write('..')
for texture in textureList:
	f.write(texture)
f.write('..')
for material in materialList:
	f.write(material)
f.close()
