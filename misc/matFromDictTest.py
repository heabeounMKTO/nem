import bpy 
import os 
import glob
from os.path import join
from pathlib import Path
import time 
from bpy.app.handlers import persistent
import numpy as np
import functools
import uuid 
import xml.etree.ElementTree as ET



createUUID = str(uuid.uuid4())
#find catalong of textures
filepath = bpy.data.filepath
directory = os.path.dirname(filepath)
directoryPath = Path(directory)

catalogPath = Path(directoryPath.parent)
    
catalogName = catalogPath.name
print(catalogName)    
assetDir = Path(catalogPath.parent)

#texture dictionary from texDict.XML
diffuseDict = list()
normalDict = list()
metallicDict = list()
dispDict = list()
roughnessDict = list()
specularDict = list()
alphaDict = list()
emissionDict = list()
metallicKeywordDict = list()
#parse XML section

dictXMLtree = open(os.path.join(directoryPath, "rootDir.txt"), 'r')
readDictXML = dictXMLtree.readlines()[1]
xMLFilePath = os.path.join(readDictXML, "texDict.xml")
dictXML = ET.parse(xMLFilePath)
dictRoot = dictXML.getroot()

    

def findDict(word, dictName):
    for word in dictRoot.findall(word):
        keyword = word.find("keyword").text
        dictName.append(keyword)
    return dictName



def renderThumb():
   bpy.data.objects['Sphere'].select_set(True)
   for area in bpy.context.screen.areas:
       if area.type == "PROPERTIES":
           bpy.context.space_data.context = 'MATERIAL'



def pbrMaterial(id):
   mat = bpy.data.materials.get(id)
   
   
   if mat is None:
       mat = bpy.data.materials.new(name=id)
   
   mat.use_nodes = True
   
   if mat.node_tree:
       mat.node_tree.links.clear()
       mat.node_tree.nodes.clear()
   return mat

def createPrincipledShader(id, type):

   mat = pbrMaterial(id)
   nodes = mat.node_tree.nodes
   links = mat.node_tree.links
   output = nodes.new(type='ShaderNodeOutputMaterial')
   output.location = (1200, 0)
   #additional types of materials and functions can be created from here
   #principled shader belo1w can be used as a template.

   if type == "Principled":
        #create all nodes
       relPath = bpy.path.abspath("//")
       displacement = nodes.new(type="ShaderNodeDisplacement")
       displacement.location = (900, -300)
       
       shader = nodes.new(type='ShaderNodeBsdfPrincipled')
       shader.location = (300, 0)
       
       
       
       diffuse = nodes.new(type = 'ShaderNodeTexImage')
       diffuse.location = (-300, 100)
       
       normal = nodes.new(type = 'ShaderNodeTexImage')
       normal.location = (-300, -100)
       
       normalMapNode = nodes.new (type = 'ShaderNodeNormalMap')
       normalMapNode.location = (-25, -450)
       
       roughness = nodes.new(type = 'ShaderNodeTexImage')
       roughness.location = (-300, -300)
       
       
      
       disp = nodes.new(type = 'ShaderNodeTexImage')
       disp.location = (-300, -800)
       
       mappingNode = nodes.new(type = 'ShaderNodeMapping')
       mappingNode.location = (-1600, 0)
       texCoords =nodes.new(type = 'ShaderNodeTexCoord')
       texCoords.location = (-2000, 0)
       
       checkMetal = checkForMap(mapName = 'metallic', dictName=metallicDict)
       if checkMetal == True:
          metallic = nodes.new(type = 'ShaderNodeTexImage')
          metallic.location = (-300, -600)
          addMapsFromRelativePath(metallic,metallicDict, "Non-Color")
       else:
           checkIfMetalMat = checkForMap(mapName = 'metallicKeyword', dictName=metallicKeywordDict)
           if checkIfMetalMat == True:
               shader.inputs.get("Metallic").default_value = 1.0
           else:
               pass
          
            
       
       checkAlpha = checkForMap(mapName = 'alpha', dictName=alphaDict)
       if checkAlpha == True:
          alpha = nodes.new(type = 'ShaderNodeTexImage')
          alpha.location = (-400, -800)
          addMapsFromRelativePath(alpha, alphaDict, "Non-Color")
       else:
           shader.inputs.get("Alpha").default_value = 1.0
        
       checkEmission = checkForMap(mapName = 'emission', dictName=emissionDict)
       if checkEmission == True:
           emission = nodes.new(type = "ShaderNodeTexImage0000") 
           emission.location = (-600, -1000)
           addMapsFromRelativePath(emission, emissionDict, "sRGB")
       else:
           pass
       
       addMapsFromRelativePath(diffuse, diffuseDict, "sRGB")
       addMapsFromRelativePath(normal, normalDict, "Non-Color")
       addMapsFromRelativePath(roughness, roughnessDict, "Non-Color")
       addMapsFromRelativePath(disp, dispDict, "Non-Color")
       
       
       
       
       
       
 
   #node linking section
   links.new(diffuse.outputs[0], shader.inputs[0])
   links.new(normal.outputs[0], normalMapNode.inputs[1])
   links.new(normalMapNode.outputs[0], shader.inputs["Normal"])
   links.new(roughness.outputs[0], shader.inputs["Roughness"])
   links.new(disp.outputs[0], displacement.inputs["Height"])
   links.new(texCoords.outputs[2], mappingNode.inputs["Vector"])
   links.new(displacement.outputs[0], output.inputs["Displacement"])
  
  
   # links.new(alphaCh.outputs[0]), shader.inputs['Alpha'])
   #tex coords and mapping linking 
   links.new(mappingNode.outputs[0], diffuse.inputs[0])
   links.new(mappingNode.outputs[0], roughness.inputs[0])
   links.new(mappingNode.outputs[0], disp.inputs[0])
   links.new(mappingNode.outputs[0], normal.inputs[0])
   links.new(shader.outputs[0], output.inputs[0])
   

   return mat
      
     
def drawPbrSphere():
   
   blendname = bpy.path.basename(bpy.context.blend_data.filepath)
      
   mat = createPrincipledShader(blendname.removesuffix(".blend"), "Principled")
   
   
   bpy.ops.mesh.primitive_uv_sphere_add(segments=32, radius = 0.5, location=(0,0,0))
   bpy.ops.object.shade_smooth()
   bpy.context.active_object.data.materials.append(mat)
   print("pbrSphereDrawn.")                

def find_files(substring, path='.', extensions=[]):
   from os import listdir
   from re import search, IGNORECASE
   return [f for f in listdir(path) 
           if search(r'%s' % substring, f, IGNORECASE) 
           and any(search(r'%s$' % ext, f, IGNORECASE) 
                   for ext in extensions)]
#find image files
def image_files(substring, path="."):
   return find_files(substring, path=path, extensions=bpy.path.extensions_image)

#nodeName is the name given to nodes created in createPrincipledShader()
#mapName is the name of the image files to search in the relative path
#mapName is the name of the image files to search in the relative path
def addMapsFromRelativePath(nodeName, textureDict, colorSpace):
   from re import search, IGNORECASE
   relPath = bpy.path.abspath("//")

   
   
   for root, subdir, filename in os.walk(relPath):
       
       for file in filename:
           check = any(ele in file for ele in textureDict)
           if check == True:
               imgpath = os.path.join(directoryPath, file)
               print(imgpath)
               nodeName.image = bpy.data.images.load(imgpath)
               nodeName.image.colorspace_settings.name = colorSpace

def checkForMap(mapName, dictName):
    relPath = bpy.path.abspath("//")
    
    for root, subdir,filename in os.walk(relPath):
        
        for file in filename:
            mapName = any(ele in file for ele in dictName)
            return bool(mapName)
    
            
            
def saveAndQuit():
   bpy.ops.wm.save_mainfile()
   bpy.ops.wm.quit_blender()        



def markAsset():
   
   target_catalog = catalogName
   blendname = bpy.path.basename(bpy.context.blend_data.filepath)
   bpy.data.materials[blendname.removesuffix(".blend")].asset_mark()
   bpy.data.materials[blendname.removesuffix(".blend")].asset_generate_preview()
   
   
   asset = bpy.data.materials[blendname.removesuffix(".blend")].asset_data
   asset.catalog_id = createUUID    

def createCatalogName():
    
    readRootDir = open(os.path.join(directoryPath, "rootDir.txt"), 'r')
    rootDir = readRootDir.readlines()[0]
    rootDir = rootDir.rstrip('\n')
    
    ba_catalogFile = os.path.join(rootDir,"blender_assets.cats.txt")
    
    splitCatalogPath = os.path.relpath(directoryPath, rootDir)
    getFolderName = os.path.split(splitCatalogPath)
    textureCategeoryName = getFolderName[0].replace(os.sep, '/')
    textureFolderName = getFolderName[1]
    # catalogUUIDFromFile = str(createUUID, ":Material/", catalogName, ":", catalogName)
    
    if (Path(ba_catalogFile).is_file() == False):
        
        
        createCatalogFile = open(ba_catalogFile, "w")
        with open(ba_catalogFile, "w") as catalogFile:
            catalogFile.write("#Other lines are of the format uu")
            catalogFile.write("\n")
            catalogFile.write("VERSION 1\n")
            catalogFile.write(createUUID)
            catalogFile.write(":")
            catalogFile.write("Material")
            catalogFile.write("/")
            catalogFile.write(textureCategeoryName)
            catalogFile.write(":")
            catalogFile.write(textureFolderName)
            catalogFile.close()
                    
    else:
        print("there is already a catalog file!")       
        print("writing to existing catalog file instead!")
        with open(ba_catalogFile, "a+") as catalogFile:
            
            catalogFile.write("\n") 
            catalogFile.write(createUUID)
            catalogFile.write(":")
            catalogFile.write("Material")
            catalogFile.write("/")
            catalogFile.write(textureCategeoryName)
            catalogFile.write(":")
            catalogFile.write(textureFolderName)
            catalogFile.close()
    return createUUID                        
   
###clearScene()

findDict(word='diffuse', dictName = diffuseDict)
findDict(word='alpha', dictName = alphaDict)
findDict(word="displacement", dictName = dispDict)
findDict(word="normal", dictName=normalDict)
findDict(word= "metallic", dictName=metallicDict)
findDict(word="roughness", dictName=roughnessDict)
findDict(word="emission", dictName=emissionDict)
findDict(word="metallicKeyword", dictName=metallicKeywordDict)

createCatalogName()
drawPbrSphere()
markAsset()

#bpy.app.timers.register(saveAndQuit, first_interval = 15)


