"""
Construction cross-section — FLOOR / WALL / CEILING build-up layers.
Danny's non-toxic spec: timber battens, sheep wool insulation, breathable membrane,
formaldehyde-free birch ply. NO spray foam.
Layer thicknesses are real (mm, labelled); display height is min-clamped so thin layers stay visible.
Run: blender --background --python build_section.py  ->  van_section.glb + section.png
"""
import bpy, os, math
OUT=os.path.dirname(os.path.abspath(__file__))
def m(v): return v/1000.0
def mat(c,r=0.6):
    mt=bpy.data.materials.new('m');mt.use_nodes=True
    b=mt.node_tree.nodes.get('Principled BSDF')
    if b: b.inputs['Base Color'].default_value=(c[0],c[1],c[2],1);b.inputs['Roughness'].default_value=r
    return mt
def box(n,x0,y0,z0,x1,y1,z1,c,r=0.6):
    bpy.ops.mesh.primitive_cube_add(size=1,location=(m((x0+x1)/2),m((y0+y1)/2),m((z0+z1)/2)))
    o=bpy.context.active_object;o.name=n;o.dimensions=(m(abs(x1-x0)),m(abs(y1-y0)),m(abs(z1-z0)))
    o.color=(c[0],c[1],c[2],1);o.data.materials.clear();o.data.materials.append(mat(c,r));return o
def label(t,x,y,z,c=(0.05,0.05,0.06),s=55):
    bpy.ops.object.text_add(location=(m(x),m(y),m(z)))
    o=bpy.context.active_object;o.data.body=t;o.data.size=m(s);o.data.align_x='LEFT';o.data.align_y='CENTER'
    o.color=(c[0],c[1],c[2],1);o.data.materials.clear();o.data.materials.append(mat(c,0.5))
    o.rotation_euler=(math.radians(90),0,0);return o

bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for d in (bpy.data.meshes,bpy.data.cameras,bpy.data.curves,bpy.data.materials):
    for b in list(d):
        try:d.remove(b)
        except Exception:pass

STEEL=(0.55,0.57,0.60);MEMB=(0.30,0.55,0.80);BATT=(0.60,0.42,0.24);WOOL=(0.93,0.90,0.80)
PLY=(0.83,0.66,0.40);VINYL=(0.25,0.25,0.28);CLAD=(0.80,0.62,0.38)
PATCH=600;GAP=45

# (label, colour, REAL mm)
FLOOR=[('Van steel floor',STEEL,2),('Battens 25mm + sheep wool between',WOOL,25),
       ('Birch ply subfloor 15mm',PLY,15),('Cork/vinyl finish 4mm',VINYL,4)]
WALL=[('Van steel + ribs',STEEL,2),('Breathable membrane',MEMB,2),
      ('38mm timber battens + sheep wool',WOOL,38),('Birch ply lining 9mm',PLY,9)]
CEIL=[('Van steel roof',STEEL,2),('45mm battens + sheep wool 50mm',WOOL,50),
      ('Birch ply / cladding 6mm',CLAD,6)]

def column(x0, title, layers):
    z=0
    label(title, x0, -160, PATCH/1000.0*1000+260, (0.05,0.05,0.06), 80)
    box('hdr_%s'%title,x0,-30,260+PATCH,x0+1,-29,261+PATCH,(1,1,1))  # spacer noop
    z=0
    for (name,col,real) in layers:
        dz=max(real,55)                     # display height (thin layers stay visible)
        box('%s_%s'%(title,name[:6]), x0,0,z, x0+PATCH,PATCH,z+dz, col, 0.7)
        if 'batten' in name.lower() or 'Battens' in name:   # draw a couple of timber battens in the wool
            box('batt_a_%s'%title, x0+90,0,z, x0+130,PATCH,z+dz, BATT,0.7)
            box('batt_b_%s'%title, x0+PATCH-130,0,z, x0+PATCH-90,PATCH,z+dz, BATT,0.7)
        label('%s  (%dmm)'%(name,real), x0, -150, z+dz/2, (0.05,0.05,0.06), 52)
        z+=dz+GAP

column(0,    'FLOOR',  FLOOR)
column(950,  'WALL',   WALL)
column(1900, 'CEILING',CEIL)

w=bpy.data.worlds.get('World') or bpy.data.worlds.new('World')
bpy.context.scene.world=w;w.use_nodes=False;w.color=(0.90,0.91,0.93)
sc=bpy.context.scene;sc.render.engine='BLENDER_WORKBENCH'
sh=sc.display.shading;sh.color_type='OBJECT';sh.light='STUDIO';sh.show_cavity=True;sh.show_shadows=True
sc.render.resolution_x=1900;sc.render.resolution_y=1100;sc.render.image_settings.file_format='PNG'
bpy.ops.object.empty_add(location=(m(950),m(300),m(380)));aim=bpy.context.active_object
bpy.ops.object.camera_add(location=(m(950),m(-3200),m(1500)));cam=bpy.context.active_object;cam.data.lens=34
con=cam.constraints.new('TRACK_TO');con.target=aim;con.track_axis='TRACK_NEGATIVE_Z';con.up_axis='UP_Y'
sc.camera=cam;sc.render.filepath=os.path.join(OUT,'section.png')
try:bpy.ops.render.render(write_still=True)
except Exception as e:print('render warn',e)
bpy.ops.export_scene.gltf(filepath=os.path.join(OUT,'van_section.glb'),export_format='GLB',export_apply=True)
print('SECTION DONE ->',OUT)
