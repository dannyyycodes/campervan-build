"""
Make Blender navigation Google-Maps/Sketchfab simple:
  - RIGHT-mouse drag      = orbit (look around)
  - SHIFT + RIGHT drag    = pan (slide)
  - mouse WHEEL           = zoom
  - LEFT click            = still selects a block (untouched)
Right-drag is used (not left) so it never fights box-select / selection.
Run headless to bake into the portable Blender's prefs:
  blender --background --python nav_easy.py
"""
import bpy

wm = bpy.context.window_manager
kc = wm.keyconfigs.user
km = kc.keymaps.get('3D View') or kc.keymaps.new('3D View', space_type='VIEW_3D')

def drop(idname, typ):
    for it in list(km.keymap_items):
        if it.idname == idname and it.type == typ:
            km.keymap_items.remove(it)

# clear any prior custom right-mouse nav we added, then re-add clean
drop('view3d.rotate', 'RIGHTMOUSE')
drop('view3d.move', 'RIGHTMOUSE')

orbit = km.keymap_items.new('view3d.rotate', 'RIGHTMOUSE', 'CLICK_DRAG')
pan   = km.keymap_items.new('view3d.move',   'RIGHTMOUSE', 'CLICK_DRAG', shift=True)

# keep right-CLICK (no drag) as the menu; CLICK_DRAG only fires on drag
# zoom stays on the wheel (default). also widen zoom range a touch:
try:
    inp = bpy.context.preferences.inputs
    inp.use_mouse_emulate_3_button = True
    inp.use_rotate_around_active = True
    inp.use_zoom_to_mouse = True
    view = bpy.context.preferences.view
    view.smooth_view = 120
except Exception as e:
    print('pref warn:', e)

bpy.ops.wm.save_userpref()
print('NAV SET: right-drag orbit, shift+right-drag pan, wheel zoom')
