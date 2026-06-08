"""
Fiat Ducato L3 (LWB) H3 — FULL van: body, cab, bonnet, windscreen, 4 wheels, bumpers, mirrors.
Built to TRUE external dimensions (mm), wrapping the exact interior load bay.
Run: blender --background --python build_van_full.py
Outputs: van_full.glb, ducato_L3H3_full.blend, full_persp.png, full_side.png

True external dims used (Fiat brochure, cross-checked):
  overall L 5998 | body W 2050 | overall H 2764 | wheelbase 4035
  front overhang 948 | rear overhang 1015 | track F 1810 / R 1790
  wheel/tyre Ø 744 | tyre width 225 | load-floor height 535
Coord origin (0,0,0) = interior load-bay front, kerb side, INTERIOR FLOOR.
Ground = z -535. Body centre line y = 935 (interior 0..1870 sits centred in body -90..1960).
"""
import bpy, os, math

OUT = os.path.dirname(os.path.abspath(__file__))
def m(v): return v / 1000.0

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
for d in (bpy.data.meshes, bpy.data.cameras, bpy.data.lights, bpy.data.curves, bpy.data.materials):
    for b in list(d):
        try: d.remove(b)
        except Exception: pass

scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.length_unit = 'METERS'

def mat(color, rough=0.55):
    mt = bpy.data.materials.new('m')
    mt.use_nodes = True
    b = mt.node_tree.nodes.get('Principled BSDF')
    if b:
        b.inputs['Base Color'].default_value = (color[0], color[1], color[2], 1.0)
        b.inputs['Roughness'].default_value = rough
    return mt

def setmat(o, color, rough=0.55):
    o.color = (color[0], color[1], color[2], 1.0)
    o.data.materials.clear()
    o.data.materials.append(mat(color, rough))

def box(name, x0,y0,z0, x1,y1,z1, color, rough=0.55, rot=None):
    cx,cy,cz=(x0+x1)/2,(y0+y1)/2,(z0+z1)/2
    bpy.ops.mesh.primitive_cube_add(size=1, location=(m(cx),m(cy),m(cz)))
    o=bpy.context.active_object; o.name=name
    o.dimensions=(m(abs(x1-x0)),m(abs(y1-y0)),m(abs(z1-z0)))
    if rot:
        bpy.ops.object.transform_apply(scale=True)
        o.rotation_euler=rot
    setmat(o, color, rough)
    return o

def wheel(name, x, y, z, color=(0.06,0.06,0.07)):
    # tyre (axis along Y)
    bpy.ops.mesh.primitive_cylinder_add(vertices=28, radius=m(372), depth=m(225),
        location=(m(x),m(y),m(z)), rotation=(math.radians(90),0,0))
    t=bpy.context.active_object; t.name=name; setmat(t, color, 0.8)
    # hub
    side = 1 if y < 935 else -1
    bpy.ops.mesh.primitive_cylinder_add(vertices=20, radius=m(150), depth=m(60),
        location=(m(x),m(y+ side*120),m(z)), rotation=(math.radians(90),0,0))
    h=bpy.context.active_object; h.name=name+'_hub'; setmat(h, (0.55,0.55,0.58), 0.4)
    return t

# ---------- palette ----------
BODY=(0.90,0.90,0.92); GLASS=(0.12,0.15,0.20); BUMP=(0.26,0.26,0.29)
TYRE=(0.06,0.06,0.07); FLOOR=(0.74,0.71,0.64); TRIM=(0.20,0.20,0.23); LIGHT=(0.92,0.85,0.55)

# ---------- geometry anchors (mm) ----------
GROUND=-535
NOSE=-2173; FAX=-1225; RAX=2810; TAIL=3825      # x: nose, front axle, rear axle, rear bumper face
BODY_Y0, BODY_Y1 = -90, 1960                      # body width 2050, centred on y=935
ROOF=2229                                          # interior ceiling 2172 + ~57 skin (=-535+2764)
CABROOF=1719                                       # H1 cab roof height above floor

# ---------- main high-roof cargo box ----------
box('Body_Box', -200,BODY_Y0,-150, TAIL,BODY_Y1,ROOF, BODY, 0.5)
# ---------- cab + bonnet ----------
box('Cab', -1500,BODY_Y0,-150, -200,BODY_Y1,CABROOF, BODY, 0.5)
box('Bonnet', NOSE,-60,-150, -1400,1930,1040, BODY, 0.5)
box('Front_Bumper', NOSE-40,-70,-300, -1480,1940,300, BUMP, 0.6)
box('Rear_Bumper', TAIL-40,BODY_Y0+20,-300, TAIL+70,BODY_Y1-20,260, BUMP, 0.6)
# ---------- windscreen (raked) ----------
ws = box('Windscreen', -1430,-70,1040, -780,1930,1700, GLASS, 0.15)
ws.rotation_euler = (0, math.radians(-26), 0)
# ---------- cab side windows + doors line ----------
box('Cab_Win_L', -1480,BODY_Y0-2,520, -560,BODY_Y0+8,1180, GLASS, 0.15)
box('Cab_Win_R', -1480,BODY_Y1-8,520, -560,BODY_Y1+2,1180, GLASS, 0.15)
# ---------- mirrors ----------
box('Mirror_L', -1360,BODY_Y0-150,1150, -1300,BODY_Y0-10,1420, TRIM, 0.5)
box('Mirror_R', -1360,BODY_Y1+10,1150, -1300,BODY_Y1+150,1420, TRIM, 0.5)
# ---------- headlights ----------
box('Head_L', NOSE-30,-40,500, NOSE+120,360,820, LIGHT, 0.3)
box('Head_R', NOSE-30,1510,500, NOSE+120,1910,820, LIGHT, 0.3)
# ---------- sliding door + rear door seams (thin dark insets, kerb side y0 ext) ----------
box('Slide_Door', 350,BODY_Y0-2,-120, 1620,BODY_Y0+6,1500, (0.84,0.84,0.86), 0.5)
# ---------- wheels ----------
wheel('Wheel_FL', FAX, 30, GROUND+372)
wheel('Wheel_FR', FAX, 1840, GROUND+372)
wheel('Wheel_RL', RAX, 40, GROUND+372)
wheel('Wheel_RR', RAX, 1830, GROUND+372)
# wheel-arch trims (dark) so wheels read as tucked in
for (ax) in (FAX, RAX):
    box('ArchTrim_%d_L'%ax, ax-430,BODY_Y0-12,-150, ax+430,BODY_Y0+30,260, TRIM, 0.6)
    box('ArchTrim_%d_R'%ax, ax-430,BODY_Y1-30,-150, ax+430,BODY_Y1+12,260, TRIM, 0.6)
# ---------- interior floor (visible if you go inside) ----------
box('Interior_Floor', 0,0,-5, 3705,1870,0, FLOOR, 0.7)
# ---------- ground plane ----------
box('Ground', NOSE-1200,BODY_Y0-1400,GROUND-40, TAIL+1200,BODY_Y1+1400,GROUND, (0.82,0.80,0.76), 0.9)

# ---------- world / render ----------
world = bpy.data.worlds.get('World') or bpy.data.worlds.new('World')
scene.world=world; world.use_nodes=True
bg=world.node_tree.nodes.get('Background')
if bg: bg.inputs[0].default_value=(0.80,0.82,0.86,1.0); bg.inputs[1].default_value=1.0

scene.render.engine='BLENDER_WORKBENCH'   # reliable headless (no GPU needed); browser does the pretty shading
sh=scene.display.shading; sh.color_type='OBJECT'; sh.light='STUDIO'; sh.show_cavity=False; sh.show_shadows=True
scene.render.resolution_x=1900; scene.render.resolution_y=1100
scene.render.image_settings.file_format='PNG'

# cameras
cx,cy,cz = 826,935,500
bpy.ops.object.empty_add(location=(m(cx),m(cy),m(cz)))
aim=bpy.context.active_object
def cam(name, loc, lens=35):
    bpy.ops.object.camera_add(location=(m(loc[0]),m(loc[1]),m(loc[2])))
    c=bpy.context.active_object; c.name=name; c.data.lens=lens
    con=c.constraints.new('TRACK_TO'); con.target=aim; con.track_axis='TRACK_NEGATIVE_Z'; con.up_axis='UP_Y'
    return c
cam_p=cam('Cam_Persp', (-5200,-6200,3200), 40)
cam_s=cam('Cam_Side', (826,-9000,400), 55)

def render(c, path):
    try:
        scene.camera=c; scene.render.filepath=path; bpy.ops.render.render(write_still=True)
    except Exception as e:
        print('render warn:', e)
render(cam_p, os.path.join(OUT,'full_persp.png'))
render(cam_s, os.path.join(OUT,'full_side.png'))

# export GLB for browser viewer
bpy.ops.export_scene.gltf(filepath=os.path.join(OUT,'van_full.glb'), export_format='GLB', export_apply=True)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT,'ducato_L3H3_full.blend'))
print('FULL DONE ->', OUT)
