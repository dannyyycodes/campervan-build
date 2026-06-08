"""
Ducato L3 (LWB) H3 — BARE empty shell, manufacturer-exact, for planning the build.
Just the box: floor, walls, sliding-door + rear apertures, roof, wheel arches.
No furniture. Run headless:
  blender --background --python build_van_shell.py
Outputs:
  ducato_L3H3_shell.blend   <- open this; empty van to scale
  shell_top.png / shell_persp.png

Coords: origin (0,0,0) = load-bay front, KERB(passenger) side, FLOOR.
  +X front->rear (0..3705)  +Y kerb->driver (0..1870)  +Z floor->ceiling (0..2172)
Also enables nicer navigation defaults (emulate-3-button + orbit-around-selection).
"""
import bpy, os, math

OUT = os.path.dirname(os.path.abspath(__file__))
os.makedirs(OUT, exist_ok=True)
def m(v): return v / 1000.0

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
for d in (bpy.data.meshes, bpy.data.cameras, bpy.data.lights, bpy.data.curves):
    for b in list(d):
        d.remove(b)

scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.length_unit = 'METERS'

def coll(name):
    if name in bpy.data.collections: return bpy.data.collections[name]
    c = bpy.data.collections.new(name); scene.collection.children.link(c); return c
C_SHELL = coll('SHELL')
C_ROOF  = coll('ROOF')
C_DIM   = coll('DIMENSIONS')

def box(name, x0,y0,z0, x1,y1,z1, color, c=C_SHELL, wire=False):
    cx,cy,cz=(x0+x1)/2,(y0+y1)/2,(z0+z1)/2
    bpy.ops.mesh.primitive_cube_add(size=1, location=(m(cx),m(cy),m(cz)))
    o=bpy.context.active_object; o.name=name
    o.dimensions=(m(abs(x1-x0)),m(abs(y1-y0)),m(abs(z1-z0)))
    o.color=(color[0],color[1],color[2],1.0)
    for uc in list(o.users_collection): uc.objects.unlink(o)
    c.objects.link(o)
    if wire: o.display_type='WIRE'
    return o

def label(text, x,y,z, color=(0.05,0.05,0.05), size=110, c=C_DIM):
    bpy.ops.object.text_add(location=(m(x),m(y),m(z)))
    o=bpy.context.active_object; o.name='dim_'+text[:8]
    o.data.body=text; o.data.size=m(size); o.data.align_x='CENTER'; o.data.align_y='CENTER'
    o.color=(color[0],color[1],color[2],1.0)
    for uc in list(o.users_collection): uc.objects.unlink(o)
    c.objects.link(o)
    return o

SHELL=(0.66,0.66,0.71); FLOOR=(0.74,0.71,0.64); ARCH=(0.42,0.42,0.48); DIM=(0.10,0.10,0.12)

BAY_L, BAY_W, BAY_H = 3705, 1870, 2172
DOOR0, DOOR1 = 550, 1800     # sliding-door aperture (kerb side, 1250 wide)
RDOOR = 1562                 # rear door aperture width
WALL = 30

# floor
box('Floor_Bay', 0,0,-25, BAY_L,BAY_W,0, FLOOR)
box('Floor_Cab', -900,0,-25, 0,BAY_W,0, (0.70,0.67,0.60))
# kerb side wall (split round sliding door)
box('Wall_Kerb_Front', 0,-WALL,0, DOOR0,0,BAY_H, SHELL)
box('Wall_Kerb_Rear', DOOR1,-WALL,0, BAY_L,0,BAY_H, SHELL)
box('Wall_Kerb_DoorTop', DOOR0,-WALL,1755, DOOR1,0,BAY_H, SHELL)
# road (driver) side wall — solid
box('Wall_Road', 0,BAY_W,0, BAY_L,BAY_W+WALL,BAY_H, SHELL)
# bulkhead (front)
box('Bulkhead', -WALL,0,0, 0,BAY_W,BAY_H, SHELL)
# rear: two door pillars only, aperture open in middle
box('Rear_Pillar_Kerb', BAY_L,0,0, BAY_L+WALL,(BAY_W-RDOOR)/2,BAY_H, SHELL)
box('Rear_Pillar_Road', BAY_L,BAY_W-(BAY_W-RDOOR)/2,0, BAY_L+WALL,BAY_W,BAY_H, SHELL)
box('Rear_Lintel', BAY_L,0,2030, BAY_L+WALL,BAY_W,BAY_H, SHELL)
# roof (own collection so it can be hidden for top-down planning)
box('Roof', 0,0,BAY_H, BAY_L,BAY_W,BAY_H+WALL, SHELL, C_ROOF)
# wheel arches (APPROX — measure the real van)
box('Arch_Kerb', 2450,0,0, 3150,224,260, ARCH)
box('Arch_Road', 2450,1646,0, 3150,BAY_W,260, ARCH)

# dimension callouts (flat on floor, readable top-down)
label('L = 3705 mm', 1850, 935, 6, DIM, 150)
label('W = 1870 mm  (1422 between arches)', 700, 300, 6, DIM, 95)
label('H = 2172 mm (H3)', 700, 1550, 6, DIM, 95)

# ---- world / render ----
world = bpy.data.worlds.get('World') or bpy.data.worlds.new('World')
scene.world = world; world.use_nodes=False; world.color=(0.90,0.90,0.93)
scene.render.engine='BLENDER_WORKBENCH'
sh=scene.display.shading; sh.color_type='OBJECT'; sh.show_cavity=False
scene.render.resolution_x=1900; scene.render.resolution_y=1100
scene.render.image_settings.file_format='PNG'; scene.render.film_transparent=False

bpy.ops.object.camera_add(location=(m(1402),m(935),9.5))
cam_top=bpy.context.active_object; cam_top.name='Cam_Top'
cam_top.data.type='ORTHO'; cam_top.data.ortho_scale=5.2; cam_top.rotation_euler=(0,0,0)

bpy.ops.object.empty_add(location=(m(1700),m(935),m(700)))
aim=bpy.context.active_object; aim.name='CamAim'
bpy.ops.object.camera_add(location=(m(-2000),m(-2700),m(3000)))
cam_p=bpy.context.active_object; cam_p.name='Cam_Persp'
cam_p.data.type='PERSP'; cam_p.data.lens=22
con=cam_p.constraints.new('TRACK_TO'); con.target=aim
con.track_axis='TRACK_NEGATIVE_Z'; con.up_axis='UP_Y'

def render(cam, path, xray, show_roof, light):
    scene.camera=cam; sh.light=light; sh.show_xray=xray; sh.xray_alpha=0.5
    bpy.data.collections['ROOF'].hide_render = not show_roof
    scene.render.filepath=path; bpy.ops.render.render(write_still=True)

render(cam_top, os.path.join(OUT,'shell_top.png'),  xray=False, show_roof=False, light='FLAT')
render(cam_p,   os.path.join(OUT,'shell_persp.png'),xray=True,  show_roof=False, light='STUDIO')

# ---- nicer navigation defaults for the GUI ----
try:
    inp = bpy.context.preferences.inputs
    inp.use_mouse_emulate_3_button = True      # Alt+Left = orbit (no middle mouse needed)
    inp.use_rotate_around_active = True        # orbit around what you select
    inp.use_auto_perspective = False
    bpy.ops.wm.save_userpref()
except Exception as e:
    print('pref warn:', e)

bpy.data.collections['ROOF'].hide_render = False
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT,'ducato_L3H3_shell.blend'))
print('DONE ->', OUT)
