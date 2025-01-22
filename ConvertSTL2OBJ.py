import bpy
import os
import mathutils

''' Usage: Open through blender
export PATH=/net/istmhome/users/hi227/Projects/blender-2.91.0-linux64/
blender -b --python "/net/istmhome/users/hi227/Projects/Blender_droplet_shear_flow/ConvertSTL2OBJ.py"
'''

input_path = "stl/"
export_path = "obj/"

decimateRatio=0.2
modifierName='DecimateMod'

##Cleans all decimate modifiers
def cleanAllDecimateModifiers(obj):
    for m in obj.modifiers:
        if(m.type=="DECIMATE"):
#           print("Removing modifier ")
            obj.modifiers.remove(modifier=m)


# completely removes cube if in scene
context = bpy.context
scene = context.scene
cube = scene.objects.get("Cube")
if cube:
    bpy.data.objects.remove(cube, do_unlink=True)


for root, dirs, files in os.walk(input_path):
    files.sort()
    #files = files[280:]
    print(files)
    for name in files:
        if name.endswith('stl'):
            # delete everything
            print(name)
            bpy.ops.object.select_all(action='SELECT')
            bpy.ops.object.delete()
            # adjust this to match the import smd operator
            bpy.ops.import_mesh.stl(filepath=os.path.join(root, name))
            #scale mesh
            k = 50000 #scale constant
            bpy.ops.transform.resize(value=(k,k,k))
            bpy.ops.object.transform_apply(scale=True)
            #translate mesh
            #get the object
            for obj in bpy.data.objects:
                loc = obj.location
                # adjustment values
                #(x,y,z) = (0,0,-2.75)
                # adding adjustment values to the property
                #obj.location = loc + mathutils.Vector((x,y,z))
                
                # Reduce amount of vertices and faces
                #if obj.type == "MESH":
                #    cleanAllDecimateModifiers(obj)
    
                #    modifier = obj.modifiers.new(modifierName, 'DECIMATE')
                #    modifier.ratio = decimateRatio
                #    modifier.use_collapse_triangulate = True

            # Add UV-Map (otherwise render complains about missing mat files)
            context = bpy.context
            scene = context.scene
            # all meshes on mesh objects in scene
            meshes = [o.data for o in scene.objects
                      if o.type == 'MESH']
            # add a new "map1" UV to each
            for m in meshes:
                # m.uv_textures.new("map1")
                print('Adding UV map')
                m.uv_layers.new()

            #export as obj
            bpy.ops.export_scene.obj(filepath=os.path.join(export_path, name[:-4]+'.obj'))
