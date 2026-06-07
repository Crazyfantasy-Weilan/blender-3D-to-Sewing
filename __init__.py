bl_info = {
        'name': 'Seams to Sewing Pattern (缝纫纸样)',
        'author': 'Thomas Kole',
        'version': (1, 1),
        'blender': (2, 80, 0),
        'category': 'Cloth',
        'description': '将带接缝的网格转换为缝纫纸样，支持布料模拟',
        'location': 'Object > Seams to Sewing Pattern > ...',
        'wiki_url': 'https://blenderartists.org/t/1248713'}

if "bpy" in locals():
    import importlib
    importlib.reload(op_seams_to_sewingpattern)
    importlib.reload(op_export_sewingpattern)
    importlib.reload(op_quick_clothsim)
    importlib.reload(op_boundary_alinged_remesh)
    importlib.reload(op_clean_up_edges)
else:
    from . import op_seams_to_sewingpattern
    from . import op_export_sewingpattern
    from . import op_quick_clothsim
    from . import op_boundary_alinged_remesh
    from . import op_clean_up_edges

import bpy
from bpy.types import Menu, Panel

# Blender 4.0+ renamed some icons
def get_icon(name):
    if bpy.app.version >= (5, 0, 0):
        icon_map = {
            'OUTLINER_DATA_SURFACE': 'MESH_DATA',
            'MOD_CLOTH': 'PHYSICS',
        }
        return icon_map.get(name, name)
    if bpy.app.version >= (4, 0, 0):
        icon_map = {
            'OUTLINER_DATA_SURFACE': 'MESH_DATA',
            'MOD_CLOTH': 'CLOTH',
        }
        return icon_map.get(name, name)
    return name

def clean_up_func(self, context):
    self.layout.separator()
    self.layout.operator("mesh.clean_up_knife_cut")

def menu_func(self, context):
    lay_out = self.layout
    lay_out.operator_context = 'INVOKE_REGION_WIN'

    lay_out.separator()
    lay_out.menu("VIEW3D_MT_object_seams_to_sewing_pattern_menu",
                text="缝纫纸样")

def uv_menu_func(self, context):
    """Add sewing pattern menu to UV Editor's UV menu"""
    lay_out = self.layout
    lay_out.operator_context = 'INVOKE_REGION_WIN'
    lay_out.separator()
    lay_out.menu("VIEW3D_MT_object_seams_to_sewing_pattern_menu",
                text="缝纫纸样")
    
class VIEW3D_MT_object_seams_to_sewing_pattern_menu(Menu):
    bl_idname = "VIEW3D_MT_object_seams_to_sewing_pattern_menu"
    bl_label = "缝纫纸样"

    def draw(self, context):
        layout = self.layout
        layout.operator("object.seams_to_sewingpattern", text="生成缝纫纸样", icon=get_icon("OUTLINER_DATA_SURFACE"))
        layout.separator()
        layout.operator("object.export_sewingpattern", text="导出缝纫纸样 (.svg)", icon="EXPORT")
        layout.separator()
        layout.operator("object.sewing_pattern_clothsim", text="布料模拟设置", icon=get_icon("MOD_CLOTH"))


class VIEW3D_PT_seams_to_sewing_pattern_uv(Panel):
    """Sewing Pattern tools in UV Editor sidebar"""
    bl_label = "缝纫纸样"
    bl_idname = "VIEW3D_PT_seams_to_sewing_pattern_uv"
    bl_space_type = 'IMAGE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "缝纫纸样"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.active_object.type == 'MESH'

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'
        
        layout.operator("object.seams_to_sewingpattern", text="生成缝纫纸样", icon=get_icon("OUTLINER_DATA_SURFACE"))
        layout.separator()
        layout.operator("object.export_sewingpattern", text="导出缝纫纸样 (.svg)", icon="EXPORT")
        layout.separator()
        layout.operator("object.sewing_pattern_clothsim", text="布料模拟设置", icon=get_icon("MOD_CLOTH"))


class VIEW3D_PT_seams_to_sewing_pattern_3d(Panel):
    """Sewing Pattern tools in 3D Viewport sidebar"""
    bl_label = "缝纫纸样"
    bl_idname = "VIEW3D_PT_seams_to_sewing_pattern_3d"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "缝纫纸样"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.active_object.type == 'MESH'

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'
        
        layout.operator("object.seams_to_sewingpattern", text="生成缝纫纸样", icon=get_icon("OUTLINER_DATA_SURFACE"))
        layout.separator()
        layout.operator("object.export_sewingpattern", text="导出缝纫纸样 (.svg)", icon="EXPORT")
        layout.separator()
        layout.operator("object.sewing_pattern_clothsim", text="布料模拟设置", icon=get_icon("MOD_CLOTH"))


# Register
classes = [
    VIEW3D_MT_object_seams_to_sewing_pattern_menu,
    VIEW3D_PT_seams_to_sewing_pattern_uv,
    VIEW3D_PT_seams_to_sewing_pattern_3d,
    op_seams_to_sewingpattern.Seams_To_SewingPattern,
    op_export_sewingpattern.Export_Sewingpattern,
    op_quick_clothsim.QuickClothsim,
    op_boundary_alinged_remesh.Remesher,
    op_clean_up_edges.CleanUpEdges
    ]

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
    
    # Try multiple menu locations for broader compatibility
    # Blender 2.8-3.x: VIEW3D_MT_object
    # Blender 4.0+: VIEW3D_MT_object may still work
    # Blender 5.x: Use editor menus system
    view3d_menus = [
        'VIEW3D_MT_object',
        'VIEW3D_MT_object_context_menu',
    ]
    for menu_name in view3d_menus:
        menu_class = getattr(bpy.types, menu_name, None)
        if menu_class is not None:
            try:
                menu_class.append(menu_func)
            except:
                pass
    
    # UV Editor menu
    uv_menus = [
        'IMAGE_MT_uvs',
        'VIEW3D_MT_uv_map',
    ]
    for menu_name in uv_menus:
        menu_class = getattr(bpy.types, menu_name, None)
        if menu_class is not None:
            try:
                menu_class.append(uv_menu_func)
            except:
                pass
    
    # Edit mesh menus
    edit_menus = [
        'VIEW3D_MT_edit_mesh_clean',
        'VIEW3D_MT_edit_mesh_edges',
        'VIEW3D_MT_edit_mesh_context_menu',
    ]
    for menu_name in edit_menus:
        menu_class = getattr(bpy.types, menu_name, None)
        if menu_class is not None:
            try:
                menu_class.append(clean_up_func)
            except:
                pass



def unregister():
    
    edit_menus = [
        'VIEW3D_MT_edit_mesh_clean',
        'VIEW3D_MT_edit_mesh_edges',
        'VIEW3D_MT_edit_mesh_context_menu',
    ]
    for menu_name in edit_menus:
        menu_class = getattr(bpy.types, menu_name, None)
        if menu_class is not None:
            try:
                menu_class.remove(clean_up_func)
            except:
                pass
    
    view3d_menus = [
        'VIEW3D_MT_object',
        'VIEW3D_MT_object_context_menu',
    ]
    for menu_name in view3d_menus:
        menu_class = getattr(bpy.types, menu_name, None)
        if menu_class is not None:
            try:
                menu_class.remove(menu_func)
            except:
                pass
    
    uv_menus = [
        'IMAGE_MT_uvs',
        'VIEW3D_MT_uv_map',
    ]
    for menu_name in uv_menus:
        menu_class = getattr(bpy.types, menu_name, None)
        if menu_class is not None:
            try:
                menu_class.remove(uv_menu_func)
            except:
                pass
    
    # Removes submenu
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)

if __name__ == "__main__":
    register()
