"""
Ducato L3 (LWB) H3 campervan — to-scale Blender planning model.
Built from Danny's locked spec. Run headless:
  blender --background --python build_van_model.py
Outputs (into this script's folder):
  ducato_L3H3_build.blend   <- open this in Blender, drag/move the blocks
  plan_top.png              <- top-down floor plan (the planning view)
  plan_persp.png            <- 3/4 dollhouse view (x-ray walls)

Coords: origin (0,0,0) = load-bay front, KERB(passenger) side, FLOOR.
  +X = front bulkhead -> rear doors   (load bay 0..3705 mm, L3 LWB)
  +Y = kerb side -> road(driver) side (0..1870 mm)
  +Z = floor -> ceiling               (0..2172 mm, H3)
UK RHD: driver = road side (high Y). Sliding door = kerb side (low Y).
All numbers in millimetres; converted to metres for Blender.
"""
import bpy, os, math

OUT = os.path.dirname(os.path.abspath(__file__))
os.makedirs(OUT, exist_ok=True)

def m(v):            # mm -> metres
    return v / 1000.0

# ---------- clean slate ----------
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
for d in (bpy.data.meshes, bpy.data.cameras, bpy.data.lights, bpy.data.curves):
    for b in list(d):
        d.remove(b)

scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.length_unit = 'METERS'

def coll(name):
    if name in bpy.data.collections:
        return bpy.data.collections[name]
    c = bpy.data.collections.new(name)
    scene.collection.children.link(c)
    return c

C_SHELL  = coll('SHELL')
C_BUILD  = coll('BUILD')
C_ROOF   = coll('ROOF')
C_LABELS = coll('LABELS')

def box(name, x0, y0, z0, x1, y1, z1, color, c=C_BUILD, wire=False):
    cx, cy, cz = (x0+x1)/2, (y0+y1)/2, (z0+z1)/2
    bpy.ops.mesh.primitive_cube_add(size=1, location=(m(cx), m(cy), m(cz)))
    o = bpy.context.active_object
    o.name = name
    o.dimensions = (m(abs(x1-x0)), m(abs(y1-y0)), m(abs(z1-z0)))
    o.color = (color[0], color[1], color[2], 1.0)
    for uc in list(o.users_collection):
        uc.objects.unlink(o)
    c.objects.link(o)
    if wire:
        o.display_type = 'WIRE'
    return o

def label(text, x, y, z, color=(0.05, 0.05, 0.05), size=95, c=C_LABELS):
    bpy.ops.object.text_add(location=(m(x), m(y), m(z)))
    o = bpy.context.active_object
    o.name = 'lbl_' + text
    o.data.body = text
    o.data.size = m(size)
    o.data.align_x = 'CENTER'
    o.data.align_y = 'CENTER'
    o.color = (color[0], color[1], color[2], 1.0)
    for uc in list(o.users_collection):
        uc.objects.unlink(o)
    c.objects.link(o)
    return o

# ---------- palette ----------
SHELL = (0.62, 0.62, 0.67)
FLOOR = (0.72, 0.69, 0.62)
ARCH  = (0.40, 0.40, 0.46)
BED   = (0.20, 0.45, 0.85)
PLY   = (0.55, 0.40, 0.24)
KIT   = (0.95, 0.55, 0.15)
WORK  = (0.82, 0.82, 0.88)
WARD  = (0.25, 0.70, 0.35)
ELEC  = (0.85, 0.20, 0.20)
WATER = (0.20, 0.75, 0.85)
HEAT  = (0.80, 0.35, 0.20)
SEAT  = (0.45, 0.45, 0.52)
DESK  = (0.62, 0.30, 0.78)
SOLAR = (0.13, 0.13, 0.20)
STAR  = (0.95, 0.85, 0.20)
FAN   = (0.80, 0.80, 0.86)
STEP  = (0.30, 0.30, 0.34)

# ---------- shell (load bay) : L3 LWB H3 ----------
BAY_L = 3705   # internal load length (L3)
BAY_W = 1870   # internal load width (max)
BAY_H = 2172   # internal load height (H3)
DOOR0, DOOR1 = 550, 1800   # sliding-door aperture (kerb side), 1250 wide

box('Floor_Bay', 0, 0, -25, BAY_L, BAY_W, 0, FLOOR, C_SHELL)
box('Floor_Cab', -900, 0, -25, 0, BAY_W, 0, FLOOR, C_SHELL)
# kerb-side wall split around the sliding-door aperture
box('Wall_Kerb_Front', 0, -30, 0, DOOR0, 0, BAY_H, SHELL, C_SHELL)
box('Wall_Kerb_Rear', DOOR1, -30, 0, BAY_L, 0, BAY_H, SHELL, C_SHELL)
box('Wall_Kerb_DoorTop', DOOR0, -30, 1755, DOOR1, 0, BAY_H, SHELL, C_SHELL)  # lintel
box('Wall_Road', 0, BAY_W, 0, BAY_L, BAY_W+30, BAY_H, SHELL, C_SHELL)         # driver side
box('Bulkhead', -30, 0, 0, 0, BAY_W, BAY_H, SHELL, C_SHELL)
box('Roof', 0, 0, BAY_H, BAY_L, BAY_W, BAY_H+30, SHELL, C_ROOF)               # hidden in top view

# wheel arches (APPROX — MEASURE the real van before cutting the bed frame)
box('Arch_Kerb', 2450, 0, 0, 3150, 224, 260, ARCH, C_SHELL)
box('Arch_Road', 2450, 1646, 0, 3150, BAY_W, 260, ARCH, C_SHELL)

# ---------- rear: transverse bed on a garage ----------
# sleeper lies along Y (1870 mm ~ 6'1"). Garage 1000 mm tall underneath.
box('Bed_Platform', 2305, 0, 980, BAY_L, BAY_W, 1000, PLY)
box('Mattress', 2325, 20, 1000, 3685, 1850, 1150, BED)
# garage contents (under the bed)
box('Elec_Bay', 2345, 40, 20, 2745, 520, 440, ELEC)       # LiFePO4 + inverter + MPPT + DC-DC
box('Water_Cans', 2345, 1360, 20, 2745, 1840, 440, WATER) # fresh + grey cans
box('Diesel_Heater', 3300, 40, 20, 3600, 260, 220, HEAT)

# ---------- kitchen (driver side, behind cab, clear of door) ----------
box('Kitchen_Unit', 0, 1270, 0, 1100, BAY_W, 900, KIT)
box('Worktop', 100, 1290, 900, 1020, 1850, 940, WORK)   # sink + gas hob

# ---------- wardrobe / tall storage (kerb front corner, before door) ----------
box('Wardrobe', 0, 0, 0, 480, 500, 1800, WARD)

# ---------- fold-down desk (faces driver swivel) ----------
box('Desk_Fold', -300, 1270, 720, 150, BAY_W, 760, DESK)

# ---------- swivel cab seats ----------
box('Seat_Driver', -850, 1250, 0, -250, 1750, 480, SEAT)
box('Seat_Driver_Back', -850, 1250, 480, -700, 1750, 950, SEAT)
box('Seat_Pass', -850, 120, 0, -250, 620, 480, SEAT)
box('Seat_Pass_Back', -850, 120, 480, -700, 620, 950, SEAT)

# ---------- entry step / mat (kerb sliding door) ----------
box('Entry_Step', 750, 0, 0, 1950, 400, 25, STEP)

# ---------- roof-mounted ----------
box('Solar_Panel', 1000, 300, BAY_H, 3000, 1550, BAY_H+40, SOLAR, C_ROOF)
box('Starlink_Mini', 300, 700, BAY_H, 700, 1200, BAY_H+83, STAR, C_ROOF)
box('Roof_Fan', 400, 750, BAY_H, 760, 1110, BAY_H+40, FAN, C_ROOF)

# ---------- labels (top-view readable) ----------
label('BED', 3005, 935, 1170)
label('GARAGE: ELEC | WATER | HEATER', 3005, 935, 1015, size=70)
label('KITCHEN', 550, 1570, 960)
label('WARDROBE', 240, 250, 1820, size=80)
label('DESK', -75, 1570, 780, size=80)
label('DRIVER', -550, 1500, 980, size=80)
label('PASS', -550, 370, 980, size=80)
label('ENTRY', 1275, 200, 60, size=80)
label('LIVING / SWIVEL LOUNGE', 1700, 935, 35, size=80)
# roof labels (perspective view only)
label('SOLAR', 2000, 925, BAY_H+58, color=(0.95, 0.95, 0.95), size=90, c=C_ROOF)
label('STARLINK', 500, 950, BAY_H+103, color=(0.1, 0.1, 0.1), size=70, c=C_ROOF)
label('FAN', 580, 930, BAY_H+58, color=(0.1, 0.1, 0.1), size=70, c=C_ROOF)

# ---------- world / render ----------
world = bpy.data.worlds.get('World') or bpy.data.worlds.new('World')
scene.world = world
world.use_nodes = False
world.color = (0.90, 0.90, 0.93)

scene.render.engine = 'BLENDER_WORKBENCH'
sh = scene.display.shading
sh.color_type = 'OBJECT'
sh.show_cavity = False
scene.render.resolution_x = 1900
scene.render.resolution_y = 1100
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = 'PNG'
scene.render.film_transparent = False

# ---------- cameras ----------
bpy.ops.object.camera_add(location=(m(1402), m(935), 9.5))
cam_top = bpy.context.active_object
cam_top.name = 'Cam_Top'
cam_top.data.type = 'ORTHO'
cam_top.data.ortho_scale = 5.2
cam_top.rotation_euler = (0, 0, 0)

bpy.ops.object.empty_add(location=(m(1700), m(935), m(650)))
aim = bpy.context.active_object
aim.name = 'CamAim'
bpy.ops.object.camera_add(location=(m(-1900), m(-2600), m(2900)))
cam_p = bpy.context.active_object
cam_p.name = 'Cam_Persp'
cam_p.data.type = 'PERSP'
cam_p.data.lens = 22
con = cam_p.constraints.new('TRACK_TO')
con.target = aim
con.track_axis = 'TRACK_NEGATIVE_Z'
con.up_axis = 'UP_Y'

def render(cam, path, xray, show_roof, light):
    scene.camera = cam
    sh.light = light
    sh.show_xray = xray
    sh.xray_alpha = 0.55
    bpy.data.collections['ROOF'].hide_render = not show_roof
    scene.render.filepath = path
    bpy.ops.render.render(write_still=True)

render(cam_top, os.path.join(OUT, 'plan_top.png'), xray=False, show_roof=False, light='FLAT')
render(cam_p, os.path.join(OUT, 'plan_persp.png'), xray=True, show_roof=True, light='STUDIO')

bpy.data.collections['ROOF'].hide_render = False
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, 'ducato_L3H3_build.blend'))
print('DONE ->', OUT)
