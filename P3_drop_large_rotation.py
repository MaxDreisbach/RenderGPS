#Render routine for synthesized drop test images.
#Takes stl files of a drop, applies correct material, applies subdivision surface modifier, renders the animation with the curent timeline settings, i.e. different seeds, focus points, angles,...
#Outputs raw image and denoised image.
#Tested using Blender 2.93 and BlendLuxCore 2.6.
#Run this script out of Blender install dir with the command (on Windows):

''' Usage: Open through blender
export PATH=../Projects/blender-2.91.0-linux64/
blender -b --python "P3_drop_large_rotation.py"
'''

dirname = "../../Data/Fink2018_non_axis_symmetrical/stl/"
blender_file = 'refresh_june_GPU_fast_96.3deg_30deg.blend'
SUBDIV = True # Subdivision refinement (significantly increases render time, but also quality by increasing mesh resolution and smoothing)
FLIP_NORMALS = False # For meshes with inverted normals
START = 0
END = 1500


from operator import index
import bpy
import os
import os.path
import mathutils
import time
import math
from pathlib import Path


def file_selection():
    req_files = input('Input the index of the files you want to render as a comma seperated list without spaces, i.e. 0,1,2. Leave empty for all\n').split(',')
    
    try:
        if req_files != ['']:
            req_files = [int(x) for x in req_files]
    except:
        print('Incorrect Input!')
        req_files = file_selection()

    return req_files


def stl_selection():
    filelist = [file for file in sorted(os.listdir(dirname)) if file.endswith('.stl')]

    return filelist
    
def cut_filelist(filelist,START,END):
    cut_filelist = filelist[START:END]
    return cut_filelist


print('Opening Blender file ' + blender_file + '...', end=' ')
bpy.ops.wm.open_mainfile(filepath=os.path.join(blender_file))
scene = bpy.context.scene
nodes = scene.node_tree.nodes
print('Done')

filelist = stl_selection()
filelist = cut_filelist(filelist,START,END)

for count,file in enumerate(filelist):

    print('Importing file ' + str(count+START) + '...' + file + '...', end=' ', flush=True)
    bpy.ops.import_mesh.stl(filepath=os.path.join(dirname, file))
    ob = bpy.context.active_object
    
    # NEW: Flip normals for inverted meshes
    if file.startswith("droplet"):
        FLIP_NORMALS = False
    else:
        FLIP_NORMALS = True

    if FLIP_NORMALS:
        bpy.context.view_layer.objects.active = ob
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.flip_normals()
        bpy.ops.object.mode_set()

    print('Apply material to drop...', end=' ', flush=True)
    mat = bpy.data.materials.get('water')
    ob.data.materials.append(mat)
    print('Done')

    if SUBDIV:
        start_time = time.time()
        print('Apply level 2 subdivision surface modifier to drop (this might take a while)...', end=' ', flush=True)
        modifier = ob.modifiers.new(name='Subdiv', type='SUBSURF')
        show_only_control_edges = False
        modifier.levels = 2
        bpy.ops.object.modifier_apply(modifier='Subdiv')
        print('Done')
        print("--- %s seconds to apply level 2 subdivision ---" % (time.time() - start_time))

    # Scale mesh
    print('Scaling mesh...', end=' ', flush=True)
    k = 0.625  # set scale constant to match with PIFu Rendering for masks and calibration matrices - TODO: implement mask rendering, etc. in Blender
    bpy.ops.transform.resize(value=(k, k, k))
    bpy.ops.object.transform_apply(scale=True)
    print('Done')

    # Translate mesh to z=0 (if necessary)
    print('Translating mesh to z=0...', end=' ', flush=True)
    loc = ob.location
    if file.startswith("droplet"):
        z_tranlate = -0.0000625
    else:
        z_tranlate = -0.000034625
    ob.location = loc + mathutils.Vector((0, 0, z_tranlate))
    print('Done')

    # Rotate the mesh by 360° in 10° increments
    angles = range(0,360,10)
    print('Rotation angles:', end=' ', flush=True)
    print(angles)
    for angle in angles:

        # Rotating mesh
        if angle !=0:
            print('Rotating mesh', angle, 'degrees...', end=' ', flush=True)
            bpy.ops.transform.rotate(value=math.radians(10), orient_axis='Z')
            bpy.ops.object.transform_apply(scale=True)
            print('Done')

        print('Create output directory...', end=' ', flush=True)
        out1 = nodes['File Output.001']
        out1.base_path = 'denoised/' + Path(os.path.join(dirname, '/stl/', file)).stem + '_' + str(angle)
        out2 = nodes['File Output']
        out2.base_path = 'render_rotation/' + Path(os.path.join(dirname, '/stl/', file)).stem + '_' + str(angle)
        print('Done')

        print('Rendering drop ' + str(count+START) + '...' + file + '...', end=' ', flush=True)
        bpy.ops.render.render(animation=True)
        print('Done')

    print('Remove ' + file + ' from scene collection...', end=' ', flush=True)
    bpy.data.objects.remove(ob, do_unlink=True)
    print('Done')
