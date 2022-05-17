from gettext import Catalog
import uuid
from pathlib import Path
import os 

# import bpy

matfolders = Path('E:\Extreme Pbr Combo With 1000 Materials Addon For Blender 2.79-2.8-2.81\Extreme PBR Combo With 1000+ Materials Addon For Blender 2.79-2.81-2.82\EXTREME_PBR_LIB')
parentFolder = matfolders.parent
parentFolderName = parentFolder.name
texFolders = list()
catalogUUID = list()

def findAllTextureFolders():
    for root,dirs,files in os.walk(matfolders):
            
        if not dirs:
            texFolders.append(root)
    return texFolders


def createCatalog_UUID():
    findAllTextureFolders()
    for x in texFolders:
        x = Path(x)
        parentFolder = x.parent
        parentFolderName = parentFolder.name 
        catalog_uuid = uuid.uuid1()
        print(catalog_uuid,":Material/"+ parentFolderName,":",parentFolderName)  
        

createCatalog_UUID()