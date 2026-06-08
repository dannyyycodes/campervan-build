"""
Import the real Fiat Ducato FBX, stand it upright, orient length along +X,
scale to L3 length (5998mm), sit on ground, export a clean GLB for the viewer.
Run: blender --background --python import_real_van.py -> real_ducato.glb + ducato_real.png
"""
import bpy, os, math, mathutils
OUT=os.path.dirname(os.path.abspath(__file__))
F=os.path.join(OUT,'real_van_download2.fbx')

bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for d in (bpy.data.meshes,bpy.data.cameras,bpy.data.curves,bpy.data.lights):
    for b in list(d):
        try:d.remove(b)
        except Exception:pass

bpy.ops.import_scene.fbx(filepath=F)
sc=bpy.context.scene;sc.unit_settings.system='METRIC';sc.unit_settings.length_unit='METERS'
roots=[o for o in sc.objects if o.parent is None]

def wbb():
    mn=[1e9]*3;mx=[-1e9]*3
    for o in sc.objects:
        if o.type!='MESH':continue
        for c in o.bound_box:
            w=o.matrix_world @ mathutils.Vector(c)
            for i in range(3):
                mn[i]=min(mn[i],w[i]);mx[i]=max(mx[i],w[i])
    return mn,mx
def dims():
    mn,mx=wbb();return [mx[i]-mn[i] for i in range(3)],mn,mx
def apply(M):
    for o in roots:o.matrix_world=M@o.matrix_world
    bpy.context.view_layer.update()

d,mn,mx=dims()
print('imported dims mm:',[round(x*1000) for x in d])
# 1) stand upright if lying down (height is the largest dim)
if d[2]>=max(d[0],d[1]):
    apply(mathutils.Matrix.Rotation(math.radians(90),4,'X'));d,mn,mx=dims()
# 2) length along X
if d[1]>d[0]:
    apply(mathutils.Matrix.Rotation(math.radians(90),4,'Z'));d,mn,mx=dims()
# 3) scale to L3 H3: length(X)=5.998m, height(Z)=2.764m, keep natural width
sx=5.998/d[0] if d[0]>0 else 1.0
sz=2.764/d[2] if d[2]>0 else 1.0
apply(mathutils.Matrix.Diagonal((sx,1.0,sz,1.0)));d,mn,mx=dims()
# 4) centre x,y at 0 and sit on ground z=0
apply(mathutils.Matrix.Translation((-(mn[0]+mx[0])/2,-(mn[1]+mx[1])/2,-mn[2])));d,mn,mx=dims()
print('final dims mm:',[round(x*1000) for x in d])

# render + export
w=bpy.data.worlds.get('World') or bpy.data.worlds.new('World')
sc.world=w;w.use_nodes=False;w.color=(0.82,0.84,0.88)
sc.render.engine='BLENDER_WORKBENCH'
shd=sc.display.shading;shd.color_type='MATERIAL';shd.light='STUDIO';shd.show_cavity=True;shd.show_shadows=True
sc.render.resolution_x=1900;sc.render.resolution_y=1100;sc.render.image_settings.file_format='PNG'
bpy.ops.object.empty_add(location=(0,0,0.8));aim=bpy.context.active_object
bpy.ops.object.camera_add(location=(-6.5,-7.5,3.4));cam=bpy.context.active_object;cam.data.lens=50
con=cam.constraints.new('TRACK_TO');con.target=aim;con.track_axis='TRACK_NEGATIVE_Z';con.up_axis='UP_Y'
sc.camera=cam;sc.render.filepath=os.path.join(OUT,'ducato_real.png')
try:bpy.ops.render.render(write_still=True)
except Exception as e:print('rwarn',e)
bpy.ops.export_scene.gltf(filepath=os.path.join(OUT,'real_ducato.glb'),export_format='GLB',export_apply=True)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT,'ducato_L3H3_realimport.blend'))
print('IMPORT DONE ->',OUT)
