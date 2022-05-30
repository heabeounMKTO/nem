from unicodedata import name
import xml.etree.ElementTree as ET
import os 
from pathlib import Path



tree = ET.parse("texDict.xml")

root = tree.getroot()

diffuseDict = list()
normalDict = list()
metallicDict = list()
metallicKeyWordDict = list()

def findMetallick():
    for mtlk in root.findall("metallickeyword"):
        label = mtlk.find("keyword").text
        metallicKeyWordDict.append(label)
    print(metallicKeyWordDict)


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



findMetallick()
