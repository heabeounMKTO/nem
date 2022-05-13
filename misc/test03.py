import os 
from pathlib import Path

testDir = (Path('D:\\nem\\nem\\testdir'))

texFolder = list()
for root,dirs,files in os.walk(testDir):
    if not dirs:
        texFolder.append(root)
print(texFolder)