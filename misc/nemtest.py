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



mainTextureFolder = Path('D:\nem\nemtest\nem\testdir')
autoMatPath = os.path.join(os.getcwd() + "\matauto.py")   
texFolders = list()
catalogMatNames = list()

# def findAllTextureFolders():
#     for root,dirs,files in os.walk(mainTextureFolder):
            
#         if not dirs:
#             texFolders.append(root)
#     return texFolders



# def createBlendInSubfolders():
        
#     findAllTextureFolders()
#     for blendPath in texFolders:    
#         blendPath = Path(blendPath)
#         blendName = blendPath.stem + ".blend"
        
#         checkForBlendFile = Path(os.path.join(blendPath,blendName))
        
#         if(checkForBlendFile.is_file() == False):
#             createBlendFile = open(os.path.join(blendPath, blendName), 'w')
#             print("creating blend file: " + createBlendFile.name)
#             print("created blend files:" + createBlendFile.name)
#         else:
#             print("blend file " + checkForBlendFile.name + " already exists!")

           
    

    
# def createMaterialInBlend():
#     findAllTextureFolders()
#     for blendFiles in texFolders:
#         blendFiles = Path(blendFiles)
#         blendName = blendFiles.stem + ".blend"
#         fullBlendPath = os.path.join(blendFiles, blendName)
        
#         print("opening file: " + blendName)
#         launchBlender = subprocess.run(["blender","--enable-autoexec",fullBlendPath, '--python', autoMatPath])
#         print("material created:" + blendFiles.stem)            

def createMaterialsCatalog():
    findAllMatCatalog = os.listdir(mainTextureFolder)
    for catalogFolders in findAllMatCatalog:
        

createBlendInSubfolders()
createMaterialInBlend()
print("all conversions done!")    
    



