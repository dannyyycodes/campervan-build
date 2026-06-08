"""
MASTER model — the real Ducato L3 H3 van with the interior build inside it.
Two exports the browser can toggle:
  van_master_closed.glb = full van exterior (wheels, cab, body, ROOF RACK + solar + Starlink + fan)
  van_master_open.glb   = same van with the kerb-side wall + roof CUT AWAY, showing the
                          transverse bed + garage + bedside shelves inside.
Run: blender --background --python build_van_master.py
True ext dims: L5998 W2050 H2764, wheelbase4035, wheel Ø744. Interior bay 3705x1870x2172.
Coord origin (0,0,0) = interior load-bay front, kerb side, interior FLOOR. Ground z-535.
"""
import bpy, os, math
OUT=os.path.dirname(os.path.abspath(__file__))
def m(v): return v/1000.0

bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for d in (bpy.data.meshes,bpy.data.cameras,bpy.data.curves,bpy.data.materials,bpy.data.lights):
    for b in list(d):
        try:d.remove(b)
        except Exception:pass
sc=bpy.context.scene;sc.unit_settings.system='METRIC';sc.unit_settings.length_unit='METERS'

def coll(n):
    if n in bpy.data.collections: return bpy.data.collections[n]
    c=bpy.data.collections.new(n);sc.collection.children.link(c);return c
KEEP=coll('KEEP');CUT=coll('CUT');ROOF=coll('ROOF');INT=coll('INT')

def mat(c,r=0.55):
    mt=bpy.data.materials.new('m');mt.use_nodes=True
    b=mt.node_tree.nodes.get('Principled BSDF')
    if b: b.inputs['Base Color'].default_value=(c[0],c[1],c[2],1);b.inputs['Roughness'].default_value=r
    return mt
def box(n,x0,y0,z0,x1,y1,z1,c,col,r=0.55,rot=None):
    bpy.ops.mesh.primitive_cube_add(size=1,location=(m((x0+x1)/2),m((y0+y1)/2),m((z0+z1)/2)))
    o=bpy.context.active_object;o.name=n;o.dimensions=(m(abs(x1-x0)),m(abs(y1-y0)),m(abs(z1-z0)))
    if rot: bpy.ops.object.transform_apply(scale=True);o.rotation_euler=rot
    o.color=(c[0],c[1],c[2],1);o.data.materials.clear();o.data.materials.append(mat(c,r))
    for uc in list(o.users_collection):uc.objects.unlink(o)
    col.objects.link(o);return o
def wheel(n,x,y,z,col):
    bpy.ops.mesh.primitive_cylinder_add(vertices=28,radius=m(372),depth=m(225),location=(m(x),m(y),m(z)),rotation=(math.radians(90),0,0))
    t=bpy.context.active_object;t.name=n;t.color=(0.06,0.06,0.07,1);t.data.materials.append(mat((0.06,0.06,0.07),0.8))
    for uc in list(t.users_collection):uc.objects.unlink(t)
    col.objects.link(t)
    s=1 if y<935 else -1
    bpy.ops.mesh.primitive_cylinder_add(vertices=18,radius=m(150),depth=m(60),location=(m(x),m(y+s*120),m(z)),rotation=(math.radians(90),0,0))
    h=bpy.context.active_object;h.name=n+'_hub';h.color=(0.55,0.55,0.58,1);h.data.materials.append(mat((0.55,0.55,0.58),0.4))
    for uc in list(h.users_collection):uc.objects.unlink(h)
    col.objects.link(h)
def label(t,x,y,z,col,c=(0.05,0.05,0.06),s=90):
    bpy.ops.object.text_add(location=(m(x),m(y),m(z)))
    o=bpy.context.active_object;o.data.body=t;o.data.size=m(s);o.data.align_x='CENTER';o.data.align_y='CENTER'
    o.color=(c[0],c[1],c[2],1);o.data.materials.append(mat(c,0.5));o.rotation_euler=(math.radians(90),0,0)
    for uc in list(o.users_collection):uc.objects.unlink(o)
    col.objects.link(o)

BODY=(0.90,0.90,0.92);GLASS=(0.12,0.15,0.20);BUMP=(0.26,0.26,0.29);FLOOR=(0.74,0.71,0.64)
TRIM=(0.20,0.20,0.23);LIGHT=(0.92,0.85,0.55);ARCH=(0.42,0.42,0.48)
MATT=(0.20,0.45,0.85);PLY=(0.55,0.40,0.24);SHELF=(0.25,0.70,0.35);NIGHT=(0.62,0.30,0.78)
ALU=(0.22,0.22,0.25);PANEL=(0.10,0.13,0.22);STAR=(0.93,0.90,0.86);FAN=(0.85,0.85,0.88)

NOSE=-2173;FAX=-1225;RAX=2810;TAIL=3825;Y0=-90;Y1=1960;ROOFZ=2229;CABROOF=1719;G=-535
BL,BW,BH=3705,1870,2172

# ---- body as PANELS so kerb side + roof can be cut away ----
box('Body_Roof',-200,Y0,ROOFZ-40,TAIL,Y1,ROOFZ,BODY,CUT,0.5)            # cut
box('Body_KerbWall',-200,Y0,-150,TAIL,Y0+40,ROOFZ,BODY,CUT,0.5)        # cut (near side)
box('Body_RoadWall',-200,Y1-40,-150,TAIL,Y1,ROOFZ,BODY,KEEP,0.5)       # keep (far)
box('Body_RearWall',TAIL-40,Y0,-150,TAIL,Y1,ROOFZ,BODY,KEEP,0.5)
box('Body_Skirt_K',-200,Y0,-150,TAIL,Y0+40,0,BODY,KEEP,0.5)            # low kerb skirt stays (so open view still reads as van)
# ---- cab / nose (solid, always) ----
box('Cab',-1500,Y0,-150,-200,Y1,CABROOF,BODY,KEEP,0.5)
box('Bonnet',NOSE,-60,-150,-1400,1930,1040,BODY,KEEP,0.5)
box('Front_Bumper',NOSE-40,-70,-300,-1480,1940,300,BUMP,KEEP,0.6)
box('Rear_Bumper',TAIL-40,Y0+20,-300,TAIL+70,Y1-20,260,BUMP,KEEP,0.6)
ws=box('Windscreen',-1430,-70,1040,-780,1930,1700,GLASS,KEEP,0.15,rot=(0,math.radians(-26),0))
box('Cab_Win_L',-1480,Y0-2,520,-560,Y0+8,1180,GLASS,KEEP,0.15)
box('Cab_Win_R',-1480,Y1-8,520,-560,Y1+2,1180,GLASS,KEEP,0.15)
box('Mirror_L',-1360,Y0-150,1150,-1300,Y0-10,1420,TRIM,KEEP,0.5)
box('Mirror_R',-1360,Y1+10,1150,-1300,Y1+150,1420,TRIM,KEEP,0.5)
box('Head_L',NOSE-30,-40,500,NOSE+120,360,820,LIGHT,KEEP,0.3)
box('Head_R',NOSE-30,1510,500,NOSE+120,1910,820,LIGHT,KEEP,0.3)
wheel('Wheel_FL',FAX,30,G+372,KEEP);wheel('Wheel_FR',FAX,1840,G+372,KEEP)
wheel('Wheel_RL',RAX,40,G+372,KEEP);wheel('Wheel_RR',RAX,1830,G+372,KEEP)
for ax in (FAX,RAX):
    box('Arch_%d_L'%ax,ax-430,Y0-12,-150,ax+430,Y0+30,260,TRIM,KEEP,0.6)
    box('Arch_%d_R'%ax,ax-430,Y1-30,-150,ax+430,Y1+12,260,TRIM,KEEP,0.6)
box('Ground',NOSE-1200,Y0-1400,G-40,TAIL+1200,Y1+1400,G,(0.82,0.80,0.76),KEEP,0.9)
# ---- interior shell bits visible in open view ----
box('Interior_Floor',0,0,-5,BL,BW,0,FLOOR,KEEP,0.7)
box('IntArch_K',2450,0,0,3150,224,260,ARCH,KEEP,0.6);box('IntArch_R',2450,1646,0,3150,BW,260,ARCH,KEEP,0.6)
box('Bulkhead_In',-30,0,0,0,BW,BH,(0.66,0.66,0.71),KEEP,0.6)

# ---- INTERIOR FITOUT (transverse bed, chosen) ----
box('Garage_Top',2305,0,980,BL,BW,1000,PLY,INT,0.7)
box('Garage_Back',BL-20,0,0,BL,BW,1000,PLY,INT,0.7)
box('Mattress',2325,20,1000,3685,1850,1150,MATT,INT,0.8)
box('Shelf_Rear',3560,20,1450,3700,1850,1480,SHELF,INT)
box('Shelf_RoadSide',2305,1810,1520,BL,BW,1550,SHELF,INT)
box('Night_K',3380,20,1150,BL,260,1430,NIGHT,INT)
box('Night_R',3380,1610,1150,BL,1850,1430,NIGHT,INT)
label('TRANSVERSE BED (6ft fits)',3000,935,1330,INT,(0.05,0.05,0.06),95)
label('GARAGE under',3000,935,520,INT,(0.1,0.1,0.1),80)

# ---- ROOF RACK + solar + starlink + fan (closed view) ----
box('Rail_K',-150,0,ROOFZ,3700,70,ROOFZ+70,ALU,ROOF,0.5)
box('Rail_R',-150,1800,ROOFZ,3700,1870,ROOFZ+70,ALU,ROOF,0.5)
for i,x in enumerate((-100,800,1700,2600,3500)):
    box('Cross_%d'%i,x,-40,ROOFZ+50,x+70,1910,ROOFZ+90,ALU,ROOF,0.5)
box('Solar_1',780,150,ROOFZ+90,2050,1750,ROOFZ+125,PANEL,ROOF,0.3)
box('Solar_2',2150,150,ROOFZ+90,3520,1750,ROOFZ+125,PANEL,ROOF,0.3)
box('RoofFan',300,760,ROOFZ,650,1110,ROOFZ+95,FAN,ROOF,0.4)
box('Starlink',-120,820,ROOFZ+90,260,1180,ROOFZ+150,STAR,ROOF,0.4)
label('SOLAR ~500W',1900,950,ROOFZ+170,ROOF,(0.95,0.95,0.97),90)
label('STARLINK',60,1000,ROOFZ+190,ROOF,(0.1,0.1,0.1),70)

# ---- world / render ----
w=bpy.data.worlds.get('World') or bpy.data.worlds.new('World')
sc.world=w;w.use_nodes=False;w.color=(0.82,0.84,0.88)
sc.render.engine='BLENDER_WORKBENCH'
shd=sc.display.shading;shd.color_type='OBJECT';shd.light='STUDIO';shd.show_cavity=False;shd.show_shadows=True
sc.render.resolution_x=1900;sc.render.resolution_y=1100;sc.render.image_settings.file_format='PNG'

def cam(loc,aimpt,lens=40):
    bpy.ops.object.empty_add(location=(m(aimpt[0]),m(aimpt[1]),m(aimpt[2])));a=bpy.context.active_object
    bpy.ops.object.camera_add(location=(m(loc[0]),m(loc[1]),m(loc[2])));c=bpy.context.active_object;c.data.lens=lens
    con=c.constraints.new('TRACK_TO');con.target=a;con.track_axis='TRACK_NEGATIVE_Z';con.up_axis='UP_Y';return c
cam_closed=cam((-5200,-6200,3200),(826,935,500),40)
cam_open=cam((1100,-6000,3400),(2300,935,700),42)

def hide(colls,val):
    for cn in colls:
        c=bpy.data.collections.get(cn)
        if c: c.hide_render=val
def export_subset(colls,path):
    bpy.ops.object.select_all(action='DESELECT')
    for cn in colls:
        c=bpy.data.collections.get(cn)
        if c:
            for o in c.objects:o.select_set(True)
    bpy.ops.export_scene.gltf(filepath=path,export_format='GLB',use_selection=True,export_apply=True)

# closed render + export
hide(['INT'],True);hide(['CUT','ROOF','KEEP'],False)
sc.camera=cam_closed;sc.render.filepath=os.path.join(OUT,'master_closed.png')
try:bpy.ops.render.render(write_still=True)
except Exception as e:print('rwarn',e)
export_subset(['KEEP','CUT','ROOF'],os.path.join(OUT,'van_master_closed.glb'))
# open render + export
hide(['CUT','ROOF'],True);hide(['INT','KEEP'],False)
sc.camera=cam_open;sc.render.filepath=os.path.join(OUT,'master_open.png')
try:bpy.ops.render.render(write_still=True)
except Exception as e:print('rwarn',e)
export_subset(['KEEP','INT'],os.path.join(OUT,'van_master_open.glb'))

hide(['INT','CUT','ROOF','KEEP'],False)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT,'ducato_L3H3_master.blend'))
print('MASTER DONE ->',OUT)
