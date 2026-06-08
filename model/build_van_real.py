"""
Realistic-looking Citroen Relay / Fiat Ducato L3 H3 exterior, procedural, exact dims, NO login.
Rounded body (bevel), proper wheels (tyre+rim+hub), grille, headlights, raked windscreen, mirrors.
Run: blender --background --python build_van_real.py -> van_real.glb + real_persp.png
Dims: L5998 W2050 H2764, wheelbase4035, wheel Ø744. Ground z-535.
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

def mat(c,r=0.5,metal=0.0):
    mt=bpy.data.materials.new('m');mt.use_nodes=True
    b=mt.node_tree.nodes.get('Principled BSDF')
    if b:
        b.inputs['Base Color'].default_value=(c[0],c[1],c[2],1);b.inputs['Roughness'].default_value=r
        try:b.inputs['Metallic'].default_value=metal
        except Exception:pass
    return mt
def box(n,x0,y0,z0,x1,y1,z1,c,r=0.5,bev=40,rot=None,metal=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1,location=(m((x0+x1)/2),m((y0+y1)/2),m((z0+z1)/2)))
    o=bpy.context.active_object;o.name=n;o.dimensions=(m(abs(x1-x0)),m(abs(y1-y0)),m(abs(z1-z0)))
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    if rot:o.rotation_euler=rot
    if bev:
        md=o.modifiers.new('bev','BEVEL');md.width=m(bev);md.segments=3
        md.limit_method='ANGLE';md.angle_limit=math.radians(40);md.use_clamp_overlap=True
    o.color=(c[0],c[1],c[2],1);o.data.materials.append(mat(c,r,metal))
    return o
def wheel(n,x,y,z):
    bpy.ops.mesh.primitive_cylinder_add(vertices=40,radius=m(372),depth=m(225),location=(m(x),m(y),m(z)),rotation=(math.radians(90),0,0))
    t=bpy.context.active_object;t.name=n;t.data.materials.append(mat((0.05,0.05,0.06),0.85));t.color=(0.05,0.05,0.06,1)
    md=t.modifiers.new('b','BEVEL');md.width=m(25);md.segments=2;md.use_clamp_overlap=True
    s=1 if y<935 else -1
    bpy.ops.mesh.primitive_cylinder_add(vertices=40,radius=m(230),depth=m(70),location=(m(x),m(y+s*100),m(z)),rotation=(math.radians(90),0,0))
    rim=bpy.context.active_object;rim.name=n+'_rim';rim.data.materials.append(mat((0.62,0.63,0.66),0.35,0.7));rim.color=(0.62,0.63,0.66,1)
    bpy.ops.mesh.primitive_cylinder_add(vertices=20,radius=m(60),depth=m(80),location=(m(x),m(y+s*110),m(z)),rotation=(math.radians(90),0,0))
    hub=bpy.context.active_object;hub.name=n+'_hub';hub.data.materials.append(mat((0.30,0.30,0.33),0.4));hub.color=(0.30,0.30,0.33,1)

BODY=(0.88,0.89,0.91);GLASS=(0.10,0.13,0.18);BUMP=(0.24,0.24,0.27);GRILLE=(0.12,0.12,0.14)
LIGHT=(0.93,0.90,0.72);TRIM=(0.18,0.18,0.21)
NOSE=-2173;FAX=-1225;RAX=2810;TAIL=3825;Y0=-90;Y1=1960;ROOFZ=2229;CABROOF=1719;G=-535

# main high-roof body (rounded)
box('Body',-260,Y0,-120,TAIL,Y1,ROOFZ,BODY,0.45,bev=60)
# cab + bonnet
box('Cab',-1520,Y0,-120,-260,Y1,CABROOF,BODY,0.45,bev=70)
box('Bonnet',NOSE,-40,-120,-1420,1910,1060,BODY,0.45,bev=60)
# windscreen (raked)
box('Windscreen',-1430,-60,1050,-820,1920,1690,GLASS,0.12,bev=20,rot=(0,math.radians(-26),0))
# cab side glass
box('Cab_Win_L',-1500,Y0-4,520,-600,Y0+6,1160,GLASS,0.12,bev=10)
box('Cab_Win_R',-1500,Y1-6,520,-600,Y1+4,1160,GLASS,0.12,bev=10)
# grille + headlights + bumpers
box('Grille',NOSE-20,420,560,NOSE+90,1500,900,GRILLE,0.5,bev=15)
box('Head_L',NOSE-25,90,560,NOSE+110,400,860,LIGHT,0.25,bev=15)
box('Head_R',NOSE-25,1520,560,NOSE+110,1830,860,LIGHT,0.25,bev=15)
box('Front_Bumper',NOSE-60,-40,-250,-1460,1910,360,BUMP,0.5,bev=40)
box('Rear_Bumper',TAIL-30,Y0+10,-250,TAIL+80,Y1-10,300,BUMP,0.5,bev=40)
# mirrors
box('Mirror_L',-1380,Y0-170,1150,-1310,Y0-10,1430,TRIM,0.5,bev=20)
box('Mirror_R',-1380,Y1+10,1150,-1310,Y1+170,1430,TRIM,0.5,bev=20)
# wheel-arch flares
for ax in (FAX,RAX):
    box('Arch_%d_L'%ax,ax-440,Y0-30,-120,ax+440,Y0+40,300,TRIM,0.6,bev=30)
    box('Arch_%d_R'%ax,ax-440,Y1-40,-120,ax+440,Y1+30,300,TRIM,0.6,bev=30)
# wheels
wheel('Wheel_FL',FAX,40,G+372);wheel('Wheel_FR',FAX,1830,G+372)
wheel('Wheel_RL',RAX,50,G+372);wheel('Wheel_RR',RAX,1820,G+372)
# side body crease (sliding door seam) + door handle hint
box('Slide_Seam',300,Y0-2,-100,1650,Y0+8,1480,(0.83,0.84,0.86),0.45,bev=8)
# ground
box('Ground',NOSE-1500,Y0-1600,G-50,TAIL+1500,Y1+1600,G,(0.80,0.79,0.75),0.95,bev=0)

# world + render (workbench, shadows + cavity for form)
w=bpy.data.worlds.get('World') or bpy.data.worlds.new('World')
sc.world=w;w.use_nodes=False;w.color=(0.80,0.83,0.88)
sc.render.engine='BLENDER_WORKBENCH'
shd=sc.display.shading;shd.color_type='OBJECT';shd.light='STUDIO';shd.show_cavity=True
shd.cavity_type='WORLD';shd.show_shadows=True;shd.shadow_intensity=0.4
sc.render.resolution_x=1900;sc.render.resolution_y=1100;sc.render.image_settings.file_format='PNG'
bpy.ops.object.empty_add(location=(m(826),m(935),m(550)));aim=bpy.context.active_object
bpy.ops.object.camera_add(location=(m(-5400),m(-6400),m(3000)));cam=bpy.context.active_object;cam.data.lens=48
con=cam.constraints.new('TRACK_TO');con.target=aim;con.track_axis='TRACK_NEGATIVE_Z';con.up_axis='UP_Y'
sc.camera=cam;sc.render.filepath=os.path.join(OUT,'real_persp.png')
try:bpy.ops.render.render(write_still=True)
except Exception as e:print('rwarn',e)
bpy.ops.export_scene.gltf(filepath=os.path.join(OUT,'van_real.glb'),export_format='GLB',export_apply=True)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT,'ducato_L3H3_real.blend'))
print('REAL DONE ->',OUT)
