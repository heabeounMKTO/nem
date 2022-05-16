import os
import sys
from pathlib import Path
from os.path import join
from os.path import exists
import subprocess
from venv import create

print("""\
 
                                                    
 heabeoun's   _____   ______        ______        ______  _______   
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



mainTextureFolder = input("enter texture directory that contains all the subfolders with textures\n")
autoMatPath = os.path.join(os.getcwd() + "\matauto.py")   
texFolders = list()

def createBlendInSubfolders():
        
    for root,dirs,files in os.walk(mainTextureFolder):
            
        if not dirs:
            texFolders.append(root)
    print(texFolders)
    for blendPath in texFolders:    
        blendPath = Path(blendPath)
        blendName = blendPath.stem + ".blend"
        
        checkForBlendFile = Path(os.path.join(blendPath,blendName))
        
        if(checkForBlendFile.is_file() == False):
            createBlendFile = open(os.path.join(blendPath, blendName), 'w')
            print("creating blend file: " + createBlendFile.name)
            print("created blend files:" + createBlendFile.name)
        else:
            print("blend file " + checkForBlendFile.name + " already exists!")

           
    

    
# def createMaterialInBlend():
#     for blendFiles in mainTexTureFolder:
            
#         blendPath = Path(currentDir) / Path(blendFiles)
            
#         blendName = blendPath.stem + '.blend'
#         blendFilePath = os.path.join(blendPath,blendName)
#         print("opening file: " + blendName)
#         launchBlender = subprocess.run(["blender","--enable-autoexec",blendFilePath, '--python', autoMatPath])
#         #DEVNULL HIDES BLENDER CONSOLE OUTPUT
#         print('file rewritten: ' + blendFilePath)
#         print('material created: ' + blendName)
        
createBlendInSubfolders()
    
    



