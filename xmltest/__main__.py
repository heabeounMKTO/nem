from unicodedata import name
import xml.etree.ElementTree as ET
import os 
from pathlib import Path



tree = ET.parse("texDict.xml")

root = tree.getroot()

diffuseDict = list()
normalDict = list()
metallicDict = list()

def findDiffuseDict():
    for diffuse in root.findall("diffuse"):
        label = diffuse.find("label").text
    
        diffuseDict.append(label)
    return diffuseDict
def findNormalDict():
    for normal in root.findall("normal"):
        label = normal.find("label").text
        
        normalDict.append(label)
    return normalDict

with open("texture_dictionary.txt", 'r') as txt:
    read = txt.readlines()[0]
    print(read)
    
# findDiffuseDict()
# findNormalDict()
# print(diffuseDict)
# print(normalDict)