bl_info = {
    'name': 'InvertDefaultWeights',
    'author': 'Celdor (formely Bay Raitt)',
    'version': (0, 2),
    'blender': (5, 00, 0),
    'category': 'View',
    'location': 'View > Weights > Invert Default Weights',
    'wiki_url': ''
}

import bpy
import rna_keymap_ui
from bpy.props import BoolProperty
# from bpy.app.handlers import persistent


addon_keymaps = []


def main(context, fuzzy_toggle):
    brush = context.tool_settings.weight_paint.brush
    if brush.name != "Paint":
        return
    weight = brush.weight
    weight = weight if fuzzy_toggle else round(weight)
    brush.weight = 1.0 - weight


class VK_OT_invert_weights(bpy.types.Operator):
    """Invert Default Weights"""
    bl_idname = "view3d.invert_default_weights"
    bl_label = "Invert Default Weights"

    @classmethod
    def poll(cls, context):
        return context.mode == 'PAINT_WEIGHT'

    def execute(self, context):
        prefs = context.preferences.addons[__name__].preferences

        main(context, prefs.fuzzy_toggle)
        return {'FINISHED'}


def menu_draw(self, context):
    self.layout.operator(VK_OT_invert_weights.bl_idname)


class VK_PT_invert_weight_preferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    fuzzy_toggle: BoolProperty(
        name="Fuzzy Toggle",
        description="Toggle Fuzzy Weights",
        default=True,
    )

    def draw(self, context):
        layout = self.layout

        layout.prop(self, "fuzzy_toggle")

        wm = context.window_manager
        kc = wm.keyconfigs.addon
        if kc is None:
            return

        box = layout.box()
        box.label(text="Keymap", icon='KEYINGSET')

        for km, kmi in addon_keymaps:
            if km:
                for item in km.keymap_items:
                    if item.idname == kmi.idname:
                        box.context_pointer_set("keymap", km)
                        rna_keymap_ui.draw_kmi([], kc, km, item, box, 0)


def register_keymaps():
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name='Weight Paint')
        kmi = km.keymap_items.new(
            idname=VK_OT_invert_weights.bl_idname,
            type='X',
            value='PRESS',
            ctrl=False,
            shift=False,
            alt=False,
        )
        addon_keymaps.append((km, kmi))


def unregister_keymaps():
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()


def register():
    bpy.utils.register_class(VK_OT_invert_weights)
    bpy.types.VIEW3D_MT_paint_weight.prepend(menu_draw)
    bpy.utils.register_class(VK_PT_invert_weight_preferences)
    register_keymaps()


def unregister():
    bpy.utils.unregister_class(VK_PT_invert_weight_preferences)
    bpy.utils.unregister_class(VK_OT_invert_weights)
    bpy.types.VIEW3D_MT_paint_weight.remove(menu_draw)
    unregister_keymaps()

