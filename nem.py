import os
import sys
from pathlib import Path
from os.path import join
import subprocess

print("""\
 
                                                       
 _____   ______        ______        ______  _______   
|\    \ |\     \   ___|\     \      |      \/       \  
 \\    \| \     \ |     \     \    /          /\     \ 
  \|    \  \     ||     ,_____/|  /     /\   / /\     |
   |     \  |    ||     \--'\_|/ /     /\ \_/ / /    /|
   |      \ |    ||     /___/|  |     |  \|_|/ /    / |
   |    |\ \|    ||     \____|\ |     |       |    |  |
   |____||\_____/||____ '     /||\____\       |____|  /
   |    |/ \|   |||    /_____/ || |    |      |    | / 
   |____|   |___|/|____|     | / \|____|      |____|/  
     \(       )/    \( |_____|/     \(          )/     
      '       '      '    )/         '          '      
                          '                            

""")
print(" THE BLENDER TOOLKIT FOR LAZY PEOPLE BY LAZY PEOPLE ")
print(" this program is provided as is there are no guaratees ")


currentDir = input("enter texture directory that contains all the subfolders with textures\n")
subfoldersList = os.listdir(currentDir)
autoMatPath = os.path.join(os.getcwd() + "\matauto.py")   

def createBlendInSubfolders():
        
    for subFolders in subfoldersList:
            
        texPath = Path(currentDir) / Path(subFolders)
            
        texName = texPath.stem + ".blend"
        
        if(os.path.join(texPath,texName) == None):    
            createBlendFile = open(os.path.join(texPath,texName), 'w')
        else:
            return None
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
    
    



