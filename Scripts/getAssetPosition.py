import bpy

vertCoords = []

meshes = [obj for obj in bpy.data.objects if obj.type == 'MESH']

for mesh in meshes:
	#un-parent the mesh
	mesh.parent = None
	
	#apply transforms and modifiers
	bpy.ops.object.select_all( action='DESELECT' )
	bpy.context.view_layer.objects.active = mesh
	mesh.select = True
	modifiers = [mod.name for mod in mesh.modifiers]
	try: 
		bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
		for mod in modifiers: bpy.ops.object.modifier_apply(modifier=mod)
		#get vertex locations
		for vert in mesh.data.vertices: vertCoords.append(vert.co)
	except: pass		

Xrange = max([co[0] for co in vertCoords]) - min([co[0] for co in vertCoords])
Yrange = max([co[1] for co in vertCoords]) - min([co[1] for co in vertCoords])
Zrange = max([co[2] for co in vertCoords]) - min([co[2] for co in vertCoords])

scaleFactor = (Xrange + Yrange + Zrange)/3

Xcenter = (max([co[0] for co in vertCoords]) + min([co[0] for co in vertCoords]))/2
Ycenter = (max([co[1] for co in vertCoords]) + min([co[1] for co in vertCoords]))/2
Zmin = min([co[2] for co in vertCoords])

print('\ndoing it! \n')

f = open('Meta/AssetPosition.txt','w')
f.write(repr(scaleFactor) + ',' + repr(Xcenter) + ',' + repr(Ycenter) + ',' + repr(Zmin))
f.close()