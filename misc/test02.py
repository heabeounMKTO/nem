
import os
import sys
from os import scandir
from pathlib import Path
from os.path import join

testDir = (Path('D:\\nem\\nem\\testdir'))
subfoldersList = os.listdir(testDir)
# print("folders inside testdir\n")
# print(subfoldersList)
textureFolderDir = []
def findAllCategeoryInDir():
    texSubfolder = []
    
    #find all subdirectories within a file 
    for subFolders in subfoldersList:
        subFolders = os.path.join(testDir, subFolders)
        texSubfolder.append(subFolders)
    return texSubfolder        


def findTexturesInCategeory():
    categeoryInDir = findAllCategeoryInDir()
  
    for texturesInCategeory in categeoryInDir:
        texturesInDirectory = os.listdir(texturesInCategeory)
        for texturesFolders in texturesInDirectory:
            textureFilePath = os.path.join(categeoryInDir, texturesFolders)
    return textureFilePath

print(findTexturesInCategeory())        


