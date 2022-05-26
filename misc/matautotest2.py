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



createUUID = str(uuid.uuid4())
#find catalong of textures
filepath = bpy.data.filepath
directory = os.path.dirname(filepath)
directoryPath = Path(directory)

catalogPath = Path(directoryPath.parent)
    
catalogName = catalogPath.name
    
assetDir = Path(catalogPath.parent)

    
print(catalogName)

def clearScene():
   
   bpy.ops.object.select_all(action = "SELECT")
   bpy.ops.object.delete()  

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
   
   #additional types of materials and functions can be created from here
   #principled shader below can be used as a template.

   if type == "Principled":
        #create all nodes
       relPath = bpy.path.abspath("//")
       
       shader = nodes.new(type='ShaderNodeBsdfPrincipled')
       shader.location = (-300, 0)

       diffuse = nodes.new(type = 'ShaderNodeTexImage')
       
       normal = nodes.new(type = 'ShaderNodeTexImage')
       
       normalMapNode = nodes.new (type = 'ShaderNodeNormalMap')
       normalMapNode.location = (-800, -200)
       
       roughness = nodes.new(type = 'ShaderNodeTexImage')

       metallic = nodes.new(type = 'ShaderNodeTexImage')
       
       disp = nodes.new(type = 'ShaderNodeTexImage')
       
       mappingNode = nodes.new(type = 'ShaderNodeMapping')
       mappingNode.location = (-1600, 0)
       texCoords =nodes.new(type = 'ShaderNodeTexCoord')
       texCoords.location = (-2000, 0)

       # alphaCh = nodes.new(type = 'ShaderNodeTexImage')
       #add maps from relative path to created nodes
       #         
       addMapsFromRelativePath(diffuse, "diff", "sRGB")
       if(diffuse.image == None):
           addMapsFromRelativePath(diffuse, "col", "sRGB")
       addMapsFromRelativePath(normal, "nor", "Non-Color")
       if(normal.image == None):
           addMapsFromRelativePath(normal, "nrm", "Non-Color")
       addMapsFromRelativePath(roughness, "rough", "Non-Color")
       addMapsFromRelativePath(disp, "disp", "Non-Color")
       addMapsFromRelativePath(metallic,"metal", "Non-Color")
       if(metallic.image == None):
           addMapsFromRelativePath(metallic, "met", "Non-Color")    
       # addMapsFromRelativePath(alphaCh,"opacity", 'Non-Color')
       # if(alphaCh.image == None):
       #     addMapsFromRelativePath(alphaCh, "alpha","Non-Color")
       
       
       
 
   #node linking section
   links.new(diffuse.outputs[0], shader.inputs[0])
   links.new(normal.outputs[0], normalMapNode.inputs[1])
   links.new(normalMapNode.outputs[0], shader.inputs["Normal"])
   links.new(roughness.outputs[0], shader.inputs["Roughness"])
   links.new(disp.outputs[0], output.inputs["Displacement"])
   links.new(texCoords.outputs[2], mappingNode.inputs["Vector"])
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

21#find files 
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
def addMapsFromRelativePath(nodeName ,mapName, colorSpace):
   relPath = bpy.path.abspath("//")
   for fp in image_files(mapName, path=relPath):
       nodeName.image = bpy.data.images.load(join(relPath, fp))
       nodeName.image.colorspace_settings.name = colorSpace
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

def createCatalongName():
    
    readRootDir = open(os.path.join(directoryPath, "rootDir.txt"), 'r')
    rootDir = readRootDir.readlines()[0]
    
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
createCatalongName()
drawPbrSphere()
markAsset()

bpy.app.timers.register(saveAndQuit, first_interval = 15)
#                
#        
#              
#        


