import os
import sys
from pathlib import Path
from os.path import join
import subprocess


currentDir = os.getcwd()
subfoldersList = os.listdir(currentDir)

def createBlendInSubfolders():
    
    for subFolders in subfoldersList:
        
        texPath = Path(currentDir) / Path(subFolders)
        
        texName = texPath.stem + ".blend"
        
        createBlendFile = open(os.path.join(texPath,texName), 'w')
        print('created blend file: ' + createBlendFile.name)

def createMaterialInBlend():
    for blendFiles in subfoldersList:
        
        blendPath = Path(currentDir) / Path(blendFiles)
        
        blendName = blendPath.stem + '.blend'
        blendFilePath = os.path.join(blendPath,blendName)
        print("opening file: " + blendName)
        launchBlender = subprocess.run(["blender","--enable-autoexec",blendFilePath, '--python', "D:\matlib\matauto.py"])
        #DEVNULL HIDES BLENDER CONSOLE OUTPUT
        print('file rewritten: ' + blendFilePath)
        print('material created: ' + blendName)
        

createBlendInSubfolders()
createMaterialInBlend()    
    
    



