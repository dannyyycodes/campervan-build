"""
Bed options for the Ducato L3 H3 rear — TRANSVERSE vs LENGTHWAYS, with bedside shelves.
Builds two GLBs the browser viewer can toggle between.
Run: blender --background --python build_bed_options.py
Outputs: van_bed_transverse.glb, van_bed_lengthways.glb + QC renders
Interior coords (mm): x0..3705 (front->rear), y0..1870 (kerb->driver), z0..2172 (floor->ceiling).
Open dollhouse: no roof, no kerb (near) wall, so you can look straight in.
Danny = 6ft (1829mm).
"""
import bpy, os, math
OUT = os.path.dirname(os.path.abspath(__file__))
def m(v): return v/1000.0

def mat(c, r=0.6):
    mt=bpy.data.materials.new('m'); mt.use_nodes=True
    b=mt.node_tree.nodes.get('Principled BSDF')
    if b: b.inputs['Base Color'].default_value=(c[0],c[1],c[2],1); b.inputs['Roughness'].default_value=r
    return mt
def box(name,x0,y0,z0,x1,y1,z1,c,r=0.6):
    bpy.ops.mesh.primitive_cube_add(size=1,location=(m((x0+x1)/2),m((y0+y1)/2),m((z0+z1)/2)))
    o=bpy.context.active_object;o.name=name;o.dimensions=(m(abs(x1-x0)),m(abs(y1-y0)),m(abs(z1-z0)))
    o.color=(c[0],c[1],c[2],1);o.data.materials.clear();o.data.materials.append(mat(c,r));return o
def label(t,x,y,z,c=(0.05,0.05,0.06),s=90):
    bpy.ops.object.text_add(location=(m(x),m(y),m(z)))
    o=bpy.context.active_object;o.data.body=t;o.data.size=m(s);o.data.align_x='CENTER';o.data.align_y='CENTER'
    o.color=(c[0],c[1],c[2],1);o.data.materials.clear();o.data.materials.append(mat(c,0.5))
    o.rotation_euler=(math.radians(90),0,0);return o   # stand text up to read in dollhouse

WALL=(0.66,0.66,0.71);FLOOR=(0.74,0.71,0.64);ARCH=(0.42,0.42,0.48)
MATT=(0.20,0.45,0.85);PLY=(0.55,0.40,0.24);SHELF=(0.25,0.70,0.35);NIGHT=(0.62,0.30,0.78)
BAY_L,BAY_W,BAY_H=3705,1870,2172

def clear():
    bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
    for d in (bpy.data.meshes,bpy.data.cameras,bpy.data.curves,bpy.data.materials):
        for b in list(d):
            try:d.remove(b)
            except Exception:pass

def shell():
    box('Floor',0,0,-25,BAY_L,BAY_W,0,FLOOR)
    box('Wall_Road',0,BAY_W,0,BAY_L,BAY_W+30,BAY_H,WALL)          # driver side (far)
    box('Bulkhead',-30,0,0,0,BAY_W,BAY_H,WALL)
    box('Rear_Wall',BAY_L,0,0,BAY_L+30,BAY_W,BAY_H,WALL)
    box('Arch_K',2450,0,0,3150,224,260,ARCH);box('Arch_R',2450,1646,0,3150,BAY_W,260,ARCH)
    # low kerb sill only (near side stays open to view in)
    box('Sill_Kerb',0,-30,0,BAY_L,0,120,WALL)

def transverse():
    # garage platform + mattress across full width; sleeper lies along Y = 1830mm (6ft fits)
    box('Garage_Top',2305,0,980,BAY_L,BAY_W,1000,PLY)
    box('Garage_Back',BAY_L-20,0,0,BAY_L,BAY_W,1000,PLY,0.7)
    box('Mattress',2325,20,1000,3685,1850,1150,MATT,0.8)
    # bedside shelves
    box('Shelf_Rear',3560,20,1450,3700,1850,1480,SHELF)            # ledge on rear wall, above head
    box('Shelf_RoadSide',2305,1810,1520,BAY_L,BAY_W,1550,SHELF)    # long shelf on driver wall
    box('Night_K',3380,20,1150,BAY_L,260,1430,NIGHT)               # cubby, kerb end of bed
    box('Night_R',3380,1610,1150,BAY_L,1850,1430,NIGHT)            # cubby, driver end of bed
    label('TRANSVERSE BED  1830 long (6ft fits)',3000,935,1320,(0.05,0.05,0.06),95)
    label('GARAGE under (elec | water | gear)',3000,935,520,(0.1,0.1,0.1),80)
    label('shelf',3630,935,1560,(0.0,0.3,0.1),70)
    label('living space ->',1500,935,300,(0.1,0.1,0.1),90)

def lengthways():
    # bed along driver side, runs front-back; sleeper along X = 1950mm; walkway kerb side
    box('Garage_Top',1700,500,980,BAY_L,BAY_W,1000,PLY)
    box('Mattress',1755,520,1000,3705,1850,1150,MATT,0.8)          # 1950 long x 1330 wide
    box('Walkway_Mark',1755,0,2,BAY_L,500,12,(0.30,0.30,0.34))     # floor strip = walkway to rear
    # bedside shelves
    box('Shelf_RoadSide',1755,1810,1500,BAY_L,BAY_W,1530,SHELF)    # long shelf on driver wall above bed
    box('Shelf_Head',3560,520,1450,3700,1850,1480,SHELF)           # head shelf on rear wall
    box('Night_Foot',1700,520,0,1980,1000,600,NIGHT)               # nightstand at foot/entry end
    label('LENGTHWAYS BED  1950 long',2730,1185,1330,(0.05,0.05,0.06),95)
    label('WALKWAY to rear doors',2730,250,260,(0.1,0.1,0.1),80)
    label('GARAGE under',2730,1185,520,(0.1,0.1,0.1),80)
    label('shelf',3630,1185,1560,(0.0,0.3,0.1),70)

def world_render(tag):
    w=bpy.data.worlds.get('World') or bpy.data.worlds.new('World')
    bpy.context.scene.world=w;w.use_nodes=False;w.color=(0.88,0.89,0.92)
    sc=bpy.context.scene;sc.render.engine='BLENDER_WORKBENCH'
    sh=sc.display.shading;sh.color_type='OBJECT';sh.light='STUDIO';sh.show_cavity=False;sh.show_shadows=True
    sc.render.resolution_x=1700;sc.render.resolution_y=1050;sc.render.image_settings.file_format='PNG'
    bpy.ops.object.empty_add(location=(m(2700),m(935),m(800)));aim=bpy.context.active_object
    bpy.ops.object.camera_add(location=(m(900),m(-3900),m(2400)))
    cam=bpy.context.active_object;cam.data.lens=30
    con=cam.constraints.new('TRACK_TO');con.target=aim;con.track_axis='TRACK_NEGATIVE_Z';con.up_axis='UP_Y'
    sc.camera=cam;sc.render.filepath=os.path.join(OUT,'bed_%s.png'%tag)
    try:bpy.ops.render.render(write_still=True)
    except Exception as e:print('render warn',e)

def build(mode):
    clear();shell()
    transverse() if mode=='transverse' else lengthways()
    world_render(mode)
    bpy.ops.export_scene.gltf(filepath=os.path.join(OUT,'van_bed_%s.glb'%mode),export_format='GLB',export_apply=True)
    print('BUILT',mode)

build('transverse')
build('lengthways')
print('BED OPTIONS DONE ->',OUT)
