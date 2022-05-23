
from gettext import Catalog
import uuid
from pathlib import Path
import os 

# import bpy

matfolders = Path("D:\\nem\\nemtest\\nem\\testdir")
parentFolder = matfolders.parent
parentFolderName = parentFolder.name
texFolders = list()
catalogUUID = list()
#walks directory to find 
#all root folders within sub directory



def findAllTextureFolders():
    for root,dirs,files in os.walk(matfolders):
        if files:   
            if not dirs:
                texFolders.append(root)
    print(texFolders)
    return texFolders


def createCatalog_UUID():
    findAllTextureFolders()
    for testsplitPath in texFolders:
        testsplitPath = Path(testsplitPath)
        splitcatpath =  os.path.relpath(testsplitPath, matfolders)
        getFolderName = os.path.split(splitcatpath)
        textureCategeoryName = getFolderName[0].replace(os.sep, '/')
        textureFolderName = getFolderName[1]
        print(textureCategeoryName)
        print(textureFolderName)


# findAllTextureFolders()
createCatalog_UUID()   
#splitPathTest()
