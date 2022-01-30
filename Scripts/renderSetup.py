'''
This script combines an asset with a render environment and saves the combined scene.
The inputs are the path of the asset (assetPath), the path of the environment (envPath),
where to save the scene (outPath), and how much the asset must scale (scaleFactor). The 
paths should all be relative to the parent directory ('Data/caleb_db/BLENDER')
'''

import sys
import os

dir = os.getcwd() + '/'

assetPath    = dir + sys.argv[1]
lampPath     = dir + sys.argv[2]
envPath      = dir + sys.argv[3]
outPath      = dir + sys.argv[4]

if  'darwin' in sys.platform: blenderPath = 'Blender_exec/blender.app/Contents/MacOS/blender'
elif 'linux' in sys.platform: blenderPath = 'Blender_exec/blender'
else: raise NameError('Unknown operating system, cant choose blenderPath')


os.system('%s -b %s -P Scripts/getAssetData.py' % (blenderPath,assetPath))
os.system('%s -b %s -P Scripts/getLampData.py'  % (blenderPath,lampPath))

#assetPath = assetPath[:-6] + '_temp.blend'
os.system('%s -b %s -P Scripts/sceneAssembler.py -- %s %s %s' % 
          (blenderPath,envPath,assetPath,lampPath,outPath))



