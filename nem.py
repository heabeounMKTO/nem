from math import remainder
import os
import sys
from pathlib import Path
from os.path import join
from os.path import exists
import subprocess

from venv import create
import argparse

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


print("                                     COMMANDS LIST:                                ")
print("[1] update mat : updates textures in input directory without overwriting existing ones")
print("[2] renew mat: deletes all existing .blend files in directory and creates new ones")

print("                     ****utilities****                        ")
print("[3] delete blend: deletes all blend file in input directory")
print("[4] remove all rootDir.txt from dir")
print("[5] create rootDir.txt in all mat dir")
print("[6] create blend files in walk dir")
mode = input("enter material processing mode(please enter only 1 number)\n")



mainTextureFolder = input("enter dir material directory\n")
autoMatPath = os.path.join(os.getcwd() + "\matauto.py")   
texFolders = list()
catalogMatNames = list()
newBlend = list()
blendFiles = list()
    
   
    
def findAllTextureFolders():
    
    for root,dirs,files in os.walk(mainTextureFolder):
        
        if not dirs:
            texFolders.append(root)
    print("walking directory...." + os.path.split(mainTextureFolder)[1])
    return texFolders
    


def renewCreateBlend():
        
    findAllTextureFolders()
    for blendPath in texFolders:    
        
           
        blendPath = Path(blendPath)
        blendName = blendPath.stem + ".blend"
      
        
        checkForBlendFile = Path(os.path.join(blendPath,blendName))
        
        if(checkForBlendFile.is_file() == False):
            createBlendFile = open(os.path.join(blendPath, blendName), 'w')
            # print("creating blend file: " + createBlendFile.name)
            # print("created blend files:" + createBlendFile.name)
            blendFiles.append(createBlendFile)
        else:
            print("blend file " + checkForBlendFile.name + " already exists!")
            pass
    print("created " + str(len(blendFiles)) + " new blend files")
             
def renewCreateMaterial():
    findAllTextureFolders()
    for blendFiles in texFolders:
        blendFiles = Path(blendFiles)
        blendName = blendFiles.stem + ".blend"
        fullBlendPath = os.path.join(blendFiles, blendName)
        
        print("opening file: " + blendName)
        launchBlender = subprocess.run(["blender","--enable-autoexec",fullBlendPath, '--python', autoMatPath])
        print("material created:" + blendFiles.stem)            


def removePathTxt():
    cRootDirCount = list()
    findAllTextureFolders()
    print("removing rootDir.txt from all texture folders")
    for blendPath in texFolders:     
        blendPath = Path(blendPath)
        os.remove(os.path.join(blendPath, "rootDir.txt"))
        cRootDirCount.append(blendPath)
        for dir in cRootDirCount:
            pass
    print("deleted"+ str(len(cRootDirCount)) + " rootDir.txt")

def createPathtxt():
    cPathTxtCount = list()
    findAllTextureFolders()
    print("creating rootDir.txt in all texture folders")
    for blendPath in texFolders:       
        blendPath = Path(blendPath)
        writeRootTxt = open(os.path.join(blendPath, "rootDir.txt"), 'w')
        writeRootTxt.write(mainTextureFolder)
        writeRootTxt.close()
        cPathTxtCount.append(blendPath)
        for dir in cPathTxtCount:
            pass
    print("created " + str(len(cPathTxtCount)) + " rootDir.txt files")
def updateCreateBlend():
    findAllTextureFolders()
    for blendPath in texFolders:
        blendPath = Path(blendPath)
        blendName = blendPath.stem + ".blend"
        
        
        # #write rootDir.txt to directory
        # writeRootTxt = open(os.path.join(blendPath, "rootDir.txt"), 'w+')
        # writeRootTxt.write(mainTextureFolder)
        # writeRootTxt.close()
        
        checkForBlendFile = Path(os.path.join(blendPath,blendName))
        if(checkForBlendFile.is_file() == True):
            print("blend file " + checkForBlendFile.name + " already exist")
            pass
        else:   
            createBlendFile = open(os.path.join(blendPath, blendName), 'w')
            newBlend.append(os.path.join(blendPath,blendName))
            print("creating blend file: " + createBlendFile.name)
            print("created blend files:" + createBlendFile.name)        
    newBlendLength = len(newBlend)
    
    print(str(newBlendLength) + " new blend files created")
    print(newBlend)
    return newBlend

def updateCreateMaterial():
    
    for blendFiles in newBlend:
        blendFilesPath = os.path.split(blendFiles)
        blendFiles = Path(blendFiles)
        blendName = blendFiles.stem + ".blend"
        # fullBlendPath = os.path.join(blendFilesPath[0], blendName)

        print(blendFiles) 
        # print(blendName)
        # print(fullBlendPath)
        print("opening file: " + blendName)
        launchBlender = subprocess.run(["blender","--enable-autoexec",blendFiles, '--python', autoMatPath]) 
        print("material created :" + blendFiles.stem)
def renewDeleteAllBlendsInDir():
    findAllTextureFolders()
    blendExtension = (".blend", ".blend1")
    for files in texFolders:
        filesList = os.listdir(files)
        for file in filesList:
            if file.endswith(blendExtension):
                blendFiles.append(os.path.join(files, file))
    for blends in blendFiles:
        os.remove(blends)
    print("deleted " + str(len(blendFiles)) + " blend files")      
        
    
def main():
    if  mode == "1":
        createPathtxt()
        updateCreateBlend()
        updateCreateMaterial()
        removePathTxt()
    
    elif mode == "2":
        createPathtxt()
        renewDeleteAllBlendsInDir()
        renewCreateBlend()
        renewCreateMaterial()     
        removePathTxt()
    
    elif mode == "3":
        renewDeleteAllBlendsInDir()
    
    elif mode == "4":
        removePathTxt()
    
    elif mode == "5":
        createPathtxt()
    
    elif mode == "6":
        renewCreateBlend()
    else:
        print("you entered and invalid processing mode! nem exiting!")
        quit()
        
    
        


main()