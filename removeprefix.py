from distutils.filelist import findall
import os, fnmatch, exifread
from pathlib import Path

mainTexFolder = Path('D:\\nem\\nemtest\\nem\\testdir')
textures = list()

picture = open(Path("D:\\nem\\nemtest\\nem\\testdir\\Bronze\\2K_Bronze_01\\Bronze_01_diffuse_xtm.png"), 'rb')
tags = exifread.process_file(picture)
def findAllTextures():
    for root,dirs,files in os.walk(mainTexFolder):
        if dirs:
            textures.append(dirs)
    
    return textures

def removeName():
    findAllTextures()
    for filename in textures:
        for folder in filename:
            name = "2K_"
            if name in folder:
                os.rename(folder, folder.replace('2K_', ''))


print(tags)