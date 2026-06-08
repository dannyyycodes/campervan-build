"""Export the shell to GLB for the browser viewer. Open-top (roof removed) so you see inside.
Run: blender ducato_L3H3_shell.blend --background --python export_glb.py
"""
import bpy, os
OUT = os.path.dirname(os.path.abspath(__file__))
# drop roof + dimension text so it's a clean open box to look into
for cname in ('ROOF',):
    c = bpy.data.collections.get(cname)
    if c:
        for o in list(c.objects):
            bpy.data.objects.remove(o, do_unlink=True)
# give every object a real material from its viewport color (so GLB isn't flat white)
for o in bpy.data.objects:
    if o.type != 'MESH':
        continue
    col = tuple(o.color)
    mat = bpy.data.materials.new('m_' + o.name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get('Principled BSDF')
    if bsdf:
        bsdf.inputs['Base Color'].default_value = (col[0], col[1], col[2], 1.0)
        bsdf.inputs['Roughness'].default_value = 0.7
    o.data.materials.clear()
    o.data.materials.append(mat)
bpy.ops.export_scene.gltf(filepath=os.path.join(OUT, 'van.glb'), export_format='GLB',
                          use_visible=False, export_apply=True)
print('GLB DONE')
