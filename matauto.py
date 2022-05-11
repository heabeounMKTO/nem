import bpy 
import os 
import glob
from os.path import join
import time 
from bpy.app.handlers import persistent

    
    
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
        #add maps from relative path to created nodes
        #         
        addMapsFromRelativePath(diffuse, "diff")
        if(diffuse.image == None):
            addMapsFromRelativePath(diffuse, "col")
        addMapsFromRelativePath(normal, "nor")
        if(normal.image == None):
            addMapsFromRelativePath(normal, "nrm")
        addMapsFromRelativePath(roughness, "rough")
        addMapsFromRelativePath(disp, "disp")
        addMapsFromRelativePath(metallic,"metal")
        if(metallic.image == None):
            addMapsFromRelativePath(metallic, "met")    
       
        
        
        
  
    #node linking section
    links.new(diffuse.outputs[0], shader.inputs[0])
    links.new(normal.outputs[0], normalMapNode.inputs[1])
    links.new(normalMapNode.outputs[0], shader.inputs["Normal"])
    links.new(roughness.outputs[0], shader.inputs["Roughness"])
    links.new(disp.outputs[0], output.inputs["Displacement"])
    links.new(texCoords.outputs[2], mappingNode.inputs["Vector"])

    #tex coords and mapping linking 
    links.new(mappingNode.outputs[0], diffuse.inputs[0])
    links.new(mappingNode.outputs[0], roughness.inputs[0])
    links.new(mappingNode.outputs[0], disp.inputs[0])
    links.new(mappingNode.outputs[0], normal.inputs[0])
    links.new(shader.outputs[0], output.inputs[0])
    

    return mat
       
      
def drawPbrSphere():
    # idx = bpy.context.window_manager.windows[:].index(bpy.context.window)
    # window = bpy.context.window_manager.windows[idx]
    # screen = window.screen
    # for a in screen.areas:
    #     if(a.type == 'VIEW_3D'):
    #         print("area is view3d")
    blendname = bpy.path.basename(bpy.context.blend_data.filepath)
    mat = createPrincipledShader(blendname, "Principled")
    bpy.data.materials[blendname].asset_mark()
    bpy.ops.mesh.primitive_uv_sphere_add(segments=32, radius = 0.5, location=(0,0,0))
    bpy.ops.object.shade_smooth()
    bpy.context.active_object.data.materials.append(mat)
    print("pbrSphereDrawn.")                
#find files 
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
def addMapsFromRelativePath(nodeName ,mapName):
    relPath = bpy.path.abspath("//")
    for fp in image_files(mapName, path=relPath):
        nodeName.image = bpy.data.images.load(join(relPath, fp))

def saveAndQuit():
    bpy.ops.wm.save_mainfile()
    bpy.ops.wm.quit_blender()        


def get_context():
    # create a context that works when blender is executed from the command line.
    idx = bpy.context.window_manager.windows[:].index(bpy.context.window)
    window = bpy.context.window_manager.windows[idx]
    screen = window.screen
    views_3d = sorted(
            [a for a in screen.areas if a.type == 'VIEW_3D'],
            key=lambda a: (a.width * a.height))



drawPbrSphere()
saveAndQuit()
       
            
        
              
        


