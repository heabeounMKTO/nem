import os
import sys
from pathlib import Path
from os.path import join
import subprocess

print("welcome to nem, lazy tool for lazy people by lazy people")
currentDir = input("WHERE IS THE TEXTURE (path pls)\n")
subfoldersList = os.listdir(currentDir)
autoMatPath = os.path.join(os.getcwd() + "\matauto.py")

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
        launchBlender = subprocess.run(["blender","--enable-autoexec",blendFilePath, '--python', autoMatPath])
        #DEVNULL HIDES BLENDER CONSOLE OUTPUT
        print('file rewritten: ' + blendFilePath)
        print('material created: ' + blendName)
        

createBlendInSubfolders()
createMaterialInBlend()    
    
    



